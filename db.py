import redis
import csv

def db():
    redis_db = redis.Redis('localhost')
    #redis = redis.from_url(os.environ.get("REDIS_URL"))
    return redis_db

def parse(csvname,t_date):
    #Create connection to redis database
    redis_db = db()
    #Flush old values
    redis_db.flushall()
    #Load Data from CSV File
    with open(csvname) as csvfile:
        datalist = list(csv.DictReader(csvfile))
    #Load data into redis as hash
    for data in datalist:
        name = data['SC_NAME'].rstrip()
        records = {'Name' : data['SC_NAME'].rstrip(), 'Code' : data['SC_CODE'], 'Open' : data['OPEN'], 'Close' : data['CLOSE'], 'High' : data['HIGH'], 'Low' : data['LOW']}
        redis_db.hmset(name, records)
        #Load into list to get first ten entries
        redis_db.rpush("insertion_order", name)
    #Last Updated time
    redis_db.lpush("last_updated", t_date)
    
def last_updated():
    redis_db = db()
    return ((redis_db.lrange("last_updated", 0, 0)[0]).decode('UTF-8'))

def top10stockentries():
    #Fetches top ten entries from redis
    req_data_list = []
    redis_db = db()
    top_ten = redis_db.lrange("insertion_order", 0, 9)
    for stock in top_ten:
        req_data = redis_db.hgetall(stock)
        req_data_list.append(req_data)
    return req_data_list

def search_stock_by_name(name):
    #Search for a stock in redis using name
    results = []
    redis_db = db()
    for stock in redis_db.scan_iter(match='*'+str(name).upper()+'*'):
        results.append(redis_db.hgetall(stock))
    return results

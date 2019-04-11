
import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
import getbhavcopy
import db

env = Environment(loader=FileSystemLoader(os.getcwd()))
class task(object):
    @cherrypy.expose
    def index(self):
        #Get Bhavcopy CSV
        csvname,t_date = getbhavcopy.fetchBhavCopy()
        #Parse CSV and feed to redis
        db.parse(csvname,t_date)
        #Get top 10 entries from redis
        stocks = db.top10stockentries()
        #Get last updated time
        last_update = db.last_updated()
        last_update = '-'.join(a+b for a,b in zip(last_update[::2], last_update[1::2]))
        stockdict = []
        for stock in stocks:
            stockdict.append({key.decode('utf8'): value.decode('utf8') for key, value in stock.items()})
        tmpl = env.get_template('index.html')
        return tmpl.render(stocks = stockdict, last_update = last_update)
        
        
    @cherrypy.expose
    def search_stock_by_name(self, search_query = None):
        #Get stock names matching the search query
        matches = db.search_stock_by_name(search_query.upper().rstrip())
        last_update = db.last_updated()
        last_update = '-'.join(a+b for a,b in zip(last_update[::2], last_update[1::2]))
        search_results = []
        for result in matches:
            search_results.append({key.decode('utf8'): value.decode('utf8') for key, value in result.items()})
        tmpl = env.get_template('search_results.html')
        return tmpl.render(search_result = search_results, query = search_query, last_update = last_update, heading = ("Results for " + search_query) if len(search_results) > 0 else "No matches found")
        
        
 #Cherrypy Config           
conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.on': True,
        'tools.staticdir.root': os.getcwd(),
        'tools.staticdir.dir' : 'static'
    },
     '/static/images/icons/favicon.ico': { 'tools.staticfile.on': True, 'tools.staticfile.filename': 'static/images/icons/favicon.ico' },
    '/static': {
        'tools.staticdir.on': True,
        
        'tools.staticdir.index' : 'index.html',
        'tools.staticdir.dir' : 'static'
    }
    
}

cherrypy.quickstart(task(), '/', config=conf)
        
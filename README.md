# zerodha-task
This repo contains the source code for test task given by the zerodha's HR team. 
This web app downloads daily bhavcopy from BSE (https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx) parses the CSV and loads the values
into Redis. On the landing page, it renders the top 10 stock entries in the Redis in a nice table. It also has a search function to search stocks
from Redis using name. 
### How to use 
-Before proceeding make sure Redis is installed. <br>
-You can install Redis on windows by downloading the msi installer from this [link](https://github.com/MicrosoftArchive/redis/releases).<br>
- On linux you can directly install from teminal using the command `sudo apt install redis-server`<br>
- Make sure `git` is installed, if not install `git`<br>

#### Run it on local system
- `git clone https://github.com/theimperium20/zerodha-task.git`
- Run `python3 script.py` on powershell or terminal
- Open a browser and visit `localhost:8080` or `127.0.0.1:8080`
#### Host the app on Google Compute Engine 
- Create a google compute engine instance with Debian as operating system
- Run `sudo apt install -y redis-server`
- Check if redis is running by using the command `ps -f -u redis`
- Here, I am using a local Redis connection, if you want to use a remote Redis connection edit the `redis.conf` using
`sudo nano /etc/redis/redis.conf` and replace -`bind 127.0.0.1 ` with `bind 0.0.0.0` and restart Redis server by running `sudo service redis-server restart`
-You might have to edit firewall rules to allow the ports you are using, I am using `8080` and `6379`
-Clone repo : `git clone https://github.com/theimperium20/zerodha-task.git`
- Install requirments `pip3 install -r requirements.txt`
- Run `python3 script.py`
- Visit `[externalipofcloudinstance:port]` to use the app

##### Check out the live app hosted on [Google Cloud Platform](http://35.184.151.246:8080/)

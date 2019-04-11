
from requests import get
import os
from io import BytesIO
from zipfile import ZipFile
from datetime import datetime, timedelta


def fetchBhavCopy():
    #Check if the time is past 5pm. BSE releases bhavcopy only EOD. If script is run before that it should use yesterday's data
    if datetime.now().hour<17 :
        t_date = datetime.today() - timedelta(days=1) #use yesterday's date
        t_date = t_date.strftime('%d%m%y')
    else:
        #Get and format today's date to be used in the bhavcopy download url
        t_date = datetime.today().strftime('%d%m%y')
    
    #Check if csv file already exists
    csv = os.getcwd()+'/EQ'+t_date+'.csv'
    csvname = 'EQ'+t_date+'.csv'
    try:
        open(csvname)
        close(csvname)
    except:
        #Generate URL for downloading latest bhavcopy
        url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+t_date+'_CSV.ZIP'
        
        #Get bhavcopy
        get_bhavcopy = get(url)
        
        #Extract the zip
        bhavcopy = ZipFile(BytesIO(get_bhavcopy.content))
        bhavcopy.extractall()

    return csvname,t_date

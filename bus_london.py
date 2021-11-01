# coding: UTF-8

import time
import warnings
from sys import platform
from matplotlib import font_manager
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
import cmocean
from bs4 import BeautifulSoup
import requests
import datetime
from pytz import timezone, common_timezones, utc
from skyfield.api import load, wgs84
from urllib.request import urlretrieve
import socket
import feedparser
import re
#import ChiWrap
from operator import itemgetter
from PIL import Image
from bs4 import BeautifulSoup
import numpy
import matplotlib.animation
import objgraph
import rclone

# if platform == 'win32':
#     chara_chi = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/YUGOTHR.TTC', size=14)
# elif platform == 'darwin':
#     chara_chi = font_manager.FontProperties(fname = '/Library/Fonts/SIMHEI.TTF', size=14)
# elif platform == 'linux':
#     chara_chi = font_manager.FontProperties(fname = '/home/pi/.local/share/fonts/Unknown Vendor/TrueType/SimHei/simhei.ttf', size=14)
    
with open('MET_key.txt') as f_MET:
    MET_key = f_MET.read()
with open('TfL_key.txt') as f_TfL:
    TfL_key = f_TfL.read()

fig = plt.figure(figsize=(12.8,9), facecolor='black')

### location search
##link_MET = 'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/all?res=hourly&time=2021-10-10T18Z&key=45e783fc-47ea-4a69-8dc8-021f380a754f'
##html_MET = requests.get(link_MET).json()
##
##for i in range(len(html_MET['SiteRep']['DV']['Location'])):
##    print((float(html_MET['SiteRep']['DV']['Location'][i]['lon']),float(html_MET['SiteRep']['DV']['Location'][i]['lat'])))
##    print(html_MET['SiteRep']['DV']['Location'][i]['name'])
##    plt.plot(float(html_MET['SiteRep']['DV']['Location'][i]['lon']),float(html_MET['SiteRep']['DV']['Location'][i]['lat']),'ro')
##    plt.annotate(html_MET['SiteRep']['DV']['Location'][i]['name'],(float(html_MET['SiteRep']['DV']['Location'][i]['lon']),float(html_MET['SiteRep']['DV']['Location'][i]['lat'])),ha='center',va='center')
##
##plt.plot(-(0+14/60+54/3600),51+35/60+27/3600,'bx')

ephem       = load('de421.bsp') #1900-2050 only
sun         = ephem['sun']
earth       = ephem['earth']
colindale   = earth + wgs84.latlon((51+35/60+27/3600),-(0+14/60+54/3600))

def busbus(i):
    global ax0, TM_temp, TM_RH
    
    T0 = time.time()

    try:
        plt.clf()
        ax0.clear()
    except:
        print('session start at '+datetime.datetime.now().strftime('%d %b %H:%M:%S'))
        pass

    ax0 = plt.axes()
    ax0.set_facecolor('k')
    ax0.set_xlim((0,210))
    ax0.set_ylim((0,140))
    ax0.axis('off')

    ax0.annotate((datetime.datetime.now()+datetime.timedelta(minutes=0.25)).strftime('%a %d %b %H:%M'),(105,125),ha='center',va='center',fontsize=96,color='y')

    ax0.annotate('HKT:',(140,110),ha='left',va='top',fontsize=36,color='orange')
    ax0.annotate((datetime.datetime.now().astimezone(timezone('Asia/Hong_Kong'))+datetime.timedelta(minutes=0.25)).strftime('%d %b %H:%M'),(210,100),ha='right',va='top',fontsize=36,color='orange')

    PC125ETA = []
    PC125ETAstr1a = ''
    PC125ETAstr1b = 'N/A'
    PC125ETAstr2a = ''
    PC125ETAstr2b = 'N/A'
    PC186ETA = []
    PC186ETAstr1a = ''
    PC186ETAstr1b = 'N/A'
    PC186ETAstr2a = ''
    PC186ETAstr2b = 'N/A'
    
    socket.setdefaulttimeout(3)

    try:
        link_PC = 'https://api.tfl.gov.uk/StopPoint/490017849E/Arrivals?mode=bus&app_key='+TfL_key+'&'+str(numpy.random.randint(100)) #cache problem of server side
        html_PC = requests.get(link_PC).json()

        for i in range(len(html_PC)):
            if html_PC[i]["lineId"] == '125':
                PC125ETA.append(datetime.datetime.strptime(html_PC[i]["expectedArrival"],'%Y-%m-%dT%H:%M:%SZ'))
                PC125dest = str(html_PC[i]["stationName"]) + ' to ' + str(html_PC[i]["destinationName"])

            elif html_PC[i]["lineId"] == "186":
                PC186ETA.append(datetime.datetime.strptime(html_PC[i]["expectedArrival"],'%Y-%m-%dT%H:%M:%SZ'))
                PC186dest = str(html_PC[i]["stationName"]) + ' to ' + str(html_PC[i]["destinationName"])
        
        #original order is chaos
        PC125ETA = sorted(PC125ETA)
        PC186ETA = sorted(PC186ETA)
        
        try: #change to tzaware UTC dt and then switch tz to London
            PC125ETAstr1a = str(timezone('UTC').localize(PC125ETA[0]).astimezone(timezone('Europe/London')).time())
            PC125ETAstr1b = str('{:.1f}'.format((PC125ETA[0]-datetime.datetime.utcnow()).total_seconds()/60))+' mins'
        except:
            PC125ETAstr1a = ''
            PC125ETAstr1b = 'N/A'
        try:
            PC125ETAstr2a = str(timezone('UTC').localize(PC125ETA[1]).astimezone(timezone('Europe/London')).time())
            PC125ETAstr2b = str('{:.1f}'.format((PC125ETA[1]-datetime.datetime.utcnow()).total_seconds()/60))+' mins'
        except:
            PC125ETAstr2a = ''
            PC125ETAstr2b = 'N/A'

        try:
            PC186ETAstr1a = str(timezone('UTC').localize(PC186ETA[0]).astimezone(timezone('Europe/London')).time())
            PC186ETAstr1b = str('{:.1f}'.format((PC186ETA[0]-datetime.datetime.utcnow()).total_seconds()/60))+' mins'
        except:
            PC186ETAstr1a = ''
            PC186ETAstr1b = 'N/A'
        try:
            PC186ETAstr2a = str(timezone('UTC').localize(PC186ETA[1]).astimezone(timezone('Europe/London')).time())
            PC186ETAstr2b = str('{:.1f}'.format((PC186ETA[1]-datetime.datetime.utcnow()).total_seconds()/60))+' mins'
        except:
            PC186ETAstr2a = ''
            PC186ETAstr2b = 'N/A'

    except Exception as e:
        print(e)
        print('Peel Centre fail')
        pass
    
    CS204ETA = []
    CS204ETAstr1a = ''
    CS204ETAstr1b = 'N/A'
    CS204ETAstr2a = ''
    CS204ETAstr2b = 'N/A'

    try:
        link_CS = 'https://api.tfl.gov.uk/StopPoint/490000054CA/Arrivals?mode=bus&app_key='+TfL_key+'&'+str(numpy.random.randint(100))
        html_CS = requests.get(link_CS).json()

        for i in range(len(html_CS)):
            if html_CS[i]["lineId"] == '204':
                CS204ETA.append(datetime.datetime.strptime(html_CS[i]["expectedArrival"],'%Y-%m-%dT%H:%M:%SZ'))
                CS204dest = str(html_CS[i]["stationName"]) + ' to ' + str(html_CS[i]["destinationName"])

        CS204ETA = sorted(CS204ETA)
        
        try:
            CS204ETAstr1a = str(timezone('UTC').localize(CS204ETA[0]).astimezone(timezone('Europe/London')).time())
            CS204ETAstr1b = str('{:.1f}'.format((CS204ETA[0]-datetime.datetime.utcnow()).total_seconds()/60))+' mins'
        except:
            CS204ETAstr1a = ''
            CS204ETAstr1b = 'N/A'
        try:
            CS204ETAstr2a = str(timezone('UTC').localize(CS204ETA[1]).astimezone(timezone('Europe/London')).time())
            CS204ETAstr2b = str('{:.1f}'.format((CS204ETA[1]-datetime.datetime.utcnow()).total_seconds()/60))+' mins'
        except:
            CS204ETAstr2a = ''
            CS204ETAstr2b = 'N/A'

    except Exception as e:
        print(e)
        print('Colindale station fail')
        pass

    TUBEETA = []
    TUBEETAstr1a = ''
    TUBEETAstr1b = 'N/A'
    TUBEETAstr2a = ''
    TUBEETAstr2b = 'N/A'
    
    try:
        link_TUBE = 'https://api.tfl.gov.uk/StopPoint/940GZZLUCND/Arrivals?mode=tube&app_key='+TfL_key
        html_TUBE = requests.get(link_TUBE).json()
        
        for i in range(len(html_TUBE)):
            if html_TUBE[i]["direction"] == 'inbound':
                TUBEETA.append([datetime.datetime.strptime(html_TUBE[i]["expectedArrival"],'%Y-%m-%dT%H:%M:%SZ'),html_TUBE[i]["towards"]])
                TUBEdest = 'Northern line - inbound'
                
        TUBEETA = sorted(TUBEETA, key=itemgetter(0))
        
        try:
            #TUBEETAstr1a = str(timezone('UTC').localize(TUBEETA[0]).astimezone(timezone('Europe/London')).time())
            TUBEETAstr1a = str(TUBEETA[0][1])
            TUBEETAstr1b = str('{:.1f}'.format((TUBEETA[0][0]-datetime.datetime.utcnow()).total_seconds()/60))+' mins'
        except:
            TUBEETAstr1a = ''
            TUBEETAstr1b = 'N/A'
        try:
            #TUBEETAstr2a = str(timezone('UTC').localize(TUBEETA[1]).astimezone(timezone('Europe/London')).time())
            TUBEETAstr2a = str(TUBEETA[1][1])
            TUBEETAstr2b = str('{:.1f}'.format((TUBEETA[1][0]-datetime.datetime.utcnow()).total_seconds()/60))+' mins'
        except:
            TUBEETAstr2a = ''
            TUBEETAstr2b = 'N/A'

    except Exception as e:
        print(e)
        print('tube fail')
        pass
    
    if len(PC125ETA) == 0:
        if datetime.time(1,0) <= datetime.datetime.now().time() < datetime.time(5,30):
            PC125dest = 'molamola'#0540-0045
        else:
            PC125dest = 'check app la'
    if len(PC186ETA) == 0:
        if datetime.time(1,0) <= datetime.datetime.now().time() < datetime.time(6,0):
            PC186dest = 'molamola'#0511-2346
        else:
            PC186dest = 'check app la'
    if len(CS204ETA) == 0:
        if datetime.time(1,0) <= datetime.datetime.now().time() < datetime.time(5,0):
            CS204dest = 'molamola'#0050-0528
        else:
            CS204dest = 'check app la'
    if len(TUBEETA) == 0:
        TUBEdest = 'Northern line - inbound'
        
    ax0.annotate('125',(0,100+10),ha='left',va='top',fontsize=84,color='w')
    ax0.annotate(PC125dest,(1,85-2+10),ha='left',va='top',fontsize=18,color='w')
    ax0.annotate(PC125ETAstr1a,(70,100-2+10),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(PC125ETAstr1b,(138,100+10),ha='right',va='top',fontsize=36,color='w')
    ax0.annotate(PC125ETAstr2a,(70,90-2+10),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(PC125ETAstr2b,(138,90+10),ha='right',va='top',fontsize=36,color='w')

    ax0.annotate('186',(0,75+20/3),ha='left',va='top',fontsize=84,color='w')
    ax0.annotate(PC186dest,(1,60-2+20/3),ha='left',va='top',fontsize=18,color='w')
    ax0.annotate(PC186ETAstr1a,(70,75-2+20/3),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(PC186ETAstr1b,(138,75+20/3),ha='right',va='top',fontsize=36,color='w')
    ax0.annotate(PC186ETAstr2a,(70,65-2+20/3),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(PC186ETAstr2b,(138,65+20/3),ha='right',va='top',fontsize=36,color='w')

    ax0.annotate('204',(0,50+10/3),ha='left',va='top',fontsize=84,color='w')
    ax0.annotate(CS204dest,(1,35-2+10/3),ha='left',va='top',fontsize=18,color='w')
    ax0.annotate(CS204ETAstr1a,(70,50-2+10/3),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(CS204ETAstr1b,(138,50+10/3),ha='right',va='top',fontsize=36,color='w')
    ax0.annotate(CS204ETAstr2a,(70,40-2+10/3),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(CS204ETAstr2b,(138,40+10/3),ha='right',va='top',fontsize=36,color='w')

    ax0.annotate('Tube',(0,25),ha='left',va='top',fontsize=84,color='w')
    ax0.annotate(TUBEdest,(1,10-2),ha='left',va='top',fontsize=18,color='w')
    ax0.annotate(TUBEETAstr1a,(70+2,25-2),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(TUBEETAstr1b,(138,25),ha='right',va='top',fontsize=36,color='w')
    ax0.annotate(TUBEETAstr2a,(70+2,15-2),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(TUBEETAstr2b,(138,15),ha='right',va='top',fontsize=36,color='w')

    ax0.annotate('Data provided by Transport for London',(1,0),ha='left',va='bottom',fontsize=10,color='w')
    
    ts = load.timescale()
    #sun alt now
    sun_vector = colindale.at(ts.utc(ts.now().utc_datetime())).observe(sun).apparent()
    #sun max alt in next 24hr
    sun_max_alt = max(colindale.at(ts.utc(ts.now().utc_datetime().year,ts.now().utc_datetime().month,ts.now().utc_datetime().day,ts.now().utc_datetime().hour,range(24*60))).observe(sun).apparent().altaz()[0].degrees)
    ax0.add_patch(patches.Rectangle((140,30),70,60,facecolor=cmocean.cm.ice(numpy.clip((sun_vector.altaz()[0].degrees+10)/sun_max_alt,0,0.9)),edgecolor=None,zorder=2))
    
    #grad_h = 35
    #for i in range(100):
    #    grad = patches.Rectangle((140,50+i*grad_h/100),70,grad_h/100,facecolor='k',edgecolor=None,alpha=0.5-i*0.5/100,zorder=2)
    #    ax0.add_patch(grad)
    
    WT = {'0':'Clear\nnight','1':'Sunny\nday','2':'Partly\ncloudy\n(night)','3':'Partly\ncloudy\n(day)',
          '4':'Not\nused','5':'Mist','6':'Fog','7':'Cloudy',
          '8':'Overcast','9':'Light\nrain\nshower\n(night)','10':'Light\nrain\nshower\n(day)','11':'Drizzle',
          '12':'Light\nrain','13':'Heavy\nrain\nshower\n(night)','14':'Heavy\nrain\nshower\n(day)','15':'Heavy\nrain',
          '16':'Sleet\nshower\n(night)','17':'Sleet\nshower\n(day)','18':'Sleet','19':'Hail\nshower\n(night)',
          '20':'Hail\nshower\n(day)','21':'Hail','22':'Light\nsnow\nshower\n(night)','23':'Light\nsnow\nshower\n(day)',
          '24':'Light\nsnow','25':'Heavy\nsnow\nshower\n(night)','26':'Heavy\nsnow\nshower\n(day)','27':'Heavy\nsnow',
          '28':'Thunder\nshower\n(night)','29':'Thunder\nshower\n(day)','30':'Thunder','NA':'Not\navailable'}
    
    try:
        link_MET = 'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3672?res=hourly&key='+MET_key
        html_MET = requests.get(link_MET).json()

        temp_northolt = html_MET['SiteRep']['DV']['Location']['Period'][-1]['Rep'][-1]['T']
        temp_cmap = matplotlib.cm.get_cmap('coolwarm')
        ax0.annotate(temp_northolt+'$\u00B0$C',(208,15),ha='right',va='bottom',fontsize=48,color=temp_cmap(numpy.clip(float(temp_northolt)/25,0,1)),zorder=3)
        
        RH_northolt = html_MET['SiteRep']['DV']['Location']['Period'][-1]['Rep'][-1]['H']
        ax0.annotate(str(round(float(RH_northolt)))+'%',(141,15),ha='left',va='bottom',fontsize=48,color='w',zorder=3)

        wind_northolt = html_MET['SiteRep']['DV']['Location']['Period'][-1]['Rep'][-1]['S']
        if float(temp_northolt) <= 10 and float(wind_northolt) >= 3:
            ws = float(wind_northolt)*1.609344
            WC = 13.12 + 0.6215*float(temp_northolt) - 11.37*numpy.power(ws,0.16) + 0.3965*float(temp_northolt)*numpy.power(ws,0.16)
            ax0.annotate('WC: '+str(round(WC,1))+'$\u00B0$C',(175,5),ha='center',va='bottom',fontsize=36,color=temp_cmap(numpy.clip(WC/25,0,1)),zorder=3)
        elif float(temp_northolt) >= 27 and float(RH_northolt) >= 40:
            HI = -8.78469475556\
                 +1.61139411*float(temp_northolt)\
                 +2.33854883889*float(RH_northolt)\
                 -0.14611605*float(temp_northolt)*float(RH_northolt)\
                 -0.012308094*float(temp_northolt)*float(temp_northolt)\
                 -0.0164248277778*float(RH_northolt)*float(RH_northolt)\
                 +0.002211732*float(temp_northolt)*float(temp_northolt)*float(RH_northolt)\
                 +0.00072546*float(temp_northolt)*float(RH_northolt)*float(RH_northolt)\
                 -0.000003582*float(temp_northolt)*float(temp_northolt)*float(RH_northolt)*float(RH_northolt)
            ax0.annotate('HI: '+str(round(HI,1))+'$\u00B0$C',(175,5),ha='center',va='bottom',fontsize=36,color=temp_cmap(numpy.clip(HI/25,0,1)),zorder=3)  
            
        W_northolt = html_MET['SiteRep']['DV']['Location']['Period'][-1]['Rep'][-1]['W']
        ax0.annotate(WT[W_northolt],(175,60),ha='center',va='center',fontsize=48,color='w',path_effects=[pe.withStroke(linewidth=2,foreground='gray',alpha=0.5)],zorder=3)

    except Exception as e:
        print(e)
        ax0.annotate(temp_northolt+'$\u00B0$C',(208,15),ha='right',va='bottom',fontsize=48,color=temp_cmap(numpy.clip(float(temp_northolt)/25,0,1)),zorder=3)
        ax0.annotate(str(round(float(RH_northolt)))+'%',(141,15),ha='left',va='bottom',fontsize=48,color='w',zorder=3)
        ax0.annotate(WT[W_northolt],(175,60),ha='center',va='center',fontsize=48,color='w',path_effects=[pe.withStroke(linewidth=2,foreground='gray',alpha=0.5)],zorder=3)
        print('MET fail')
    
    ax0.annotate('northolt weather updated: '+datetime.datetime.now().strftime('%H:%M:%S'),(209,0),ha='right',va='bottom',fontsize=10,color='w')
    
    plt.tight_layout()
    fig.canvas.draw() 
    fig.canvas.flush_events()
    
    #upload to Dropbox
    plt.savefig('bus_london.png')
    cfg_path = r'/home/pi/.config/rclone/rclone.conf'
    with open(cfg_path) as f:
        cfg = f.read()
        
    ULdropbox = rclone.with_config(cfg).copy('/home/pi/Desktop/bus_london.png','webpage:webpage')
    
    T1 = time.time()
    #print(T1-T0)
    objgraph.show_growth()
    
def busbusbus(i):
    try:
        busbus(i)
    except Exception as e:
        print(e)
        pass

ani = matplotlib.animation.FuncAnimation(fig, busbusbus, repeat=False, interval=20000, save_count=0)
warnings.filterwarnings('ignore',category=matplotlib.cbook.mplDeprecation)
plt.tight_layout()
###plt.get_current_fig_manager().window.wm_geometry('-2-0')
plt.show()

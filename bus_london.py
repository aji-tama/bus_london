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
from datetime import datetime, timedelta
from pytz import timezone, common_timezones
from skyfield.api import load, wgs84
from urllib.request import urlretrieve
import socket
import feedparser
import re
#import ChiWrap
from PIL import Image
from bs4 import BeautifulSoup
import numpy
import matplotlib.animation
import objgraph
import rclone

if platform == 'win32':
    chara_chi = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/YUGOTHR.TTC', size=14)
elif platform == 'darwin':
    chara_chi = font_manager.FontProperties(fname = '/Library/Fonts/SIMHEI.TTF', size=14)
elif platform == 'linux':
    chara_chi = font_manager.FontProperties(fname = '/home/pi/.local/share/fonts/Unknown Vendor/TrueType/SimHei/simhei.ttf', size=14)
    
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
        print('session start at '+datetime.now().strftime('%d %b %H:%M:%S'))
        pass

    ax0 = plt.axes()
    ax0.set_facecolor('k')
    ax0.set_xlim((0,210))
    ax0.set_ylim((0,140))
    ax0.axis('off')

    ax0.annotate((datetime.now()+timedelta(minutes=0.25)).strftime('%a %d %b %H:%M'),(105,125),ha='center',va='center',fontsize=96,color='y')

    ax0.annotate('HKT:',(140,110),ha='left',va='top',fontsize=36,color='orange')
    ax0.annotate((datetime.now().astimezone(timezone('Asia/Hong_Kong'))+timedelta(minutes=0.25)).strftime('%d %b %H:%M'),(210,100),ha='right',va='top',fontsize=36,color='orange')

    KMB61META = []
    KMB61METAstr1a = ''
    KMB61METAstr1b = 'not available'
    KMB61METAstr2a = ''
    KMB61METAstr2b = 'not available'
    KMB52XETA = []
    KMB52XETAstr1a = ''
    KMB52XETAstr1b = 'not available'
    KMB52XETAstr2a = ''
    KMB52XETAstr2b = 'not available'
    
    socket.setdefaulttimeout(3)

    try:
        link_KMB = 'https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/630AA1866C5372B6'
        html_KMB = requests.get(link_KMB).json()

        for i in range(len(html_KMB['data'])):
            if html_KMB['data'][i]['route'] == '61M':
                KMB61META.append(datetime.strptime(html_KMB['data'][i]['eta'],'%Y-%m-%dT%H:%M:%S+08:00'))
                KMB61Mdest = '往' + str(html_KMB['data'][i]['dest_tc'])

            elif html_KMB['data'][i]['route'] == '52X':
                KMB52XETA.append(datetime.strptime(html_KMB['data'][i]['eta'],'%Y-%m-%dT%H:%M:%S+08:00'))
                KMB52Xdest = '往' + str(html_KMB['data'][i]['dest_tc'])
               
        try:
            KMB61METAstr1a = str(KMB61META[0].time())
            KMB61METAstr1b = str('{:.1f}'.format((KMB61META[0]-datetime.now()).total_seconds()/60))+' mins'
        except:
            KMB61METAstr1a = ''
            KMB61METAstr1b = 'not available'
        try:
            KMB61METAstr2a = str(KMB61META[1].time())
            KMB61METAstr2b = str('{:.1f}'.format((KMB61META[1]-datetime.now()).total_seconds()/60))+' mins'
        except:
            KMB61METAstr2a = ''
            KMB61METAstr2b = 'not available'

        try:
            KMB52XETAstr1a = str(KMB52XETA[0].time())
            KMB52XETAstr1b = str('{:.1f}'.format((KMB52XETA[0]-datetime.now()).total_seconds()/60))+' mins'
        except:
            KMB52XETAstr1a = ''
            KMB52XETAstr1b = 'not available'
        try:
            KMB52XETAstr2a = str(KMB52XETA[1].time())
            KMB52XETAstr2b = str('{:.1f}'.format((KMB52XETA[1]-datetime.now()).total_seconds()/60))+' mins'
        except:
            KMB52XETAstr2a = ''
            KMB52XETAstr2b = 'not available'

    except:
        print('KMB fail')
        pass
    
    CTB962SETA = []
    CTB962SETAstr1a = ''
    CTB962SETAstr1b = 'not available'
    CTB962SETAstr2a = ''
    CTB962SETAstr2b = 'not available'

    try:
        link_962S = 'https://rt.data.gov.hk/v1/transport/citybus-nwfb/eta/CTB/002031/962s'
        html_962S = requests.get(link_962S).json()

        for i in range(len(html_962S['data'])):
            if html_962S['data'][i]['route'] == '962S':
                CTB962SETA.append(datetime.strptime(html_962S['data'][i]['eta'],'%Y-%m-%dT%H:%M:%S+08:00'))
                CTB962Sdest = '往' + str(html_962S['data'][i]['dest_tc'])
                
        try:
            CTB962SETAstr1a = str(CTB962SETA[0].time())
            CTB962SETAstr1b = str('{:.1f}'.format((CTB962SETA[0]-datetime.now()).total_seconds()/60))+' mins'
        except:
            CTB962SETAstr1a = ''
            CTB962SETAstr1b = 'not available'
        try:
            CTB962SETAstr2a = str(CTB962SETA[1].time())
            CTB962SETAstr2b = str('{:.1f}'.format((CTB962SETA[1]-datetime.now()).total_seconds()/60))+' mins'
        except:
            CTB962SETAstr2a = ''
            CTB962SETAstr2b = 'not available'

    except:
        pass

    CTB962XETA = []
    CTB962XETAstr1a = ''
    CTB962XETAstr1b = 'not available'
    CTB962XETAstr2a = ''
    CTB962XETAstr2b = 'not available'
    
    try:
        link_962X = 'https://rt.data.gov.hk/v1/transport/citybus-nwfb/eta/CTB/002599/962x'
        html_962X = requests.get(link_962X).json()
        
        for i in range(len(html_962X['data'])):
            if html_962X['data'][i]['route'] == '962X':
                CTB962XETA.append(datetime.strptime(html_962X['data'][i]['eta'],'%Y-%m-%dT%H:%M:%S+08:00'))
                CTB962Xdest = '往' + str(html_962X['data'][i]['dest_tc'])
       
        try:
            CTB962XETAstr1a = str(CTB962XETA[0].time())
            CTB962XETAstr1b = str('{:.1f}'.format((CTB962XETA[0]-datetime.now()).total_seconds()/60))+' mins'
        except:
            CTB962XETAstr1a = ''
            CTB962XETAstr1b = 'not available'
        try:
            CTB962XETAstr2a = str(CTB962XETA[1].time())
            CTB962XETAstr2b = str('{:.1f}'.format((CTB962XETA[1]-datetime.now()).total_seconds()/60))+' mins'
        except:
            CTB962XETAstr2a = ''
            CTB962XETAstr2b = 'not available'

    except:
        pass

    if len(KMB61META) == 0:
        KMB61Mdest = '無車'
    if len(KMB52XETA) == 0:
        KMB52Xdest = '無車'
    if len(CTB962SETA) == 0:
        CTB962Sdest = '無車'
    if len(CTB962XETA) == 0:
        CTB962Xdest = '無車'
        
    ax0.annotate('61M',(0,100+10),ha='left',va='top',fontsize=84,color='w')
    ax0.annotate(KMB61Mdest,(1,85-2+10),fontproperties=chara_chi,ha='left',va='top',color='w')
    ax0.annotate(KMB61METAstr1a,(70,100-2+10),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(KMB61METAstr1b,(138,100+10),ha='right',va='top',fontsize=36,color='w')
    ax0.annotate(KMB61METAstr2a,(70,90-2+10),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(KMB61METAstr2b,(138,90+10),ha='right',va='top',fontsize=36,color='w')

    ax0.annotate('52X',(0,75+20/3),ha='left',va='top',fontsize=84,color='w')
    ax0.annotate(KMB52Xdest,(1,60-2+20/3),fontproperties=chara_chi,ha='left',va='top',color='w')
    ax0.annotate(KMB52XETAstr1a,(70,75-2+20/3),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(KMB52XETAstr1b,(138,75+20/3),ha='right',va='top',fontsize=36,color='w')
    ax0.annotate(KMB52XETAstr2a,(70,65-2+20/3),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(KMB52XETAstr2b,(138,65+20/3),ha='right',va='top',fontsize=36,color='w')

    ax0.annotate('962S',(0,50+10/3),ha='left',va='top',fontsize=84,color='w')
    ax0.annotate(CTB962Sdest,(1,35-2+10/3),fontproperties=chara_chi,ha='left',va='top',color='w')
    ax0.annotate(CTB962SETAstr1a,(70,50-2+10/3),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(CTB962SETAstr1b,(138,50+10/3),ha='right',va='top',fontsize=36,color='w')
    ax0.annotate(CTB962SETAstr2a,(70,40-2+10/3),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(CTB962SETAstr2b,(138,40+10/3),ha='right',va='top',fontsize=36,color='w')

    ax0.annotate('962X',(0,25),ha='left',va='top',fontsize=84,color='w')
    ax0.annotate(CTB962Xdest,(1,10-2),fontproperties=chara_chi,ha='left',va='top',color='w')
    ax0.annotate(CTB962XETAstr1a,(70,25-2),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(CTB962XETAstr1b,(138,25),ha='right',va='top',fontsize=36,color='w')
    ax0.annotate(CTB962XETAstr2a,(70,15-2),ha='center',va='top',fontsize=18,color='w')
    ax0.annotate(CTB962XETAstr2b,(138,15),ha='right',va='top',fontsize=36,color='w')
    
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
        link_MET = 'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3672?res=hourly&key=45e783fc-47ea-4a69-8dc8-021f380a754f'
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
    
    ax0.annotate('northolt weather updated: '+datetime.now().strftime('%H:%M:%S'),(209,0),ha='right',va='bottom',fontsize=12,color='w')
    
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

ani = matplotlib.animation.FuncAnimation(fig, busbusbus, repeat=False, interval=15000, save_count=0)
warnings.filterwarnings('ignore',category=matplotlib.cbook.mplDeprecation)
plt.tight_layout()
###plt.get_current_fig_manager().window.wm_geometry('-2-0')
plt.show()

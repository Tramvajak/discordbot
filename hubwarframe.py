import requests
from datetime import datetime
platform = 'pc'
site = f'https://api.warframestat.us/{platform}/'
params= {'language': 'ru','Accept-Language': 'ru' }

#cambionCycle - деймос

#r = requests.get(f'https://api.warframestat.us/{platform}/arbitration', params={'language': 'ru','Accept-Language': 'ru' })
#print(r)
#json = r.json()
#print(json)
#print(json['active'])


def get_cambion_drift_status(): #деймос
    json = get_json_result('cambionCycle')
    #date_activation = date_convert(json['activation'])
    #print('Время начала: '+date_convert(json['activation']))#str(date_activation))
    #print('Время окончания: '+date_convert(json['expiry']))
    #print('Стадия: '+json['active'])
    #text = 'Время начала: '+date_convert(json['activation']) +
    #'\nВремя окончания: '+date_convert(json['expiry'])+
    ##'\nОсталось: '+
    #'\nСтадия: '+json['state']
    print(json)
    return json

def get_cetus_status():
    json = get_json_result('cetusCycle')
    print(json)
    print('Время начала: '+ date_convert_str(json['activation']))
    print('Время окончания: '+ date_convert_str(json['expiry']))
    print('Стадия: '+json['state'])
    print(json['shortString'])
    return json

def get_sortie_data():
    json = get_json_result('sortie')
    print(json)
    return json

def get_void_trade():
    json = get_json_result('voidTrader')
    print(json)
    return json

def get_nigthwave():
    json = get_json_result('nightwave')
    print(json)
    return(json)

def get_alerts():
    json = get_json_result('alerts')
    print(json)
    return(json)

def get_json_result(quest):
    r = requests.get(f'{site}/{quest}', params=params)
    return r.json()

def date_convert_str(date): # convert 2021-03-23T22:29:00.000Z to 
    cdate = date.split('T')
    cdate = cdate[0] +' '+ cdate[1]
    cdate = cdate[:-5]
    #return datetime.strptime(cdate,"%Y-%m-%d %H:%M:%S")
    now = datetime.strptime(cdate,"%Y-%m-%d %H:%M:%S")
    return "{}.{}.{} {}:{}".format(now.day, now.month, now.year, now.hour+3, now.minute)

def date_convert_date(date): # convert 2021-03-23T22:29:00.000Z to 
    cdate = date.split('T')
    cdate = cdate[0] +' '+ cdate[1]
    cdate = cdate[:-5]
    #return datetime.strptime(cdate,"%Y-%m-%d %H:%M:%S")
    now = datetime.strptime(cdate,"%Y-%m-%d %H:%M:%S")
    return now

#get_cambion_drift_status()
#get_cetus_status()
#get_sortie_data()
#get_void_trade()

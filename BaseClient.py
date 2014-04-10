from datetime import date, datetime
import urllib3 as url
from token import *
import json
import time
SIGNGAPORE = {u'lat': 1.290301, u'lon': 103.844555}
TOKYO =  {u'lat': 35.678403, u'lon': 139.670506}
PARIS =  {u'lat': 48.856614, u'lon': 2.352222}
NYC =  {u'lat': 40.738187, u'lon': -74.005204}
LOCATION = NYC
last_activity_date = '2014-04-09T04:41:38.276Z'
js = json.JSONDecoder()
URL = 'api.gotinder.com'
matches = []
def calc_age(dob):
    today = date.today()
    try:
        birthday = dob.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = dob.replace(year=today.year, month=dob.month+1, day=1)
    if birthday > today:
        return today.year - dob.year - 1
    else:
        return today.year - dob.year


class person():
    def __init__(self,data):
        if type(data) == type(""):
            self.data = js.decode(data)
        else:
            if type(data) == type({}):
                self.data = data
            else:
                raise Exception('Person isn\'t a string or dict')

    def getAge(self):
        return self.age if hasattr(self,'age') else calc_age(datetime.strptime(self.data['birth_date'].split('T')[0],"%Y-%M-%d").date())
    def getName(self):
        return self.data['name']

    def getBio(self):
        return  self.data['bio']

    def __str__(self):
        return str(self.data)

    def sum(self):
        print "["+self.getName() + str(self.getAge()) +"]",": \t", self.data['bio'].replace('\n','\t'),
    def __repr__(self):
        return self.getName()


class client():
    def __init__(self):
        self.req = url.HTTPSConnectionPool(URL)
        print self.req.request('POST','/auth',fields= {"facebook_token":facebook_token}).data
    def likePeople(self,num):
        while num >0:
            peopleList =  js.decode(self.req.request('POST','/user/recs',headers=HEADERS,fields= {"limit":40}).data)
            people = peopleList['results']
            for i in people:
                if num>0:
                    if i['gender'] == 1:
                        num-=1
                        print i['name'],': Match' if self.req.request('GET','/like/'+i['_id'],headers=HEADERS).data != '{"match":false}' else ''
                        time.sleep(.2)
    def handleUpdate(self,request):
        if request:
            print request
            self.last_activity_date = request['last_activity_date']
            if request['matches']:
                matches = request['matches']
                for i in matches:
                    if i.has_key('person'):
                        matches.append([person(i['person']),(i.has_key('messages') and i['messages'] != [])])
    def update(self):
        return self.handleUpdate(js.decode(self.req.request('POST','/updates',headers=HEADERS,fields= {'last_activity_date': self.last_activity_date if hasattr(self, 'last_activity_date') else '2014-04-07T06:36:49.027Z'}).data))
    def sendMessage(self, message, id):
        print self.req.request('POST','/user/matches/'+ id,headers=HEADERS,fields= {"message":message}).data
    def getMatches(self, id):
        print self.req.request('GET','/user/matches/'+ id,headers=HEADERS).data

HEADERS = {
    'Accept-Language': 'en-GB;q=1, en;q=0.9, fr;q=0.8, de;q=0.7, ja;q=0.6, nl;q=0.5',
    'User-Agent': 'Tinder/3.0.3 (iPhone; iOS 7.0.6; Scale/2.00)',
    'X-Auth-Token':'1a5069f1-4f11-4a08-a9ab-4c41544ad34e',
    'os_version': '70000000006',
    'Accept': '*/*',
    'platform': 'ios',
    'Connection': 'keep-alive',
    'Proxy-Connection': 'keep-alive',
    'app_version': '1',
    'Accept-Encoding': 'gzip, deflate',
}
c = client()
c.update()
c.likePeople(500)




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
    def getId(self):
        return self.data['id']
    def getName(self):
        return self.data['name']
    def getBio(self):
        return  self.data['bio']
    def likeUser(self):
        None
    def __str__(self):
        return str(self.data)

    def sum(self):
        print "["+self.getName() + str(self.getAge()) +"]",": \t", self.data['bio'].replace('\n','\t'),
    def __repr__(self):
        return self.getName()


class client():
    def __init__(self):
        self.req = url.HTTPSConnectionPool(URL)
        self.HEADERS = HEADERS
        self.HEADERS['X-Auth-Token'] = js.decode(self.req.request('POST','/auth',fields= {"facebook_token":facebook_token}).data)['token']
    def gatherUsersInfo(self, numOfUsers, keywords= None):
        users = []
        if keywords is None:
            list = js.decode(self.req.request('POST','/user/recs',headers=self.HEADERS,fields= {"limit":40}).data)['results']
            users+= [x['bio'].lower() for x in list ]
        elif type(keywords) == type([]):
            while users.__len__() < numOfUsers:
                list = js.decode(self.req.request('POST','/user/recs',headers=self.HEADERS,fields= {"limit":40}).data)['results']
                users+=[(ext in x['bio'] for ext in keywords) for x in list]
        elif type(keywords) == type(""):
            while users.__len__() < numOfUsers:
                list = js.decode(self.req.request('POST','/user/recs',headers=self.HEADERS,fields= {"limit":40}).data)['results']
                users+=[x for x in list if keywords in x['bio'].lower()]
        else:
            raise(ValueError('Please enter either a string or an array of strings for the keywords variable'))
        return users
    def likePeople(self,num):
        while num:
            recList =  js.decode(self.req.request('POST','/user/recs',headers=self.HEADERS,fields= {"limit":40}).data)
            people = recList['results']
            for i in people:
                if num:
                    num-=1
                    print i['name'],': Match' if self.req.request('GET','/like/'+i['_id'],headers=self.HEADERS).data != '{"match":false}' else ''
                    time.sleep(.2)
    def handleUpdate(self,request):
        if request:
            self.last_activity_date = request['last_activity_date']
            if request['matches']:
                pastMatches = request['matches']
                for i in pastMatches:
                    if i.has_key('person'):
                        matches.append([i['person']['name'],(i.has_key('messages') and i['messages'] != [])])
    def update(self):
        return self.handleUpdate(js.decode(self.req.request('POST','/updates',headers=self.HEADERS,fields= {'last_activity_date': self.last_activity_date if hasattr(self, 'last_activity_date') else '2014-04-07T06:36:49.027Z'}).data))
    def sendMessage(self, message, id):
        print self.req.request('POST','/user/matches/'+ id,headers=self.HEADERS,fields= {"message":message}).data
    def getMatches(self, id):
        print self.req.request('GET','/user/matches/'+ id,headers=self.HEADERS).data
HEADERS = {'Accept-Language': 'en-GB;q=1, en;q=0.9, fr;q=0.8, de;q=0.7, ja;q=0.6, nl;q=0.5',
                    'User-Agent': 'Tinder/3.0.3 (iPhone; iOS 7.0.6; Scale/2.00)',
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




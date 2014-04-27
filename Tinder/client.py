from threading import Thread
import time
import datetime
import requests
from simplejson import JSONDecodeError
import urllib3 as url
from objects import person,userOverview
from token import *

last_activity_date = '2014-04-09T04:41:38.276Z'

URL = 'https://api.gotinder.com'

TOKYO =  {u'lat': 35.678403, u'lon': 139.670506}
SIGNGAPORE = {u'lat': 1.290301, u'lon': 103.844555}
PARIS =  {u'lat': 48.856614, u'lon': 2.352222}
NYC =  {u'lat': 40.738187, u'lon': -74.005204}
location = NYC
theInteger = 0
def datetimeToTimestamp(datetime):
    split = str(datetime).split(' ')
    return split[0]+'T'+split[1]+'Z'
def processMessages(data):
    print data
class BaseClient():
    def __init__(self,token):
        self.req = url.HTTPSConnectionPool(URL)
        self.HEADERS = HEADERS
        r = requests.post(URL+'/auth', data= {"facebook_token":token}).json()
        self.HEADERS['X-Auth-Token'] = r['token']
        self.id = r['user']['_id']
    def updateLocation(self,location):
        return requests.post(URL+'/user/ping', headers=self.HEADERS, data=location).json()

    def likeUser(self, id):
        return requests.get(URL+'/like/' + id, headers=self.HEADERS).json()

    def getRecs(self):
        return requests.post(URL+'/user/recs', headers=self.HEADERS, data={"limit": 40}).json()

    def getUpdate(self, date='2014-04-07T06:36:49.027Z'):
        return requests.post(URL+'/updates', headers=self.HEADERS, data={'last_activity_date': date}).json()

    def sendMessage(self, message, matchid):
        return requests.post(URL+'/user/matches/' + matchid, headers=self.HEADERS, data={"message": message}).json()

class ExampleClient(BaseClient):

    def getUsers(self, numusers):
        users = []
        while(len(users) < numusers):
            users += self.getRecs()['results']
        return users

    def likeUsers(self, numUsers):
        users = self.getUsers(numUsers)
        for i in users:
            print self.likeUser(i['_id'])

    def likeUsers(self):
        global theInteger
        while True:
            try:
                rec = self.getRecs()['results']
                for i in rec:
                    self.likeUser(i['_id'])
                    theInteger+=1
                print theInteger
            except JSONDecodeError:
                print 'JsonError'
                time.sleep(60)
            except KeyError:
                break
    def SearchForMatchesLoop(self):
        global j
        threadPool = []
        ec = ExampleClient(facebook_token)
        for i in xrange(10):
            t = Thread(target=ec.likeUsers)
            t.start()
            threadPool.append(t)
        print 'Done creating threads'
        while True:
            if len([x for x in threadPool if x.is_alive()]) == 0:
                print 'Thread Pool is empty...', theInteger
                while not 'results' in ec.getRecs().keys():
                    time.sleep(20)
                print 'Found new people... restarting'
                Thread(target=main).start()
                break


HEADERS = {'Accept-Language': 'en-GB;q=1, en;q=0.9, fr;q=0.8, de;q=0.7, ja;q=0.6, nl;q=0.5',
           'User-Agent': 'Tinder/3.0.3 (iPhone; iOS 7.0.6; Scale/2.00)',
           'os_version': '70000000006',
           'Accept': '*/*',
           'platform': 'ios',
           'Connection': 'keep-alive',
           'Proxy-Connection': 'keep-alive',
           'app_version': '1',
           'Accept-Encoding': 'gzip, deflate',}
j = 0
def main():
    ec = ExampleClient(facebook_token)
    ec.SearchForMatchesLoop()


if __name__ == "__main__":
    main()


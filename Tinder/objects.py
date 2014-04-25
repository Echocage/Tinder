from datetime import date, datetime
import json
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
    def __init__(self, data):
        self.data = data

    @property
    def age(self):
        return calc_age(
            datetime.strptime(self.data['birth_date'].split('T')[0], "%Y-%M-%d").date())

    @property
    def id(self):
        return self.data['_id']

    @property
    def name(self):
        return self.data['name']

    @property
    def bio(self):
        return self.data['bio']

    def __str__(self):
        return str(self.data)

    def sum(self):
        print "[{}{}]".format(self.getName, self.getAge()), ": \t", self.data['bio'].replace('\n', '\t'),

    def __repr__(self):
        return self.getName()
class message():
    def __init__(self,data):
        self.data = data

    @property
    def x(self):
        return self.data['sent_data']
    
    @property
    def match_id(self):
        return self.data['match_id']

    @property
    def timestamp(self):
        return self.data['timestamp']

    @property
    def to(self):
        return self.data['to']
    @property
    def created_data(self):
        return self.data['created_data']

    @property
    def fromField(self):
        return self.data['from']

    @property
    def message(self):
        return self.data['message']
    @property
    def id(self):
        return self.data['_id']

    def __str__(self):
        return message

class userOverview():
    def __init__(self, data):
        self.data = data
        self.user = person(data['person'])
    @property
    def match_id(self):
        return self.data['_id']
    @property
    def messages(self):
        return [message(x) for x in self.data['messages']]

    @property
    def closed(self):
        return self.data['closed']


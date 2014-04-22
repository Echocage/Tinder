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
        if type(data) is str:
            self.data = json.JSONDecoder().decode(data)
        else:
            if type(data) is dict:
                self.data = data
            else:
                raise Exception("Person isn't a string or dict")

    def getAge(self):
        return self.age if hasattr(self, 'age') else calc_age(
            datetime.strptime(self.data['birth_date'].split('T')[0], "%Y-%M-%d").date())

    def getId(self):
        return self.data['_id']

    def getName(self):
        return self.data['name']

    def getBio(self):
        return self.data['bio']

    def __str__(self):
        return str(self.data)

    def sum(self):
        print "[{}{}]".format(self.getName, self.getAge()), ": \t", self.data['bio'].replace('\n', '\t'),

    def __repr__(self):
        return self.getName()

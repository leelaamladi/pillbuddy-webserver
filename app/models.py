from mongoengine import *
import datetime

class Prescription(EmbeddedDocument):
    name = StringField(max_length=60, required=True)
    amount = StringField(required=True)
    description = StringField(max_length=149, required=True)
    doctor = StringField(max_length=40, required=True)
    morningalarm = BooleanField(default=False, required=True)
    afternoonalarm = BooleanField(default=False, required=True)
    eveningalarm = BooleanField(default=False, required=True)
    nightalarm = BooleanField(default=False, required=True)

    def to_dict(self):
        props = {}
        props['name'] = str(self.name)
        props['amount'] = str(self.amount)
        props['description'] = str(self.description) 
        props['doctor'] = str(self.doctor)
        props['morningalarm'] = self.morningalarm
        props['afternoonalarm'] = self.afternoonalarm
        props['eveningalarm'] = self.eveningalarm
        props['nightalarm'] = self.nightalarm
        return props
        
    def time_sort(self):
        props = {}
        props['name'] = str(self.name)
        props['amount'] = str(self.amount)
        return props

class Follower(EmbeddedDocument) :
    email = StringField(required=False)
    phonenumber = StringField(required=False)
    twitter = StringField(required=False)
    phone_on = BooleanField(default=False, required=True)
    email_on = BooleanField(default=False, required=True)
    twitter_on = BooleanField(default=False, required=True)

    def to_dict(self):
        props = {}
        props['email'] = str(self.email)
        props['phonenumber'] = str(self.phonenumber)
        props['twitter'] = str(self.twitter) 
        props['phone_on'] = bool(self.phone_on)
        props['email_on'] = bool(self.email_on)
        props['twitter_on'] = bool(self.twitter_on)
        return props

class User(Document):
    username = StringField(max_length=25, required=True, unique=True)
    password = StringField(max_length=65, required=True)
    email = StringField(max_length=40, required=True, unique=True)
    phone = StringField(max_length=15)
    first_name = StringField(max_length=25, required=True)
    last_name = StringField(max_length=25, required=True)
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    prescriptions = ListField(EmbeddedDocumentField(Prescription))
    followers = ListField(EmbeddedDocumentField(Follower, default=[]))

    def to_dict(self):
        chars = {}
        chars['username'] = str(self.username)
        chars['password'] = str(self.password)
        chars['email'] = str(self.email)
        chars['phone'] = str(self.phone)
        chars['first_name'] = str(self.first_name)
        chars['last_name'] = str(self.last_name)
        
        chars['followers'] = []
        for follower in self.followers:
            chars['followers'].append(follower.to_dict())

        chars['prescriptions'] = []
        for prescription in self.prescriptions:
            chars['prescriptions'].append(prescription.to_dict())



import requests
import json
from flask import Flask, render_template
from flask_ask import (
                       Ask,
                       request as ask_request,
                       session as ask_session,
                       statement,
                       question as ask_question
                       )


app = Flask(__name__)
ask = Ask(app, "/")
ASK_APPLICATION_ID = "amzn1.ask.skill.1515a753-c518-417c-8970-3761cb905bd6"
app.config['ASK_VERIFY_REQUESTS'] = False

@ask.intent('FindPerson')
def find_person():
    print "invoking find team"
    user = ask_request.intent.slots.User.value
    
    # if bob is looked for, we say, I last saw bob in cafeteria
    # if jane is looked for, we say, I last saw Jane with Joseph
    if user.lower() == "bob":
        text = "Last saw %s at Cafeteria" %(user)
    if user.lower() == "jane":
        text = "I think I saw Jane with Joseph"
    return statement(text)

@ask.intent('FindTeam')
def find_team():
    print "Invoking find team"
    # if team looked for is storage, we say they are all at table 13
    # if team looked for is unix, we say, havent seen them in past 13 hr
    team = ask_request.intent.slots.Team.value
    print team
    if team.lower() == "storage":
        text = "Last saw %s team at table 13" %(team)
    if team.lower() == "unix":
        text = "I have not seen the %s team in the past 13 hours" %(team)
    return statement(text)

@ask.intent('WhoAte')
def who_ate():
    print "invoking who ate"
    # if food is cookie, say I saw Jane eating it last. do you want to ask her
    food = ask_request.intent.slots.Food.value
    if food.lower() == "cookie":
        text = "I saw Jane eating it last. do you want to ask her"
    return statement(text)

@ask.intent('FindRoom')
def find_room():
    print "invoking find room"
    room = ask_request.intent.slots.Room.value
    print room
    text = "found " + room
    return statement(text)

@ask.intent('AMAZON.StopIntent')
def find_room():
    print "invoking Stop Intent"
    text = "ok canceling"
    return statement(text)



@ask.intent('BookARooom')
def find_room():
    print "invoking find room"
    room = ask_request.intent.slots.Name.value
    time = ask_request.intent.slots.Time.value
    
    url = "https://api.robinpowered.com/v1.0/spaces/39793/events"
    Authorization = "Access-Token nW0pUpuNu40dIq5wtzhZTwWx5iti8IAGUHXFnwZxtSGvCabzNq7C6OEyqZnXEjOYXYs22uuBz1WrH1rlVLDFVb7210mMT2awsW5D7IAaPxpd1Oom1WsHqw6cm4fRCdL1"
    headers = {
        "Authorization" : Authorization,
        "Content-Type" : "application/json",
    
    }
    payload = """{
        "description": "Alexa booked meeting",
        "start": {
        "date_time": "2017-11-30T21:30:00Z",
        "time_zone": "America/Los_Angeles"
        },
        "end": {
        "date_time": "2017-11-30T22:30:00Z",
        "time_zone": "America/Los_Angeles"
        },
        "invitees": [
        {
        "display_name": "Jane Doe",
        "email": "janedoe@josephyi.com"
        }
        ]
        }"""
    #payload = json.dumps(payload)
    #print type(payload)
    response = requests.request("POST", url, headers=headers, json = payload)
    print response
    text = "Ok Table 13 is booked!"
    return statement(text)

"""
    
    https://api.robinpowered.com/v1.0/spaces/39793/events
    Authorization: Access-Token nW0pUpuNu40dIq5wtzhZTwWx5iti8IAGUHXFnwZxtSGvCabzNq7C6OEyqZnXEjOYXYs22uuBz1WrH1rlVLDFVb7210mMT2awsW5D7IAaPxpd1Oom1WsHqw6cm4fRCdL1
    Content-Type: application/json
    {
    "description": "Alexa booked meeting",
    "start": {
    "date_time": "2017-11-30T21:30:00Z",
    "time_zone": "America/Los_Angeles"
    },
    "end": {
    "date_time": "2017-11-30T22:30:00Z",
    "time_zone": "America/Los_Angeles"
    },
    "invitees": [
    {
    "display_name": "Jane Doe",
    "email": "janedoe@josephyi.com"
    }
    ]
    }
    """


if __name__ == '__main__':
    app.run(debug=True)


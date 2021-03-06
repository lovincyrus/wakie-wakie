#!/usr/local/bin/python

import os
import bottle
from bottle import route, run, post, Response
from twilio.rest import Client

app = bottle.default_app()

# Your Account SID from twilio.com/console
ACCOUNT_SID = os.environ['ACCOUNT_SID']

# Your Auth Token from twilio.com/console
AUTH_TOKEN = os.environ['AUTH_TOKEN']

twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '+16473602674')
BASE_URL = os.environ.get('BASE_URL', 'https://wakie-wakie.herokuapp.com')

calls = twilio_client.calls.list()


@route('/')
def index():
    """Returns standard text response to show app is working."""
    return Response("wakie wakie is up and running!")

@route('/call-logs')
def call_logs():
    for record in calls:
        return (record.sid)


@route('/call/<outbound_phone_number>')
def outbound_call(outbound_phone_number):
    """Uses the Twilio Python helper library to send a POST request to
    Twilio telling it to dial an outbound phone call from our
    specific Twilio phone number (that phone number must be owned by our
    Twilio account).
    """
    twilio_client.calls.create(to=outbound_phone_number,
                               from_=TWILIO_NUMBER,
                               url=BASE_URL)
    return Response('Calling ' + outbound_phone_number)


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 9000)))
else:
    run(host="localhost", port=8080, debug=True)
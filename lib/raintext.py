""" Library for Rain Text notification system
"""
import requests
import simplejson as json
import sys
import yaml
from twilio.rest import TwilioRestClient

def get_config(f):
    """ Load YAML config from file
    """
    with open(f, 'r') as config_file:
        config = yaml.load(config_file)

        return config

def get_today_rain(weather_underground_key, loc_state, loc_city):
    """ Get today's expected rain for the given location
    """
    url = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (weather_underground_key, loc_state, loc_city)
    try:
        r = requests.get(url)
        j = json.loads(r.content)
        rain = float(j['current_observation']['precip_today_in'])

        return rain
    except:
        print "Failed to fetch rain data from Weather Underground API"
        sys.exit(1)


def send_rain_text(phone_number, twilio_phone_number, rain_amount, twilio_key, twilio_auth_token):
    """ Send a text to [phone number], with the expected rain
    """
    client = TwilioRestClient(twilio_key, twilio_auth_token)
    msg = "It's expected to rain %.1f inches today" % (rain_amount)
    client.messages.create(
            to=phone_number,
            from_=twilio_phone_number,
            body=msg
        )

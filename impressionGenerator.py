import argparse
import http.client
import json
import random
import requests
import string

from time import sleep
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num', dest='impressionCount', type=int, required=True, help='Number of impressions to generate')
parser.add_argument('-v', '--videoId', dest='videoId', type=str, required=True, help='Video ID')

parser.add_argument('-d', '--deviceId', dest='deviceId', type=str, help='DeviceID to use (randomised string by default)')
parser.add_argument('-s', '--serverUrl', dest='host', type=str, help='URL of the Overlay Engine to poke (http://localhost:3000 by default)')
parser.add_argument('-t', '--type', dest='type', choices=['overlay', 'upcoming'], help='Request type - default overlay')
parser.add_argument('--delay', dest='delay', type=int, help='Delay (in seconds) between requests. Default is none.')
parser.add_argument('--body', dest='body', type=int, help='Custom JSON to send in the request body')
args = parser.parse_args()

if 'args.deviceId' not in locals():
    args.deviceId = 'impressionGenerator:' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

if 'args.type' not in locals():
    args.type = 'overlay'

if 'args.host' not in locals():
    args.host = 'http://localhost:3000'

url = args.host + '/' + args.type + '/' + args.videoId

def get_impression_url():
    if (args.body):
        postBody = args.body
    else:
        postBody = json.loads("""{
            "platformId":"vizio",
            "authId": "authId",
            "deviceId":"MGDemo",
            "language":"en-US",
            "canHandleKeys":true,
            "model":"L7300",
            "call_sign":"",
            "city": "",
            "location": {
            "city" : "New York",
            "continent" : "Asia",
            "country" : "Vietnam",
            "geo" : [
            100.5018,
            13.7563
            ],
            "region" : "",
            "county" : "VN"
            }
            }""")

    postBody['deviceId'] = args.deviceId
    postBody['location']['city'] += '_' + str(random.randint(1, 1000000))
    r = requests.post(url, json=postBody)
    if (r.text == 'Not Found'):
        print('Could not generate impressions - no overlays were available')
        return False;
    else:
        return json.loads(r.text)['impressions'][0]

def logImpression(url):
    localUrl = url.replace('http://new-dev.sorensonpromote.com', args.host)
    r = requests.get(localUrl)
    if (r.text == 'OK'):
        print('Impression logged.')
    return r.text

for _ in range(args.impressionCount):
    impressionUrl = get_impression_url()
    if (impressionUrl):
        logImpression(impressionUrl)
        if (args.delay):
            sleep(args.delay)

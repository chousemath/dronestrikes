from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Attr
import requests
from datetime import datetime
from pprint import pprint
from time import time

LOWER_TIMESTAMP = 1467590400
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dronestrikes')

def str_to_ts(date_str: str) -> int:
    timestamp = 0

    try:
        timestamp = int(datetime.strptime(date_str.split('T')[0], '%Y-%m-%d').timestamp())
    except Exception as e:
        pprint(e)

    return timestamp

def safe_str_to_float(raw: str) -> float:
    if raw:
        try:
            return Decimal(raw)
        except Exception as e:
            print(e)
    return 0

def safe_str_to_int(raw: str) -> int:
    if raw:
        try:
            return int(raw)
        except Exception as e:
            print(e)
    return 0

class Dronestrike:
    def __init__(self, strike):
        self.id = strike['_id'] or 'n/a'
        self.num = strike['number']
        self.country = strike['country'] or 'n/a'
        self.ts = str_to_ts(strike['date'])
        self.desc = strike['narrative'] or 'n/a'
        self.sum = strike['bij_summary_short'] or 'n/a'
        self.town = strike['town'] or 'n/a'
        self.loc = strike['location'] or 'n/a'
        self.deaths = strike['deaths'] or 'n/a' # str
        self.deaths_min = safe_str_to_int(strike['deaths_min'])
        self.deaths_max = safe_str_to_int(strike['deaths_max'])
        self.civ = strike['civilians'] or 'n/a'
        self.target = strike['target'] or 'n/a'
        self.injuries = strike['injuries'] or 'n/a'
        self.children = strike['children'] or 'n/a'
        self.lat = safe_str_to_float(strike['lat'])
        self.lon = safe_str_to_float(strike['lon'])

    def format(self):
        return {
                'id': self.id,
                'num': self.num,
                'country': self.country,
                'ts': self.ts,
                'desc': self.desc,
                'sum': self.sum,
                'town': self.town,
                'loc': self.loc,
                'deaths': self.deaths,
                'deaths_min': self.deaths_min,
                'deaths_max': self.deaths_max,
                'civ': self.civ,
                'target': self.target,
                'injuries': self.injuries,
                'children': self.children,
                'lat': self.lat,
                'lon': self.lon,
                }


root_url = 'http://api.dronestre.am/data'

def reads(event, ctx):
    try:
        ts = int(event['ts']) if 'ts' in event else LOWER_TIMESTAMP
        response = table.scan(FilterExpression=Attr('ts').gt(ts))
        items = response['Items']
        return {'ok': True, 'data': items}
    except Exception as e:
        return {'ok': False, 'data': e}


def update(event, ctx):
    try:
        res = requests.get(root_url)
        data = res.json()
        if data['status'] == 'OK':
            with table.batch_writer() as batch:
                for strike in data['strike']:
                    dstrike = Dronestrike(strike)
                    batch.put_item(Item=dstrike.format())
    except Exception as e:
        print(e)

    return {
            'ok': True,
            }

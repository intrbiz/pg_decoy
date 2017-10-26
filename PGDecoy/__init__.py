from logging import ERROR, INFO, DEBUG, WARNING, CRITICAL

from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres

import requests

class PGDecoyDriverBergamot:

    def __init__(self, options):
        self.host = options.get('host', None)
        self.key  = options.get('key', None)
        self.trap = options.get('trap', None)
        self.pot = options.get('pot', 'unknown')

    def fire(self):
        requests.post(
            'https://' + self.host + '/api/trap/id/' + self.trap + '/submit', 
            headers = { 
                'Content-type': 'application/x-www-form-urlencoded',
                'Authorization': self.key
            }, 
            data = { 
                'status': 'CRITICAL', 
                'output': 'Honeypot ' + self.pot + ' triggered'
            }
        )

class PGDecoyDriverWebhook:

    def __init__(self, options):
        self.url = options.get('url', 'http://127.0.0.1/honeypot')
        self.authorization  = options.get('authorization', None)
        self.pot = options.get('pot', 'unknown')

    def fire(self):
        headers = { 
            'Content-type': 'application/x-www-form-urlencoded'
        }
        if self.authorization != None:
            headers['Authorization'] = self.authorization
        requests.post(
            self.url, 
            headers = headers, 
            data = { 
                'pot': self.pot
            }
        )


class PGDecoyFDW(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(PGDecoyFDW, self).__init__(options, columns)
        self.columns = columns
        self.loadDriver(options)
    
    def loadDriver(self, options):
        driver = options.get('driver', 'webhook')
        if driver == 'bergamot':
            self.driver = PGDecoyDriverBergamot(options)
        elif driver == 'webhook':
            self.driver = PGDecoyDriverWebhook(options)
        else:
            raise Exception('Unknown decoy driver: ' + driver)

    def execute(self, quals, columns):
        self.driver.fire()

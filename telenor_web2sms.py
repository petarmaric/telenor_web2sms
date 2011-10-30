import json
import requests


__version__ = '1.0.1'


class TelenorWeb2SMSException(Exception):
    """A generic exception for all others to extend.""" 
    
    def __str__(self):
        # Use the class docstring if the exception message hasn't been provided
        if len(self.args) == 0:
            return self.__doc__
        return super(TelenorWeb2SMSException, self).__str__()


class AuthenticationFailure(TelenorWeb2SMSException):
    """The given username and password might not be correct."""


class SMSNotSent(TelenorWeb2SMSException):
    """SMS has not been sent."""


class UnsupportedPhoneNumberFormat(TelenorWeb2SMSException):
    """The given phone number isn't in any of the supported formats."""


class TelenorWeb2SMS(object):
    auth_url = 'https://www.telenor.rs/portal/index.php'
    send_sms_url = 'https://www.telenor.rs/portal/usluge/sendsms.php'
    
    def __init__(self, username, password, auth_url=None):
        self.session = requests.session(headers={
            'User-Agent': "telenor_web2sms/%s" % __version__,
        })
        self.auth(username, password, auth_url)
    
    def auth(self, username, password, auth_url=None):
        auth_url = auth_url or self.auth_url
        
        r = self.session.post(
            url=auth_url,
            data={
                'brtel': username,
                'lozinka': password,
            }
        )
        # Check if we made a bad request
        r.raise_for_status()
        if r.url == self.auth_url:
            raise AuthenticationFailure()
    
    def parse_phone_number(self, phone_number):
        if phone_number.startswith('0'):
            normalized = phone_number[1:]
        elif phone_number.startswith('+381'):
            normalized = phone_number[4:]
        else:
            raise UnsupportedPhoneNumberFormat()
        
        area_code = normalized[:2]
        number = normalized[2:]
        return area_code, number
    
    def send_sms(self, phone_number, message, send_sms_url=None):
        send_sms_url = send_sms_url or self.send_sms_url
        
        area_code, number = self.parse_phone_number(phone_number)
        r = self.session.post(
            url=send_sms_url,
            data={
                'pozivni': area_code,
                'BBroj': number,
                'smsporuka': message,
            }
        )
        
        # Check if we made a bad request
        r.raise_for_status()
        j = json.loads(r.content)
        if j['status'] != 'OK':
            raise SMSNotSent("SMS has not been sent, because '%s'." % j['message'])
    
    def __call__(self, phone_number, message, send_sms_url=None):
        self.send_sms(message, phone_number, send_sms_url)

def main():
    import argparse
    import os
    import sys
    
    def env(e):
        return os.environ.get(e, '')
    
    parser = argparse.ArgumentParser(
        description='Send a SMS through the Telenor WEB2SMS web app'
    )
    
    parser.add_argument(
        '-u',
        '--username',
        default = env('TELENOR_WEB2SMS_USERNAME'),
        help='Your Telenor WEB2SMS username. Defaults to env[TELENOR_WEB2SMS_USERNAME]'
    )
    
    parser.add_argument(
        '-p',
        '--phone-number',
        help='Recipients phone number'
    )
    # As Telenor WEB2SMS cuts of newlines, there's no point in allowing
    # multiline input.
    parser.add_argument(
        '-m',
        '--message',
        help='Message to send'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version="%(prog)s " + __version__
    )
    args = parser.parse_args()
    
    try:
        # Authenticate to Telenor WEB2SMS
        username = args.username or raw_input('What is your Telenor WEB2SMS username? ')
        password = env('TELENOR_WEB2SMS_PASSWORD') or raw_input('What is your Telenor WEB2SMS password? ')
        web2sms = TelenorWeb2SMS(username, password)
        
        # Send SMS
        phone_number = args.phone_number or raw_input('Who are you sending this SMS to? ')
        message = args.message or raw_input('Enter your message: ')
        web2sms.send_sms(phone_number, message)
        print 'SMS sent successfully.'
    except Exception, e:
        print >> sys.stderr, "ERROR:", e
        sys.exit(1)

if __name__ == '__main__':
    main()

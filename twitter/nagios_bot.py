import urlparse
import oauth2 as oauth
import argparse
import sys
import urllib

'''
Nagios_bot: https://dev.twitter.com/apps/815483
__author__="David Busby"
__copyright__="David Busby <d.busby@saiweb.co.uk>"
__license__="GNU v3 + part 5d section 7: Redistribution/Reuse of this code is permitted under the GNU v3 license, as an additional term ALL code must carry the original Author(s) credit in comment form."
'''

#This is realy just a glorified twitter updater with oauth enabled, if you want to use the code with your own twitter app
#change these keys

CONSUMER_KEY=''
CONSUMER_SECRET=''


REQUEST_TOKEN_URL   = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL    = 'https://api.twitter.com/oauth/access_token'
AUTHORIZE_URL       = 'https://api.twitter.com/oauth/authorize'
UPDATE_URL          = 'http://api.twitter.com/1/statuses/update.json'


def setup():
    '''
        Adapted from readme here: https://github.com/simplegeo/python-oauth2
    '''
    print 'Running Nagios_bot Setup ...'
    print
    consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    client = oauth.Client(consumer)
    resp, content = client.request(REQUEST_TOKEN_URL, "GET")

    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))
    print "Request Token:"
    print "    - oauth_token        = %s" % request_token['oauth_token']
    print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
    print

    # Step 2: Redirect to the provider. Since this is a CLI script we do not
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (AUTHORIZE_URL, request_token['oauth_token'])
    print

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
    oauth_verifier = raw_input('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this
    # access token somewhere safe, like a database, for future use.
    token = oauth.Token(request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(ACCESS_TOKEN_URL, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    print "Access Token:"
    print "    - oauth_token        = %s" % access_token['oauth_token']
    print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
    print
    print "You may now access protected resources using the access tokens above."
        
def alert(token_key,token_secret,consumer_key,consumer_secret,update):

    token = oauth.Token(key=token_key, secret=token_secret)
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)


    client = oauth.Client(consumer, token)

    request_uri = 'https://api.twitter.com/1/statuses/update.json'
    data = {'status': update[:140]}
    resp, content = client.request(request_uri, 'POST', urllib.urlencode(data))

    print resp
   

def main():
    parser = argparse.ArgumentParser(description="Nagios_bot python, essentialy a glorified cli python twitter updater (https://dev.twitter.com/apps/815483)")
    parser.add_argument('-s', '--setup',action='store_true')
    parser.add_argument('-u', '--update',nargs=3,metavar=('token_key','token_secret','update_message'))
    args = parser.parse_args()
    if args.setup == True:
        setup()
        sys.exit()
    elif len(args.update) == 3:
        alert(args.update[0],args.update[1],CONSUMER_KEY,CONSUMER_SECRET,args.update[2])
    
    
if __name__ == '__main__':
    main()
    
#!/usr/bin/env python

###############################################################################
#
#   Config
#

TWITTER_USERNAME    =   'mikewest'
TWEET_ROOT          =   './twitter'

###############################################################################
#
#   Code
#

import os, sys, re
import json, yaml, urllib2
import errno, rfc822, calendar

def write_tweet( obj ):
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                pass
            else: raise
    obj['user'] = None
    parsedtime  = rfc822.parsedate(obj['created_at'])
    created     = calendar.timegm(parsedtime)
    obj['id']   = str( obj['id'] )
    path = '%s/%04d/%02d/%02d' % ( TWEET_ROOT, parsedtime[0], parsedtime[1], parsedtime[2] )
    mkdir_p( path )
    filename = '%s/%04d%02d%02d%02d%02d-%s.yaml' % ( path, parsedtime[0], parsedtime[1], parsedtime[2], parsedtime[3], parsedtime[4], obj['id'] )
    print "Writing %s" % filename
    with open( filename, 'w' ) as outputFile:
        outputFile.write( 
          yaml.safe_dump(
            obj,
            default_flow_style=False,
            allow_unicode=True,
            encoding='utf-8',
            explicit_start=True,
            explicit_end=True,
            indent = 2 ) )
    os.utime( filename, ( created, created ) )

def get_latest_tweet_id():
    max  = ''
    tree = os.walk( '%s/' % TWEET_ROOT )
    for directory in tree:
        for file in directory[2]:
            if file > max:
                max = file
    m = re.search( '-(\d+).yaml', file ) 
    return m.group( 1 )

def get_tweets_since( id ):
    endpoint = 'http://twitter.com/statuses/user_timeline/%s.json?count=200&since_id=%s' % ( TWITTER_USERNAME, id )
    t = urllib2.urlopen( endpoint )
    tweets = json.load( t )
    return tweets

def main():
    id = get_latest_tweet_id()
    print "Last local tweet is #%s, asking Twitter for newer tweets." % id
    
    for tweet in get_tweets_since( id ):
        write_tweet( tweet )

    print "All done!"
    return True

if __name__ == '__main__':
    main()

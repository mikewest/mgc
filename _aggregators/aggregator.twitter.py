#!/usr/bin/env python

###############################################################################
#
#   Config
#

TWITTER_USERNAME    =   'mikewest'
TWEET_ROOT          =   '/home/git/mirrored-repositories/mgc/twitter'

###############################################################################
#
#   Code
#

import os, sys, re
import json, yaml
from aggregator.aggregator import Aggregator

class AggregateTwitter( Aggregator ):
    def __init__( self ):
        self.latest_id = ''
        self.tweets    = []

    def aggregate( self ):
        self.get_latest_tweet_id()
        print "Last local tweet is #%s, asking Twitter for newer tweets." % self.latest_id
       
        self.get_new_tweets()
        for tweet in self.tweets:
            self.write_tweet( tweet )

        print "All done!"
        return True
    
    def get_latest_tweet_id( self ):
        self.latest_id  = ''
        tree = os.walk( '%s/' % TWEET_ROOT )
        for directory in tree:
            for file in directory[2]:
                if file > self.latest_id:
                    self.latest_id = file
        m = re.search( '-(\d+).yaml', file ) 
        self.latest_id = m.group( 1 )

    def get_new_tweets( self ):
        endpoint = 'http://twitter.com/statuses/user_timeline/%s.json?count=200&since_id=%s'
        t = self.fetch( endpoint % ( TWITTER_USERNAME, self.latest_id ) )
        self.tweets = json.load( t )

    def write_tweet( self, obj ):
        obj['text'] = re.sub(
                        self.MATCH_URL,
                        self.normalize_matched_url, 
                        obj['text'] )

        obj['user'] = None
        obj['id']   = str( obj['id'] )
        parsedtime  = self.parse_rfc822( obj['created_at'] )
        created     = self.mktime( parsedtime )

        path = '%s/%04d/%02d/%02d' % ( TWEET_ROOT, parsedtime[0], parsedtime[1], parsedtime[2] )
        self.mkdir_p( path )

        filename = '%s/%04d%02d%02d%02d%02d-%s.yaml' % ( path, parsedtime[0], parsedtime[1], parsedtime[2], parsedtime[3], parsedtime[4], obj['id'] )

        print "Writing %s" % filename
        with open( filename, 'w' ) as outputFile:
            outputFile.write( self.yaml( obj ) )
        self.set_timestamp( filename, created )

if __name__ == '__main__':
    a = AggregateTwitter()
    a.aggregate()

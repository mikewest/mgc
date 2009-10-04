#!/usr/bin/env python

###############################################################################
#
#   CONFIGURATION
#

STARRED_FEED    =   'http://www.instapaper.com/starred/rss/203164/fvc7FjLu4aIN5wsniOahrlWgbLw'
INSTAPAPER_ROOT =   './instapaper'

###############################################################################
#
#   CODE
#

import os, sys, re
from xml.etree.cElementTree import parse
from aggregator.aggregator import Aggregator

class AggregateInstapaper( Aggregator ):
    def __init__( self ):
        self.articles = []

    def aggregate( self ):
        print "Asking Instapaper for new starred articles."
       
        self.get_new_articles()
        for article in self.articles:
            self.write_article( article )

        print "All done!"
        return True

    def get_new_articles( self ):
        rss = self.fetch( STARRED_FEED )
        xml = parse( rss )
        for element in xml.findall( 'channel/item' ):
            link    =   {
                            'guid':             element.find('guid').text,
                            'title':            element.find('title').text,
                            'url':              element.find('link').text,
                            'description':      element.find('description').text,
                            'published':        element.find('pubDate').text,
                            'starred':          True,
                            'tags':             ['instapapered','starred','ireadthis']
                        }
            m = re.search( r'(\d+)$', link['guid'] )
            link['id'] = m.group( 1 )
            self.articles.append( link )

    def write_article( self, obj ):
        parsedtime  = self.parse_rfc822( obj['published'] )
        created     = self.mktime( parsedtime )

        path = '%s/%04d/%02d/%02d' % ( INSTAPAPER_ROOT, parsedtime[0], parsedtime[1], parsedtime[2] )
        self.mkdir_p( path )

        filename = '%s/%04d%02d%02d%02d%02d-%s.yaml' % ( path, parsedtime[0], parsedtime[1], parsedtime[2], parsedtime[3], parsedtime[4], obj['id'] )

        if not os.path.exists( filename ):
            obj['url'] = self.normalize_url( obj['url'] )
            print "Writing %s" % filename
            with open( filename, 'w' ) as outputFile:
                outputFile.write( self.yaml( obj ) )
            self.set_timestamp( filename, created )

if __name__ == '__main__':
    a = AggregateInstapaper()
    a.aggregate()

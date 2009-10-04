# -*- coding: utf-8 -*-

import os, sys, re, urllib2, errno, rfc822, calendar, yaml

class Aggregator( object ):
    MATCH_URL = r'(http[s]?://[a-zA-Z0-9]+(?:[-.]{1}[a-z0-9]+)*\.[a-z]{2,5}/\S+?)(?:[\)\]\.\s]|$)';

    ###########################################################################
    #
    #   Helper functions, useful for all aggregators
    #
    def fetch( self, url ):
        """Wrapper for urllib2 call"""
        try:
            return urllib2.urlopen( url, timeout=5 )
        except urllib2.URLError:
            raise

    def mkdir_p( self, path ):
        try:
            os.makedirs(path)
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                pass
            else: raise

    def shorten_url( self, url ):
        """
            Returns a truncated version of a provided URL:

            "http://example.com/abcdefghijklmnopqrstuvwxyz" => "http://example.com/abcd...wxyz"
        """
        mo      = re.match( r'(http[s]?://.+?)(/.+)', url )
        if mo:
            host    = mo.group( 1 )
            path    = mo.group( 2 )
            if len( path ) > 10:
                path = '%s&hellip;%s' % ( path[:5], path[-4:] )
            return "%s%s" % ( host, path )

    def normalize_url( self, url ):
        """
            Requests a page, following redirects to determine the cannonical URL
        """
        try:
            x = self.fetch( url )
            return "[%s](%s)" % ( self.shorten_url( x.geturl() ), x.geturl() )
        except urllib2.HTTPError, urllib2.URLError:
            return url

    def normalize_matched_url( self, matchobj ):
        return self.normalize_url( matchobj.group( 1 ) )

    def parse_rfc822( self, timestring ):
        return rfc822.parsedate( timestring )

    def mktime( self, timetuple ):
        return calendar.timegm( timetuple )

    def yaml( self, obj ):
      return yaml.safe_dump(
        obj,
        default_flow_style=False,
        allow_unicode=True,
        encoding='utf-8',
        explicit_start=True,
        explicit_end=True,
        indent = 2 ) 

    def set_timestamp( self, filename, created ):
        os.utime( filename, ( created, created ) )

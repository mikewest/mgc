---
layout:     post
title:      "Playing with Placemaker"
slug:       "playing-with-placemaker"
aliases:
    - http://blog.mikewest.org/post/110959538
    - http://blog.mikewest.org/post/110959538/playing-with-placemaker
tags: 
    - yahoo
    - placemaker
    - api
    - geolocation
    - xml
    - curl
---
Yahoo's latest API is really quite cool: [Placemaker][] takes your unstructured data (e.g. any HTML page, RSS feed, etc), and extracts a nice list of _locations_ that your data refers to.  It's a brilliant tool, and I can think of quite a few ways I'd like to use it in the future.  Along with their release of a _ton_ of [WhereOnEarth ID codes][woe] that allows you to make use of Yahoo's various geo-services, this is a really good day to play with geocoding unstructured data.

So, let's play:

Accessing Placemaker is simple: assuming that you've somehow managed to [obtain an application id][appid], you simply make an HTTP `POST` request to Yahoo!'s Placemaker endpoint with a tiny bit of data specifying the nature of the data you're dealing with, and it's URL.  If you like `curl` on the command line, this might look like:

    curl -d 'inputLanguage=en-US&documentType=text/html&documentURL=http://mikewest.org/&appid=[APPID]' http://wherein.yahooapis.com/v1/document
    
You'll get back an XML document (RSS is also available as a response format).  Digging into the contents yields:

*   Boilerplate:

        <?xml version="1.0" encoding="utf-8"?>
        <contentlocation xmlns:yahoo="http://www.yahooapis.com/v1/base.rng" xmlns="http://wherein.yahooapis.com/v1/schema" xml:lang="de-DE">
          <processingTime>0.380778</processingTime>
          <version> build 090508</version>
          <documentLength>15906</documentLength>

*   A (list of) document element(s) containing the extracted locations:

          <document>

*   A best guess at the document's "scope" (the smallest region that "best
    describes" the document):
    
            <administrativeScope>
              <woeId>20071093</woeId>
              <type>County</type>
              <name><![CDATA[Munich, Bavaria, DE]]></name>
              <centroid>
                <latitude>48.1549</latitude>
                <longitude>11.5417</longitude>
              </centroid>
            </administrativeScope>
            <geographicScope>
              <woeId>29388625</woeId>
              <type>MMA</type>
              <name><![CDATA[MMA München, Bavaria, DE]]></name>
              <centroid>
                <latitude>48.1549</latitude>
                <longitude>11.5417</longitude>
              </centroid>
            </geographicScope>

*   Latitude/longitude for a bounding box that contains the places mentioned
    in the document (which makes it trivial to draw an "area of discussion" on
    a map):
    
            <extents>
              <center>
                <latitude>48.1364</latitude>
                <longitude>11.5775</longitude>
              </center>
              <southWest>
                <latitude>48.0417</latitude>
                <longitude>11.3771</longitude>
              </southWest>
              <northEast>
                <latitude>48.2292</latitude>
                <longitude>11.749</longitude>
              </northEast>
            </extents>
            
*   Detailed breakdown of the places mentioned in your document, giving you
    lat/long coordinates identifying the place's center point.  Moreover, it
    tells you _where_ in your document the place was found (string offsets
    _and_ XPath expressions, to each their own).  This is helpful for those
    occasions when the text you've entered doesn't exactly match the place's
    name that Yahoo returns ("Munich" vs. "Munich, Bavaria, DE", in this
    example)  Annotating your documents with this data should be a piece of
    cake.
    
            <placeDetails>
              <place>
                <woeId>676757</woeId>
                <type>Town</type>
                <name><![CDATA[Munich, Bavaria, DE]]></name>
                <centroid>
                  <latitude>48.1364</latitude>
                  <longitude>11.5775</longitude>
                </centroid>
              </place>
              <matchType>0</matchType>
              <weight>1</weight>
              <confidence>7</confidence>
            </placeDetails>
            <referenceList>
              <reference>
                <woeIds>676757</woeIds>
                <start>50</start>
                <end>56</end>
                <isPlaintextMarker>0</isPlaintextMarker>
                <text><![CDATA[Munich]]></text>
                <type>xpathwithcounts</type>
                <xpath><![CDATA[/html[1]/body[1]/div[2]/div[1]/p[1]]]></xpath>
              </reference>
            </referenceList>
            
*   And some more boilerplate.  :)

          </document>
        </contentlocation>

Full documentation of the Placemaker [query parameters][query] and [response format][response] are available on YDN.  Christian has put together a demo of a [basic PHP implementation][php] (though it's XSSable, and shouldn't ever be used in production).

In general, this is _brilliant_ stuff.  I'm looking forward to playing with it!

[Placemaker]: http://developer.yahoo.com/geo/placemaker/guide/
[woe]: http://developer.yahoo.com/geo/geoplanet/data/
[appid]: http://developer.yahoo.com/wsregapp/
[query]: http://developer.yahoo.com/geo/placemaker/guide/api_docs.html#query_parameters
[response]: http://developer.yahoo.com/geo/placemaker/guide/api-reference.html
[php]: http://isithackday.com/hacks/placemaker/

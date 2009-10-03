---
layout:     post
title:      "(Mildly) improving Google Analytics' JS Embed"
slug:       "mildly-improving-google-analytics-js-embed"
aliases:
    - http://blog.mikewest.org/post/102353505
    - http://blog.mikewest.org/post/102353505/mildly-improving-google-analytics-js-embed
tags: 
    - googleanalytics
    - google
    - javascript
---
Celebrity that I am, I use Google Analytics to figure out exactly how many
times I've visited my own website in a given day.  The interface is
surprisingly good (given that it's a Google app), and generally I'm happy with
the service.  Also, it's free (assuming that you don't worry about giving
Google _even more_ of your data).  Yay free.

The JavaScript that Google suggests using to embed their tracking code,
however, is a bit wasteful.  Take a look:

    <script type="text/javascript">
      var gaJsHost = (
        ( "https:" == document.location.protocol ) ?
          "https://ssl." :
          "http://www."
        );
      document.write(
        unescape( "%3Cscript src='"             +
                  gaJsHost                      +
                  "google-analytics.com/ga.js'" +
                  " type='text/javascript'%3E%3C/script%3E"
        )
      );
    </script>
    <script type="text/javascript">
      try {
        var pageTracker = _gat._getTracker("[YOUR TRACKING NUMBER]");
        pageTracker._trackPageview();
      } catch(err) {}
    </script>
    
I understand why they need to differentiate SSL requests, but passing a cobbled-together string through `unescape` before feeding it to `document.write` is a bit much, don't you think?  Also, injecting `pageTracker` and `gaJsHost` as new global variables isn't particularly friendly.

Given that I can make the assumption that this site is unencrypted, let's change the code a bit to fix these two points:

    <script
      type="text/javascript"
      src="http://www.google-analytics.com/ga.js"></script>
    
    <script type="text/javascript">
      /*globals _gat */
      try {
        ( function ( $g ) {
          $g._getTracker("[YOUR TRACKING NUMBER]")._trackPageview();
        }( _gat ) );
      } catch ( err ) {}
    </script>

That's a little better.  And it even [JSLints][lint].

[lint]: http://jslint.com/

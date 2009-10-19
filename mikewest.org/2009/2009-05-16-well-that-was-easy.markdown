---
layout:     post
title:      "Well.  That was easy."
slug:       "well-that-was-easy"
aliases:
    - http://blog.mikewest.org/post/108618244
    - http://blog.mikewest.org/post/108618244/well-that-was-easy
tags: 
    - spidermonkey
    - python
    - jslint
Teaser:     "Getting JSLint running inside Spidermonkey was much simpler than I expected it to be."
---
Getting [JSLint running inside Spidermonkey][that] was much simpler than I expected it to be:

    [14:12] src/jslint $ python
    Python 2.6.2 (release26-maint, Apr 19 2009, 01:58:18) 
    [GCC 4.3.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import spidermonkey
    >>> rt = spidermonkey.Runtime()
    >>> cx = rt.new_context()
    >>> text = file( './fulljslint.js' ).read()
    >>> cx.execute( text )
    u'use strict'
    >>> cx.execute( text + 'JSLINT("i++", {})' )
    False
    >>> cx.execute( text + 'JSLINT("i++", {}); JSLINT.report();' )
    u'<div id=errors><i>Error:</i><p><i>Implied global:</i> <code>i</code>&nbsp;<i>1</i></p><p>Problem at line 1 character 4: Missing semicolon.</p><p class=evidence>i++</p></div><br><div id=functions><div><i>No new global variables introduced.</i></div></div>'

Yay!

[that]: http://blog.mikewest.org/post/108613427/running-python-spidermonkey-on-jeos

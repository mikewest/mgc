---
layout:     post
title:      "Mnot's Redbot"
slug:       "mnots-redbot"
aliases:
    - http://blog.mikewest.org/post/111856958
    - http://blog.mikewest.org/post/111856958/mnots-redbot
tags: 
    - redbot
    - mnot
    - python
    - code
    - webdev
    - testing
    - http
    - headers
    - github
Teaser:     "Mark Nottingham has put together a really useful tool that aids in the analysis of the behavior of HTTP resources.  I've started putting together a command line version based on the web version he's released on GitHub."
---
[Mark Nottingham][mnot] has put together a really useful tool that aids in the analysis of the behavior of HTTP resources.  Visit [http://redbot.org/][redbot], type in a web address, and Redbot will report the resource's cachability based on the returned headers, and provide a helpful list of recommendations for improvement.

Running it on [http://mikewest.org/][mike], for instance, [flags the fact][redbotme] that I compress the response if the browser tells me that it can accept compressed content, but that I've neglected to send the proper `Vary` header to let caches know that the response needs to be negotiated, and cached based on the `Accept-Encoding` request header.  This is _useful_, especially for _actual_ applications for which it might matter.

So useful, in fact, that I'm forking it to submit some patches.  Mark's put the Redbot code up on GitHub ([mnot/redbot][github]), and I've started putting together a [command line version][cli] based on the web version he's built.

I've mentioned that [I love GitHub][heart], right?  This is exactly why.  :)

[mnot]:     http://www.mnot.net/
[redbot]:   http://redbot.org/
[mike]:     http://mikewest.org/
[github]:   http://github.com/mnot/redbot/tree/master
[redbotme]: http://redbot.org/?uri=http%3A%2F%2Fwww.mikewest.org%2F
[heart]:    http://mikewest.org/2008/11/i-love-github
[cli]: http://github.com/mikewest/redbot/blob/master/src/redbotcli.py

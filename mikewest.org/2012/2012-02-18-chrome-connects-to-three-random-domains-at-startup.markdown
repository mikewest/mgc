---
layout: post
title: "Chrome connects to three random domains at startup."
tags:
  - chrome
  - random
  - domain
  - startup
  - omnibox
  - codewalkthrough

Teaser:
  "When you start Chrome, it attempts to connect to three random domains. I've seen a
   few theories about why exactly this happens that brush up against the nefarious. 
   The true rationale is incredibly mundane: hopefully this short summary will clear 
   things up."
---
When you start Chrome, it attempts to connect to three random domains like `http://aghepodlln/` or `http://lkhjasdnpr/`. I've seen a [few][1] [theories][2] about why exactly this happens that brush up against the nefarious. The true rationale is incredibly mundane: hopefully this short summary will clear things up.

The goal of the requests is to determine if you're currently on a network that intercepts and redirects requests for nonexistent hostnames. For example, it's not at all uncommon for ISP to transparently redirect failed DNS lookups in order to convert requests like `http://text/` into requests for `http://your.helpful.isp/search?q=text`. Leaving aside a discussion of the rightness or wrongness of these "helpful" activities, this behavior causes problems for Chrome. Specifically, it breaks some heuristics the Omnibox uses to determine whether a user means to _search_ for a specific term, or to visit a non-standard domain name.

Google's internal network is a good example of how this can cause problems. Internally, a short-link service named "go" makes sharing memorable links straightforward. If I type "go" in Chrome's Omnibox and hit enter, it's not exactly clear whether I mean to visit `http://go/` or to search for "Go" (which is an interesting programming language, by the way). Chrome does its best to do The Right Thing™ in response to this sort of user input by executing a search, and then, in the background, executing a `HEAD` request for the potential domain. If the server responds, Chrome will display an infobar, asking if you meant to navigate to `http://go/`, and it will remember your response for future reference.

As you can see, this feature is completely broken if your ISP intercepts all such requests: you'd get infobars on every one-word search. So Chrome checks things out at startup, and whenever your IP address changes. And, Chrome is beautifully open-source, so let's take a quick look at the very straightforward implementation:

[`IntranetRedirectDetector`][3] is the place to start. When Chrome starts up, it creates an `IntranetRedirectorDetector` object. This sets up a short delay (currently hard-coded to 7 seconds) in order to ensure that it doesn't get in the way of time-critical startup activities, and then calls [`IntranetRedirectDetector::FinishSleep()`][4] where the real work begins. This method [generates three random domain names][5], and kicks off asynchronous `HEAD` requests to each in such a way that [they don't generate cache entries, and don't save cookies][6]. As each of these requests completes, [`IntranetRedirectDetector::OnURLFetchComplete()`][7] is called to record the result. If any two of the three requests resolve to the same host, that host is stored as the network's "redirect origin". Easy.

This information is used in [`AlternateNavURLFetcher`][8] to determine whether or not an infobar should be shown for a specific Omnibox-generated search. If the `HEAD` request returns the same site as the redirect origin Chrome saw at startup, then it's ignored. If it's a different origin, then a helpful infobar might be in order.

So there you have it. Chrome makes three requests to random domains just after startup in order to provide its Omnibox heuristics with enough information to correctly work out a user's intent. These requests are not sending your valuable data anywhere for nefarious purposes, nor are they useful for tracking purposes. The requests happen in order to fix [crbug.com/18942][9], and for no other reason.

[1]: http://stackoverflow.com/questions/7464378/why-is-google-chrome-pinging-mdioussrvd-and-other-random-hosts-that-dont-reso

[2]: http://www.freesmug.org/forum/t-433541/chromium-chrome-and-mysterious-server-connections

[3]: http://code.google.com/codesearch#OAMlx_jo-ck/src/chrome/browser/intranet_redirect_detector.h&exact_package=chromium&ct=rc&cd=1&sq=

[4]: http://code.google.com/codesearch#OAMlx_jo-ck/src/chrome/browser/intranet_redirect_detector.cc&l=63

[5]: http://code.google.com/codesearch#OAMlx_jo-ck/src/chrome/browser/intranet_redirect_detector.cc&l=79

[6]: http://code.google.com/codesearch#OAMlx_jo-ck/src/chrome/browser/intranet_redirect_detector.cc&l=87

[7]: http://code.google.com/codesearch#OAMlx_jo-ck/src/chrome/browser/intranet_redirect_detector.cc&l=95

[8]: http://code.google.com/codesearch#OAMlx_jo-ck/src/chrome/browser/alternate_nav_url_fetcher.cc&l=214

[9]: http://crbug.com/18942

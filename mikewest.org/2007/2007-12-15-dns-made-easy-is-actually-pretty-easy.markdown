---
Alias:
- http://mikewest.org/blog/id/85
Modified: '2007-12-15T14:09:56Z'
Teaser: In a spontaneous burst of productivity, spawned mostly by my complete and
    utter failure as a sysadmin, I moved my parent's email account off my server.  DNS
    Made Easy made this a trivial task.
layout: post
tags:
- Personal
- DNS
- DNSMadeEasy
title: DNS Made Easy is actually pretty easy
---
In a spontaneous burst of productivity, spawned mostly by my complete and utter failure as a sysadmin, I moved my parent's email account off my server, and onto Google's [Apps for your Domain][apps] platform.

This finally gave me an excuse to move my DNS hosting to [DNS Made Easy][dns].  The move turned out to be easier than I thought, and stunningly fast.  The dark times of multi-day propagation waiting-periods are (apparently) over: the whole process from account signup to complete and totally successful migration was about an hour.  I'm thrilled.  This is the best hosting-related $15 I've spent all year.

I've moved my parent's domain over, as well as `mikewest.org`.  While moving the latter, I had a little fun setting up "[Vanity DNS][vdns]."  I have _no_ need for this feature whatsoever, and it'll probably cause me some pain in the future whenever the nameserver IP addresses change for whatever reason, but it satisfies my inner geek to see `ns0.mikewest.org` as the canonical name server for my domain:

<img src="http://mikewest.org/images/5.png">

So, two thumbs up for [DNS Made Easy][dns].  They're absolutely living up to their name's promise.

## Potentially Useful Technical Note ##


Relatedly, the `lookupd` command is gone in Leopard.  If you want to clear your DNS cache under 10.5, you need to use `dscacheutil`.  I've added a quick alias to my `~/.bash_login` file, because I'm sure I'm going to forget this in about 10 minutes.

    alias flushcache='sudo dscacheutil -flushcache';
    
I'd suggest you do the same, if you plan on mucking about with DNS settings, or editing your hosts file.

[apps]: http://www.google.com/a/org/ "Google Apps"
[dns]: https://www.dnsmadeeasy.com/ "DNS Made Easy"
[vdns]: https://www.dnsmadeeasy.com/s0306/tuts/vanitydns.html "DNS Made Easy: Setting up your own Vanity DNS"
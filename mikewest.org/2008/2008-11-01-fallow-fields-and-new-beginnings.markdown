---
Alias:
- http://mikewest.org/blog/id/92
Modified: '2008-11-01T19:27:36Z'
Teaser: It's been quite some time since I put any serious effort into mikewest.org.  I've
    had tons of work, I've been burnt out, I've been complacent... the excuses pile
    on top of each other, each valid, each sufficient, none satisfactory.  For the
    sake of my own sanity, I need to start working on personal projects again.  Last
    week's GitHub dump was the first step in that direction.  Consider this relaunch
    to be the second.
layout: post
tags:
- personal
- mikewest.org
- projects
- fallow
- webdev
- development
title: Fallow fields and new beginnings
---
It's been quite some time since I put any serious effort into mikewest.org.  I've had tons of work, I've been burnt out, I've been complacent... the excuses pile on top of each other, each valid, each sufficient, none satisfactory.  For the sake of my own sanity, I need to start working on personal projects again.  Last week's [GitHub dump][dump] was the first step in that direction.  Consider this relaunch to be the second.

## A Brief History ##

The design has been sitting in my head and strewn across my hard drive in a few overlapping HTML files for months now.  The site as it stands today is most clearly influenced (both in form and function) by [Ryan Tomayko][tomayko], and his [stark interpretation][debris] of Tufte's admonitions against "administrative debris".  I couldn't bring myself to go quite as clean as Ryan, mostly because I was rapidly becoming enthralled with [Jon Tan][tan] and his absolutely [gorgeous site][tangerine].  I owe my current obsession with Baskerville to him.

I had mockups finished in June or July that more or less look like what you're seeing now.  I didn't, however, have the heart to put them up on top of the site as it sat.  Until today, mikewest.org was running on [TextPattern][], which is a fine CMS indeed, but one whose intricacies I've never been able to fully wrap my head around.  It's also stunningly inefficient.  Everything in TextPattern is a database hit; usually several.  The content is in the database, the templates are in the database, the plugins are _serialized PHP_ that sits in the database, and so on.  Doing anything at all in TextPattern requires some not insignificant amount of processing power, and caching isn't something that's built in.  

TextPattern wasn't the CMS I wanted to use going forward, but I had neither the inclination nor the time to investigate all the options that were out there.  Hosted services seemed like a copout (I'm a _webdev_, damnit!), and the rest seemed like too much work to get going.

So mikewest.org sat, empty, alone, partially broken, and unmaintained.  A sad website indeed.

## And then... ##

A month or two ago, [Carlo][] re-introduced me to [GitHub][], and something clicked.  If I simply sat down and _wrote_ myself a _new_ blogging engine I could solve the problems I saw with my TextPattern installation.  Moreover, I could experiment with [git][] and teach myself [ruby][] at the same time.  After a few guys at the office convinced me of the beauty of setting _everything_ up myself at [slicehost][], I was on my way. This was really just what I needed: a quick `git init` later, and [Fallow][] was born.

As experiments go, this has been terrifically successful.  I've built myself a new blog from scratch in a little under a month, using a distributed version control system I'd never touched, and a language I knew nothing about.  I sincerely doubt anyone in the world will touch any of the code I've put out, but putting it out _feels good_.

## Fallow in a nutshell ##

[Fallow][] is firmly grounded in three principles:

*   Markdown is a wonderful, wonderful thing; why would I need an admin interface when I have TextMate?
*   Static content shouldn't be generated twice.  It's _static_, after all.
*   Databases aren't, strictly speaking, _necessary_ for a simple blog like mine.

Accordingly, Fallow uses flat Markdown files as data sources for articles, flat YAML for bookmarks, and regenerates a tagging and caching Sqlite3 database on the fly after every deployment.  Article pages and old archive pages render HTML once, and cache it out to a static HTML document on the server, which is served to all subsequent users.  The homepage and tag pages are currently fully dynamic, but I'll get around to resolving that shortly.

It's been a ton of fun to build, and I intend to go into a bit more detail of some of the design decisions in the future.  But first, I need to get some more functionality built in.  Flickr and Twitter sync is coming, as are a plethora of tag-based Atom feeds, etc.  There's a [lot of work left to do][todo], and I don't think I'll ever actually be done.

But I have a side project again.  I'm enjoying that.  :)

[dump]:         /2008/10/gently-abandoning-dead-to-me-projects
[tomayko]:      http://tomayko.com/about
[debris]:       http://tomayko.com/writings/administrative-debris
[tan]:          http://jontangerine.com/about/
[tangerine]:    http://jontangerine.com/
[TextPattern]:  http://textpattern.com/
[Carlo]:        http://carlo.zottmann.org/  "Carlo Zottmann"
[GitHub]:       http://github.com/  
[git]:          http://git.or.cz/   "Git: Fast Version Control System"
[ruby]:         http://www.ruby-lang.org/   "Ruby Programming Language"
[Fallow]:       https://github.com/mikewest/fallow/tree
[slicehost]:    http://slicehost.com/
[todo]:         http://github.com/mikewest/fallow/tree/master/README.markdown "Fallow's README and TODO."
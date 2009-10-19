---
layout:     post
title:      "Fallow fields, revisited"
Teaser:     "I'm currently in the process of gutting my website, and rebuilding it piece by piece.  I suspect I'm doing this to distract myself from the fact that I don't seem to have anything interesting floating around my head to write about. Rather that catalog the failings of the system I'm replacing (for they are legion), in this article I'd like to touch on the carefully considered bits I'm keeping around."
tags:
    -   mikewest.org
    -   jekyll
    -   fallow
    -   webdev
    -   url
    -   redirect
    -   blog
    -   blogging
    -   architecture
---
I'm currently in the process of gutting my website, and rebuilding it piece by piece.  I suspect I'm doing this to distract myself from the fact that I don't seem to have anything interesting floating around in my head to write about.  "Surely it's the _site's_ fault; raze it to the ground!", the large, simple, and shouty part of my brain tells me.  So I build anew (this is possibly [ironic][], but I'm ignoring that).

Happily, the small, quiet, and generally reasonable portion of my brain agrees with the plan, at least insofar as it's clear that the current system ([fallow][]) was a solid idea but poorly implemented.  The system works, and I'm happy I wrote it.  It was a good introduction to Ruby and Git, and a good reason to migrate off the almost-as-inefficient-as-wordpress Textpattern.  But it's failing me in a number of ways, the most important being that I literally forgot how to get content onto the site, and it took me 45 minutes of reading through painfully structured Ruby code to figure it out again.  That's the sort of thing that happens when you don't touch a website for 6 months.

Rather that catalog the failings of the system I'm replacing (for they are legion), I'd like to touch on the carefully considered bits I'm keeping:

*   URL structure: Posts live at `/[year]/[month]/[URLified Title]` which
    seems more or less perfect to me.  It's meaningful, while containing just
    enough temporal context to make completely outdated information easy to
    spot.  Moreover, it provides a natural `/[year]/` and `/[year]/[month]/`
    for yearly and monthly archive pages.  Tag pages live under `/tags/[tag]`,
    which makes sense, and ad hoc pages have ad hoc URLs (`/is/`, for instance).
    This strikes me as a clean setup, one which I can't see any way to improve 
    upon.

*   Content storage: The site's content consists entirely of UTF-8 encoded text
    files on disk.  Text files are simple to work with, and have a more or less
    infinite shelf life.  A site like this one simply doesn't need a database,
    a single flat text file per piece of content is [good enough][].  Metadata
    (title, tags, etc.) is contained in a YAML block at the top of each file.
    It's a format that is clear, human readable, and easily parsed, and I'm
    especially pleased to see that the format I'd decided upon for Fallow
    matches up quite well against more widely used systems like [Jekyll][].

*   Static HTML: Dynamic content doesn't really exist on this site.  I write an
    article, then post it online.  That's the extent of the processing that
    particular page needs.  The server shouldn't be working to rebuild an
    article from last week (or last year!) every time it's requested, that's
    simply wasteful.  This site, therefore, generates a page once when it's
    created, or when a template changes, and then simply serves that cached copy
    over and over again.  Similarly, overview pages (like tag pages, or current
    archives) are regenerated when a new article is published, then served
    straight from disk.  On a small VPS, I can serve upwards of 300 static 
    requests per second through Nginx with extremely low load.  Textpattern
    would fall over and die at those absurd traffic levels.

*   Historical redirects: The (miserable) `/blog/id/[ID]` URL structure I
    decided upon in 2005 still works for the content I've kept from that period.
    The (also bad) `/archives/[Title]/` structure from 2007-8 works too.  The
    (not so lovely) Tumblr-generated links for content that used to be at
    `blog.mikewest.org` will redirect nicely.  All these old URLs will continue
    to generate nice, clean permanent redirects
    [for the foreseeable future][url]: why make the reader jump through hoops
    created by my lack of foresight?

So, those are the good bits I'd like to keep going as I rebuild.  With the understanding that I'm about to make one of those dangerous "forward looking statements" that I never seem to follow through on as cleanly as I'd like, I expect `mikewest.org` to be running a new Jekyll-based backend sometime in October.  With luck, no one will notice a thing but me.  With even more luck, I'll squeeze out a post or two about the bits of Jekyll I'm adjusting, and the places where it's falling down completely.

[ironic]:  http://mikewest.org/2009/09/productivity-or-my-lack-thereof
[fallow]:  http://github.com/mikewest/fallow/
[good enough]: http://mnmlist.com/a-case-for-storing-all-your-info-in-text-files/
[jekyll]:  http://jekyllrb.com/
[url]:     http://www.w3.org/Provider/Style/URI

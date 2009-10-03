---
Alias:
- http://mikewest.org/blog/id/68
Modified: '2007-05-21T07:43:15Z'
Teaser: Italian (and other languages) are full of single-quotes.  Maybe I should escape
    them...
layout: post
tags:
- Yahoo
- Personal
title: Stupid i18n Mistake.
---
Italian, apparently, is full of single quotes.  I'm sure they're not called "single quotes" in Italian, and I'm sure that the Italian people didn't have exactly _my_ code in mind when they settled upon that convention...  That said, my broken code is still obviously their fault.

Note to self:  Escape all quotes.  At a minimum, do something like:

    $title =~ s/\'/\\\'/g;

before writing out strings for use later.  Potentially even use correct typography with code like:

    $title =~ s/\'/&#x2019;/g;

depending on context.
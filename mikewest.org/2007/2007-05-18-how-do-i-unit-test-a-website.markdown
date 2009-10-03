---
Alias:
- http://mikewest.org/blog/id/67
Modified: '2007-05-18T09:32:28Z'
Teaser: Unit testing seems like an unqualified good, I'm just not sure how to apply
    the concepts to my work.
layout: post
tags:
- Yahoo
- JavaScript
title: How do I unit test a website?
---
I've been spending a lot of time recently attempting to puzzle out a _good_
way of testing the work I'm been doing.  I'm enamoured with the idea of unit
tests, and I have the feeling that I could save myself a bit of misery if I
had a mechanism to build tests for each bug I close.  It's a great dream, but
I'm not coming up with much in the way of a solid solution for my work.

Sketching out the broad outlines of what I want is pretty simple.  There are
two broad categories of things I want to test:

1.  Core functionality: If I click on an article from some listing page, I
should end up at _the same_ article's page.  I shouldn't ever see 404's.  PHP
errors and warnings shouldn't exist on the site.  

2.  Presentation tests: Each module in the sidebar should be X pixels wide in
all the A-Grade browsers.  Text shouldn't be cut off because of overflow
issues.  Thing X should be Y pixels away from thing Z.

Core functionality is easy, rather, I can come up with good ways of writing
those tests.  A spider is just a quick Perl script away, and the tests I want
to do are almost completely doable with regular expressions.  If a link's text
matches the headline of the page to which it leads, wonderful!  If not, error!
With a few hardcoded exceptions to handle "More" links and the like, I've got
a solid testing system.  Presentation, on the other hand, is hard.

It's hard not because it's terribly complex, it's hard because it's
tremendously difficult for a computer to determine if a page _looks_ right.
The only test mechanism I've come up with is a convoluted system of JavaScript
checks: grab an element's `computedStyle` and run a series of checks.  That
covers a good chunk of presentational issues, but it's incredibly
timeconsuming to build out a testing system that way.  Moreover, it only
catches the subset of errors that are directly tied to the box model.  I don't
really know how to generically test to see if a particular link is floated
next to an image, or gets pushed under it, for example.  Sure, I can check X
and Y offsets and compare those to the image's width and height, but those
sorts of interdependencies get very complex, very quickly.

So I'm still looking.  [Selenium][] looks like something I should play with,
even if the notion of writing tests using HTML `table` elements is somewhat
disheartening.  [JSUnit][] is likewise a potential source of testing goodness.
Any other good sources I should be taking a look at?

[Selenium]: http://www.openqa.org/selenium/ "Selenium"
[JSUnit]: http://www.jsunit.net/ "JSUnit"
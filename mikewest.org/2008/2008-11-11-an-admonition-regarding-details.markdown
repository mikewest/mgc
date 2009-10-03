---
Alias:
- http://mikewest.org/blog/id/97
Modified: '2008-11-11T22:33:41Z'
Teaser: Details are everything, but worrying about details at the expense of progress
    puts the cart before the horse, misses the forest for the trees, makes perfect
    the enemy of the good, and can be described by many other metaphors with similar
    meaning.
layout: post
tags:
- mikewest.org
- personal
- inspiration
- projects
- workflow
- productivity
- tdd
- neilcrosby
- crosby
- goodlatte
- robgoodlatte
- baskerville
- details
title: An Admonition Regarding Details
---
If Apple's taught me anything about design, it's that details are everything.  The overall product might be brilliant, but it's the tiny bits of _perfection_ that really bring things together and imbue an experience with a sense of wonder and care.  When I noticed that [Rob Goodlatte][rob] (who has gone dark, apparently?) replaces the ampersands on his Lucida Grande dominated page with lovely, lovely Baskerville, I was thrilled.  The first time I saw the little bit of bounce-back at the end of an iPhone's scrolled list, I was hooked.  These almost insignificant changes have an effect on the overall experience far out of proportion to their apparent importance.

[rob]: http://robgoodlatte.com/

It's important, however, not to miss the forest for the trees.  Attention to details will often make or break a project, but first laying down a solid foundation of functionality in broad strokes is _critical_.  If you haven't yet _built_ a bit of your application, worrying about making it pixel-perfect cross-browser and subtly animated to amaze your users is nonsensical and counterproductive.

Put (virtual) pen to (virtual) paper, and start working.  Details will fall into place naturally, either in the nooks and crannies of unconnected code you cleverly hack together to solve a problem, or in the long periods of iteration and polishing that you'll start to go through near the middle of a project when things _mostly_ work.

Test-Driven Development generally advocates that you should begin by ignoring (irrelevant) details and "Do the simplest thing that could possibly work."  [Neil Crosby][neil] similarly says "[Make it work, Make it pretty, Make it right][miw]."  My Dad (enthralled with the message while completely missing the commercial point of the Nike campaign) always told us "Just do it."  These are starting to resonate with me, and I like the idea of the development process as a continual process of iteration, building something delightful


[neil]: http://neilcrosby.com/vcard/
[miw]: http://thecodetrain.co.uk/2008/11/make-it-work-make-it-pretty-make-it-right/

This, of course, is a long-winded way of justifying the [gaudy hack I've just put into Fallow][commit] to handle simple conditionals in templates.  It's ugly, but functional, and I know I can make it cleaner tomorrow.  But right now, it works; That's better than yesterday, and I can live with that.

[commit]: http://github.com/mikewest/fallow/commit/9d9b4e69e56841fabe38eb4724caa8b629f40db3
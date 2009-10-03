---
Alias:
- http://mikewest.org/blog/id/102
Modified: '2009-01-10T19:32:15Z'
Teaser: 'I liked many things about working at Yahoo.  I''m coming to realize that
    what I (in hindsight) like _most_ is probably the piece of software I thought
    about the _least_ positively, namely Yahoo''s mostly centralized and completely
    open bug tracking system: Bugzilla.  We abused it more than a bit, attempting
    to layer task and project management on top of a system that wasn''t really designed
    to support it, but all told, Bugzilla made my work life better.'
layout: post
tags:
- mikewest.org
- yahoo!
- y!
- sanity
- bug
- tracking
- bugtracking
- bugzilla
- lighthouse
- sifter
- mantis
- fogbugz
- corporateculture
- work
- bestpractice
title: Centralized Bug Tracking
---
I liked many things about working at Yahoo.  I'm coming to realize that what I (in hindsight) like _most_ is probably the piece of software I thought about the _least_ positively, namely Yahoo's mostly centralized and completely open bug tracking system: Bugzilla.  We abused it more than a bit, attempting to layer task and project management on top of a system that wasn't really designed to support it, but all told, Bugzilla made my work life better.

As a generic employee, the centralization of bug tracking meant that I was able to quickly and easily file bugs against any Yahoo property.  I didn't have to know who was responsible for a project in order to raise bugs against it.  I didn't need the group responsible for a project to know _me_.  When I saw an issue on a Yahoo site, I filed a bug against the project, and knew _someone_ with the capability to fix the issue would be notified about it.  Bugzilla minimized the friction caused by unclear answers to the question "I found a bug, now what?".  Instead of sending out a few emails, looking for someone to stick with a problem, it gave everyone in the company a clear "next step", and (in the best cases) fostered a corporate culture of _reporting_ bugs rather than avoiding them.

As a developer, Bugzilla meant that _I_ didn't have to keep the list of bugs on my projects.  The bug database was maintained for me, triaged and prioritized by my managers, and brutally honest.  Every bug that was reported against News sat in my queue, staring at me pleadingly until I fixed it.  I made appropriate comments on each bug when necessary, which simple integration with CVS made trivial, with the cumulative effect that I didn't worry about forgetting to fix something, or losing track of a bug's status.  Everything was maintained for me, removing a burden from my shoulders.

This isn't to say Bugzilla was perfect.  It was a bit of a mess, honestly, often difficult to use, full of confusing forms and confused categorizations, and plagued by an understaffed team of developers who played with the UI far too often.  For these reasons and more, it probably annoyed me more than any piece of software at Yahoo, but it's existence was hugely advantageous.  In hindsight, I'm coming to consider this a critical component of any development team; a central bug tracking system provides __visibility__ and __accountability__ in a way difficult (impossible) to replicate with personal to-do lists and email.

Don't read this as an endorsement of Bugzilla in particular, but as an endorsement of the concept of bug tracking.  Working without a centralized bug database makes your work life more difficult for no good reason.  It's something I highly suggest that you avoid.

If you'd like to get started quickly with an externally hosted bug tracking system, I've heard good things about [Lighthouse][1] and [Sifter][2].  I'm still looking for a locally hosted system that I like, but I've been recommended [Mantis][3], [FogBugz][4], and, of course, [Bugzilla][5].  Honestly, even a hand-maintained text file in [Tasks][6] format that you print out and pin to the wall for people to write on is better than nothing.  For the sake of your own sanity, use _something_.

[1]: http://lighthouseapp.com/
[2]: http://sifterapp.com/
[3]: http://www.mantisbt.org/
[4]: http://www.fogcreek.com/FogBUGZ/
[5]: http://www.bugzilla.org/
[6]: http://github.com/henrik/tasks.tmbundle/tree/master
---
layout: post
title:  JSLint needs some Bad Parts
tags:
    - javascript
    - bestpractice
    - tooling
    - validation
    - jslint
    - automatedtesting
    - linting
    - webdevelopment
    - webdev
    - css
    - crockford
    - douglascrockford
    - community
    - opensource
    - fork
Teaser:
    One of the few tools that I consider truly indispensable when developing
    websites is JSLint.  Too bad it's almost impossible to contribute back to
    the project, and that the project's run by someone who "will hurt your
    feelings."
---
One of the few tools that I consider truly indispensable when developing
websites is [JSLint][1].  A marvel of applied compiler theory, the program
has saved me from stupid mistakes more times than I care to remember.  I
have it set up to automatically sanity-check my code [every time I push a
commit to SVN][jslint-utils], and it's generally my best friend in the whole
wide world.

JSLint isn't always perfect, however, especially when used to check CSS
files.  I think [Douglas Crockford][2] is a JavaScript wizard, but I'm
somewhat less blindly acquiescent when it comes to his take on the Good
Parts of style sheets.  For better or worse, browsers are _much_ less
similar in their interpretation of what I mean when I write a particular
style, and certain hacks and workarounds are par for the course when
putting together a layout of any complexity.  JSLint's CSS checks do a
good job warning about certain types of errors (missing semicolons, for
instance), but a relatively terrible job when it comes to some of the
necessary evils of practical development.  In short, JSLint's CSS mode
needs some [Bad Parts][11] to be really _usable_ for me.

In itself, this wouldn't be an issue.  Crockford has kindly released 
JSLint as open source (under a unique (to say the least) "Do no evil"
license), and I'm generally able to puzzle out how to go about adding
support for the features that I believe are necessary.  Getting those
patches into the mainline JSLint project is, unfortunately, often a
miserable process.  I have two issues with the current process:

First, there's no public repository (that I've come across).  Crockford
is pretty good about announcing changes on [the JSLint mailing list][3],
and he keeps a timestamp in the current `fulljslint.js` file, but that's
hardly a solid basis for contributing patches.  This isn't a show stopper,
it just makes things harder to follow than they could be, and more
difficult to give back to the project than it should be.  I asked about
this [in May 2009][4], and was met with silence.  Ah well.

Second, the aforementioned list is easily the most (passive-)aggressive
I've been on recently.  The (true) warning that "JSLint will hurt your
feelings" goes double for posting questions or suggestions, especially
as a newbie.  I almost fell off my chair when I saw [this question][5]
("I have this problem, and I've found this workaround.  Why is it a
problem in the first place?") received [this response][6] ("Thanks for
the report.  JSLint now no longer accepts your workaround.")  Crockford
is a _smart_ guy, and he's opinionated in the best possible way, but he
couples that with a periodic lack of tact that's really influenced the
way the list as a whole works.  It's simply not a fun place to
contribute ideas or code, and that's a shame.  [Arguing about the
validity of suggestions][7] is simply not something I'm willing to do
_every single time_ I make a suggestion, especially when the suggestions
are quite often met with silence from the one guy who actually has 
commit access to the mainline trunk.

So, to resolve these issues for myself, I'm forking JSLint.  I fully
expect this to be of interest to almost exclusively myself, but I'll
find it useful, and I'll hold out hope that some of the patches will
eventually make it back into JSLint proper.

To resolve the issue of a base "official"  repository, I'll pull down
a copy of the current iteration of JSLint on a daily basis, and
mirror it on GitHub ([jslint/mirror][8]).  My patches will be pushed
to [jslint/master][9] (along with QUnit-based regression tests), and
I'll do my best to keep `master` merged with the latest from `mirror`,
and the changes continually rebased on top of `mirror` into
[jslint/rebased][10] for ease of application (in the unlikely event
that Crockford pays attention :) ).

I'll keep the [changelog][11] up to date as I add the functionality
I find that I need to do my job.  If you find the idea useful, I hope
you'll help me out.  Reasonable patches most humbly accepted (although
_my_ arbitration of "reasonable" might hurt your feelings too).

[1]:    http://www.jslint.com/
[2]:    http://www.crockford.com/
[3]:    http://tech.groups.yahoo.com/group/jslint_com/
[4]:    http://tech.groups.yahoo.com/group/jslint_com/message/476
[5]:    http://tech.groups.yahoo.com/group/jslint_com/message/1168
[6]:    http://tech.groups.yahoo.com/group/jslint_com/message/1170
[7]:    http://tech.groups.yahoo.com/group/jslint_com/message/1280
[8]:    http://github.com/mikewest/jslint/tree/mirror
[9]:    http://github.com/mikewest/jslint/
[10]:   http://github.com/mikewest/jslint/tree/rebased
[11]:   http://github.com/mikewest/jslint/raw/master/CHANGELOG.markdown

[jslint-utils]: http://github.com/mikewest/jslint-utils

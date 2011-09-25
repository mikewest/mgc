---
layout: post
title:  Chrome Privacy
tags:
    - chrome
    - chromium
    - privacy
    - davewiner
    - benbrooks

Teaser:
    Dave Winer ends an otherwise quite reasonable piece about his concern
    at Facebook's "frictionless sharing" with a non sequitur attack on
    Chrome for, as far as I can tell, nothing it's actually doing.
---
Dave Winer ends an [otherwise quite reasonable piece][1] about his concern at
Facebook's "frictionless sharing" with a non sequitur attack on Chrome for,
as far as I can tell, nothing it's actually doing:

> One more thing. Facebook doesn't have a web browser, yet, but
> Google does. It may not be possible to opt-out of Google's 
> identity system and all the information gathering it does, if
> you're a Chrome user.

[Ben Brooks picked up on that][2], adding:

> Read Winer’s take on this, it’s pretty creepy of Facebook — 
> what’s more scary is the possibility of Google doing this to 
> Chrome users.

A direct response to this sort of speculation about Chrome's _potential_ for
evil, slipped in as a conclusion to a discussion about an unrelated company
_being_ evil, is difficult, so let me step back a bit. Chrome founded a privacy team
here in Munich back around the release of Chrome 4. I'm proud to be a small
part of this clever group of developers who care about making Chrome's use of
data transparent, and giving you control over how it's used to whatever extent
possible. We build APIs that enable privacy-relevant extensions and apps to
fine-tune a browser with an already good set of privacy features, and review
features built by other teams for potential impact on user's private
information. I'm biased, but I think we do a decent job.

So, to Dave, Ben, and everyone else: If you see Chrome doing something you
don't like with your information, or you have specific questions about some
feature or another, send an email to the team at <privacy@chromium.org>, or
to me directly, <mkwst@chromium.org>. You can also file a bug on the public
tracker at [new.crbug.com][3] and mail me the bug ID. I'll make sure it gets
triaged into the right team.

With that in mind, here's a direct answer to what I think is being criticized:
The browser doesn't secretly send information about your browsing habits to
Google, nor will it. The feature that comes closest is Sync, which is a)
opt-in, b) encrypted locally before being sent to Google, optionally with a
password separate from your Google account.



*Update*:

* [Some good discussion is taking place on Hacker News][4].

* I've removed an unintentional [ad hom][5] that was personally
inflammatory: Sorry Dave, I honestly didn't mean to offend you, just to argue
with you. The focus of my frustration is both the suggestion that Chrome may
at some point in the future start being evil, and the way it was casually
slipped as a conclusion into a discussion of an unrelated company arguably
_being_ evil. I hope that remains clear. This article's history is [available
on GitHub][6], so the edits I've made remain transparent.

[1]: http://scripting.com/stories/2011/09/24/facebookIsScaringMe.html
[2]: http://brooksreview.net/2011/09/facebook-winer/
[3]: http://new.crbug.com/
[4]: http://news.ycombinator.com/item?id=3034155
[5]: http://en.wikipedia.org/wiki/Ad_hominem
[6]: https://github.com/mikewest/mgc/commits/master/mikewest.org/2011/2011-09-24-chrome-privacy.markdown

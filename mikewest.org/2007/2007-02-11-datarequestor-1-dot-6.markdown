---
Alias:
- http://mikewest.org/blog/id/55
Modified: '2007-04-16T20:01:40Z'
Teaser: After a brief (ha!) hiatus, DataRequestor's 1.6 release fixes many outstanding
    bugs.  Grab it now!
layout: post
tags:
- DataRequestor
- JavaScript
title: "DataRequestor \u2014 Version 1.6"
---
I took some time tonight to fix some long-outstanding bugs in the [DataRequestor Ajax library][datarequestor].  No new features have been added since 1.5, but some significant bugs have been taken care of in [this 1.6 release][download].

[Download DataRequestor 1.6][download] and get started.

## Release Notes ##

*   Fixed major bug with `addArgsFromForm`; it now properly reads form variables anywhere under a `FORM` element's DOM tree, instead of simply those that are the `FORM`'s direct children.
*   Changed the internal handling of get and post variables to avoid some spurious get and post variables caused by other scripts' overzealous addition of methods via `.prototype`.
*   Better handling of certain error situations (calling `onfail` to handle unexpected exceptions, etc.)
*   Moved handling of strangely cased `onLoad`, `onFail`, etc. out of callback function, into `getURL`.
*   Add ability to deal with Mozilla-based browser's `NS_ERROR_NOT_AVAILABLE` error.
*   Trigger an `onfail` event, or throw an error if the browser is disconnected from the internet when a request is made.

## Future Plans ##

The landscape has changed a lot since I released DataRequestor in March, 2005.  Frameworks have appeared that do everything DataRequestor does, and I certainly don't have the time or desire to compete with them on a feature-for-feature basis.  Happily, I think that's a feature, not a bug.  :)

I believe there's room for, and demand for, a simple library that does the bare minimum in terms of enabling Ajaxy interactions in existing applications.  I think the API that DataRequestor exposes is clear, concise, and trivial to implement.  In short, it's not going to disappear.

In the next couple of weeks, I'll be making some changes to DataRequestor's backend in order to leverage some of the incredible work being done on [Yahoo's User Interface library][yui].  I'll be pulling pieces of that library's code to increase DataRequestor's overall stability and elegance, while keeping the external interface the same.  Just like this 1.6 release, 2.0 will be a drop-in replacement for any previous version of DataRequestor.  I'll be releasing some new features with that release (foremost: automatically repeated requests for timed site updates), and offering an alternate execution path I've been thinking about, but all your current code will work just the way it always has.  We'll see where it goes from there.

[datarequestor]: http://mikewest.org/archive/datarequestor/
[download]: http://mikewest.org/file_download/10
[yui]: http://developer.yahoo.com/yui/
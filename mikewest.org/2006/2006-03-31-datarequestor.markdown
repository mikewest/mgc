---
Alias:
- http://mikewest.org/blog/id/8
Modified: '2008-10-18T13:34:09Z'
Teaser: DataRequestor is a JavaScript wrapper for the `XMLHttpRequest` object that
    enables the trivial implementation of dynamic interfaces without the painful necessity
    for a complete page-refresh to talk to the server. It's Ajax without the confusing
    API.
layout: post
tags:
- DataRequestor
- JavaScript
title: "DataRequestor 1.6.1 - Ajax without the confusing API"
---
DataRequestor is a JavaScript wrapper for the `XMLHttpRequest` object that enables the trivial implementation of dynamic interfaces without the painful necessity for a complete page-refresh to talk to the server. In other words: Ajax without the confusing API.

## How can you use DataRequestor? ##

When building applications, the most typical Ajaxy sort of thing I find myself doing is sending off data to a server-side script, and then sticking the resulting HTML directly into some element on the page. DataRequestor makes this process absolutely trivial, and enables quite a bit more functionality with minimal effort.

    var req = new DataRequestor();
    req.setObjToReplace('objID');
    req.getURL('/path/to/my/file.php');

Those three lines build an `XMLHtmlRequest` object, grab the relevant data from the server, and use that information to replace the `innerHTML` of an element with id '`objID`'. Trivial, right?

What if we wanted to do something else when the data’s loaded? Instead of replacing an element’s `innerHTML`, maybe we want to do some crazy JavaScript stuff once the data’s finished loading. Typically, this would involve being annoyed at the `XMLHttpRequest` object’s rather irritating callback structure. Happily, DataRequestor wraps this complexity in a warm blanket of event-driven goodness:

    req.onload = function (data, obj) {
        // Insert crazy JavaScript stuff here!
    }

DataRequestor is a solid, stable, and event-driven JavaScript class that you can simply drop into a page and start running with. It makes `XMLHTTPRequest`'s functionality available in a way that doesn’t make my brain hurt, and hopefully it will do the same for you.  [Download DataRequestor.js][datarequestor] and browse through the code.  It's well commented; use cases and instructions abound.

## How can I get it? ##

You may download the [current stable version (1.6) of DataRequestor.js **right here**][download].  How's that for convenience?

## Future Plans ##

__Update, 2008-10-18__: Despite well intentioned promises in the past, there are no future plans.  I've released this project under the MIT license, and [placed the code on GitHub][github] for you to fork at your leisure.

<del style="text-decoration: line-through;">The landscape has changed a lot since I released DataRequestor in March, 2005.  Frameworks have appeared that do everything DataRequestor does, and I certainly don't have the time or desire to compete with them on a feature-for-feature basis.  Happily, I think that's a feature, not a bug.  :)</del>

<del style="text-decoration: line-through;">I believe there's room for, and demand for, a simple library that does the bare minimum in terms of enabling Ajaxy interactions in existing applications.  I think the API that DataRequestor exposes is clear, concise, and trivial to implement.  In short, it's not going to disappear.</del>

<del style="text-decoration: line-through;">In the next couple of weeks, I'll be making some changes to DataRequestor's backend in order to leverage some of the incredible work being done on [Yahoo's User Interface library][yui].  I'll be pulling pieces of that library's code to increase DataRequestor's overall stability and elegance, while keeping the external interface the same.  Just like this 1.6 release, 2.0 will be a drop-in replacement for any previous version of DataRequestor.  I'll be releasing some new features with that release (foremost: automatically repeated requests for timed site updates), and offering an alternate execution path I've been thinking about, but all your current code will work just the way it always has.  We'll see where it goes from there.</del>

[github]: http://github.com/mikewest/datarequestor/tree/master

## Release Notes ##

### Changes in Version 1.6.1 ###
*   Removed _debug code_ that broke the whole library in every browser that didn't have Firebug installed.  I hate being a moron.  :)

### Changes in Version 1.6 ###
*   Fixed major bug with `addArgsFromForm`; it now properly reads form variables anywhere under a `FORM` element's DOM tree, instead of simply those that are the `FORM`'s direct children.
*   Changed the internal handling of get and post variables to avoid some spurious get and post variables caused by other scripts' overzealous addition of methods via `.prototype`.
*   Better handling of certain error situations (calling `onfail` to handle unexpected exceptions, etc.)
*   Moved handling of strangely cased `onLoad`, `onFail`, etc. out of callback function, into `getURL`.
*   Add ability to deal with Mozilla-based browser's `NS_ERROR_NOT_AVAILABLE` error.
*   Trigger an `onfail` event, or throw an error if the browser is disconnected from the internet when a request is made.

[datarequestor]: http://mikewest.org/archive/datarequestor/
[download]: http://github.com/mikewest/datarequestor/tree/master
[yui]: http://developer.yahoo.com/yui/
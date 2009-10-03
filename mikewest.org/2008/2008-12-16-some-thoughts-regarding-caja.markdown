---
Alias:
- http://mikewest.org/blog/id/101
Modified: '2008-12-16T20:39:27Z'
Teaser: Yesterday, Yahoo! made some announcements regarding The Future&trade; of many
    of their high profile properties.  Specifically, they're (slowly) opening up,
    enabling third-party developers to build applications that can be seen on and
    interact with your My Yahoo! page, or your mailbox.  I think this is a great step,
    and one I wish they'd made _before_ they laid me off.
layout: post
tags:
- mikewest.org
- yahoo!
- y!
- yep
- caja
- adsafe
- capabilities
- security
- xss
- javascript
- crockford
- douglascrockford
- thefuture
- open
- accessibility
- progressiveenhancement
- ugly
- google
title: Some Thoughts Regarding Caja
---
Yesterday, Yahoo! made some announcements regarding The Future&trade; of many of their high profile properties.  Specifically, they're (slowly) opening up, enabling third-party developers to build applications that can be seen on and interact with your [My Yahoo!][my] page, or your [mailbox][mail].  I think this is a great step, and one I wish they'd made _before_ they laid me off. 

Ah well.

One of the core technologies that's behind this set of features is called [Caja][].  Caja is a code sanitizer: it takes an HTML fragment, and JavaScript that operates on it, and "cajoles" it into a chunk that can be embedded into a page without the risk of maliciousness.  I'd like to ramble about that, briefly, at a very high level.  I'm still trying to wrap my head around it's details

JavaScript is, simply, dangerous.
---------------------------------

If you've paid attention to any of [Doug Crockford's presentations][yuit], you'll know that the browser security model is simply broken-as-designed.  The internet, therefore, is a place where one can barely trust _first-party_ code, much less code written by your neighbor.  You have to keep a constant eye out for new cross-site scripting vectors, and be very careful about how you filter third-party input before making it available as "user generated content."

Seen in this light, Yahoo! has a massive problem to confront with it's new "open" initiatives.  On the one hand, they _must_ protect the security of their sites.  On the other, they want to pull in content from their users, and not just _text_, but _code_.  Working applications, written outside of Yahoo!, running directly _on_ a Yahoo! site.  The project specification itself is basically a nightmare scenario for the security team.  They need to find a way to include third-party JavaScript safely and sanely onto Yahoo! pages.  This mechanism needs to be pretty automatic, as they can't dedicate an engineering team to manually review (potentially) thousands of applications.

There are two broad paths to take to this end:

*   Code sanitization, which reads unknown code, processes it, and outputs
    a sandboxed version (if possible).  [Caja][] is the best known example of
    this tact.

*   Static analysis, which reads unknown code, parses it, and gives a
    thumbs-up if it only does known-safe things.  [AdSafe][] is a
    work-in-progress along these lines.
    
Yahoo!'s running with the former, so let's dive in.

Code Sanitization
-----------------

Untrusted JavaScript must not be allowed access to the `document` or `window` objects.  This means that it must not gain direct access to any DOM node, as every DOM node enables you to crawl back up to `document`.  `event` objects are right out as well, as they contain dangerous references as well.  Really, when you get right down to it, you have to throw out practically everything of practical use.

I mentioned that JavaScript was broken, right?

Caja is an attempt to distill a safe subset of JavaScript out of this mess through server-side sanitization.  A third-party uploads an application, consisting of JavaScript, CSS, and HTML fragments, and Caja transforms it into something that can be guaranteed not to damage the page into which it's embedded.  This is a good thing.

Caja is a capability-based system, meaning in practice that it begins by defining an extremely restrictive sandbox in which code must run, and enabling well thought-out bits of functionality by selectively injecting access as needed.

Think of it this way: when you hand your car to a valet, you would be better off if you gave them the valet key, which _only_ enables them to _drive_ the car.  You shouldn't give them _your_ key, which would also let them rummage through your glove box, etc.  In the same way, you shouldn't give a program access to _everything_ in the DOM if it's only supposed to change a background colour in a particular location.  You'd be better off if you could restrict it's scope of access.  Caja attempts to do this.

The token you give the valet, the key, can be looked at as a set of _capabilities_.  The valet key enables "drive the car", your key enables much more.  Similarly, handing an object to a program _is_ handing it capabilities, enabling it to act in whatever ways are exposed by that object.  Since JavaScript's default objects are _so_ overpowered, Caja exposes a new set of objects that completely wrap things like the DOM or the event model, and rewrites input programs to use these objects instead, severely limiting the damage they can do.  These wrapper objects contain a series of runtime checks to ensure that a malicious program hasn't somehow broken out of their constraints, and the entire rewriting process fails if the program is written in such a way as to make it impossible to sandbox.

Big Drawback
------------

Though I understand Caja's practical necessity, I really don't like the way it works.  In short: it breaks progressive enhancement completely, and introduces a hard dependency on JavaScript for functionality.

As a quick demo, let's look at the following code:

    <script src="searchbox.js"></script> 
    <link rel=stylesheet href="searchbox.css" /> 
    <form> 
      <input type="text" size="60" name="q"> 
      <input type="button" value="Search" onclick="doSearch(this)"> 
    </form> 

After "cajoling", it will look something more like:

    ...
    IMPORTS___.htmlEmitter___.p('form') 
        .a('onsubmit', 'return false') 
        .ih('  <input type="text" size="60" name="q">\n' 
          + '  <input type="button" value="Search"' 
          + ' onclick="return plugin_dispatchEvent___(…)">\n') 
        .e('form'); 
    ...

The HTML is transformed into a series of JavaScript method calls that _generate_ HTML.  This makes sense, as it enables Caja to retain complete control over what's written to the page, but it has the side effect of making the form completely inaccessible to anyone who isn't running JavaScript.

I'd much prefer more thought to be put into [AdSafe][], which sets up the same sort of wrapped-object sandbox, as well as a series of rules which third-party developers must follow.  The system them simply _verifies_ that they have done so, rather than rewriting their code to ensure that they have.  If the rules are solid, the effect will be the same as can be achieved with Caja, but much more elegant, and with more respect for the fundamentals of the web.

Crockford has (finally) put up some example code on the [AdSafe site][adsafe].  I'd suggest that you go take a look at it.  It looks like a very interesting way to program indeed.

[my]:       http://my.yahoo.com/
[mail]:     http://mail.yahoo.com/
[caja]:     http://code.google.com/p/google-caja/
[yuit]:     http://developer.yahoo.com/yui/theater/
[adsafe]:   http://adsafe.org/

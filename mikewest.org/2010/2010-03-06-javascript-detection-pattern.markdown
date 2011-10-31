---
layout: post
title:  A JavaScript Detection Pattern
tags:
    - javascript
    - bestpractice
    - pattern
    - webdevelopment
    - webdev
    - progressiveenhancement
    - progressive
    - enhancement
    - html
    - css
    - twitter
Teaser: Progressive enhancement of our sites and applications has become a relatively well accepted best practice for web development.  This article outlines a technique I've used successfully to ensure that core functionality is available without JavaScript, while maintaining a quality experience for the majority of users with JavaScript enabled.
---
Progressive enhancement of our sites and applications has become a relatively well accepted best practice for web development.  It simply makes sense to implement core functionality in a universally accessible way before layering new behaviors and possibilities for interaction on top via JavaScript.

This implementation model has one drawback that we need to consider.  If we render a basic version of a module before reworking it with JavaScript, it's possible that visitors would briefly be exposed to the unenhanced module, only to see it morph into something new before their eyes.  This distraction is especially likely when we consider the [well-known performance benefits][performance] associated with loading JavaScript at the very bottom of a page.  The page as a whole will load well before JavaScript is completely parsed and executed, leaving a space of time during which the raw versions of your modules are visible.

To avoid this issue, I'd suggest inserting the following code directly after opening your page's `body` element:

    <script>document.documentElement.className += " js";</script>

When a visitor comes to the site with JavaScript enabled, this snippet will add a `js` class to the document's root node (in most cases, the `html` element).  This gives us a styling hook that allows us to generate CSS rules that only take effect when JavaScript is present.  Prefixing rules with a `.js` selector ensures that they only apply when this script has executed, meaning that the visitor must have JavaScript enabled in her browser.  We can use this information to pre-style the widgets in preparation for the JavaScript manipulations we'll do later on.

I've put together a [demonstration of this JavaScript detection technique][demo] in action.  It's worth visiting that demonstration both with and without JavaScript enabled, simply to get a feel for what's possible.  It's not a perfect solution (JavaScript could error out somewhere in the middle of the page, for instance), but I find it to be a reasonable compromise that avoids distracting flashes of incompletely styled content.

That demonstration, however, is pretty abstract.  Let's look at a more practical example of how this could improve a site's usability.  Take [Twitter][], for instance: with JavaScript enabled, clicking on the "Sign in" button in the top right-hand corner of the page exposes the login form, which is otherwise hidden away.  Without JavaScript, the form doesn't show up at all, users are instead directed to a separate page that just displays this form.

This is a reasonable fallback, all things considered (and certainly better than sites like CNN, whose login link goes nowhere without JavaScript).  Still, I see it as a missed opportunity as the login form's HTML code is delivered to the user on the homepage regardless, it's simply hidden by default.  I think a better decision would have been to design the page such that the login form shows up for all users, and is simply presented differently for users with JavaScript.

I've implemented a [demonstration of how this might work][twitterdemo] by copying down the Twitter homepage's code, adding the JavaScript detection snippet from above, moving the login form HTML lower down on the page, and adding a few lines of CSS to make things halfway usable (a caveat: [the twitter demo][twitterdemo] looks good in Chrome/Webkit, decent in Firefox, and miserable in IE: Twitter's HTML is dependent upon server-side browser detection, which I'm not going to attempt to recreate here.).  I'm no designer, but it seems like a step in the right direction to me, and adds a bit of bulletproofing with next to no effort expended.

With this in your toolkit, I don't think there's any excuse for mandating a hard requirement for JavaScript for most interactive widgets.  Certainly complex applications would be hard-pressed to come up with ways of presenting the same functionality to all users, but I think we can all agree that "simple" functionality (like logging in) should be equally available to everyone, and we should absolutely take that into account when building websites.

__Update__: [Tim Huegdon][tim] mentioned, rightly, that `class` isn't actually a valid attribute on the `html` element, and that it might be better to set the `js` class on the document's `body` element instead.  It's a valid point, one which ought not be ignored out of hand.  I'm sticking with `document.documentElement` for a simple reason: I know it works stably in every browser I've tested (IE6+, FF2+, Safari 2+, Opera 9.5+).  I've heard anecdotal evidence of problems in IE caused by manipulating the document's `body` while it's loading ("Operation Aborted", and the like), which I've never experienced with this technique, and which I'd like to avoid.

__Update to the Update__:   [Martijn van der Ven][martijn] notes, also rightly, that HTML5 allows `class` attributes (as well as all other [global attributes][global]) on the `html` element.  One more reason to switch over to the [HTML5 doctype][doctype], if you ask me.

[performance]:  http://developer.yahoo.com/performance/rules.html#js_bottom
[twitter]:      http://twitter.com/
[demo]:         /static_content/2010-03-javascript-detection.html
[twitterdemo]:  /static_content/2010-03-javascript-detection-twitter.html
[tim]:          http://timhuegdon.com/
[martijn]:      http://vanderven.se/martijn/
[global]:       http://dev.w3.org/html5/spec/dom.html#global-attributes
[doctype]:      http://diveintohtml5.org/semantics.html#the-doctype

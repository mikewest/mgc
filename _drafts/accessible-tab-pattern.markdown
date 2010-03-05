An Accessible Tab Pattern

Tabs are as ubiquitous on the web as they are on the desktop (as they are in the Real World™ for that matter...), and they serve as a useful mechanism for organizing and displaying information to a site's visitors.  Ubiquity, however, is not consistency; tabs on the web suffer the fate of most non-native widgets.  Their core implementation varies wildly from one page to the next, as do their behaviors and interactions.  Successful manipulation of a tab widget on one page gives only a vague guarantee of success in the future, and I think we can do better.

Here, I'll outline what I consider to be best practice when building a tab widget, with a particular focus on ensuring that it's as accessible as possible to anyone who runs across it.  


First things first: Progressive Enhancement
-------------------------------------------

Before we dive into the behavior and interaction model we'd like to put together, it's important to consider the basics.  How will this widget work when JavaScript isn't available?  More to the point, what semantics lie at the core of the widget, and how can we cleanly represent that in HTML?  Only once we've laid that universal foundation can we move on to enhancing it for capable browsers.

So.  What is a tab widget?  Disregarding for the moment how it looks and behaves, what are it's _semantics_?  What does it contain?  At its core, a tab widget contains little more than a list of distinct chunks of labelled content, and possibly an overarching title for the entire set.  Important here is the point that the content and the content's label ought not be separated in the code.  Many libraries ([YUI 2][y2], [YUI 3][y3], and Google's [Closure][], among others) define tabs as two lists, one containing the labels, the other containing the contents.

This, I believe, confuses the core semantics of the unenhanced tab widget by attempting to replicated the expected behavior of the enhanced tab widget.  The only library I've seen that gets this right is [Dirk Ginader's][dirk] [Accessible-Tabs][dirktabs] (which, really, is excellent). 

[y2]:       http://developer.yahoo.com/yui/tabview/
[y3]:       http://developer.yahoo.com/yui/3/examples/node-focusmanager/node-focusmanager-2.html
[Closure]:  http://closure-library.googlecode.com/svn/trunk/closure/goog/demos/tabbar.html

 Most libraries define the list of tab headers as a list distinct from the contents, which makes no sense, semantically.

[dirk]: http://blog.ginader.de/archives/2009/02/07/jQuery-Accessible-Tabs-How-to-make-tabs-REALLY-accessible.php
[dirktabs]: http://github.com/ginader/Accessible-Tabs

  So what does an unenhanced version of a tab widget look like?  How does it behave?  The most straightforward answer is to display the complete contents of each panel, hiding nothing from less capable browsers.  

[ Discussion + Code ]

Progressively enhancing this module by starting with a non-interactive version and layering behaviors on top has one drawback that we need to consider.  If we render a basic version of the module, and then rework it with JavaScript, it's possible that visitors would be briefly exposed to the unenhanced module, only to see it morph into something new before their eyes.  To avoid this distraction, I'd suggest putting the following code directly after opening your page's `body` element:

    <script>document.documentElement.className += " js";</script>

If a visitor comes to the site with JavaScript enabled, this snippet will add a `js` class to the document's root node (in most cases, the `html` element).  This allows us to generate CSS rules that only take effect when JavaScript is present by prefixing them with `.js`.  It's not a perfect system (JavaScript could error out somewhere in the middle of the page, for instance), but I find it to be a reasonable compromise that avoids distracting flashes of incompletely styled content.








Progressive enhancement of our sites and applications has become relatively well accepted "best practice" for web development.  It simply makes sense to implement core functionality in a universally accessible way before layering behaviors on top via JavaScript.

This implementation model has one drawback that we need to consider.  If we render a basic version of a module before reworking it with JavaScript, it's possible that visitors would be briefly exposed to the unenhanced module, only to see it morph into something new before their eyes.  To avoid this distraction, I'd suggest inserting the following code directly after opening your page's `body` element:

    <script>document.documentElement.className += " js";</script>

If a visitor comes to the site with JavaScript enabled, this snippet will add a `js` class to the document's root node (in most cases, the `html` element).  This allows us to generate CSS rules that only take effect when JavaScript is present by prefixing them with `.js`.  It's not a perfect system (JavaScript could error out somewhere in the middle of the page, for instance), but I find it to be a reasonable compromise that avoids distracting flashes of incompletely styled content.



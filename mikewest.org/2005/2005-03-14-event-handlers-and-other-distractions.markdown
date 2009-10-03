---
Alias:
- http://mikewest.org/blog/id/5
Modified: '2006-03-29T20:48:02Z'
Teaser: Attaching behaviors to the semantic elements in your HTML document isn't nearly
    so hard as it sounds.
layout: post
tags:
- JavaScript
title: Event Handlers and Other Distractions
---
A few things are vigorously jumping around in my head, which is making it incredibly hard to sleep. So, I’ll blog in a futile attempt to exorcise the little beasties from my brain for the night.

I had a quick discussion with [Molly Holzschlag][1] after the [Hi-Fi Design panel][2] about the behavioral/JavaScript layer of websites, and the lack of attention over the past few years in favor of standards coverage. I don’t at all think that the lack of attention was unjustified, because without a solidly standards-based document tree, it’s going to be very difficult to do anything of use with the behavioral layer. However, I do think that it’s time to begin thinking less about standards in terms of CSS and Valid (X)HTML, and more about how we can hook into that valid document tree with some really useful JavaScript methods.

An excellent example is the recent(ish) [Zebra Tables][3] article on [ALA][4]. This technique relies on a properly marked-up table of data, and enhances the presentation without adding irrelevant cruft to the actual code of the page. It can be made even more valuable by tacking on another article’s code: [Table Rulers][5]. Combining these two techniques into a single function that gets called when your page loads means that you can have nicely styled tables without adding any additional markup in your source document. How would we go about doing this, you ask?

Excellent question: Let’s look first at [Zebra Tables][3]. How does it work? In broad strokes, it simply grabs a list of tables on your page, loops through all the rows of each table, and marks each row as “odd” or “even” based on it’s position in the table. Simple stylesheet rules for those classes finish out the process. It’s a sweet little marriage of the behavioral, semantic, and presentational layers. It can, I think, be improved upon. Let’s break striping out into it’s own function. We’ll pass the function a reference to a DOM object, and stripe all `tbody` elements we find under it:
    
    function stripeTable(table) {
        var tbodies = table.getElementsByTagName("tbody");
        for (i=0, numBodies=tbodies.length; i<numBodies; i++) {
            var even    = false;
            var trs = tbodies[i].getElementsByTagName("tr");
            for (var j=0, numTrs=trs.length; j<numTrs; j++) {
                trs[j].className += (even)?" even":" odd";
                even = !even;
            }
        }
    }
    

Simple, eh? Using standard DOM methods, we’ve written a function that dramatically improves the readability of our data tables. But as it currently stands, we’d have to call this function for each table on our page:
    
    stripeTable(document.getElementByID("table1"));
    stripeTable(document.getElementByID("table2"));
    ...
    

That doesn’t seem to make things easier at all. How could we improve the interface? We can do a number of things, in fact. The most obvious is to write a function that grabs all the tables on the page and loops through them, striping each in turn:
    
    function stripeAllTables() {
        var tables = document.getElementsByTagName("table");
        for (i = 0, numTables=tables.length; i<numTables; i++) {
            stripeTable(tables[i]);
        }
    }
    

But how do we set this up to run once we’ve decided that we’re done loading the page? How do we make that decision in the first place? JavaScript, luckily, makes this trivial. One of JavaScript’s most powerful concepts is an “event”. You’ve almost certainly used events before by setting up an onmouseover action for a link or an onclick action for a button. 
    
    <input type="button" onclick="someFunction();" value="A button am I!" />
    

We can use a similar technique to call our table striping function by adding an onload handler to the body element:
    
    <body onload="stripeAllTables();">

This works pretty well, but has a huge disadvantage. Several huge disadvantages, in fact.  
First, it mixes the behavioral layer with the semantic layer. There’s nothing semantic about event handlers. They’re simply hooks that provide a level of functionality to particular user interfaces. Avoid this syntax for the same reasons that you’d want to avoid presentational tags like `B`, `I`, and `BLINK`. Second, it limits you to one action per event. Let’s say that striping tables wasn’t the only thing you wanted to do once the page was loaded. It’s not at all uncommon to have five or six different things going on, all of which need to be triggered once everything on the page is already in place. How could we squeeze all of those into the body element without being reduced to absurdities like:
    
    <body onload="
                  stripeAllTables();
                  addTableRulers(); 
                  jumpUpAndDown(); 
                  doSomethingElse();
                 ">
    

That’s just ugly code, and it’s not at all in keeping with the strict separation of layers that we really want to keep in place. So how can we improve things?

Simple: use standards. The DOM provides an event handling facility that should be used instead of embedding the event handling code inside your content. The usage (of course) differs a bit across browsers, but the following code seems pretty solid in my testing:
    
    function handleEvent(obj, event, func) {
        try {
            obj.addEventListener(event, func, false);
        } catch (e) {
            if (typeof obj['on'+event] == "function") {
                var existing = obj['on'+event];
                obj['on'+event] = function () { existing(); func(); };
            } else {
                obj['on'+event] = func;                        
            }
        }
    } 
    

You pass the function three bits of information: the object which generates the event (in our example, this would be the `window` object), the event name (without the “on” prefix), and the function that should be called when the event happens.
    
    handleEvent(window, "load", stripeAllTables);
    

This enables us to handle an arbitrary event with an arbitrary number of functions, each of which getting called in turn to enable some behavior. Let’s use this new knowledge to add the Table Ruler functionality into our striping function:
    
    function stripeTable(table) {
        var tbodies = table.getElementsByTagName("tbody");
        for (i=0, numBodies=tbodies.length; i<numBodies; i++) {
            var even    = false;
            var trs = tbodies[i].getElementsByTagName("tr");
            for (var j=0, numTrs=trs.length; j<numTrs; j++) {
                trs[j].className += (even)?" even":" odd";
                even = !even;
                handleEvent(
                    trs[j], 
                    "mouseover", 
                    function(e) { 
                        var self = this;
                        if (window.event) {
                            self = window.event.srcElement.parentNode;
                        }
                        if (!self.className) {
                            self.className = "hoverClass";
                        } else if (!self.className.match(/hoverClass/)) {
                            var classes = self.className.split(/s+/);
                            classes.push("hoverClass");
                            self.className = classes.join("");
                        }
                     }
                );
                handleEvent(
                    trs[j], 
                    "mouseout", 
                    function() {
                        var self = this;
                        if (window.event) {
                            self = window.event.srcElement.parentNode;
                        }
                        self.className = self.className.replace(/hoverClass/, "");
                    }
                );
            }
        }
    }
    

There’s some complex stuff in there, so let’s take it slowly. The big idea is to add a handler to the `mouseover` and `mouseout` events of each table’s row. When you mouseover the row, we want to set it’s `className` to “hoverClass”. When you mouseout, we want to remove that designation. This is pretty much the same technique used by the [Suckerfish dropdown menus][6]. We accomplish this goal by adding two event handlers to each row that we’ve striped: one handles mouseovers, the other mouseouts. So, how does it work? We’ll take a close look at the mouseout handler, since that’s the less complex of the two:

We call `handleEvent`, and pass it the row we’re currently looking at: `trs[j]`, the event we want to handle: `mouseout`, and then create an anonymous function that does the heavy lifting. Don’t worry too much about how functions get passed around in JavaScript, that’s a topic for another article. For the moment, just accept on blind faith that this sort of syntax works. Let’s look at that function in more detail:

First, we declare a variable `self` and assign it the value of `this`. We do this because JavaScript sometimes has strange scoping issues with regard to `this`; it’s simply a good habit to get into.  
Next, we check to see if there’s a `window.event` object. IE/Win handles events a little strangely: in this case, the event gets triggered on a table cell instead of a table row. `this` is therefore set to the incorrect object, and things don’t work like we want them to. So, we grab the `parentNode` instead. Finally, we remove any reference to `hoverClass` in the row’s `className`. That pretty much takes care of things.

So there you have it. With a little simple code, we’ve managed to put together a framework in which to handle JavaScript events, and we’ve got a useful little demonstration of the framework’s power that combines the best of two [ALA][4] articles. Isn’t this stuff neat?

This code is wrapped up in [a nice little example][7]. Take a look, it's pretty great stuff.

   [1]: http://molly.com/
   [2]: http://2005.sxsw.com/interactive/conference/panels/?action=show&id=IAP0074
   [3]: http://alistapart.com/articles/zebratables/
   [4]: http://alistapart.com/
   [5]: http://alistapart.com/articles/tableruler/
   [6]: http://www.alistapart.com/articles/dropdowns/
   [7]: /projects/files/EventHandler/javascriptEventHandlingExample.html


---
Alias:
- http://mikewest.org/blog/id/4
Modified: '2006-04-14T10:50:11Z'
Teaser: 'An expansion of earlier unobtrusive JavaScript articles: this time we''re
    adding type-ahead search functionality to SELECT elements.'
layout: post
tags:
- JavaScript
title: Type-Ahead search for select elements
---
In the previous [two][1] [articles][2] on the topic, we’ve outlined methods for hooking JavaScript behaviors onto events on your pages, and ways of encapsulating those behaviors so that they don’t interfere with any other JavaScript goodness your site may be sporting. We’ve been careful to ensure that the added behaviors are just that: additions or enhancements that don’t effect the usability or accessibility of the page for those browsing without the benefit of JavaScript. But let’s be honest, the examples have been a bit boring thus far. We changed the colours of some table rows.

Yippie.

Let’s be a little more adventurous in our enhancements: Let’s make everyday, run of the mill `select` boxes a bit more interesting (and usable!) by adding a type-ahead search.

How do we start on a project like this? The first thing to do is to map out how we want the action to proceed. If we don’t have a good goal in mind, we stand a good chance of wandering off into the dark and getting lost. I think that the best method from a pedagogical standpoint is something like the following: We’ll add a button next to each `select` element we want to be able to search through. Clicking that button will pop up a nicely styled `input` field that we can type into. As we type into that field, the associated `select` box will automatically jump to the value we’re typing in. So typing “mi” into a list containing “Bob Smith”, “Frank Jones”, “Mike West”, and “Zed Zebra” would jump instantly to “Mike West.” That makes sense, and could really help out if we’re dealing with a list that’s a little longer than 4 elements. Just for fun, let’s also stipulate that I should be able to type the up or down arrow to scroll through the select box while I’m typing, and that hitting enter should hide the `input` field. That sounds pretty useful, right? It’s not the ideal way from a usability perspective, but it’s going to give us a chance to really dive into some DOM functionality and give us lots of events to hook into, which makes it perfect to teach with. :) As a last item, we’re going to stipulate that each of the `select` boxes we work with be pre-sorted. It would be pretty simple to adapt the script to deal with unsorted lists, but if we stipulate that the lists are pre-sorted, we can make it work much, much more quickly.

So, once we’ve got that map solidly in place, we can start in on the coding. Initially, we’ll need to come up with a nice package name that distinguishes this widget from any other we might come up with in the future. I’ve chosen “TypeAheadSelect”, feel free to branch out from that on your own; it’s fairly arbitrary. With the name chosen, we’ll go ahead and create the package:
    
    function TypeAheadSelect () {
        var self = this;
        ...
    }
    

Looks good so far. We’ve set up an alias for `this` in order to bypass some scoping issues that might crop up later, and we’ve got everything wrapped in a function to provide a namespace to work within. What next? 

We’ll tackle the remaining tasks one at a time: first, we’ll generate a list of the elements we want to work with. But how do we know which those are? We can pretty easily generate a list of all the `select` elements on the page with a simple call to `getElementsByTagName`:
    
    var allSelects = document.getElementsByTagName('select');
    

But we probably don’t want to apply this functionality to all of our select boxes. A simple yes/no toggle certainly wouldn’t need it, and we wouldn’t want to apply it to any `selects` that already have `onChange` events associated with them. We really want to add the behavior to only those `select` elements that we specify beforehand… but how? We’ve really got two methods: class names, or [custom attributes][3]. The former’s trivial, and I used it in the example code for the previous two articles. We simply come up with a descriptive class name, and apply it to the relevant `select` elements:
    
    <select class='typeAheadable'>
        <option value='0'>Hi!</option>
        ...    
        <option value='1'>Bye!</option>
    </select>
    

That certainly makes sense, but it’s arguably non-semantic in more or less the same way that `class='blue'` causes problems. Strictly speaking, they’re both really just presentational. Neither class name carries with it any **semantic** designation. It’s a minor quibble, but it could be a problem for you. (Of course, you could get around this argument by defining certain **types** of `select` boxes on your pages. You could have a “nameList” `class`, for instance, to describe the list we talked about earlier. That would carry semantic meaning, and would remain quite hookable. The tradeoff is that we’d lose some of our code’s genericness. Instead of being able to easily drop into any site, we’d end up hard-coding a list of classes it should apply to. That tradeoff might or might not be worth it to you, depending on your reaction to the next method I’ll discuss.)

The other method is to define your own addition to the XHTML spec (as discussed at length in [this ALA article][3]), and add a custom attribute to the `select` elements you’d like to enhance. This carries with it a bit of a burden, in that you’ll have to [define your own DTD][4] in order to make your site validate. This is the method I’m going with in this article, just because it gives me a chance to talk about attribute nodes and other geeky tech stuff like that. In the same vein as attributes like `multiple` and `selected`, our attribute (`typeAheadable`) could look something like:
    
    <select typeAheadable='typeAheadable'>
        <option value='0'>Hi!</option>
        ...    
        <option value='1'>Bye!</option>
    </select>
    

With that choice in mind, let’s tackle the problem at hand. We’ve already got the first part of our solution: the code that grabs all the `select` elements on the page. To that, we’ll need to add a loop in order to iterate through the list, a test to see if the particular `select` we’re looking at is one we should work with, and then the code to actually put our new functionality into place. This ends up looking something like:
    
    self.instantiate = function () {
        var allSelects = document.getElementsByTagName('select');
        for (var i = 0; i < allSelects.length; i++) {
             if (allSelects[i].getAttribute('typeAheadable')) {
                self.addFilter(allSelects[i]);
            }
        }
    }
    

The `getAttribute` code is probably the only part of that that you don’t already understand, but it’s fairly self-explanatory. It returns the value of the attribute you specify, or null if the attribute doesn’t exist. Very simple, very useful. If the attribute is specified, we call `addFilter` in order to do the heavy lifting, if not, we ignore the `select`. 

If we wanted to do a class name based test, we could easily replace the `if` statement’s condition with something like:
    
    if (allSelects[i].className.match(/typeAheadable/)) {
        ...
    }
    

That would work just as well.

Regardless of which method you choose, let’s go ahead and create the new elements we’re going to be working with. We’ll want a button to press in order to toggle the visibility of our text field, and we’ll also need the text field itself. Let’s look at the `input` field first. It’s functionality is pretty straightforward: as we type, we want to check the keys we’re pressing to see if they’re the up arrow, the down arrow, the enter key, or just some other character. We’ll bind a function to the `input` element’s `onkeyup` event to handle that check.
    
    // Create the element
    typeAheadInput = document.createElement("input");
    // Give it a type: in this case 'text'
    typeAheadInput.setAttribute('type', 'text');
    
    /*
        This is important: we set the 'haystack' property of our INPUT
        element to a reference to our master SELECT element.  This powerful
        feature of JavaScript enables us to talk to the SELECT element 
        in our INPUT element's event handler, which is critical.
    
        We'll see later where `obj` is coming from.  For the moment, just 
        keep it in mind as a question I need to answer for you.
    */
    typeAheadInput.haystack = obj;
    
    /*
        The heavy stuff: this binds an anonymous function to the INPUT
        element's onkeyup event in order to intercept the keypresses 
        and parse them in order to determine what to do.
    */
    handleEvent(
        typeAheadInput, 
        'keyup',
        function(e) {
            if (!e) {
                /*
                    If `e` wasn't set, then we know that we're using the Internet
                    Explorer style event model.  So, we'll have to do a little work
                    to merge the two systems together.
                */
                e        = window.event;
            }
            var theInput = this;
    
            var keycode = e.keyCode;
    
            switch (keycode) {
                case 38: // up arrow
                    /*
                        We want to respond to the up arrow by moving the current 
                        value up one in our list.  But we don't want to run off 
                        the top of the list, so we get the maximum value: 0, or 
                        the currentIndex - 1.  So if we're at the 8th value, 
                        we'll move to the 7th, but if we're already at the top, 
                        we'll stay at the 0th (numbering starts at 0 in JavaScript)
                    */
                    var newIndex = Math.max(0, theInput.haystack.currentIndex-1);
                    theInput.haystack.currentIndex  = newIndex;
                    theInput.haystack.selectedIndex = newIndex;
                    
                    /*
                        We'll also need to clear out our current filter, since 
                        we've messed with the position in the list.  If we didn't
                        do this, some of our later optimizations would die horribly.
                    */
                    theInput.haystack.currentFilter = "";
                    break;
                    
                case 40: // down arrow
                    /*
                        Same thing as the up arrow here, except we want to get 
                        the minimum value between the last element in the list, 
                        and the currentIndex + 1 to make sure we don't run off
                        the end.
                    */
                    var newIndex = Math.min(
                                            theInput.haystack.options.length-1, 
                                            theInput.haystack.currentIndex+1
                    );
                    theInput.haystack.currentIndex  = newIndex;
                    theInput.haystack.selectedIndex = newIndex;
                    theInput.haystack.currentFilter = "";
                    break;
    
                case 13: // enter
                    /*
                        If we hit enter, tell our containing DIV to hide itself
                    */
                    theInput.parentNode.style.display = "none";
                    break;
    
                default:
                    /*
                        If it's not the up/down arrow, or the enter key, then process
                        it by telling the SELECT box to set itself to the correct value.
                        We'll talk about telling the SELECT element how to do that in 
                        a few moments.
                        
                        The timeout code is here in order to deal with fast typists: we
                        don't want to tell the SELECT box to filter itself for every keypress
                        if we're in the middle of typing a word.  That would slow things 
                        and potentially cause problems if the value of the INPUT field 
                        changed during the middle of an event.  So we store a timer that
                        waits 25 milliseconds before telling the SELECT object (stored in 
                        this.haystack) to filter itself using the currently typed-in text.
                        
                        Every time a key is pressed, we clear out that timer, and reset it
                        for another 25 milliseconds.  That solves our problem.
                    */
                    clearTimeout(theInput.timer);
                    theInput.timer = setTimeout(
                                    "document.getElementById('" +
                                    theInput.haystack.id + 
                                    "').filterSelf('" +
                                    theInput.value +
                                    "')", 
                                    25
                    );
                    break;
            }
        }
    );
    

That’s the `input` field in a nutshell. Not too tough, right? We just create the element, and give it a function to handle the keyup event. Hopefully the commented code makes sense, because it’s going to get a little more complex later on. :) For strictly presentational reasons, I’m going to wrap the `input` inside of a `div` so that we can give it some nice borders and background colours. We’ll give this `div` a class of ‘typeAheadBox’, since it’s a box that contains a type ahead search widget. Let’s create that now and append the `input` element inside it, that’s pretty trivial:
    
    var typeAheadBox       = document.createElement('div');
    typeAheadBox.className = "typeAheadBox";
    typeAheadBox.appendChild(typeAheadInput);
    

Two things are left now, we need to create the button that toggles the visibility of the `div` containing the `input` field, and we need to explain to the `select` element we started with how it’s supposed to be able to figure out which value it should jump to when we type something in.

The former’s easier, let’s get it out of the way:
    
    var toggleButton             = document.createElement('input');
    toggleButton.className       = "toggleButton";
    toggleButton.filterContainer = typeAheadBox;
    toggleButton.setAttribute('type', 'button');
    toggleButton.setAttribute('value', 'Type Ahead!');
    
    /*
        When we click on the button, we want to make the DIV containing our INPUT
        element visible, and position under the button, aligned with it's left edge.
        
        This javascript code is fairly self-explanatory, but if there are questions,
        I'll be happy to answer them in the comments section.
    */
    handleEvent(
        toggleButton, 
        'click', 
        function (e) {
            if (!e) e = window.event;
            var theButton = this;
                      
            var theFilter = theButton.filterContainer;
            if (theFilter.style.display == "block") {
                // it's visible, so hide it:
                theFilter.style.display = "none";
            } else {
                // display it, and focus on it                              
                theFilter.style.display = "block";                            
                theFilter.childNodes[0].focus();                                
                theFilter.style.left    = (
                                            findPosX(theButton)
                                            - 
                                            theFilter.offsetWidth 
                                            + 
                                            theButton.offsetWidth
                                          ) + "px";            
                theFilter.style.top     = (
                                            findPosY(theButton)
                                            + 
                                            theButton.offsetHeight
                                          ) + "px";                                 
            }
        }
    );
    

All that’s left now is the code that actually takes the search string that we’ve typed in, and selects the proper option in our `select` box. The function takes a single argument (the text that it should look for), and processes the list accordingly:
    
    obj.filterSelf = function (needle) {
        /*
            If we've backspaced or deleted all the text in the 
            INPUT field, then we need to do one of two things:
                If our SELECT is a multi-select box, then we set
                the selectedIndex to -1 in order to deselect all
                the options.  Otherwise, we set it to 0 to choose
                the first option in the list.
        */
        if (needle == "") {
            obj.currentIndex  = 0;
            obj.selectedIndex = (obj.getAttribute("multiple") == "multiple")?-1:0;
            this.currentFilter = "";
            return;
        }
    
        // we lower-case the needle text so that our comparisons make sense.
        needle = needle.toLowerCase();
    
        /*
            I've gone with a binary search technique here, because it's generally 
            pretty darn fast on large arrays.  This is the main reason we require
            a sorted list, since a binary search can only work when items are in
            order.  In a nutshell, the technique is this:
                To begin, set `high` to the end of the list (this.options.length), 
                and `low` to the beginning of the list (0).  Then pick the middle
                element.  If that item is higher than the value you're looking for,
                then your value must be before it in the list.  So reset `high` or
                `low` to the index of the current element, and repeat until you 
                find your value, or run out of items.
    
                At the end of the search routine, we'll either have a value of -1, 
                or an index.
        */
        theIndex = "";
        if (this.currentFilter == "") {
            var low = -1;
            var high = this.options.length;
        } else if (needle < this.currentFilter) {
            var low  = -1
            var high = this.currentIndex;
        } else if (needle > this.currentFilter) {
            var low = this.currentIndex;
            var high = this.options.length;
        }
        if (high == 1) {
            if (this.options[0].text.toLowerCase() == needle) {
                theIndex = 1;
            } else {
                theIndex = 0;
            }
        }
        high = high - 1;
        if (theIndex == "") {
            for (;(high-low>1) && (theIndex == "");) {
                var j = Math.floor((high+low)/2);
                if (needle <= this.options.item(j).text.toLowerCase()) {
                    high = j;
                } else {
                    low = j;
                }
            }
            if (needle == this.options.item(high).text.toLowerCase()) {
                theIndex = high;
            } else {
                theIndex = low;
            }
        }
    
        /*
            If theIndex is -1, then we've got nothing, so set the currentIndex to
            0.  Else, if we've found the value, set the currentIndex to theIndex.
            Else, we ended up somewhere in the middle of the list, but didn't find
            the value we were looking for.  In that case, set the currentIndex to 
            the value just after the one we ended up on.
        */        
        if (
                theIndex == -1 
                || 
                needle == this.options[theIndex].text.toLowerCase()
        ) {
            this.currentIndex  = Math.max(theIndex, 0);
            this.selectedIndex = Math.max(theIndex, 0);
        } else {
            this.currentIndex  = Math.max(theIndex+1, 0);
            this.selectedIndex = Math.max(theIndex+1, 0);
        }
    }
    

Take all of that code (the button, the `input` element, and the `filterSelf` method), and wrap it up in the following: 
    
    self.addFilter = function(obj) {
        ...
    }
    

This is where the aforementioned `obj` comes from: it’s passed in when you instantiate the object.

Now that we’ve got the proper behaviors associated with the proper events, it’s a simple matter of sticking the toggleButton and typeAheadBox into the flow of the document:
    
    obj.parentNode.insertBefore(toggleButton, obj);
    obj.parentNode.insertBefore(typeAheadBox, obj);
    obj.parentNode.insertBefore(obj, toggleButton);
    

We’ll also set the currentIndex and currentFilters to 0 and “”, just to ensure that everything works when we first start typing information into the system.
    
    obj.currentIndex = 0;
    obj.currentFilter = "";
    

And there you have it. All the code is packaged together in [this example file][5] for your perusal.

[1]: /2005/03/event-handlers-and-other-distractions
[2]: /2005/03/component-encapsulation-using-object-oriented-javascript
[3]: http://alistapart.com/articles/scripttriggers/
[4]: http://alistapart.com/articles/customdtd/
[5]: /projects/files/EventHandler/typeAheadSelectExample.html


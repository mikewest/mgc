---
Alias:
- http://mikewest.org/blog/id/2
Modified: '2006-06-27T10:12:44Z'
Teaser: A walkthrough of the process I used to make an accessible slider widget from
    a SELECT element.
layout: post
tags:
- JavaScript
title: Slidable Select Widgets Explained
---
When designing a web-based application, we’re working with a hugely impoverished set of widgets as compared to what might be available in a native app. Dropdowns, text-input fields, and a variety of buttons more or less define the boundaries within which we need to work. Despite this, we’ve managed to make some truly interesting user interfaces, and the possibilities are only expanding as we start to explore some newly rediscovered technologies like XMLHttpRequest.

That’s one direction to explore; as [Matthew May][1] points out, it basically throws the doors wide open for new paradigms. I’ll certainly be talking about that sort of thing on this site (especially since I’m heavily involved in trying to [improve XMLHttpRequest’s JavaScript interface][2]), but for the moment I’d like to point out another option. We can transparently extend the widgets we already have, an approach which I think has some real potential in terms of maintaining accessibility while leaping forward with regard to the typical user’s experience. I’ve started down this road in previous articles, specifically the idea of [adding type-ahead searching to `select` elements][3], which certainly isn’t anything really _new_. It _is_, however, something that allows us to gradually improve the way that we interact with applications on the web. Small steps like that will eventually take us quite a long way towards replicating a native-like feel in our apps without diving into the inaccessible quagmire of ActiveX or Flash plugins. This article will explain another of those small steps: a slidable `select` widget that replaces the typical dropdown with a nicer-looking (we’ll ignore my Photoshop ‘skills’ for the moment, and assume that people can make better skins for the widget) alternative that works in all the modern browsers (Mozilla, IE6, Safari/Konqueror, and Opera).

[Example code for this slider is available at /projects/files/Widgets/SliderSelect/][4]

Again, we’ll start this project by mapping out what functionality we want to provide. So, here’s what we’re planning on accomplishing. Using a `select` box as our template, we’ll create a slider bar with a few distinct visual elements: A ‘gutter’ that defines the space in which we can slide. A ‘slider’ that indicates our current position within the gutter, and several ‘placeholders’ that indicate defined selection points within the gutter. These selection points will correspond to the `option` elements inside our `select` template. This is about as simple as we can make the slider, so we’ll start with this, and discuss some additional features that might be nice to add in later. Importantly, the slider needs to somehow maintain a value that can be manipulated via the DOM and submitted via a form, just like it’s parent `select` element.

So how can we accomplish this, using the tools that we currently have available? Let’s start by coming up with a way of presenting a slider bar, and work backwards from there. Here’s what I decided upon for a structure:
    
    <select id='selectBoxId' name='selectBoxName' presentation='slider'>
        <option value='0'>Option 1</option>
        ...
        <option value='N'>Option N</option>
    </select>
    

Becomes:
    
    <div class='SliderContainer'>
        <div class='gutter'>
            <span class='slider'></span>
            <span class='placeholder'></span>
            ...
            <span class='placeholder'></span>
        </div>
        <input type='hidden' id='selectBoxId' name='selectBoxName' />
    </div>
    

That seems fairly straightforward to me, and provides all the structure we’ll need in order to fully encapsulate the functionality of each slider bar from every other slider bar on the page. We need the container `div`, for example, in order to easily identify the slider’s `input` element via some simple DOM calls (e.g. this.parentNode.childNodes[1]) from any of the slider’s other elements. It also makes styling via CSS a little more specific so that we don’t have to come up with _truly_ unique class names.

Now that we’ve got a solid DOM structure in mind, let’s get started on the JavaScript needed to generate that model from a `select` element. We’ll begin with some code that should be pretty familiar by now (if it’s not, take a quick look at my [object encapsulation article][5] for some help):
    
    function SliderSelect() {
        var self = this;
    
        /*
         *  Hook into each `select` element with a `presentation` attribute set to `slider`,
         *  and call `slidify` to flip it's presentation from a dropdown to a nice looking
         *  slider.
         */
        self.instantiate = function () {
            var allSelects = document.getElementsByTagName('select');
            for (var i = allSelects.length-1; i >= 0; i--) {
                if (allSelects[i].getAttribute('presentation') == "slider") {
                    self.slidify(allSelects[i]);
                }
            }
        }
    
        ...
    
        handleEvent(window, "load", self.instantiate);
    }
    

We’re looking for all the `select` elements on the page with a `presentation` attribute of “slider”, and calling a method named “slidify” on all of them. That’s where we’ll create our structure. We’ll take a look at that code now:
    
    self.slidify = function (selectBox) {
    

Starting off, we determine how wide the `select` element that we’re replacing was. We’ll use the same width for our slider. This gives us a simple method of controlling the amount of space the slider takes up by simply styling the `select` element it’s going stand-in for. We then create the outermost `div` that will contain the remainder of our structure. It gets the class name “SliderContainer”, and we set it’s width to the width of the `select` element it replaces.
    
        var selectBoxWidth  = selectBox.offsetWidth;
    
        var containerDiv         = document.createElement('div');
        containerDiv.className   = "SliderContainer";
        containerDiv.style.width = selectBoxWidth + "px";
    

The gutter is the next item on the list. It’s going to hold most of the variables associated with the slider, because as we’ll see later, it ends up being the element that does most of the work. 

We’ll need to keep track of a few bits of information, including the number of options in our `select` element’s dropdown, the currently selected option’s index, and the list of option values and names. As it turns out, the simplest way to keep track of that latter set of info is just to grab the entire `options` collection off the `select` element, and store it on the gutter `div`. JavaScript’s loose typing makes that a breeze. Finally, we’ll need to figure out how wide each option should be on the slider. That’s a simple calculation: divide the width of the box by one less than the total number of items (because the first item lines up with the left edge of the slider). The code to do all that is as follows:
    
        var theGutter                = document.createElement('div');
            theGutter.className      = "gutter";
            theGutter.options        = selectBox.options;                        
            theGutter.numOptions     = selectBox.options.length;
            theGutter.optionDistance = Math.floor(selectBoxWidth/(theGutter.numOptions-1));
            theGutter.defaultOption  = (selectBox.selectedIndex)?selectBox.selectedIndex:0;
    

The slider is next, and it’s trivial: just a span with a `className` of “slider”.
    
        var theSlider           = document.createElement('span');
            theSlider.className = "slider";
    

We’ll set up a hidden `input` field to store the value that used to be associated with the `select` element, and give it the same `name` and `id` attributes so that any references to it won’t need to be rewritten.
    
        var theInput            = document.createElement('input');
            theInput.id         = selectBox.id;
            theInput.name       = selectBox.name;
            theInput.type       = "hidden";
            theInput.value      = selectBox.options[theGutter.defaultOption].value;
            theInput.onchange   = selectBox.onchange;
            theInput.options    = selectBox.options;
    

Now we’ve gotten the major components of our slider created, let’s start sticking them together into a coherent whole. First, we’ll append the slider to the gutter (meaning that it can be referenced as `theGutter.childNodes[0]`):
    
        theGutter.appendChild(theSlider);
    

Next, we’ll create some placeholder `span`s that we’ll use for the tick marks that delineate options. We’ll create as many of these `span`s as we have options, and place each at the proper location in the slider by setting their `left` style attribute:
    
        var placeHolder = document.createElement('span');
            placeHolder.className  = 'placeHolder';
            theGutter.appendChild(placeHolder);     
    
        for (i = 1; i < theGutter.numOptions; i++) {
            var placeHolder = document.createElement('span');
            placeHolder.className  = 'placeHolder';
            placeHolder.style.left = Math.min(selectBoxWidth, (i * theGutter.optionDistance)) + "px";
            theGutter.appendChild(placeHolder);
        }
    

So, the gutter is complete: let’s stick it into the container `div`, and then place the `input` field in there too:
    
        containerDiv.appendChild(theGutter);
        containerDiv.appendChild(theInput);
    

Two steps remain: First, we set up an event handler to make the slider work correctly (which we’ll talk about in a moment):
    
        handleEvent(theGutter, "mousedown", self.registerSlider);
    

And finally, we position the slider in the proper location on the gutter, and replace the original `select` element with the slider that we’ve created.
    
        theSlider.style.left = (
                                    Math.min(
                                        selectBoxWidth, 
                                        (theGutter.defaultOption * theGutter.optionDistance)
                                    ) 
                                    - 
                                    Math.floor(
                                        theSlider.offsetWidth/2
                                    )
                               ) + "px";                            
        selectBox.parentNode.replaceChild(containerDiv, selectBox);
    }
    

So, most of the hard work is done at this point. Using a little CSS to set up background images and colours, we’ve got a nice looking slider bar sitting on our page, waiting for us to play with it. Now comes the hard part. How the heck do we make this thing work?

Well, you saw above that we registered an event handler that fires off when we click anywhere on the gutter. We’re going to use that event to set up everything else that we need to take care of. The plan is this: when you click on the gutter, we’ll set three tracking variables — `activeSlider`, `activeInput` and `activeGutter`— to keep track of which slider it is that you’ve clicked on. This enables us to run multiple sliders on the same page, because we’ve cleverly encapsulated all of a slider’s relevant information in properties that hang out on the gutter itself. Once we’ve saved off references to the slider we’re currently working with, we register two event handlers on the `document` object. These handlers trigger based on mouse movement (`mousemove`) and letting go of the mouse button (`mouseup`). 

In a nutshell, these triggers will allow us to replicate click-and-drag functionality on our slider by letting us know what state the mouse is in. When we click on the gutter, we set up some variables so that we know that the mouse button is down. While the mouse button is down, we want to use the information gathered from the `mousemove` event to position the slider on the gutter. When the mouse button is lifted, we want to stop moving the slider around, and lock it into one of the demarcated positions on the gutter. In essence, we’ve created a simple [state machine][6].
    
    self.registerSlider = function (e) {
        if (!e) e = window.event;
    
        /*
         *  Inside the event handler, `this` refers to the object that
         *  triggered the event: in this case, the gutter.
         */    
        self.activeGutter = this;
        self.activeSlider = this.childNodes[0];
        self.activeInput  = this.parentNode.childNodes[1];
        handleEvent(document, "mouseup",   self.unregisterSlider);
        handleEvent(document, "mousemove", self.mousemove);
        /*
         *  We call mousemove here in order to deal with the case in which
         *  the user simply clicks on the gutter instead of clicking and
         *  dragging.  Calling mousemove here, and passing in the current
         *  event object, allows us to reuse the mousemove code to set
         *  the initial position of our slider.
         */
        self.mousemove(e);
        e.cancelBubble = true;
        return false;
    }
    

`registerSlider` deals when the `mousedown` event, and sets things up to let us know that we should be processing `mousemove` events. Let’s quickly talk about `unregisterSlider`, which gets called when we let go of the mouse button. A few things need to happen here: first, we want to reposition the slider to whichever of the tick marks it’s closest to (It’s a `select` element, after all. You can’t sit on the fence between two `options`, it’s one or the other). We determine which option we’re closes to in the `mousemove` handler, which we’ll discuss in a moment, so all that’s left is to ensure that the slider is actually positioned on that option. This is a simple multiplication of the `optionNum` that we already know, and the `optionDistance` that we calculated when we instantiated the slider bar. Due to rounding issues, we’ll make sure we don’t jump off the end of the bar by using `Math.min` to get the minimum value between our calculated position and the slider bar’s actual width. That should take care of things. All that’s left is to set the activeSlider, activeGutter, and activeInput values to `null`.
    
    self.unregisterSlider = function (e) {
        if (!self.activeGutter) { return; }
    
        self.activeSlider.style.left = (
                                            Math.min(
                                                self.activeGutter.offsetWidth, 
                                                (   
                                                    self.activeGutter.optionNum 
                                                    * 
                                                    self.activeGutter.optionDistance
                                                )
                                            ) 
                                            - 
                                            Math.floor(self.activeSlider.offsetWidth/2)
                                       ) + "px";
        self.activeInput.value = self.activeGutter.options[self.activeGutter.optionNum].value;
    
        document.onmousemove = null;
        self.activeGutter    = null;
        self.activeSlider    = null;
        self.activeInput     = null;        
    }
    

The last thing to discuss is probably the most important piece of the puzzle. How do we make the slider move when we drag it with the mouse? As it turns out, this isn’t at all difficult. The event object gives us the coordinates of the mouse on the page (of course, [this isn’t precisely true][7], but for our purposes, the quirks don’t matter) with the simple syntax `e.clientX` and `e.clientY`. This coordinate information is all we need in order to position the slider correctly. The only magic in this function is the code that snaps the slider to a placeholder when it comes within a certain number of pixels. We take the pixel value of the slider’s current position, and mod it by the `optionDistance`. That gives us the number of pixels between the current position, and one of the options. From that, we can determine if we’re close enough to the option to jump right to it. I’ve chosen 10% of the option distance as my snap-to distance, but that could easily be pulled out into a configuration option when the object is instantiated. Also, I’ll note that the function `findPosX` is borrowed from PPK’s excellent [QuirksMode][8]. I’ll leave it’s explanation to him:
    
    self.mousemove = function (e) {
        if (!e) {
            e             = window.event;
            e.returnValue = false;
        }
        if (!self.activeGutter) { return; }
    
        self.offset = Math.min(
                            Math.max(0, (e.clientX - findPosX(self.activeGutter))),
                            self.activeGutter.offsetWidth
                         );
    
        var currentPos     = self.offset;
        var snapTo         = currentPos % self.activeGutter.optionDistance;
        var snapToDistance = Math.floor(self.activeGutter.optionDistance / 10)
        self.activeGutter.optionNum = Math.round(currentPos / self.activeGutter.optionDistance);
    
        if (snapTo <= snapToDistance) {
            currentPos = currentPos - snapTo;
        } else if (self.activeGutter.optionDistance - snapTo <= snapToDistance) {
            currentPos = Math.min(
                                    self.activeGutter.offsetWidth, 
                                    currentPos + (self.activeGutter.optionDistance - snapTo)
                                 );
        } 
    
        self.activeSlider.style.left = (
                                    currentPos 
                                    - 
                                    Math.floor(self.activeSlider.offsetWidth/2)) + "px";
    }
    

And that’s it. Plug that code into the framework outlined above, and you’ve got yourself a working slider bar.

There are, however, some vaguely large drawbacks to this method. First, the normal event handling of the `select` element more or less goes away. You see, JavaScript doesn’t fire an `onchange` event when an input field is programatically changed. This means that we can’t easily hook into the hidden `input` field in order to take some action when the user repositions the slider. What we can do, however, is partially fake the functionality by providing a mechanism for calling some user-defined function when the slider changes position. I’ll leave that implementation detail for another article. :)

Additionally, I'll be talking about some more visible improvements that could be made: for example, I'd like to display the names of each selected option somehow, perhaps as a tooltip? That's going to take a little work. Look for things like that next time I put an article together.

[Example code for this slider is available at /projects/files/Widgets/SliderSelect/][9]

   [1]: http://www.bestkungfu.com/archive/date/2005/03/ajaxessibility/
   [2]: /2006/03/datarequestor/
   [3]: /2005/03/type-ahead-search-for-select-elements
   [4]: /projects/files/Widgets/SliderSelect/sliderSelectExample.html
   [5]: /2005/03/component-encapsulation-using-object-oriented-javascript
   [6]: http://en.wikipedia.org/wiki/State_machine
   [7]: http://evolt.org/article/Mission_Impossible_mouse_position/17/23335/index.html
   [8]: http://www.quirksmode.org/js/findpos.html
   [9]: http://mikewest.org/projects/files/Widgets/SliderSelect/sliderSelectExample.html


---
Alias:
- http://mikewest.org/blog/id/3
Modified: '2007-05-18T18:49:04Z'
Teaser: An introduction to using classes in JavaScript in order to avoid namespace
    conflicts and gain interesting object-oriented functionality.
layout: post
tags:
- JavaScript
title: Component encapsulation using Object-Oriented JavaScript
---
Yesterday, I talked a little bit about the ways in which events could be handled across browsers in order to pave the way for a more in-depth discussion of the various methods by which we can enable a true behavioral layer on a website without corrupting the pristine semantic layer we’ve already perfected. So now we’ve got a strategy in place for hooking into our DOM tree: we add event handlers to elements on the page, and use those triggers to generate new and interesting behaviors. Simple enough. But we need at least one more basic concept before we can really start making leaps forward in terms of interesting behaviors: encapsulation.

Let’s say, for instance, that we wanted to use the [table striping code][1] outlined in yesterday’s article. That defines three functions: `stripeTable`, `stripeAllTables`, and `handleEvent`. All of these functions go directly into what’s called the “Global Namespace”. This is a fancy way of saying that they’re defined everywhere. I could call `stripeTable` within any other JavaScript function I created, which - generally speaking - is a good thing.

However, there’s a danger here of polluting the global namespace with functions and variables that really shouldn’t be there. What if I needed another JavaScript function that swapped out a picture of a plain dining-room table with a picture of a colorfully striped dining-room table? I’d end up with two functions that would naturally be named `stripeTable`, and that would indeed cause problems! This example is, naturally, a bit contrived, but the danger is real, especially once we get around to building reusable components that can be simply included into a page for some effect. We’ll want to ensure that the functions we define for our component don’t mesh badly with anyone else’s components. So how can we get around this sort of problem?

Simple: we create JavaScript objects. I’ll outline how to do that, and it’s going to take us a bit far afield from the initial discussion of namespaces. Trust me, the diversion is worth it, if a bit long and boring.

So. Object-oriented programming is all the rage these days, and it’s a little known fact that JavaScript is remarkably proficient at defining reusable components that can be dynamically created and modified in your applications. Let’s look at the syntax for a really simple object:
    
    function MyObject() {
        var self = this;
    
        self.setValue = function (value) {
            self.value = value;
        }
        self.getValue =  function() {
            return self.value;
        }
    
        self.value = 0;
    }
    

That looks a lot like a function definition. In fact, it **is** a function definition. What gives? The simple explanation is that JavaScript can treat functions like other languages treat objects. There are [more complicated explanations][2], but I’ll leave those aside in the interests of simplicity. Just flow with the syntax, it’ll quickly become second nature.

So, what’s happening here? In a nutshell, we’re creating an object definition (a `class` in the lingo of Object-Oriented programming). The overused, but fairly accurate, example that I heard over and over in school goes something like this: The object definition (`class`) acts very much like a building’s blueprint. An architect draws up a blueprint that details exactly how a building is going to look, what it’s made out of, and how it works. Given a blueprint, we could build fifty houses, all with exactly the same features.

In the same way, the function MyObject allows us to create an arbitrary number of `instances`: actual, usable objects. The syntax for that is probably familiar to you:
    
    var anInstance = new MyObject();
    

This bit of code is using the definition we wrote for MyObject to create an `instance` of that `class`.  
Cool, eh? So let’s look a little more closely at our blueprint to see what we can do with this newly-created instance.

The first line of the definition is something I just habitually do: `var self = this;`. JavaScript has some weird [scoping issues][3] that this seems to resolve. We’ll use `self` to refer to the particular instance of our object that we’re currently working with. In some sense, it’s like the address of each house that we’ve created using our blueprint. Each house starts out the same, with empty cupboards and closets; each house quickly gets filled with tons and tons of distinct stuff. We might get confused about which house **our** stuff was in if it wasn’t for the street address that uniquely distinguishes my house from your house. In the same way, `self` provides a mechanism for referring to the object we’re currently working inside, so that our object definition can be nicely generic.

With `self` out of the way, let’s look at the next two groups of code. Each follows the same pattern:
    
    self.<NAME> = function(...) {
        // Function definition
    }
    

What we’re doing here is defining `methods` for our objects. These methods hang off our object, and can be executed by using the dot operator, like `anInstance.getValue()`. If you’ve used Java, this all makes perfect sense to you. If not, well, keep reading. :)

In this case, we’re creating two functions: `setValue`, which accepts a single argument, and assigns whatever value gets passed in to a local variable (more about that in a moment), and `getValue`, which simply returns the value that was previously set. The last little bit of code defines the local variable I mentioned a moment ago, and sets it’s initial value to 0. We’ll talk about these sorts of variables more in a later article, for the moment, let’s just say that this value is specific to the particular instance of MyObject that we’re working with. Some code might help:
    
    var anInstance      = new MyObject(); // Create an instance of our object.
    var anotherInstance = new MyObject(); // Create another, separate, instance.
    
    anInstance.setValue(1);      // Call the setValue method to set a value
    anotherInstance.setValue(2); // Ditto.
    
    alert(anInstance.getValue());      // This will pop up "1"
    alert(anotherInstance.getValue()); // This will pop up "2"

Hopefully that makes sense. If not, don’t worry. It’ll come up again in another article. 

So, with all that background out of the way, let’s actually address the topic that this article began with: How do we create modular components that don’t jump all over the names of other functions you might want to define? The answer’s probably obvious at this point. We create an object definition that contains our functions, and use that as our namespace. To use our example from yesterday, we might do something like:
    
    function ZebraTables() {
        var self = this;
    
        self.stripeTable = function (table) {
            // Throw the stripe table code in here
        }
    
        self.stripeAllTables = function () {
            // Throw the stripe all tables code in here, making sure to replace
            // the reference to `stripeTable` with `self.stripeTable`.
        }
    
        handleEvent(window, "load", self.stripeAllTables);
    }
    

This would create a ZebraTables object definition for us that wouldn’t pollute the global namespace, and could be easily included on any webpage we desired. One more change should probably be made (removing `handleEvent` from the global space, and making it a method of the `window` object), but it requires a discussion of prototypes that we’re just going to have to get to later.

An [example of this technique][4] is available. :)

   [1]: /2005/03/event-handlers-and-other-distractions
   [2]: http://www.crockford.com/javascript/javascript.html
   [3]: http://www.crockford.com/javascript/private.html
   [4]: /projects/files/EventHandler/objectOrientedEventHandlingExample.html


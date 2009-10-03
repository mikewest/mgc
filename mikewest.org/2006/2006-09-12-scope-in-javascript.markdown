---
Alias:
- http://mikewest.org/blog/id/32
Modified: '2006-09-12T08:30:04Z'
Teaser: My latest article for Digital Web, 'Scope In JavaScript', is up and waiting
    for you to read it.
layout: post
tags:
- JavaScript
- Digital-Web
title: Scope in JavaScript
---
I've got [a new article][scope] in the latest issue of [Digital Web][], diving deeply into JavaScript's concepts of scope and execution context.  

[Scope in JavaScript][scope] was originally an ode to the single most useful piece of the [Prototype framework][] -- the `bind` method.  I wanted to discuss in detail how `bind` makes it possible to have interesting and readable object-oriented code, while at the same time embracing event handlers and `setTimeout` to control your code's execution.  The issue is simply that event handlers execute your code in a context outside your objects, which makes the `this` keyword confusing at best, and flat-out wrong at worst.  `bind` is an elegant solution to the problem, and the article concludes with a deep dive into a simplified version of that function to tease out exactly what it does, and how it works.

I found, however, that the article was mostly incomprehensible to those without a firm grounding in the issues of scope and execution context, and the lesser-known ways of manipulating execution context (`apply` and `call`).  In an effort to give that audience something to sink their teeth into, I added a good amount of discussion of the basic concepts of scope, and what an execution context really means.  I hope I've struck a good balance between the two, and that the article builds a solid foundation as it goes.

If you're interested in this sort of thing, read [Scope in JavaScript][scope], and let me know what you think.  The comments should be interesting.  :)

[Digital Web]: http://digital-web.com/ "Digital Web Magazine"
[scope]: http://digital-web.com/articles/scope_in_javascript/ "Mike West: 'Scope in JavaScript'"
[Prototype framework]: http://prototype.conio.net/ "The Prototype JavaScript Framework"
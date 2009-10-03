---
Alias:
- http://mikewest.org/blog/id/24
Modified: '2006-07-11T07:00:10Z'
Teaser: I've got an article up on Digital Web, outlining the processes I use to build
    accessible UI controls for web applications.
layout: post
tags:
- Digital-Web
- JavaScript
title: Building Accessible Widgets for the Web
---
Building interfaces for web applications is hard work, and it's not made any easier by the dearth of [widgets][] available in modern browsers.  We've got the basics -- `SELECT` dropdowns, `INPUT` text boxes -- but native applications have a much wider selection of controls to choose from.  This lack can be mitigated with clever JavaScripting and CSS techniques; we can build them, we have the technology!

However, it's critical to ensure that we don't leave accessibility by the wayside when creating new UI controls for our applications.  I've got an article up on [Digital Web][digitalweb] that describes the basic guideline I adhere to when constructing widgets, cleverly entitled ["Building Accessible Widgets for the Web"][article].  I've put together a working combo-box as an example of the technique, and I'm looking forward to [your feedback][comment].

Something that I gloss over in [the article][article] is the decision-making process that leads up to building a new widget, and I want to address that here, since it's an important piece of the puzzle.  In short, _think about what you're doing_ when you decide to go with a custom piece of UI design.  [Garrett Dimon][garrett] argues that [customizing a form's look and feel might harm usability][custom_forms] by breaking user expectations, and I agree.  Before building a new widget, ensure it makes sense for your application.  Something like a combo-box is pretty straightforward, users deal with the model everyday in the address bar of their browser, but a weird [sliding widget][slider] might be pushing the limits a bit more.  Or, depending on your audience, the exact inverse might be true.  Make sure that usability is taken into account, along with accessibility, when you're souping up your forms.

[widgets]: http://en.wikipedia.org/wiki/Widget_%28computing%29 "Wikipedia: 'Widgets'"
[digitalweb]: http://digital-web.com/ "Digital Web Magazine: The web professional's online magazine of choice"
[article]: http://digital-web.com/articles/building_accessible_widgets_for_the_web/ "Digital Web Magazine: 'Building Accessible Widgets for the Web'"
[garrett]: http://www.garrettdimon.com/archives/front-end-architecture-browsers
[custom_forms]: http://www.garrettdimon.com/archives/front-end-architecture-browsers "Garrett Dimon: 'Front-End Architecture: Browsers'"
[slider]: http://mikewest.org/archive/slidable-select-widgets-explained "Mike West: 'Slidable Select Widgets Explained'"
[comment]: http://digital-web.com/articles/building_accessible_widgets_for_the_web/comments/ "Comment on the article"
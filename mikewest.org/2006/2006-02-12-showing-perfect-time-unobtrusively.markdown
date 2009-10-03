---
Alias:
- http://mikewest.org/blog/id/6
Modified: '2006-03-29T21:20:15Z'
Teaser: We can use JavaScript to deal with the nasty annoyance of displaying times
    in a user's local time-zone.
layout: post
tags:
- JavaScript
title: Showing Perfect Time (Unobtrusively)
---
Via [Simon Willison][1]'s [Blogmarks][2], I came across an interesting idea 
regarding the display of timestamps on web pages, and how the nasty annoyance of
time-zones can be dealt with in a fairly elegant manner.  In a nutshell, 
["Showing Perfect Time"][3] describes a method of displaying timestamps to 
visitors in the visitor's own time zone, using JavaScript to convert a 
seconds-since-the-GMT-epoch stamp into something pretty and localized.

[1]: http://simon.incutio.com/
[2]: http://simon.incutio.com/blogmarks/2006/01/16/
[3]: http://redhanded.hobix.com/inspect/showingPerfectTime.html

I love the idea, but the implementation doesn't work for me.  Importantly, it
relies on `<noscript>` to display times for users without JavaScript turned on
and `document.write` to dump out times for those who do.  I'm not a fan of this 
method, so I stood on [the author's][4] shoulders (who, by the way, was 
[standing on shoulders already][5]), and wrote my own version.

[4]: http://whytheluckystiff.net/
[5]: http://ecmanaut.blogspot.com/2006/01/ajax-date-time-time-zones-best.html

[PerfectTime.js][6] is a self-contained JavaScript class that runs `onload`, and
unobtrusively replaces the contents of a specially constructed `span` with a 
properly formatted timestamp.  The code on the webpage might look something like

    <span class='PerfectTime' gmt_time='1111396060'>3/21/2005 1:03 CST</span>

which I find to be more semantically meaningful, and accessible.  This article 
details the process, but if you'd like to skip ahead and play with the code 
yourself, [the PerfectTime JavaScript class][6] is available for download.

[6]: http://mikewest.org/projects/files/PerfectTime/PerfectTime.js

---

Writing this class begins in much the same way as the other classes I've written
about on this site.  We ought to map out what, exactly, we're trying to achieve
in order to give ourselves a clear goal to code towards.

The final goal is to take a GMT timestamp that's sitting in our database, and 
display it to the user in her own time-zone.  We know that her browser can make
this translation for us if she's using JavaScript, so we just have to figure out
a nice method of making that translation possible while at the same time
maintaining the semantic meaning of our page's markup, and providing an
alternative to those users visiting without JavaScript enabled.  To me, this
semantic HTML code looks like:

    <span class='PerfectTime' gmt_time='60'>Jan 1, 1970 00:01 GMT</span>

A `span` surrounds the time in some baseline acceptable format (e.g. whatever 
you're currently writing out), and has a custom attribute `gmt_time` that 
contains the seconds-since-epoch integer associated with that timestamp.

Without JavaScript, nothing more happens, and your users see the timestamp
in some specific time-zone.  With JavaScript enabled, we can take this a step
further, and dynamically replace the contents of this `span` with a timestamp
keyed off the user's local timezone.

The steps, therefore, are straightforward:

1. Find all the `spans` on the page of class `PerfectTime`.
2. Extract the GMT stamp from each `span`.
3. Translate each GMT stamp to a local timestamp.
4. Replace the content of each `span` with the new timestamp.

So, let's start coding.

We pick a name ("PerfectTime" sounds catchy) to distinguish this class from 
others we might use in the future, and create the package [as per usual][7]
aliasing `this` to avoid scoping issues, as per usual.

[7]: /2005/03/component-encapsulation-using-object-oriented-javascript

    function PerfectTime() {
        var self = this;

        ...

        self.instantiate = function () {
           var spans = document.getElementsByTagName('span');
           for (i=0, numSpans=spans.length; i < numSpans; i++) {
               if (spans[i].className.match(/PerfectTime/)) {
                   self.processSpan(spans[i]);
               }
           }
        }
        
        ...
        
        handleEvent(window, 'load', self.instantiate);
    }

We're looking for all the `spans` on the page with a `className` of
"PerfectTime", and calling a method called (astoundingly enough) `processSpan`
on each one.  That's where we'll make the magic happen.  As it turns out, that
magic is quite straightforward:

        self.processSpan = function (theSpan) {
            var GMT = parseInt(theSpan.getAttribute('gmt_time')) * 1000;
            var newDate = new Date(GMT);
            theSpan.innerHTML = self.strftime(newDate);
        }
    
So, what's going on in these three lines?  

The first line grabs the `gmt_time` attribute off the `span`, and turns it into
an integer using `parseInt` (because the `getAttribute` method _always_ returns
a string).  We also have to multiply this number by 1000 to account for the fact
that JavaScript's `Date` object expects microseconds as opposed to seconds.  

The second line creates our `Date` object, and populates it with our GMT stamp.

The third line calls a method called `strftime` to translate the GMT timestamp
into a localized timestamp, and sticks that information into our `span`'s 
`innerHTML`.  We've taken care, therefore, of steps #1, #2, and #4.  
`strftime()` handles the heavy lifting in #3.

`strftime()` is based upon [whytheluckystiff][3]'s reworking of 
[Johan Sundström's][8]'s clever [`formatTime` method][5].  I've simply moved the
code around so that it fits into our self-contained environment.  The function
takes a `Date` object as it's only argument, and returns the properly formatted
time string just as it would have been returned from any other `strftime()`
implementation (say, [PHP's `strftime`][9], which happens to have nicely
available documentation).  The formatting string is set when the class is 
instantiated with the following code:

[8]: http://ecmanaut.blogspot.com
[9]: http://php.net/strftime


    self.defaultFormat = '%d %b %Y at %H:%M';
    self.format        = (arguments[0])?arguments[0]:self.defaultFormat;
                

We use the `arguments` array of the constructor to determine if a formatting
string was passed in.  If one exists, we use it.  If not, we use the default
format string.

And that's it.  Simple, eh?

I've set up an example proof-of-concept PHP script that writes out various Unix
timestamps (in fact, the timestamps of each and every blog post on mikewest.org)
that will hopefully make the process clear.

The demo is [PerfectTimeDemo.php][10].
The PHP source code for the example is [PerfectTimeDemo.phps][11].
The JavaScript class is [PerfectTime.js][6].

[10]: http://mikewest.org/projects/files/PerfectTime/PerfectTimeDemo.php
[11]: http://mikewest.org/projects/files/PerfectTime/PerfectTimeDemo.phps
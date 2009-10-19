---
layout:     post
title:      "Asynchronous Execution, JavaScript, and You"
slug:       "asynchronous-execution-javascript-and-you"
aliases:
    - http://blog.mikewest.org/post/103860287
    - http://blog.mikewest.org/post/103860287/asynchronous-execution-javascript-and-you
tags: 
    - asynchronous
    - javascript
    - jquery
    - code
    - webdev
    - süddeutsche
Teaser:    "I spent more time than I care to admit this afternoon tracking down a bug in some relatively straightforward jQuery code.  As it turned out, I was overlooking my error because I was thinking about my code in absolutely the wrong way."
---
I spent more time than I care to admit this afternoon tracking down a bug in
some relatively straightforward jQuery code.  As it turned out, I was
overlooking my error because I was thinking about my code in absolutely the
wrong way.  Here's more or less what I was trying to do:

Given a long list of thumbnails, I want to display only the first few, while
giving the user the ability to page through the rest at will.  The markup for
the list is simple, something like:

    <ul class="thumbnails">
        <li><a href="#ARTICLE"><img src="#PHOTO" alt="#ALT"></a></li>
        <li><a href="#ARTICLE"><img src="#PHOTO" alt="#ALT"></a></li>
        ...
        <li><a href="#ARTICLE"><img src="#PHOTO" alt="#ALT"></a></li>
        <li><a href="#ARTICLE"><img src="#PHOTO" alt="#ALT"></a></li>
    </ul>

My initial stab at it went something like:

    var speed = 200,
        inc   = 50;
        
    $.getJSON( [JSON TARGET], [AND OPTIONS HERE], function callback( json ) {
      if ( json.data ) {
        var current   = 0,
            list      = $( '#thumbnails' ),
            elements  = list.children( 'li' );
            
        elements.each( function () {
            var el = $( this );
            el.fadeOut( speed, function () {
              if ( current < json.data.length ) {
                var new_thumbnail = [ GENERATE THUMBNAIL HTML SOMEHOW ];
                el.replaceWith( new_thumbnail );
                list.find( ':hidden' ).fadeIn( speed );
                current += 1;
              } else {
                el.remove();
              }
            } );
            speed += inc;
        } );
      }
    });

I grab some JSON data to populate the remainder of the list, then loop through
all the `li` elements, fading each one out, replacing it with a new thumbnail,
and fading the new element in.  For each element, I bump the `speed` up a bit
to fade each element after the previous, rather than fading them all out at
once.

This worked pretty well, but I ran into a case I didn't consider: my code
assumes that the next "page" of thumbnails will always be the same size as the
current page, or smaller.  That assumption turned out to be incorrect.  I
need to adjust the code to handle datasets larger than the number of `li`
elements that I start out with.

I thought that'd be a simple task.  I have `current` populated with the last
new thumbnail I processed, so I'd just write a simple loop to append the
remaining items to the end of the list, fade them in, and be done with it:

    ...
    $.getJSON( [JSON TARGET], [AND OPTIONS HERE], function callback( json ) {
      if ( json.data ) {
        var current   = 0,
            list      = $( '#thumbnails' ),
            elements  = list.children( 'li' );
            
        elements.each( function () {
            var el = $( this );
            el.fadeOut( speed, function () {
              ...
            }
            speed += inc;
        } );
        while ( current < json.videos.length ) {
            var thumb = [ GENERATE THUMBNAIL HERE ];
            list.append( thumb ).find(':hidden').fadeIn( speed );
            current += 1;
            speed   += speed_inc;
        }
      }
    });
    
Easy, right?  Not really.  The behavior this code produced was very odd.  It
seemed like everything got appended all at once, and faded in together.  If
you're cleverer than I, you probably already see what I did wrong.

In short: I looked at the `each` block, and thought "Hey!  A loop!"  I
overlooked the fact that the `fadeOut` bit contained a _callback_, and that
this callback executed _after `speed` milliseconds_.  It was a block of
asynchrony, sitting in the middle of my otherwise linear code.

Since I only incremented `current` when the `fadeOut` completed, the browser
started a series of fades, then continued on to the `while` and ran through it
before any of the fades had actually finished.  This, naturally, screwed up my
otherwise lovely plan.

The solution I'm running with at the moment is this:

    ...
    $.getJSON( [JSON TARGET], [AND OPTIONS HERE], function callback( json ) {
      if ( json.data ) {
        var current   = 0,
            list      = $( '#thumbnails' ),
            elements  = list.children( 'li' );
            
        elements.each( function () {
            var el = $( this );
            el.fadeOut( speed, function () {
              ...
              if ( current >= elements.length ) {
                while ( current < json.videos.length ) {
                    var thumb = [ GENERATE THUMBNAIL HERE ];
                    list.append( thumb ).find(':hidden').fadeIn( speed );
                    current += 1;
                    speed   += speed_inc;
                }
              }
            }
            speed += inc;
        } );
      }
    });
    
Moving the `while` inside the callback, and only executing it if I've just
finished processing the final `li`, injects a bit of linearity into an
otherwise asynchronous process.  I can guarantee that this code is always
going to execute _after_ all the fading is complete, solving my problem, and
producing a pretty nice effect (which I'll be able to point to in a week or
two when the page I'm working on goes live.  Hooray for projects...)

This is the solution I've come up with, but I'm still pretty new to jQuery.
Are there shortcuts I've missed?

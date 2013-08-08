---
layout: post
title: "Debugging runtime errors with 'window.onerror' in Blink"
tags:
  - error
  - exception
  - javascript
  - blink
  - onerror
  - windowonerror

Teaser:
  "After working with Blink's implementation of `window.onerror` a little bit
   over the last week or so, I'm somewhat amazed that anyone ever used it for
   anything at all. Happily, we've made some big improvements in the last week
   or two that I think it's worth highlighting here."
---
After working with Blink's implementation of `window.onerror` a little bit
over the last week or so, I'm somewhat amazed that anyone ever used it for
anything at all. For those of you to whom the API is news, the current
implementation in Chrome's stable channel (28) looks a little bit like this:

    window.onerror = function (message, filename, lineno) {
        // Do some centralized error reporting here, for example, by POSTing
        // the error message, filename, and line number to a collection
        // server for later processing.
  
        return true; // The exception is handled, not reported to the user.
    };

    ...

    throw new Error('OMG!');

'window.onerror' acts something like a global try/catch block, allowing you
to gracefully handle uncaught exceptions you didn't expect to see. This, in
theory, is brilliant.

Two issues have made it less than brilliant in practice:

1.  Unlike a local try/catch block, the `window.onerror` handler doesn't have
    direct access to the exception object, and is executed in the global
    context rather than locally where the error occurred. That means that
    developers don't have access to a call stack, and can't build a call stack
    themselves by walking up the chain of a method's callers.

2.  Browsers go to great lengths to sanitize the data provided to the handler
    in order to prevent unintentional data leakage from cross-origin scripts.
    If you host your JavaScript on a CDN (as you ought), you'll get "Script
    error.", "", and 0 in the above handler. That's not particularly helpful.

There are a few other concerns, but those are the big two. I'm happy to say
that recent patches have addressed many of the concerns in Blink.

1.  Christophe Dumez [added the column number to the handler][1].

2.  After a lot of back-and-forth, Hixie [added an 'error' parameter to the
    `onerror` handler in the WHATWG spec][2]. This, as you might imagine,
    contains the exception that was thrown, just as you'd get in a `catch`
    block. The [Blink implementation landed last week][3], which means that you
    can now access the stack trace in your handler via something like the
    following:

        window.onerror = function (message, filename, lineno, colno, error) {
            console.log("This is a stack trace! Wow! --> %s", error.stack);
        };
    
3.  Blink [now follows][4] Mozilla's and WebKit's practice of enabling full
    detail in exceptions generated from cross-origin scripts that are served
    with proper access-control headers and attributes. If you add a
    `crossorigin` attribute to a `script` tag, and serve that script with an
    `Access-Control-Allow-Origin` header that allows access to the document
    loading the script, then you'll be given unsanitized data in your error
    handlers. That might look something like this:

        <script crossorigin="anonymous" src="http://cdn.example.com/script.js"></script>

    Note that this is a bit tricky: you'll need to make quite sure that your
    server is properly configured. If a script has a `crossorigin` attribute
    but the server doesn't send appropriate CORS headers, the script load
    will fail miserably.

4.  [Stringification of custom errors is (slightly) improved][5] for the case
    where an Error object is directly set as the prototype of your custom
    error. Handlebars, for instance, created a `Handlebars.Exception` object
    with code like this:

        Handlebars.Exception.prototype = new Error();

    V8 didn't support that very well in `window.onerror`: the stringification
    looked something like `[object Object]`, which wasn't particularly useful
    for anyone. Now you'll get the expected message, as long as you haven't
    overridden the `toString` method.

5.  I'm still knee-deep in the Worker implementation, which is a bit of mess
    really. I expect to [fix the sanitization][6] shortly, and I think it
    shouldn't be too difficult to [add the `error` property to the Worker's
    `onerror` handler][7].

I think this set of changes will make centralized error reporting a bit more
realisticly possible in the near future. I'd love for you folks to start
banging on these initial implementations now so that I can fix bugs and clean
up edge-cases now, before these start rolling into Stable. When you see a bug
please do file it at <http://crbug.com/new>, and ping me the bug ID
([+Mike West][gplus], [@mikewest][twitter], or <mkwst@chromium.org>).

Enjoy Blink's newly more-usable error reporting!

[1]: http://crbug.com/264197
[2]: http://html5.org/r/8086
[3]: http://crbug.com/147127
[4]: http://crbug.com/159566
[5]: https://code.google.com/p/v8/issues/detail?id=2822
[6]: http://crbug.com/269538
[7]: http://crbug.com/270005

[gplus]: https://google.com/+MikeWest
[twitter]: https://twitter.com/mikewest

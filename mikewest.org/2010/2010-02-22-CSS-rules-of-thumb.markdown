---
layout: post
title:  CSS Rules of Thumb
Teaser: "Apropos of nothing, a few CSS tips that have nothing to do with browser incompatibilities, and everything to do with your own sanity when dealing with code you've written."
tags:
    - CSS
    - webdev
    - stylesheets
    - howto
    - styleguide
    - documentation
    - webdevelopment
    - sanity
    - oocss
---
Apropos of nothing, a few CSS tips that have nothing to do with browser
incompatibilities, and everything to do with your own sanity when dealing
with code you've written:

## Comment your CSS files ##

This is incredibly basic advice that I don't think is taken at all seriously
enough.  I've made an effort over the last few months to begin every CSS file
I write with a comment block that looks something like:

    /**
     *  Title of the CSS file
     *
     *  A Brief description of the CSS file's contents, and, if
     *  relevant, it's dependencies.  This should generally only
     *  be a sentence or three long, anything more, and the file's
     *  almost certainly attempting to do too much.
     *
     *  <pre><code>
     *      <div class="the markup this css file expects">
     *          You'll be ever so happy you included this part
     *          in about three months, when you come back to this
     *          project, having completely forgotten it's
     *          structure and purpose.
     *      </div>
     *  </code></pre>
     *
     *  @author     Mike West <mike@mikewest.org>
     *  @package    some_greppable_name
     */

This is the basis upon which you can start writing reasonable CSS rules that
you have a good chance of understanding the next time you read them.
Especially the expected markup.  You may think that's overly verbose, and
simply overkill for most projects, but without it, you'll get lost when trying
to map the file's CSS to anything at all on the actual website you're coding.

It's important to put as much context into the CSS file as possible, because
CSS is a complex language when you use it the way you're supposed to. The more
you rely on the cascade to reuse code and concepts, the more you'll come to
rely on good documentation to keep your bearings.

## Write many, highly specialized CSS files ##

The general rule of thumb about documenting your code has a corollary: __you
should use _lots_ of CSS files__.  You should be able to pick up a small,
focused chunk of code, read through it, and understand more or less how it
fits into the site as a whole.  If it depends on some other chunk of code,
that code should be referenced, but not included in the same file.  Here's
why: long CSS files are opaque, confused, and unstructured.  I don't care how
disciplined you are: this is true 100% of the time, without fail.

If you find yourself sifting through a CSS file, trying to figure out where
best to stick a new bit of code, you're simply doing it wrong. The fewer
CSS files you have, the larger they'll be, and the more tempted you'll be
to simply stick some new rules on the end to save time.  You'll do this
because your teammates are doing it, and they'll do it because you're doing
it. This is the path to poor code quality, poor code reuse, and simple
insanity.

In short, I see long CSS files as the [broken windows][] of web development.
The longer and more convoluted the file, the more likely even the best 
developers are to simply make it more confused.

[broken windows]: http://en.wikipedia.org/wiki/Fixing_Broken_Windows

## Name your files well ##

To whatever extent possible, you should develop a naming convention to make a
file's purpose clear, minimizing the chance that you'll have to go looking for
a good home for new code.

For example, on my current project, I've written a lot of modules that are all
based upon the same root class.  The markup might look like:

    <div class="basebox">
        [Module basics go here]
    </div>

    <div class="basebox special">
        [Module basics, plus "special" markup go here]
    </div>

`basebox.css` defines the presentation of the features common to all
"Basebox" style modules.  In that file's documentation block, I'd define a
`@package` of "projectname_basebox".  The "special" presentation is then
defined in `basebox_special.css`, with a `@package` of
"projectname_basebox_special".  The filename makes dependencies clear when
determining import order, and the `@package` marker makes dependencies clear
inside the file (and available to `grep`).

## Style guides are good ##

You should organize a style guide for your team, and stick to it.  As with
any language, it's helpful when your whole team speaks the same dialect.
Insofar as that's true, I think it's more important that you agree on _a_ set
of rules defining how you write CSS, rather than _my_ set of rules. The more
your CSS looks like your neighbors, the more likely she is to understand your
rules quickly when she needs to change them (and the more likely _you_ are to
understand rules you wrote months ago...).

That said, you should of course all write CSS like I do.  Because it's the
right way.  Here's how and why:

*   Selectors are to be written in order of specificity, and nested
    according to the site's markup.  Given a `basebox` module:

        <div class="basebox">
            <div class="header"></div>
            <div class="body"></div>
            <div class="footer"></div>
        </div>

    I'd expect to see CSS code that looked something like:

        .basebox {
            /* Properties go here */
        }
            .basebox .header {
                /* Properties go here */
            }
            .basebox .body {
                /* Properties go here */
            }
            .basebox .footer {
                /* Properties go here */
            }

    I'd argue for this format for the same reasons that indenting a "real"
    programming language makes sense: it's easier to understand a file's
    scope when selectors are nested (this, incidentally, is another reason
    that multiple CSS files are beneficial: each file's "scope" begins
    anew at the left-hand column).

    This also operates on the principle of least surprise.  I expect to see
    the most general rules first, and to work towards more specific rules at
    the bottom of the file.  I think most developers would agree.

*   Properties are written _one per line_.  Period.  I consider this
    self-evident, and I'm always shocked when otherwise intelligent people
    argue with me about it.  Writing properties one per line has two
    distinct advantages:

    1.  Selectors with more than two or three properties don't require
        horizontal scrolling.  Nor do they require maintaining a parse
        tree in your head while reading code.

        To make this point more clearly, I'll cherry-pick a horrid example
        out of [Nicole's OOCSS][horrid] (Hi, [Nicole][]!  Sorry I'm picking on
        you! :) ):

            /* This is unreadable */
            .lastUnit{display:table-cell;float:none;width:auto;*display:block;*zoom:1;_position:relative;_left:-3px;_margin-right:-3px;} 

            /* This is less so */
            .lastUnit {
                display:        table-cell;
                float:          none;
                width:          auto;
                *display:       block;
                *zoom:          1;
                _position:      relative;
                _left:          -3px;
                _margin-right:  3px;
            }


    2.  Properties written on more than one line make version control
        (which generally operates with line-based `diff` presentation)
        much more user friendly.  If I ever had to resolve conflicts in
        a file with 100+ character lines, I think I'd simply rewrite the
        rule rather than spend the time to figure things out.

    All that said, I do find single-line rulesets acceptable (and, in fact, 
    preferable) when writing long runs of single-rule groups.  Sprite 
    definitions are the canonical example.  It simply makes sense to write 
    code like:

        .sprited li {
            background: url(/path/to/sprite.png) no-repeat 0 0;
        }
            .sprited .s1 { background-position: 0 -20px; }
            .sprited .s2 { background-position: 0 -40px; }
            .sprited .s3 { background-position: 0 -60px; }
            .sprited .s4 { background-position: 0 -80px; }

*   Properties are formatted for readability using 4-space tab stops.
    Readability improves when the eye has a clean line to jump to.  Again
    using Nicole's code as an example, would you rather read this:

        .lastUnit {
            display: table-cell;
            float: none;
            width: auto;
            *display: block;
            *zoom: 1;
            _position: relative;
            _left: -3px;
            _margin-right: 3px;
        }
    
    Or this:
    
        .lastUnit {
            display:        table-cell;
            float:          none;
            width:          auto;
            *display:       block;
            *zoom:          1;
            _position:      relative;
            _left:          -3px;
            _margin-right:  3px;
        }

    I don't think it's much of a contest.

*   Properties are written in alphabetical order.  This also helps keep
    diffs sane, as you no longer get into fights about which rules should
    be written together.

*   Browser hacks are inline, and documented.  Taking Nicole's example above,
    I'd expect to see (at least) two comment blocks, explaining the rationale
    behind the various IE hacks:
    
        .lastUnit {
            display:        table-cell;
            float:          none;
            width:          auto;
        
            /**
             *  @HACK:  Giving `haslayout` to IE 6 and 7 via the
             *          `zoom` and the star hack.
             */
            *display:       block;
            *zoom:          1;
        
            /**
             *  @HACK:  Something IE6 specific that I don't understand
             *          because it wasn't documented.  Maybe it's in a
             *          wiki somewhere?  Who knows.  Danger!
             */
            _position:      relative;
            _left:          -3px;
            _margin-right:  3px;
        }
    
    This is, of course, more verbose, and will take up some of your valuable
    time.  I don't care.  Write the comments anyway.  You'll need them later
    on when you've forgotten why you wrote them.  Labeling your hacks makes
    you think about and justify them, and makes them simple to remove when
    you decide to stop supporting broken browsers.

[horrid]: http://github.com/stubbornella/oocss/blob/master/core/grid/grids.css
[nicole]: http://www.stubbornella.org/content/

## Write code for human consumption ##

Your code should first and foremost be human-readable.  Of course you want to
deliver a single [combined][] and [minified][] CSS file to the browser, and of
course that means that you'll have to do some work to transform the nicely
readable code you've written into something lean and mean for performance and
efficiency (a good place to start would be [Tim Huegdon's][tim] article
"[Website Builds Using Make][make]").  

So don't worry about the performance penalties to writing long comments,
detailing every tricky piece of your CSS.  And don't worry about the
performance penalties of splitting your code into many easily understood
chunks.  There aren't any.  Your build process will combine all your files,
and compress them into a single file that's completely incomprehensible to
human eyes.  This is a purely mechanical act, and it's something that should
be scripted.  Your concern when writing code should be _your_ understanding
of that code, not the browser's.

[combined]: http://developer.yahoo.com/performance/rules.html#num_http
[minified]: http://developer.yahoo.com/performance/rules.html#minify
[tim]:      http://timhuegdon.com/
[make]:     http://nefariousdesigns.co.uk/archive/2010/02/website-builds-using-make/

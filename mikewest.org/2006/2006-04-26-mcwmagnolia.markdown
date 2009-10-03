---
Alias:
- http://mikewest.org/blog/id/13
Modified: '2006-06-17T15:41:46Z'
Teaser: '`mcw_ma_gnolia` is a TextPattern plugin that generates a customizable Ma.gnolia
    link roll for use on your website.'
layout: post
tags:
- TextPattern
title: mcw_ma_gnolia
---
`mcw_ma_gnolia` is a TextPattern plugin that generates a customizable Ma.gnolia link roll for use on your website.  [Download it now][download], and start playing! 

__Updated 17. June, 2006:__ [Version _0.4_][download] is out, tweaking the plugin to work with Ma.gnolia's new linkroll JavaScript.  This, of course, is a good reason to start working on something that actually uses the Ma.gnolia API instead of parsing through a linkroll JavaScript file.  I'll be starting on that soon.

__Updated 26. April, 2006:__ Version _0.3_ is out, adding the ability to filter the links in your linkroll by a specific tag, and changing the link retrieval mechanism so that it functions correctly on more servers.

__Updated 25. April, 2006:__ Version _0.2_ is out, and corrects a small bug with the `mcw_ma_gnolia_uri` tag.

## What is it? ##

[Ma.gnolia][mag] is a social bookmarking site (somewhat like [del.icio.us][del]) that I use to keep track of interesting websites I come across.  It provides the built in ability to display your most recent bookmarks on your personal website (a 'link roll'), but I don't like the mechanism it uses to make that happen.

[Ma.gnolia][mag] provides you with a JavaScript file that uses `document.write` to dump the link roll to your site.  This works, but it's not exactly accessible, nor is it very flexible.  `mcw_ma_gnolia` leverages this built-in mechanism to provide what I hope is an extremely flexible and accessible link roll without the use of client-side JavaScript.

In a nutshell, the plugin downloads and caches the JavaScript file server-side on a quasi-hourly basis, extracts the link information, and makes the data available for you via a series of TextPattern tags that you can use in your `forms` and `pages`.

## How Do I Use `mcw_ma_gnolia`? (e.g. quickstart) ##

Start by [downloading the plugin][download] and installing it like you would any other.  Once you've gotten the plugin installed, `edit` it, and enter your ma.gnolia username and the number of links you'd like displayed into the public config section of the PHP code (should be lines 6 and 7 or so).  If you don't do this, you'll be seeing my links.  That's a fine way to test, but you'll probably want to make this change before you go live.

Next, click on the `extensions` tab, and then on the `Ma.gnolia Linkroll` subtab.  Hitting this page will automatically create a `form` called `mcw_ma_gnolia`, and offer you the opportunity to force-update your cached ma.gnolia links.  Go ahead and hit that button now to speed things up later.

Finally, edit a `page` to include the `<txp:mcw_ma_gnolia />` tag.  Viola, ma.gnolia links on your page.  Astounding!

## How do I configure the output? ##

Excellent question.  Here's brief documentation of each of the tags this plugin enables:

*   `txp:mcw_ma_gnolia` -- The `mcw_ma_gnolia` tag is a _single tag_ that gets
    replaced with the Link Roll.  It can be included on a `page` directly, or
    as part of a `form` that's displayed on a page.
    
    Attributes:    
    *   `form` -- this specifies the `form` to be used for each of the
        displayed links.  Defaults to `mcw_ma_gnolia`.
    *   `wrap_tag` -- specifies the block-level tag to wrap the links.
        Defaults to `ul`.
    *   `class` -- applies a CSS class to the block-level tag specified
         in the `wrap_tag` attribute.

*   `txp:mcw_ma_gnolia_uri` -- The `mcw_ma_gnolia_uri` tag is a _single tag_
    that gets replaced with a link's URI (the actual address of the link).
*   `txp:mcw_ma_gnolia_link` -- The `mcw_ma_gnolia_link` tag is a _single tag_
    that gets replaced with a link's ma.gnolia redirect (e.g. `http://ma.gnolia.com/bookmarks/bupuxeseq/dispatch`)
*   `txp:mcw_ma_gnolia_title` -- The `mcw_ma_gnolia_title` tag is a _single
    tag_ that gets replaced with a link's title.
*   `txp:mcw_ma_gnolia_desc` -- The `mcw_ma_gnolia_desc` tag is a _single tag_
    that gets replaced with a link's description.

Example page:

    Page: default
    
    ...
        <div id='ma_gnolia_linkroll'>
            <h2>My Recent Bookmarks</h2>
            <txp:mcw_ma_gnolia
                form='mcw_ma_gnolia'
                wrap_tag='ol'
                class='ma_gnolia_list'
            />
        </div>
    ...
    
Example form:

    Form: mcw_ma_gnolia
    
    <li>
        <a 
            href='<txp:mcw_ma_gnolia_link />'
            title='<txp:mcw_ma_gnolia_title />'
        ><txp:mcw_ma_gnolia_title /></a> - <txp:mcw_ma_gnolia_desc />
    </li>
    
Would produce:

    <div id='ma_gnolia_linkroll'>
        <h2>My Recent Bookmarks</h2>
        <ol class='ma_gnolia_list'>
            <li>
                <a 
                    href='LINK_GO_HERE'
                    title='TITLE_GO_HERE'
                >TITLE_GO_HERE</a> - DESCRIPTION GO HERE
            </li>
            ...
            <li>
                <a 
                    href='LINK_GO_HERE'
                    title='TITLE_GO_HERE'
                >TITLE_GO_HERE</a> - DESCRIPTION GO HERE
            </li>
        </ol>
    </div>
    
Nice, eh?

[mag]: http://ma.gnolia.com     "ma.gnolia.com: a social bookmarking site"
[del]: http://del.icio.us       "del.icio.us: a social bookmarking site"
[download]: http://mikewest.org/file_download/8 "`mcw_ma_gnolia` download"
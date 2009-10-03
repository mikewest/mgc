---
Alias:
- http://mikewest.org/blog/id/1
Modified: '2006-03-31T20:26:59Z'
Teaser: The PerfectTime JavaScript class gets updated to support the hCalendar format.
layout: post
tags:
- JavaScript
title: 'Son of PerfectTime: The Validationator!'
---
By far, the biggest bit of feedback I've gotten on ["Showing Perfect Time"][1] is the glaringly invalid attribute (`gmt_time`) in the structure I chose to use (from [Johan Sundström][2], for example).  I don't think that the attribute by itself is a huge deal, and [Peter-Paul Koch][3] makes [a convincing argument][4] for that position at [A List Apart][5].

[1]: /2006/02/showing-perfect-time-unobtrusively
[2]: http://ecmanaut.blogspot.com/2006/01/ajax-date-time-time-zones-best.html#c113978133722812093
[3]: http://www.quirksmode.org/
[4]: http://alistapart.com/articles/scripttriggers/ "JavaScript Triggers"
[5]: http://alistapart.com/

However, [Daniel Morrison][6] points out that the display of dates on webpages is already more or less a solved problem.  [hCalendar][7] is a [microformat][8] used by blogs all over the place to display dates and times, and there's absolutely no good reason why I should try to invent a new format rather than using one already in the wild.

[6]: http://ifstatement.blogspot.com/
[7]: http://microformats.org/wiki/hcalendar#Example
[8]: http://microformats.org/

I've rewritten [PerfectTime.js][9] to support the [hCalendar][7] format ([an updated PHP-driven demo][10] is also avaliable), and I'll describe the changes in the remainder of this article.

[9]: /projects/files/PerfectTime/PerfectTime.js
[10]: /projects/files/PerfectTime/PerfectTimeDemo.php

The [hCalendar][7] format uses an `abbr` tag to display dates and times.  The date is machine-readable in the tag's `title` attribute, while the element's contents are human-readable.  For example:

    <abbr title="2005-10-08">October 8th, 2005</abbr>
    
Or, for slightly more complexity:

    <abbr title="19721128T115524-0800">Tue, 28 Nov 1972 11:55:24 -0800</abbr>
    
The `title` attribute is encoded according to [ISO 8601][11], while the human readable contents can be formatted however you like.  I've modified the original PerfectTime class to support this format, with the following caveats:

[11]: http://en.wikipedia.org/wiki/ISO_8601

1.  The script only attempts to modify `abbr` elements of class `PerfectTime`.
    If you want your beginning and ending [hCalendar][7] times to be localized,
    you'll have to set them as something like:
    
        <abbr class='dtend *PerfectTime*' title='...'>...</abbr>

2.  ISO 8601 is not completely supported.  Specifically, the formats accepted 
    by this script are the following:

        YYYY
        YYYY-MM
        YYYY-MM-DD
        YYYY-MM-DDTHH:MM
        YYYY-MM-DDTHH:MM[+-]HHMM
        YYYY-MM-DDTHH:MM:SS.sZ
        YYYY-MM-DDTHH:MM:SS
        YYYY-MM-DDTHH:MM:SS.s
        YYYY-MM-DDTHH:MM:SS.s[+-]HHMM    
        YYYY-MM-DDTHH:MM:SS.sZ

    Additionally, the hyphens seperating the date components and the colons
    seperating the time components are optional.  For example, "March 22, 2006 
    at 12:00 CET (+0100)" could be written as any of:
    
        2006-03-22T12:00+0100        
        20060322T12:00+0100        
        2006-03-22T1100Z
    
    All of those point to the exact same minute in time.

3.  The script does not (yet) support the 'week dates' (YYYY-Www-D) or 'ordinal
    dates' (YYYY-DDD) formats.  This probably won't be a problem for most usages
    since my impression is that a script like this will likely be used for hours
    and minutes much more than for specific days.

The piece of the script that parses [ISO 8601][11] timestamps is based on [Paul Sowden's parser][12].  I've modified it to fit into the self-contained JavaScript class we're looking at here, to make the colons and hyphens optional, and to reuse a single `RegEx` object instead of creating a new one on every parse.  

[12]: http://delete.me.uk/2005/03/iso8601.html

To verify that the methods are giving the same times, I modified the [the PerfectTime demo page][10] to generate 10 random timestamps between 1970 and 2010, and output both the `span` and `abbr` formats.  It looks like it's working pretty well for me on Firefox, but I don't have access to a windows machine right now, so I've no idea if it's working correctly there.  I'd love it if someone would bang on that for me and let me know how it goes.

With that said, [PerfectTime 1.1][9] is ready for you to run away with.
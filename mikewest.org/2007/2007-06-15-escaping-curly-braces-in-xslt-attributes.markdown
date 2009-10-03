---
Alias:
- http://mikewest.org/blog/id/72
Modified: '2007-06-15T12:54:54Z'
Teaser: Curly braces in the attributes of XSLT document's elements are interpreted
    as XPATH expressions to be evaluated.  This sometimes causes problems...
layout: post
tags:
- JavaScript
- Yahoo
title: Escaping Curly Braces in XSLT Attributes
---
For future reference:

Curly braces in the attributes of XSLT document's elements are interpreted as XPATH expressions to be evaluated.  This, generally, is fine: I like shortcuts.  I don't, however, like them when they interfere with my ability to embed JavaScript hacks into a document.

You may be thinking to yourself: "Mike, you shouldn't embed JavaScript into an element's attributes!  That's simply idiotic!"  You'd be right, of course.  But assume for the moment that I had a good reason for doing it (in this particular case, the link simply doesn't work at all without JavaScript.  which is also bad.  but something I can't do anything about right now.  don't do this at home, kids.).  In that obscure case, I'd need to remember to set the attribute via the magical `<xsl:attribute>` element.  

    <a>
        <xsl:attribute name="href">
            http://curlyquotes.com/i/can/use/{/and/}/yay!/
        </xsl:attribute>
    </a>

Now you know.  And now I'll be able to look this up in a few weeks when I have no idea what my code's doing.  :)

Also: I hate XSLT.
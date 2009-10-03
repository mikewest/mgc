---
Alias:
- http://mikewest.org/blog/id/48
Modified: '2007-01-21T00:46:45Z'
Teaser: This site is built on top of the Textpattern engine, running Markdown instead
    of Textile.  Here's how to make that happen.
layout: post
tags:
- HOWTO
- TextPattern
title: Installing Textpattern 4.0.4 with Markdown
---
[Textpattern][] is a brilliant blogging tool, one which seems completely
dedicated to the task of putting words on a page.  It has a great plugin
structure, and in in practically every respect _the_ blogging tool I'd
recommend above all others.  

The one place where it fails remarkably to exceed my expectations is it's
single-minded dedication to Dean Allen's [Textile][] format.  I don't
particularly _like_ Textile, you see.  I simply get too hung up on the
formatting.  [Markdown][] (in combination with [SmartyPants][]), on the other
hand, is a lightweight markup language I can really get behind.  It feels like
it just gets out of my way, and lets me write without thinking about the 
rendering framework.

Happily, Michel Fortin's [PHP port][php] of the language has the ingenious
ability to _pretend_ to be Textile, so it can serve as a drop-in replacement
in programs like [Textpattern][].  So if you'd like to get a clean copy of
Textpattern 4.0.4 running Markdown, just copy and paste the following
commands.  You'll end up with a clean install in `~/src/`, ready for you to
start playing with.

    mkdir ~/src
    cd ~/src
    #
    #   GET PHP MARKDOWN
    #
    curl -O http://www.michelf.com/docs/projets/php-markdown-extra-1.1.1.zip
    unzip php-markdown-extra-1.1.1.zip 'PHP Markdown Extra 1.1.1/markdown.php'
    rm php-markdown-extra-1.1.1.zip
    mv 'PHP Markdown Extra 1.1.1/markdown.php' ./classTextile.php
    rm -rf 'PHP Markdown Extra 1.1.1'
    #
    #   GET SMARTYPANTS
    #
    curl -O http://www.michelf.com/docs/projets/php-smartypants-typographer-1.0.zip
    unzip php-smartypants-typographer-1.0.zip 'PHP SmartyPants Typographer 1.0/smartypants.php'
    rm php-smartypants-typographer-1.0.zip
    mv 'PHP SmartyPants Typographer 1.0/smartypants.php' ./smartypants.php
    rm -rf 'PHP SmartyPants Typographer 1.0'
    #
    #   GET TEXTPATTERN FROM SVN
    #
    svn export --force http://svn.textpattern.com/releases/4.0.4/source/ .
    #
    #   INSTALL MARKDOWN AND SMARTYPANTS
    #
    mv classTextile.php ./textpattern/lib/classTextile.php
    mv smartypants.php ./textpattern/lib/smartypants.php
    #
    #   FIX SMALL BUG IN PHP MARKDOWN EXTRA'S TEXTILE EMULATION
    #
    NICE="\$new = 'function TextileRestricted(\$text, \$lite, \$encode) { return \$this->TextileThis(\$text, \$lite, \$encode); }';if (/function blockLite/) { \$_ = \$_.\"\\t\\t\".\$new.\"\\n\"; }";
    perl -pi.bak -e "$NICE" classTextile.php;
    #
    #    SUCCESS!
    #
    
That's it!  Enjoy!

__UPDATE__: [Carlo][] noticed that comments broke on my site after updating to Textpattern 4.0.4.  As it turns out, a new feature was added to Textile at some point between the Textpattern 4.0.3 and 4.0.3 releases, which hasn't yet made it's way into PHP Markdown Extra's Textile emulation mode.  I've added a quick fix for it in the code here, and submitted a patch to [Michel Fortin][michel] who maintains PHP Markdown.

In short, Textile now supports a "Restricted" mode when submitting comments, which does some things differently than the normal Textile processing.  Links are automatically "nofollow"d, images are restricted, and block tags are limited to quotes and paragraphs.  It might be worth implementing something like that in Markdown, but for the moment, my "fix" simply calls the normal Markdown routine when `TextileRestricted` is called.  That's not perfect, but it's better than dying entirely with a fatal error.

[textpattern]: http://www.textpattern.com/ "Textpattern: A flexible, elegant, easy-to-use content management system for all kinds of websites, even weblogs."
[textile]: http://en.wikipedia.org/wiki/Textile_%28markup_language%29 "Wikipedia: Textile (Markup Language)"
[markdown]: http://en.wikipedia.org/wiki/Markdown "Wikipedia: Markdown"
[php]: http://www.michelf.com/projects/php-markdown/extra/ "PHP Markdown Extra"
[smartypants]: http://daringfireball.net/projects/smartypants/ "Smartypants"
[michel]: http://www.michelf.com/ "Michel Fortin"
[carlo]: http://carlo.zottmann.org/ "Carlo Zottmann: tail -f carlo.log"
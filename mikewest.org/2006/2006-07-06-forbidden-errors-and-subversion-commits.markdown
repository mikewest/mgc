---
Alias:
- http://mikewest.org/blog/id/23
Modified: '2006-07-06T09:17:51Z'
Teaser: A wayward `mod_rewrite` rule broke my Subversion commits with 403 ("Forbidden")
    errors.  Here's how I fixed it.
layout: post
tags:
- Subversion
title: '&#8220;Forbidden&#8221; Errors and Subversion Commits'
---
So, I got pretty clever with my [`mod_rewrite` rules][rewrite] to deal with some of the programs out there that nefarious types use to find vulnerable targets for exploits.  At least, I thought I was being clever.  As it turns out, I ended up shooting myself in the foot with the following rule:

    RewriteCond %{REQUEST_URI}    ^(.*)main.php$  [NC]
    RewriteRule ^(.*)           -               [F,L]
    
It's intention was to stop a bot from hammering me with requests for `main.php` in a wide variety of directories in the hopes that I had a broken version of [Horde][horde] installed.  These requests were generating tons of 404 ("Not Found") errors, making my log files pretty much worthless.  Sending 403 ("Forbidden") responses solved the immediate problem, but caused me some headaches yesterday when I tried to import a new project into [Subversion][svn].  Specifically, I was getting the following error:

    svn: Commit failed (details follow):
    subversion/libsvn_ra_dav/util.c:296: (apr_err=175002)
    svn: PUT of '/svn/<snipped long directory string>/lang_main.php': 403 Forbidden (https://mikewest.org)
    
In context, this is obvious.  The file I was trying to import was triggering the `mod_rewrite` rule, generating a 403 response.  I simply forgot entirely that my `mod_rewrite` rules were a factor when running Subversion over [WebDAV][webdav].  Once the support staff at [TextDrive][textdrive] pointed out my oversight, fixing the problem was trivial.  

I added the following rule to the top of my `.htaccess` file's list of `mod_rewrite` rules:

    RewriteCond %{REQUEST_URI}    ^/svn
    RewriteRule    ^(.*)            -        [L]
    
That simply stops the engine from rewriting anything under my `/svn/` directory, which solved the problem completely.  One more thing to look out for...

[rewrite]: http://mikewest.org/archive/leveraging-modrewrite "Leveraging `mod_rewrite`"
[horde]: http://www.horde.org/ "Horde Project"
[svn]: http://subversion.tigris.org/ "Subversion"
[webdav]: http://en.wikipedia.org/wiki/WebDAV "Wikipedia: WebDAV"
[textdrive]: http://textdrive.com/ "TextDrive"
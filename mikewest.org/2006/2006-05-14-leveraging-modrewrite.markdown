---
Alias:
- http://mikewest.org/blog/id/14
Modified: '2007-05-09T06:49:28Z'
Teaser: I have three kinds of `mod_rewrite` rules in my `.htaccess` file, this article
    explains each, and lays out best practices for managing your site's URL scheme.
layout: post
tags:
- HOWTO
title: Leveraging `mod_rewrite`
---
I have three kinds of `mod_rewrite` rules in my `.htaccess` file:

* "This Doesn't Exist Anymore" Rules
* "Go Away" Rules
* "Fixing Other People's Links" Rules

Through judicious application of these `mod_rewrite` rules, I have more or less complete control over the URLs people use to visit my site, and moreover, control over the way search engines deal with my old (and at times obsolete) content.

## "This Doesn't Exist Anymore" Rules ##

Once upon a time, I uploaded some mp3's to a _super secret_ directory on my webserver so that I could download them at the office and enjoy some tunes on my horridly locked-down work machine.  As you might guess, the _super secret_ directory name was neither particularly super, nor spectacularly secret.  MP3 search engines tracked down the directory within hours, and I realized my mistake after my bandwidth usage for the week skyrocketed.

I killed off the directory pretty quickly, but the damage was done.  I was still getting tons of hits for those non-existent files, and the 'file not found' responses were making it pretty much impossible to get any useful information out of my error logs.

The right thing to do in this situation is to serve up a [410 ('Gone') HTTP error][gone] for any and all requests for files that were sitting around at some point in the past, but have since been removed.  `mod_rewrite` makes this an absolute breeze:

    RewriteCond %{REQUEST_URI}  ^/mp3/  [NC]
    RewriteRule ^(.*)           -       [G,L]
    
In fact, I have a whole series of rules that return 410 errors.  The relevant section of my `.htaccess` files looks like:

    RewriteCond %{REQUEST_URI}  ^/mint                       [NC,OR]
    RewriteCond %{REQUEST_URI}  ^/mp3                         [NC,OR]
    RewriteCond %{REQUEST_URI}  ^/matchmaker                 [NC,OR]
    RewriteCond %{REQUEST_URI}    ^/ars/?                        [NC]
    
    RewriteRule ^(.*)           -                           [G,L]
    
The `OR` at the end of each `RewriteCond` chains them together in exactly the way you might imagine.  If _any_ of the conditions matches, then the rule triggers, and a 410 error code is returned.  Brilliant!

## "Go Away" Rules ##

Along with 410 error codes, you'll probably also find some use for 403 ('Forbidden') errors.  For example, if you deploy content with CVS or SVN, then you've got files sitting around in your public document root that contain information you'd probably prefer not to share with everyone in the world (see [Dan Benjamin's explanation][hive] for discussion of this very issue with Ruby on Rails' [Capistrano][capistrano]).  The files exist, so you shouldn't send a 404 ('Not Found') or a 410 ('Gone') error, but do you want to forbid access via the web.  The following rules solve the problem:

    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_URI}    ^(.*/)?CVS/                    [NC,OR]
    RewriteCond %{REQUEST_URI}    ^(.*/)?\.svn/                [NC]
    RewriteRule ^(.*)           -                           [F,L]
    
The first line tests to see whether or not the requested `CVS` or `.svn` file actually exists before throwing a 403 ('Forbidden') error.  It's a bit pedantic, but one ought not return a 'Forbidden' error for a file that's really 'Not Found'.

It's also worth noting here that the `OR` binds more tightly than the implicit `AND` in the first line.  The rules therefore evaluate to something like "If the file exists AND (it's a `CVS` OR `.svn` file)", which makes sense for this application.

## "Fixing Other People's Links" Rules ##

I've used a few domains over the lifetime of this blog, and search engines have links to files on all of them.  Since I want all my URLs to refer to the same domain (to reduce confusion, and accumulate Page Rank correctly), I use `mod_rewrite` to map all requests to those other domains to my domain of choice.  [John Gruber's recent `.htaccess` article][gruber] does a brilliant job explaining this sort of redirection, so I'll just note the syntax I use here (I like to explicitly note that the error code is 301 ('Moved Permanently') instead of using the full name, but that's simply personal preference; both work fine):

    RewriteCond %{HTTP_HOST}    ^(www\.)?reversal\.org$ [NC]
    RewriteRule ^(.*)           http://mikewest.org/$1  [R=301,L]

Beyond differing domains, I've used a number of different URL schemas.  Before I migrated to [TextPattern][txp], each article on the site was accessible via a URL that looked something like '`/blog/id/<id number>`'.  I wasn't a huge fan of this URL schema, and I welcomed the chance to flip to something that made more sense.  The new URL schema looks like '`/archive/<short title>`', which is friendlier both to end-users and search engines.  

The problem, of course, is that the articles on the old site had been indexed by search engines, and linked by other bloggers.  When I migrated to the new URL schema, I wanted to make sure that those old links would still go somewhere relevant.

There isn't much to say about this, really, as it's simply a manual mapping from URL #1 to URL #2 using a 301 ('Moved Permanently') error code:

    RewriteCond %{REQUEST_URI}  ^/blog/id/12                [NC]
    RewriteRule ^.*$            /archive/event-handlers-and-other-distractions? [R=301,L]

If you're planning a similar move, it would be best to determine which of your pages are actually linked regularly by other sites, and generate the `mod_rewrite` rules that are most relevant to your circumstances.  I examined my 'Not Found' error logs religiously for the first couple of days after moving to the new framework, and created `mod_rewrite` rules for any errors that popped up more than once or twice.  

This practice is actually a good ongoing maintenance idea.  In his recent [Django talk at Google][django-google], [Jacob Kaplan-Moss][jacob] mentioned that the Django team uses the 'Not Found' errors as a useful source of user suggestions.  If people continually look for an '/archives/' URL, then maybe it's a good idea to make one, or write a `mod_rewrite` rule to direct that request to your '/past-posts/' page, etc.  For example, I'm directing a few 'suggestions' to my [bio][me]:

    RewriteCond %{REQUEST_URI}  ^/resume.php            [NC,OR]
    RewriteCond %{REQUEST_URI}  ^/contact.php           [NC,OR]
    RewriteCond %{REQUEST_URI}  ^/contact/              [NC,OR]
    RewriteCond %{REQUEST_URI}  ^/resume/               [NC,OR]
    RewriteCond %{REQUEST_URI}  ^/bio.php               [NC]
    RewriteRule ^(.*)           http://mikewest.org/is/ [R=301,L]

## Resources ##

* Dave Child's "[`mod_rewrite` Cheat Sheet][cheat]" is a great one-stop reference, including a list of the flags for `RewriteRule` that I continually mix up in my head.
* John Gruber's "[Using .htaccess Redirection to Standardize Web Server Addresses][gruber]" is an excellent resource for (very) basic explanations of the regular expressions that drive his `mod_rewrite` domain name redirections.
* Apache's [`mod_rewrite` documentation][apache-docs], and the less incomprehensible "[URL Rewriting Guide][apache-guide]" from Ralf Engelschall who wrote `mod_rewrite` in the first place.

[txp]: http://textpattern.com/  "TextPattern"
[gone]: http://diveintomark.org/archives/2003/03/27/http_error_410_gone "Mark Pilgrim - HTTP Error 410: Gone"
[hive]: http://hivelogic.com/articles/2006/04/30/preventing_svn_exposure "Hivelogic - Preventing SVN Exposure"
[cheat]: http://www.addedbytes.com/cheat-sheets/mod_rewrite-cheat-sheet/ "Dave Child - `mod_rewrite` Cheat Sheet"
[django-google]: http://video.google.com/videoplay?docid=-70449010942275062 "Jacob Kaplan-Moss talks about Django at Google"
[jacob]: http://www.jacobian.org/ "Jacob Kaplan-Moss' Website"
[me]: /is/ "Mike West's Bio/Resume"
[gruber]: http://daringfireball.net/2006/05/htaccess_redirection "John Gruber - Using .htaccess Redirection to Standardize Web Server Addresses"
[apache-docs]: http://httpd.apache.org/docs/1.3/mod/mod_rewrite.html
[apache-guide]: http://httpd.apache.org/docs/2.0/misc/rewriteguide.html "URL Rewriting Guide"
[capistrano]: http://manuals.rubyonrails.com/read/book/17
---
Alias:
- http://mikewest.org/blog/id/15
Modified: '2006-06-16T17:11:32Z'
Teaser: Setting up virtual domains on your local OS X Apache installation is pretty
    easy.  Here's a quick description of the process.
layout: post
tags:
- HOWTO
title: Virtual Hosting on OS X
---
[Headdress][1] looks like a nice little app for configuring virtual hosting on the local installation of Apache that comes with OS X.  If you like doing things via a GUI, it's probably right up your alley.

I don't, and luckily, this sort of thing is really not that hard at all to do on your own with your good friend, the text editor.  You'll just need to edit two files, restart Apache, and then you're done.

[1]:    http://headdress.twinsparc.com/ "Headdress"

## Map a domain to your local machine ##

First, you'll need to tell your computer what domains should point to the local web server.  I generally use '.dev' to distinguish these from the real, live domains.  `mikewest.org` is hosted on my machine locally as `mikewest.dev`, `lddebate.org` is `lddebate.dev`, etc.

Generally speaking, names like `mikewest.org` are resolved by asking a DNS server which IP address to request.  We're going to bypass that system for our local development domains by explicitly mapping each to our machine.  

The easiest way to do this is to pop open `/etc/hosts` and add in a line mapping the domain to the loopback IP address: 127.0.0.1.

If you're using TextMate, then from the terminal, you can type:

    mate /etc/hosts
    
to open the hosts file for editing.  You'll see some mappings already in there, _please don't touch them_.  Instead, add a line at the end of the file for each domain you plan to host locally in the following format:

    127.0.0.1        domainname.dev

Type the names and addresses in, one per line.  When you're finished, it should look something like:

    127.0.0.1       mikewest.dev
    127.0.0.1       lddebate.dev
    127.0.0.1       supersecretproject.dev
    127.0.0.1       iamsocool.dev

Your machine looks at this file to resolve a domain before it looks anywhere else, so this mapping takes precedence on your local machine.  

It's important to note, however, that this has absolutely no effect whatsoever on anyone else's system.  Telling your best friend about your test site at `iamsocool.dev` isn't helpful at all, as she's simply not going to be able to see it from her machine.

You'll almost certainly have to restart your web browser in order to clear it's cache, and you might even have to flush the system's DNS cache by typing the following into terminal:

    lookupd -flushcache

##    Tell Apache what to do with the domain ##

Now you've gotten your development domain set up to point to your machine, but Apache doesn't know anything about it; We'll need to set up some virtual hosts by editing the Apache configuration.

Pop open the `httpd.conf` file by typing the following at the terminal:

    mate /etc/httpd/httpd.conf
    
Search for the string "NameVirtualHost" (on my install, it was on line 1063),
and uncomment it by removing the leading [octothorpe][pound] `#`.  It should look like this when you're done:

    NameVirtualHost *:80

This explains to Apache that you're going to be hosting multiple domains on your computer, and that it needs to use the name of each domain to distinguish which directory to serve files from.  Now, we need to tell it which names to expect.  For each of your domains, add in a virtual host definition that looks like this:

    <VirtualHost *:80>
        DocumentRoot    /path/to/your/project
        ServerName        projectname.dev
    </VirtualHost>
    
The `DocumentRoot` is the directory in which your project lives.  The `ServerName` is the name that Apache should respond to.  I lay out my projects as subdirectories of `/Users/mwest/Projects/`, so my configuration looks like:

    <VirtualHost *:80>
        DocumentRoot    /Users/mwest/Projects/org_mikewest
        ServerName        mikewest.dev
    </VirtualHost>

    ...

    <VirtualHost *:80>
        DocumentRoot    /Users/mwest/Projects/org_lddebate
        ServerName        lddebate.dev
    </VirtualHost>

Once you've added in all the virtual host definitions that you need, save the configuration file, then hop back into Terminal to restart Apache by typing:

    sudo apachectl restart

It should pop right back up, and you'll be ready to go!

## Additional Resources ##

*   If you'd like to test PHP/MySQL driven projects locally, the simplest way
    to get set up is to install [MySQL's binary package][mysql] and Marc
    Liyanage's [PHP module][php].  
*   Apache has great documentation on [name-based virtual hosting][apache_doc]
    and a Cookbook-style series of [virtual hosting examples][apache_examples]
    that cover some of the more complicated configurations you might run into.


[pound]: http://en.wiktionary.org/wiki/Octothorpe "Wiktionary: Octothorpe"
[mysql]: http://dev.mysql.com/downloads/mysql/5.0.html
[php]: http://www.entropy.ch/software/macosx/php/ 
[apache_doc]: http://httpd.apache.org/docs/1.3/vhosts/name-based.html
[apache_examples]: http://httpd.apache.org/docs/1.3/vhosts/examples.html
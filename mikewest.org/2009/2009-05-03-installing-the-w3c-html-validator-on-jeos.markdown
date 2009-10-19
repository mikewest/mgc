---
layout:     post
title:      "Installing the W3C HTML Validator on JeOS"
slug:       "installing-the-w3c-html-validator-on-jeos"
aliases:
    - http://blog.mikewest.org/post/102905143
    - http://blog.mikewest.org/post/102905143/installing-the-w3c-html-validator-on-jeos
tags: 
    - html
    - validation
    - testing
    - w3c
    - webdev
    - development
Teaser:      "So.  W3C has quite decent installation instructions for the HTML validator, but it makes a few assumptions about a typical linux environment that don't actually hold true if you're running a stripped down JeOS distro in a virtual machine."
---
So.  W3C has quite decent [installation instructions][install] for the HTML
validator, but it makes a few assumptions about a typical linux environment
that don't actually hold true if you're running a stripped down JeOS distro in
a virtual machine.

Here's what I ended up doing to get the software working on my VM.  Hopefully
it'll work for you too.  :)

[install]: http://validator.w3.org/docs/install.html

Install Apache2:

    sudo aptitude install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert

Turn on SSI:

    sudo a2enmod include

Install OpenSP SGML parser:

    mkdir ~/src
    cd ~/src
    curl -O http://switch.dl.sourceforge.net/sourceforge/openjade/OpenSP-1.5.2.tar.gz
    tar xzvf ./OpenSP-1.5.2.tar.gz
    cd OpenSP-1.5.2
    ./configure --enable-http --disable-doc-build && make && sudo make install

Install perl dependencies:

    sudo apt-get install libxml2-dev

    sudo perl -MCPAN -e shell
    ...
    install Bundle::W3C::Validator
    install SGML::Parser::OpenSP

Install cvs:

    sudo apt-get install cvs

Checkout the validator code into `/usr/local/validator

    $ cd /usr/local
    $ sudo mkdir /usr/local/validator
    $ sudo chmod a+w /usr/local/validator
    $ export CVSROOT=":pserver:anonymous@dev.w3.org:/sources/public"
    $ cvs login
    CVS password: anonymous
    $ cvs get validator

Adjust the default configuration file a bit:

1.  Change the directory for the two `AliasMatch` lines at the top of the file.  For whatever reason, they're pointing to the wrong place.  The first ought point to `/usr/local/validator/httpd/cgi-bin/check`, the second to `/usr/local/validator/httpd/cgi-bin/sendfeedback.pl`.
    
        AliasMatch ^/+w3c-validator/+check(/+referer)?$   /usr/local/validator/httpd/cgi-bin/check
        AliasMatch ^/+w3c-validator/+feedback(\.html)?$ /usr/local/validator/httpd/cgi-bin/sendfeedback.pl
    
2.  Comment out the `<Proxy>` block at the bottom of the file.

Symlink the validator config into `/etc/w3c`

    sudo ln -s /usr/local/validator/htdocs/config /etc/w3c

Symlink the configuration file from CVS to the `/etc/apache2/sites-available/` directory:

    sudo ln -s /usr/local/validator/httpd/conf/httpd.conf /etc/apache2/sites-available/

Enable the new site:

    sudo a2ensite validator

Reload the Apache config:

    sudo /etc/init.d/apache2 reload

Test the checker:

    /usr/local/validator/httpd/cgi-bin/check uri=http://www.w3.org/

Win!

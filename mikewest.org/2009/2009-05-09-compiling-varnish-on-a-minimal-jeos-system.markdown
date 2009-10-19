---
layout:     post
title:      "Compiling Varnish on a minimal JeOS System"
slug:       "compiling-varnish-on-a-minimal-jeos-system"
aliases:
    - http://blog.mikewest.org/post/105540440
    - http://blog.mikewest.org/post/105540440/compiling-varnish-on-a-minimal-jeos-system
tags: 
    - jeos
    - install
    - howto
    - varnish
    - compile
    - cli
    - webdev
    - caching
Teaser:    "Varnish is an excellent-looking 'HTTP accelerator', designed specifically as a high-performance caching reverse-proxy to sit in front of your hard-working application servers, and relieve them of load.  It's a bit of a pain in the ass to install from source on JeOS, though."
---
Varnish is an excellent-looking "HTTP accelerator", designed specifically as a high-performance caching reverse-proxy to sit in front of your hard-working application servers, and relieve them of load.  It's a bit of a pain in the ass to install from source on JeOS, though.  Here's what I ended up doing:

1.  Install XSLTProc:

        sudo apt-get install xsltproc

2.  Install some helpful GNU tools:

        sudo apt-get install automake autoconf libtool libncurses5

3.  Install `groff-base`.  If you don't do this, your compilation will fail because [`soelim`][soelim] isn't available:

        sudo apt-get install groff-base

4.  Install Subversion:

        sudo apt-get install subversion

5.  Checkout the Varnish trunk:

        mkdir -p ~/src
        cd ~/src
        svn co http://varnish.projects.linpro.no/svn/trunk/varnish-cache
    
6.  Generate `configure` and makefiles:

        cd ~/src/varnish-cache
        ./autogen.sh

7.  Configure, make, test (this is SVN trunk, after all), install.  This step (particularly the tests) will take a while, go make some tea:

        ./configure && make && make check && sudo make install

8.  Tell JeOS where to look for Varnish's shared libraries.  I can't imagine why the installer doesn't do this, I'll assume for the moment that it's an artifact of building directly from SVN.  If you don't do this, you'll get errors like "varnishd: error while loading shared libraries: libvarnish.so.1: cannot open shared object file: No such file or directory":

        sudo ldconfig -n /usr/local/lib

9.  Go read the [Varnish introduction][intro].  That's what I'm doing at the moment... it seems like a good next step.  :)

[intro]:  http://varnish.projects.linpro.no/wiki/Introduction
[soelim]: http://www.linuxcommand.org/man_pages/soelim1.html

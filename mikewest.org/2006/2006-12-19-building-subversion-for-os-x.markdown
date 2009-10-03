---
Alias:
- http://mikewest.org/blog/id/41
Modified: '2007-01-26T11:34:00Z'
Teaser: Metissian's pre-build Subversion binaries are out of date, and Dan Benjamin's
    excellent guide to building Subversion yourself runs into a wall for 1.4+.  You,
    however, are an impatient pioneer.  You want to build the latest stable (impatient,
    not _imprude
layout: post
tags:
- Subversion
- HOWTO
title: Building Subversion 1.4.3 for OS X
---
__UPDATE__: _[Subversion 1.4.3 was released][svn_143]
([Release Notes][release_143]) on Jan 25th, 2007.  I've updated the
instructions here accordingly._

[svn_143]: http://subversion.tigris.org/servlets/NewsItemView?newsItemID=1807
[release_143]: http://svn.collab.net/repos/svn/tags/1.4.3/CHANGES

The [pre-built Subversion binaries][metissian_svn] that [Metissian][] generally
puts together are running a little behind the times, and
[Dan Benjamin's][hivelogic] excellent [guide to building Subversion from
source][hivelogic_svn] needs a bit of an update to support 1.4.3.   Those are still
the sources I'd recommend that you visit in the future; they're diligent folk
indeed.

You, however, are an impatient pioneer.  You want to build the latest stable
(impatient, not _imprudent_) Subversion release yourself, _right now_. This
article explains the process.

Prerequisites
-------------

If you haven't installed Subversion yet, visit Dan's [guide to building
Subversion][hivelogic_svn] that I mentioned above, and ensure that you've
followed the the instructions under the __Set Your Path__ heading.  They're
important.

You'll also need to ensure that you have a recent version of Xcode installed
(I'm running 2.4.1).  You will get errors if you're running a sufficiently old
version (I'm _guessing_ 2.2 or below).

Process
-------

So, you're good to go.  Simply pop open Terminal and run:

    mkdir ~/Desktop/src/
    cd ~/Desktop/src/
    curl -O http://subversion.tigris.org/downloads/subversion-1.4.3.tar.gz
    curl -O http://subversion.tigris.org/downloads/subversion-deps-1.4.3.tar.gz
    tar xvzf ./subversion-1.4.3.tar.gz
    tar xvzf ./subversion-deps-1.4.3.tar.gz
    cd subversion-1.4.3
    ./configure --prefix=/usr/local --with-openssl --with-ssl --with-zlib
    make
    sudo make install

That last command will require you to enter your password; do so, it's ok.
    
That's it.  You're done.

Problems
--------

What?  You got an error helpfully informing you that your "C compiler cannot
create executables See 'config.log' for more details"?  I did too.

The answer's simple: you have either an outdated version of the `GCC`
compiler, or an outdated `ln` utility.  Either way, you need to upgrade your
Xcode installation.  It's an absurdly large package that you can grab (for
free) from [Apple's Developer Connection][adc].  Sign up for an account if you
don't already have one, download the upgrade, install it, reboot for good
measure (though logging out and then back in is probably enough), then re-run:

    ./configure --prefix=/usr/local --with-openssl --with-ssl --with-zlib
    make
    sudo make install

That should take care of the issue.
    
[metissian]: http://metissian.com/
[metissian_svn]: http://metissian.com/projects/macosx/subversion/ "Subversion Packages for Mac OS X"
[hivelogic]: http://hivelogic.com/ "Dan Benjamin: Hivelogic"
[hivelogic_svn]: http://hivelogic.com/articles/2006/04/19/svn_on_os_x "Building Subversion (SVN) on Mac OS X"
[adc]: http://developer.apple.com/ "Apple Developer Connection"
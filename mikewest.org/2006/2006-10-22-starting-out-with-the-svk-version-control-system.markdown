---
Alias:
- http://mikewest.org/blog/id/40
Modified: '2006-10-22T11:06:41Z'
Teaser: SVK is a version control system that sits on top of a Subsverion, CVS, Perforce,
    etc. repository, and provides the promise of a common interface.  Here's how to
    install it on OS X.
layout: post
tags:
- HOWTO
- Subversion
title: Starting out with the SVK Version Control System
---
I have the distinct impression that I'm going to be playing with a lot of CVS repositories in the near future, and I'm not exactly thrilled about the idea.  I've been almost exclusively using SVN for the last year or two, and it's going to be a bit of a leap to "revert" to CVS for version control.  I'm hoping that [SVK][] will be able to help me bridge the conceptual gap.

[SVK]: http://svk.elixus.org/ "SVK Version Control System"

SVK is a decentralized version control system, based on Subversion.  The piece that interests me is it's ability to sit on top of a variety of repositories, providing a single interface to all of them regardless of server.  The ability to map SVN-like commands to a CVS repository, for example, is very interesting.  I have no idea if it will work, and I haven't found a whole lot of material online about others' success or failure, so I'll just play around with it myself and see if I can get it going anywhere.  

## Installing SVK on OS X ##

There's a [packaged SVK installer for OS X][svkdmg] that you can download and run.  I generally prefer to compile things myself, but the package is probably the best option; the command line install for SVK is more annoying than usual.

[svkdmg]: http://homepage.mac.com/hiirem/SVK-1.07-1.dmg

If you're a nut, and want to install from the command line, then type:

    curl -O http://homepage.mac.com/hiirem/svkbuild-1.07-1.tar.bz2
    bunzip2 ./svkbuild-1.07-1.tar.bz2
    tar -xvf ./svkbuild-1.07-1.tar
    cd svkbuild-1.07-1
    sudo mkdir /usr/local/svk-`cat VERSION`
    sudo chown $USER /usr/local/svk-`cat VERSION`
    ./build.sh
    
`build.sh` uses CPAN to install some required Perl modules.  It'll ask for confirmation before pulling them down, so you'll have to babysit the installation a bit to hit enter at the appropriate times.  That's more than a little annoying.  I hope that gets cleaned up in the future, because it's driving me nuts.  :)
    
## References ##

I'll continue populating this section as I read more about SVK.  For now, I'm starting with:

*   [Version Control with SVK][svkbook] is _the_ resource for SVK.  It's
    fairly complete, but still very much a work in progress.

[svkbook]: http://svkbook.elixus.org/ "Version Control with SVK"
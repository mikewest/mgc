---
layout:     post
title:      "Running `python-spidermonkey` on JeOS"
slug:       "running-python-spidermonkey-on-jeos"
aliases:
    - http://blog.mikewest.org/post/108613427
    - http://blog.mikewest.org/post/108613427/running-python-spidermonkey-on-jeos
tags: 
    - javascript
    - spidermonkey
    - rhino
    - mozilla
    - python
    - webdev
    - testing
    - pauldavis
---
Paul Davis' [`python-spidermonkey`][ps] project looks brilliant.

In a nutshell, he's building a Python bridge to Mozilla's [SpiderMonkey][] "JavaScript on C" environment.  I'm excited about that, because it means I might be able to put together a headless testing environment without trying to make everything work correctly inside Rhino.  Hooray for options!

I ran into a snag or two while getting up and running on JeOS (my [dev environment of choice][brad]), so I'm documenting the process here.

[brad]: http://intranation.com/entries/2009/03/development-virtual-machines-os-x-using-vmware-and/
[SpiderMonkey]: http://www.mozilla.org/js/spidermonkey/
[ps]: http://github.com/davisp/python-spidermonkey/tree/master

1.  Install python headers and `pkg-config`.  Forgetting to install
    `pgk-config` will give you some exciting errors in the compilation phase
    later on that make it sound like NSPR failed to install correctly.  If
    you're on JeOS, it's more likely the case that you don't have `pkg-config`
    at all:

        sudo apt-get install python2.6-dev pkg-config

2.  Install netscape portable runtime:

        sudo apt-get install libnspr4-dev
        
3.  Pull down python-spidermonkey

        mkdir -p ~/src
        cd ~/src
        git clone git://github.com/davisp/python-spidermonkey.gitnsp

4.  Build `python-spidermonkey`

        cd ~/src/python-spidermonkey
        python setup.py build

5.  Test `python-spidermonkey`:

    Actually, __don't__ do this.  [One of the tests fails on JeOS][fail], and it
    fails in a way that sucks up all your resources and leaves you in an
    infinite loop.  Yay!
    

6.  Install:  Even though the max time test fails (spectacularly), the bridge
    seems to work pretty well.  Install the package anyway, just don't rely on
    being able to set a max execution time on your code.  :)

        sudo python setup.py install

Now, to see about getting [JSLint][] running in this environment... Fun!

[fail]: http://davisp.lighthouseapp.com/projects/26898-python-spidermonkey/tickets/15-test_exceed_time-fails-on-jeos
[JSLint]: http://jslint.com/

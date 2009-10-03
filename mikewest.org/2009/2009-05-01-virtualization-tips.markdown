---
layout:     post
title:      "Virtualization Tips"
slug:       "virtualization-tips"
aliases:
    - http://blog.mikewest.org/post/102255116
    - http://blog.mikewest.org/post/102255116/virtualization-tips
tags: 
    - virtualization
    - virtual machines
    - vm
    - vmware
    - vmwarefusion
    - fusion
    - tinyxp
    - jeos
    - ubuntu
---
In the last three weeks, I've set up something like 6 virtual machines to play with a variety of bits and pieces of things that I come across.  Virtual machines are a perfect fit for, say, setting up [CouchDB][] to see how it works, or for giving [Varnish][] a try.  They have the distinct advantage of being more or less throw-away sandboxes, where I simply don't have to worry about accidentally screwing things up.  If I break PHP or PHPUnit on my development laptop, then I've got real problems; if I break it in a VM, I make a new one.

[CouchDB]: http://couchdb.apache.org/
[Varnish]: http://varnish.projects.linpro.no/

Off the top of my head, here are a few lessons learned:

1.  Buy youself a copy of [VMWare Fusion][].  In my experience, it's been a
    bit more stable than [Parallels][], and a _lot_ friendlier than
    [VirtualBox][].  There's a great community around VMWare tools in general,
    and if you end up using virtual machines for anything more than
    development (deploying public applications, for instance), then you'll
    literally be able to copy your VM over to a "real" server and run it
    without problems.

[VMWare Fusion]: http://vmware.com/products/fusion/
[Parallels]: http://www.parallels.com/
[VirtualBox]: http://www.virtualbox.org/

2.  Follow Brad's [excellent Ubuntu setup instructions][intranation].  He
    walks through the process of getting a baseline [JeOS][] machine up and
    running, which takes something on the order of 10 minutes.
    
    I've tried a few distros of Linux and BSD, and in my opinion, JeOS hits
    the sweet spot dead on.  It's a relatively small install (~1GB, all said
    and done), and runs very smoothly indeed with 256MB RAM.  It's chock-full 
    of Ubuntu goodness for package installs, and relatively easy to configure.

[intranation]: http://intranation.com/entries/2009/03/development-virtual-machines-os-x-using-vmware-and/ "Brad Wright: 'Development Virtual Machines on OS X using VMWare and Ubuntu'"
[JeOS]: http://www.ubuntu.com/products/whatisubuntu/serveredition/jeos

3.  Setup [linked clones][] to save yourself some disk space, and to make the
    process of spinning off new VMs as frictionless as possible.  In short,
    this will allow you to install JeOS once, and use that install as a clean 
    base for new machines without copying the entire disk.  You'll end up with
    a ~1GB base and ~100MB VMs for each of your applications, which is a huge
    savings indeed (especially if you want to carry a VM or two around with
    you on a USB stick).
    
    It's a bit of a manual process at this point, but very straightforwardly
    explained, and easy to implement.  Hopefully VMWare will expose the
    functionality via some sort of GUI in a future version, as they already do
    in [Workstation][].
    
    With linked clones, it's _trivial_ to bring up a new, clean VM to test
    something out, or to install some new component.  It's transformational:
    you'll wonder how you _ever_ got around with just one development
    environment.
    
[linked clones]: http://communities.vmware.com/docs/DOC-5611
[workstation]: http://www.vmware.com/products/ws/

4.  After creating clones of an Ubuntu VM, you'll need to do a tiny bit of
    work to get networking up and running again.  The system will be assigned
    a new MAC address, and get a bit confused about the references to the old
    virtual network card.
    
    Jamis Buck has [described the solution in detail][buck], and I've codified
    it into a [small script][].  Grab that code, then just run
    `update_copied_vm` to update the hostname, hosts file, and network
    settings for the new VM.  Piece of cake...
    
[buck]: http://weblog.jamisbuck.org/2008/8/15/cloning-ubuntu-hardy-image-in-vmware-fusion "Jamis Buck: 'Cloning Ubuntu Hardy image in VMWare Fusion'"
[small script]: http://github.com/mikewest/homedir/blob/master/bin/update_copied_vm

5.  For Windows development, browser testing, etc, visit your favourite
    interweb download site, and find yourself a copy of [TinyXP][].  Clever
    folks have ripped all the inessential bits out of XP, meaning that it runs
     _quickly_ with minimal investment of RAM and disk space.  Combined with
     the linked clones tip above, you'll have IE6, 7, and 8 test environments
    up and running in no time at all.
    
[TinyXP]: http://en.wikipedia.org/wiki/TinyXP

Developing your applications on virtual machines really does make your life simpler, and opens up opportunities for you to explore things that would have probably just been a _little bit_ too much work to get running otherwise.  It's very much worth the up-front investment to get yourself set up.

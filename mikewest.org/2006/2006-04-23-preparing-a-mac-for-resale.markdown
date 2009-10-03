---
Alias:
- http://mikewest.org/blog/id/12
Modified: '2006-06-12T19:38:09Z'
Teaser: Describes the easy process of setting up a mac for resale (patches, etc) while
    keeping the Setup Assistant experience for the new owner.
layout: post
tags:
- HOWTO
title: Preparing a Mac for Resale
---
I'm loaning an old TiBook to a friend to tide him over until he can replace an iBook whose hard drive just crashed.  I wanted to load OS X and push in the various software updates that are out there so he can just get going, but I didn't particularly want to leave a user account sitting there.

Luckily, after a bit of digging around in [asr man pages][asr] and googling, I've pieced together a pretty solid method of setting up a machine while retaining the 'just out of the box' set up experience for the new owner.  It's not a tough process; Apple's made it fairly trivial.

[asr]: http://www.hmug.org/man/8/asr.php  "Apple Software Restore: manual pages"

## Prepare the Mac ##

First, simply install OS X, just as you always would.  Watch the pretty OS X intro movie, run through the setup screens, and you'll end up logged into the machine as an admin-level user.  We'll use this account to update the machine, and then we'll remove all traces of it's existence.  Make sure you write down the 'short name' you used when creating your user.  We'll need it later.

While logged in, run `System Update` to download all the latest patches to the OS.  You can also install software at this time, as long as you make sure to install it into the root level Applications folder (`/Applications/`, not `~/Applications/`).  Once you've got everything updated and installed, we'll move on to the next phase.

To proceed, you can either follow the instructions [on this page][no-single-user] (which I don't recommend because they advocate removing your account while you're still logged into the machine, which is more than a little dangerous), or continue reading below.

## Remove your account ##

Reboot the machine, and hold `command-s` to boot into single-user mode.  This is vaguely risky business, as you have complete access to your mac as root, so be careful about what you type.

In single-user mode, the hard drive defaults to being mounted as a read-only volume.  This stops you from doing something silly, like accidentally deleting your user account.  However, we're _purposefully_ deleting our user account, so we'll need to fsck the drive to make sure it's safe to work with, and then remount the volume with write access.  The following two commands take care of that for us:

    /sbin/fsck -y
    /sbin/mount -uw /
        
The first might not be necessary if your drive is formatted using a journaled filesystem, but it doesn't hurt anything, so run it just to be safe.  The second (note the trailing slash: it's not a typo) mounts the drive as a writable volume, which allows us to proceed.

Now it's time to kill off the user we created.  We need to do two things: remove the user's home directory, and remove the user's entry in the system's NetInfo database:

    rm -r /Users/[user's short name]
    nicl -raw /var/db/netinfo/local.nidb delete /users/[user's short name]

## Cleanup ##

We've removed our account, and now we just need to trick the system into running the Startup Assistant again.  This is straightforward:

    rm /var/db/.AppleSetupDone

We're done.  All that's left is to gracefully shut the machine down:

    shutdown -h now
    
And that's it.  Pack the machine up, and hand it off to it's new owner so she can hop on and experience the sublime pleasure of OS X.

[no-single-user]: http://www.niload.com/archives/2005/10/03/start-over-mac/ "Give an updated Mac that like-new feeling"
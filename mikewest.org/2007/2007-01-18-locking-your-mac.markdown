---
Alias:
- http://mikewest.org/blog/id/51
Modified: '2007-01-21T00:22:38Z'
Teaser: My coworkers love playing pranks on poor, unlocked computers. This is the
    method I've decided on to quickly and securely walk away from my Mac.
layout: post
tags:
- HOWTO
title: Locking Your Mac
---
I've tried a few different methods to walk away from my Mac without worrying about jackass coworkers sending e-mails and IM messages on my behalf, and after a bit of experimentation with various screensavers and applescripts, finally hit upon a solution that I'm happy with. It's pretty simple, and leverages the power of [Quicksilver triggers][triggers] to make the process of locking my computer absolutely second-nature.

## Terminal Magic

First, open up a terminal window, and copy and paste the following line:

    echo "alias lock='/System/Library/CoreServices/Menu\\ Extras/user.menu/Contents/Resources/CGSession -suspend; exit;'" >> ~/.bash_profile

This adds an alias to your bash profile that gives you the ability to simply type lock at the command line to securely suspend your current session. I always have a terminal window open, so this was a good first step for me, and might reasonably be enough for you if you're also a terminal geek. However, adding [Quicksilver][] into the mix makes the process more flexible.

## Triggers

We can create a trigger to bind a hotkey to the terminal command we've just created. Whenever I hit ???\, my computer locks itself down; it's trivial.

Bring up Quicksilver's preference screen by hitting your Quicksilver hotkey (mine's bound to ?-Space), then ?-Comma. Select "Triggers" from the menu at the top, then create a new custom trigger by hitting the plus button near the bottom and selecting "Hotkey." Set this new trigger to run our lock command by hitting "." to enter text entry mode, typing "lock", then tabbing to the next field and selecting "Run a Text Command in Terminal" (if you don't have this command, make sure the Terminal plugin is installed).

Once the trigger is created, give it a hotkey by double clicking on the trigger (or clicking on the "info" icon in the bottom right-hand corner), then clicking on the "Hot Key" field, and hitting the keys you'd like to assign. I chose ???\ because it requires both hands, and isn't something I could possibly hit by accident.

And that's all there is to it! You can now lock your computer with impunity! Enjoy your new-found power.

[quicksilver]: http://quicksilver.blacktree.com/
[triggers]: http://docs.blacktree.com/quicksilver/triggers
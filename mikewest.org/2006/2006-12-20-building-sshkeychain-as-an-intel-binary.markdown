---
Alias:
- http://mikewest.org/blog/id/42
Modified: '2007-01-29T19:37:22Z'
Teaser: I've seen a few Universal Binary builds of SSHKeychain floating around, but
    I'm paranoid, so I built my own.  It's easier than I expected.
layout: post
tags:
- HOWTO
title: Building SSHKeychain as an Intel Binary
---
I've seen a few Universal Binary builds of [SSHKeychain][] floating around,
which is a wonderful thing, since SSHKeychain is one of the few apps I use on 
a daily basis that triggers the Rosetta performance hit.  That said, I'm
paranoid enough to have gone through the trouble of creating separate SSH keys
for each of the servers I connect to (I'll post the bash script at some
point).  Moreover, they're all passworded.  It doesn't really make sense that
I'd use/trust someone else's build of a utility with complete access to all
that information.

Happily, building my own binary turned out to be absolutely trivial.  I've never used XCode before, so if I can do this, you can too.  Assuming you have SVN and a fairly recent XCode version installed, you can simply hop into Terminal and have a bright, shiny SSHKeychain.app sitting on your desktop within a minute or so:

    mkdir ~/Desktop/src/
    cd ~/Desktop/src/
    svn co http://svn.sshkeychain.org/repos/trunk/ .
    xcodebuild
    mv ./build/Default/SSHKeychain.app ~/Desktop

Drag that application bundle to your favourite applications folder, drag the `src` directory to the trash, and you're good to go.

__UPDATE (Jan 8th, 2007):__ Charles Sprickman dropped me an e-mail today, noting that on his machine, the version of SSHKeychain currently committed into SVN (revision 95) crashes, either on startup, or on wake from sleep.  Since the SVN repository has been more or less inactive since early 2006, I'm not hopefully that an official solution will get rolled into the trunk anytime soon.  Thankfully, [le?ksman][leuksman] has put together a [quick, one-line patch][patch] that solved the problem for Charles, and might solve it for you too.

Given the likelihood of a long wait for an "official" blessing, and given that the modifications were trivial, and haven't crashed on me since I rebuilt it, I've inserted that fix into the instructions here.  In the event that a future build fixes the problem, I'll come back and update this page again.  Until then, happy SSHing.

__UPDATE (Jan 29th, 2007):__ The wait wasn't nearly so long as I expected.  :)  The trunk has been [updated to fix the crasher][changeset_96], so I'm pulling the relevant line from these instructions.

[SSHKeychain]: http://www.sshkeychain.org/ "SSHKeychain: Painless SSH key management for Mac OS X"
[leuksman]: http://leuksman.com/log/2006/12/24/sshkeychain/ "SSHKeychain"
[patch]: http://leuksman.com/mac/keychain/sshkeychain-crash-fix.diff "SSHKeychain: Patch for Crash on Wake issue"
[changeset_96]: http://trac.sshkeychain.org/cgi-bin/trac.cgi/changeset/96 "Changeset for SSHKeychain Revision 96"
---
Alias:
- http://mikewest.org/blog/id/27
Modified: '2006-07-28T09:59:09Z'
Teaser: Brad Choate has a great summary of what looks like a _wonderful_ presentation
    on Subversion best practices, given at OSCON 2006 by Ben Collins-Sussman & Brian
    W. Fitzpatrick
layout: post
tags:
- Subversion
title: "I wish I was at OSCON: 'Subversion Best Practices'"
---
In the same spirit as this week's [revision control article][article], I ran across a [great summary][bestpractices] of an [OSCON presentation entitled "Subversion Best Practices"][oscon] (via: [Brad Choate][brad]).  Normally, I'd just stuff this into my linkroll and leave it at that, but this is really interesting material that's worth talking about.  Ben Collins-Sussman & Brian W. Fitzpatrick's (Subversion developers, and co-authors of ["Version Control with Subversion"][svnbook]) presentation deals with the way Subversion is _actually used_ on large software projects.  Two ideas that jumped out at me:

*   Binary file modifications; or other files that can’t be merged. You’d
    want to lock such files to prevent conflicts.  Property svn:needs-lock
    accommodates this. It checks out the file as read-only, and becomes
    read/write once you lock it for modifications. If you try to lock and
    can’t, it’s because someone else is working on the file.
*   hotcopy versus rsync: Use hotcopy to make the backup to preserve
    consistency, then use rsync on **that**.

I learned some things just by flipping through [Brad's summary of the presentation][bestpractices], and I'm hoping a more detailed report pops up at some point soon, because it looks like there was some great client-side stuff in there that Brad's summary doesn't really give enough insight into.

[article]: http://www.alistapart.com/articles/revisioncontrol "A List Apart: 'I Wonder What This Button Does'" 
[bestpractices]: http://bradchoate.com/weblog/2006/07/27/oscon-subversion-best-practices "Brad Choate: 'OSCON: Subversion Best Practices'"
[brad]: http://bradchoate.com/ "Brad Choate"
[oscon]: http://conferences.oreillynet.com/cs/os2006/view/e_sess/8671
[svnbook]: http://svnbook.red-bean.com/ "Version Control with Subversion"
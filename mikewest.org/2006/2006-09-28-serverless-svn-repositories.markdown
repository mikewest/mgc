---
Alias:
- http://mikewest.org/blog/id/35
Modified: '2006-09-28T14:24:44Z'
Teaser: You don't _need_ a powerful SVN server in order to reap the benifits of version
    control.  This article explains how to set up repositories on any machine you
    have SSH access into.
layout: post
tags:
- HOWTO
- Subversion
title: Serverless SVN Repositories
---
A little known fact about Subversion is that you don't need a special server to get running.  You can actually host Subversion repositories locally on your own computer, or on any remote machine you've got SSH access into.

## Localhosting

You can easily create a local repository on your machine with the `svnadmin` command.  To set up a repository in my home directory, I'd just drop to the command line, and type:

    svnadmin create ~/new_repository
    
That would create the `new_repository` directory under my home, and initialize it for use as an SVN repository.  From there, you can reference it via the `file` protocol, and use it just like any other repository:

    svn import ./my_project file:///Users/mwest/new_repository
    
Easy!

## Remotehosting

If you don't have a dedicated SVN server, or a [decent web host][textdrive], you can gain some of the advantages of a remote repository by creating a local repository, and then uploading it to a server where you have SSH access.  This trick works wonderfully on services like [Strongspace][] where you have nothing more than SSH access, with no opportunity to log in and run `svnadmin`.  

To set up a repository on such a server, I'd create it locally, just like before:

    svnadmin create ~/temp
    
Instead of using it locally with the `file:///` protocol, we'll _upload_ it to our remote server using `scp` (or whatever file transfer mechanism makes sense to you):

    scp -r ~/temp me@my.server.com:/path/to/repository
    
Now, the initialized repository is up waiting for us on the remote server.  We can't use the `file` protocol to get to it anymore, since it isn't part of our local filesystem.  Instead, there's a special protocol for using SVN over an SSH connection: `svn+ssh`.  To run the same import command from above on the remote server, we'd type:

    svn import ./my_project svn+ssh://me@my.server.com/path/to/repository

And there you go.  Easy, straightforward SVN access without any server setup whatsoever.

You lose a little bit of functionality, and it feels a little duct-taped together, but it's a great first-step into the world of SVN, and you can easily migrate to a "real" SVN server when you're ready to use the additional features that enables.

## Resources

*   [Andrew Ho][ho] pointed this technique out on the Strongspace forums, I
    hadn't thought about it at all before his post.
    
*   If you're not interested in typing in a password every time (and who is),
    follow the instructions under the [Set up key based login][key] section of
    this post.  And be sure to read the rest anyway, it's excellent
    information about backing up your system.  You _do_ back up, right?

[ho]: http://andrewho.co.uk/ "Andrew Ho"
[key]: http://blog.invisible.ch/2005/10/06/back-up/ "Back Up"
[textdrive]: http://textdrive.com/ "TextDrive"
[strongspace]: http://strongspace.com/
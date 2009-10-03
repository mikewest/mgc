---
Alias:
- http://mikewest.org/blog/id/17
Modified: '2007-09-07T09:32:20Z'
Teaser: The "Hello World!" of Subversion `post-commit` hooks is the use of `SVNnotify`
    to send e-mails out to a project team every time a new revision is committed to
    the repository.  This is easier than it sounds.
layout: post
tags:
- HOWTO
- Subversion
title: Subversion Post-Commit Hooks 101
---
The "Hello World!" of Subversion `post-commit` hooks is the use of [`SVNnotify`][svnnotify] to send e-mails out to a project team every time a new revision is committed to the repository.

This is easier than it sounds:

1.  Make sure [`svnnotify`][svnnotify] is installed on your system.  I'll
    leave that as an exercise for the reader.

2.  Navigate to your repository's `hooks` directory.  This is almost always a
    directory cleverly named "hooks" right inside the top level of your
    repository:

        cd /Users/mwest/svn/my_repository/hooks/
    
3.  Create a new file called `post-commit`, and make it executable by the
    `www` user.

        touch ./post-commit
        chmod 755 ./post-commit
    
4.  Open up the file you just created, and add the following bit of code:

        #!/bin/sh
    
        REPOS="$1"
        REV="$2"
    
        /usr/local/bin/svnnotify                    \
            --repos-path    "$REPOS"                \
            --revision      "$REV"                  \
            --subject-cx                            \
            --with-diff                             \
            --handler       HTML::ColorDiff         \
            --to            <your e-mail address>   \
            --from          <from e-mail address>
                
    It's all pretty straightforward, so let's take it line by line:
    
    *   The first line is the so-called [`shebang`][shebang] that tells
        the system that the file is a shell script that ought be executed.
        
    *   Next, we set two variables based on the information that
        Subversion passes into the script when it's called.  The
        `post-commit` hook gets two bits of data: the path to the
        repository, and the new revision number that the commit created.
        
    *   Finally, we call [`svnnotify`][svnnotify] to actually generate and
        send a nicely formatted e-mail using the repository path and
        revision number that we gathered earlier.  Make sure to put your
        e-mail address (or list's address) in the last two lines!
            
5.  Do some work, and commit it.

6.  Check your e-mail.

7.  Bask in the glorious glow of a really, really useful tool.

For further reading on the nine hooks provided by Subversion, visit [the "Hook Scripts" section][hook_scripts] of [Version Control with Subversion][svnbook].

[svnnotify]: http://search.cpan.org/dist/SVN-Notify/bin/svnnotify "SVNnotify on CPAN"
[shebang]: http://en.wikipedia.org/wiki/Shebang_(Unix)  "Wikipedia: 'Shebang'"
[hook_scripts]: http://svnbook.red-bean.com/nightly/en/svn.reposadmin.create.html#svn.reposadmin.create.hooks "Version Control with Subversion: Hook Scripts"
[svnbook]: http://svnbook.red-bean.com/nightly/en/index.html "Version Control with Subversion"
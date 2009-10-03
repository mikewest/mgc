---
Alias:
- http://mikewest.org/blog/id/26
Modified: '2006-07-25T06:09:32Z'
Teaser: 'I''ve got an article up on A List Apart, introducing my favourite behind-the-scenes
    development tool: Subversion.'
layout: post
tags:
- Subversion
- Personal
title: I Wonder What This Button Does
---
This morning, I can happily announce the publication of my latest article, ["I Wonder What This Button Does"][article], in the 220th issue of [A List Apart][ala].

The article is a fairly light and non-technical look at my favourite development tool: Subversion.  I hope this introduction to revision control inspires a few of you to dive in and try things out in your own projects.  I think you'll be shocked both at how easy it is to get things going in a revision controlled environment, but also at how _freeing_ it is, knowing that you no longer have to _worry_ about irrevocably breaking something.

[ala]: http://alistapart.com/
[article]: http://alistapart.com/articles/revisioncontrol "A List Apart: 'I Wonder What This Button Does'"

After reading [the article][article], I hope you're looking for a little more information about getting started with Subversion.  There's really no better general-purpose resource than ["Version Control with Subversion"][svnbook].  It's got all the information you'll need to get started, and goes into far more breadth and depth than you'll probably ever need.

Additionally, I've collected a few articles that pinpoint specific pieces of Subversion, detailing methods for tweaking Subversion to meet your needs.  Enjoy!

*   [Working with Subversion File Properties][props]

    Subversion has a very powerful system for associating metadata with the
    files you have under version control. This article describes how to
    automate the process of adding properties to the files you put under
    version control using `auto-props`.
    
*   [Subversion Post-Commit Hooks 101][post]

    Subversion's system of "hooks" allows you to trigger scripted responses to
    your interactions with your repositories.  This article maps out the
    "Hello World" of hooks: using `SVNnotify` to send out e-mails to your 
    project team every time a new revision is committed.
    
*   [“Forbidden” Errors and Subversion Commits][forbidden]

    Since Subversion can run over HTTP, it's easy to cause problems for
    yourself with wayward `mod_rewrite` rules.  This article notes one such
    conflict scenario, and provides an easy solution.
    
*   [Leveraging `mod_rewrite`][leverage]

    Continuing in the `mod_rewrite` vein, you'll want to make sure that the 
    hidden directories that Subversion generates aren't available for general
    consumption.  This article, among other things, shows you how to use
    `mod_rewrite` to block requests for those directories that you'd rather
    the world not see.

*   [Building Subversion (SVN) on Mac OS X][building]

    Dan Benjamin rocks.  This article of his spells out in exacting detail the
    (simple) process of compiling Subversion from source and installing it on
    OS X.  Why would you do this when you could just [grab the
    binaries][download]?  Because it's fun, that's why.

[svnbook]: http://svnbook.red-bean.com/ "Version Control with Subversion"
[props]: http://mikewest.org/archive/working-with-subversion-file-properties
[post]: http://mikewest.org/archive/subversion-post-commit-hooks-101
[forbidden]: http://mikewest.org/archive/forbidden-errors-and-subversion-commits
[leverage]: http://mikewest.org/archive/leveraging-modrewrite
[download]: http://subversion.tigris.org/project_packages.html
[building]: http://hivelogic.com/articles/2006/04/19/svn_on_os_x "Hivelogic: 'Building Subversion (SVN) on Mac OS X'"
---
Alias:
- http://mikewest.org/blog/id/16
Modified: '2006-06-28T07:30:01Z'
Teaser: Subversion has a very powerful system for associating metadata with the files
    you have under version control.  This article describes how to automate the process
    of adding properties to the files you put under version control using `auto-props`.
layout: post
tags:
- HOWTO
- Subversion
title: Working with Subversion File Properties
---
Subversion has a very powerful system for associating metadata with the files you have under version control.  These are described in detail in [the "Properties" section][properties_desc] of [Version Control with Subversion][svn_book], so I won't go into too much detail about them here.

I'll simply note that:

*   `svn:eol-style` is absolutely critical when working with developers on
    multiple platforms, since you'll otherwise almost certainly end up with
    massively useless diffs as line-endings are accidentally changed as files
    hop between OS X, *nix, and Windows.
    
*   `svn:keywords` is quite helpful in terms of tagging files with revision
    data.  I can add something like:
    
        /*
            Last Editor:    $Author$
            Last Edit:      $Date$            
            Last edited in revision:    $Rev$
        */
    
    To the top of my script files to keep track of when they last changed.
    
*   `svn:mime-type` is useful if you have a tendency to browse through your
    repository via HTTP(S).

Properties are cool things.  This article describes how to automate the process of adding properties to the files you put under version control, and how to quickly add properties to the files you've already got in a repository.

Automation
----------

It's a little cumbersome to set properties on each file that you add to your repository.  In fact, if you had to add everything manually, you probably wouldn't use properties at all...  Happily, you can configure Subversion to set properties automatically based on the extension of the file that you're adding.

The first time you run Subversion, it creates a user-specific configuration area.  On OS X and *nix, this shows up as a `.subversion` directory in your user's home directory.  On Windows, it generally creates a directory named `Subversion` in your user's `Application Data` directory.  These areas are described in detail in the [Runtime Configuration Area][user_config] section of [Version Control with Subversion][svn_book]. The remainder of this article assumes an OS X environment.

So, to set up some automation for your SVN commits, simply:

1.  Open up your Subversion configuration file by dropping to a terminal, and
    typing:

        mate ~/.subversion/config
    
2.  Find the line reading `# enable-auto-props = yes`, and uncomment it by
    removing the leading `#`.  

3.  Configure the automatic property settings by skipping down to the line
    reading `[auto-props]`, and adding your settings directly under it.  These
    settings are based on the file name, and use a simple wildcard system to
    match property settings to files.  The rule's general form looks like:
    
        <file definition>   =   <property 1>[;<property 2>[;...]]
        
    If we wanted to set `svn:eol-style` to `native` for all our PHP scripts,
    we'd add a line reading:
        
        *.php   = svn:eol-style=native

    To set more than one property for a given file-type, simply separate each 
    with a semi-colon.  Adding `Date`, `Author`, and `Revision` keywords to
    the PHP definition looks like:
    
        *.php   = svn:eol-style=native;svn:keywords="Date Author Revision"
    
That's all we need to do to enable the automatic setting of properties for various file types.  It's quite straightforward, really.  For the curious, my whole configuration looks like:

    [auto-props]
    *.txt       = svn:eol-style=native;svn:keywords="Date Author Revision"
    *.markdown  = svn:eol-style=native;svn:keywords="Date Author Revision"
    *.textile   = svn:eol-style=native;svn:keywords="Date Author Revision"

    *.php   = svn:eol-style=native;svn:keywords="Date Author Revision"
    *.html  = svn:eol-style=native;svn:keywords="Date Author Revision"
    *.rhtml = svn:eol-style=native;svn:keywords="Date Author Revision"
    *.pl    = svn:eol-style=native;svn:keywords="Date Author Revision"
    *.rb    = svn:eol-style=native;svn:keywords="Date Author Revision"
    *.js    = svn:eol-style=native;svn:keywords="Date Author Revision"
    *.css   = svn:eol-style=native;svn:keywords="Date Author Revision"
    *.sql   = svn:eol-style=native;svn:keywords="Date Author Revision"

    *.png   = svn:mime-type=image/png
    *.jpg   = svn:mime-type=image/jpeg
    *.gif   = svn:mime-type=image/gif
  
It's important to note that this automation happens on a client-by-client basis.  Setting up automatic property assignments on Developer A's computer does nothing to ensure that they're set up on Developer B's machine.  To get consistently set properties for all developers working in a repository, you'll have to ensure that each developer has the same `auto-props` rules set up.

You could also take care of the issue at the server level by setting up a pre-commit script.  [An example of such a script is available][precomit_hook] from the Subversion guys, but left completely up to you to decipher.  :)
  
But what about an existing repository?
--------------------------------------

The automation described above takes care of files we add to a repository, but what about all the files that we've already got under version control?  The only way to get properties set on these files is to use `svn propset` to add each property manually.  

That said, manually setting properties on all your existing files doesn't have to be _completely_ manual.  I've put together a quick ruby script that can be used to replicate my property setup, or modified to meet your needs: 

1.  Make sure your working copy is up to date by navigating to the directory
    in the terminal, and typing:
    
        svn up
        
2.  While still in the working copy's directory, type:

        ruby
    
    to open the ruby interpreter.
    
3.  Paste in the script as follows (or modify it to meet your needs):

        [
            # Setting script-type file properties
            "php","rb","pl","cgi","js",
            # Setting text-type file properties
            "txt","markdown","textile",
            # Setting HTML/CSS file properties
            "html","rhtml","css",
            # Setting SQL file properties
            "sql",
            # Setting image file properties  
            "gif","jpg","png"
        ].each do |extension|
            Dir.glob("**/*.#{extension}").each do |filename|
                case extension
                when
                    "php","rb","pl","cgi","js",
                    "txt","markdown","textile",
                    "html","rhtml","css",
                    "sql"
                then
                    puts "Setting eol-style, keywords on #{filename}"
                    `svn propset svn:eol-style native "#{filename}"`
                    `svn propset svn:keywords "Date Author Revision HeadURL ID" "#{filename}"`
                when "gif" then
                    puts "Setting mime-type on #{filename}"
                    `svn propset svn:mime-type 'image/gif' "#{filename}"`
                when "jpg" then
                    puts "Setting mime-type on #{filename}"
                    `svn propset svn:mime-type 'image/jpeg' "#{filename}"`
                when "png" then
                    puts "Setting mime-type on #{filename}"
                    `svn propset svn:mime-type 'image/png' "#{filename}"`
                end
            end
        end

4.  Hit `return` to add a line break after the last `end`, then type
    `control-d` to execute the script.
    
5.  Once the script's finished running, commit the new properties back to your
    repository with a memorable commit note:

        svn commit -m "* Set properties for all known file-types"

Easy!

[properties_desc]: http://svnbook.red-bean.com/nightly/en/svn.advanced.props.html "Version Control with Subversion - Chapter 7. Advanced Topics :: Properties"
[user_config]: http://svnbook.red-bean.com/nightly/en/svn.advanced.html#svn.advanced.confarea "SVN Book: Chapter 7. Advanced Topics :: Runtime Configuration Area"
[svn_book]: http://svnbook.red-bean.com/ "Version Control with Subversion"
[precomit_hook]: http://svn.collab.net/repos/svn/trunk/contrib/hook-scripts/check-mime-type.pl
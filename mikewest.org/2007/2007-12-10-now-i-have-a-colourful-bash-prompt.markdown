---
Alias:
- http://mikewest.org/blog/id/83
Modified: '2007-12-12T16:08:41Z'
Teaser: My jealousy of Adriano's pretty `bash` prompt has been assuaged by the construction
    of my own, _prettier_ and _more functional_ prompt.  So there!
layout: post
tags:
- Personal
title: Now I have a colourful `bash` prompt
---
After seeing [Adriano Castro's][adriano] presentation last week on [R3][], I was inspired both to play a little bit with R3 itself (cool!), and just as importantly, to finally taking a few minutes to customize my bash prompt.  His brightly coloured prompt was full of information and life, mine not; I'd just done an entire presentation on [loving the terminal][love], so this deficit was particularly shameful.

So, I spent a few minutes this evening toying around with things, and ended up with this:

<img src="http://mikewest.org/images/4.png" alt="My newly colourful and lively Terminal window." height="267" width="575">

Ah, lovely; it's _really_ simple to do for yourself.

Here's how it works
-------------------

The terminal prompt is controlled via the `PS1` environment variable in `bash`.  You simply need to construct a particular string, and assign it to that variable by adding a line to your `.bash_login` file like the following:

    export PS1="<your formatting string goes here>"

This prompt in particular is:

    export PS1="\[\033]2;\u@\h\a[\[\033[37;44;1m\]\t\[\033[0m\]] \[\033[32m\]\w\[\033[0m\] \$ \[\033[0m\]"
    
This breaks down into:
    
    \[\033]2;\u@\h\a                    #    which writes the `user@host` string
                                        #    into the terminal window's title bar
                    
    [\[\033[37;44;1m\]\t\[\033[0m\]]    #    which writes (in white-on-blue)
                                        #    `[HH:MM:SS]` at the beginning of
                                        #    each line, so that I know exactly
                                        #    when I executed a command
    
    \[\033[32m\]\w\[\033[0m\]            #    which writes (in a pleasant green) 
                                        #    the current working directory
                                    
    \$                                    #    which writes "$" if I'm logged in as
                                        #    a normal user, and "#" if I'm logged
                                        #    in as `root`.
    
To build your own, I'd suggest taking a look at [Daniel Robbins' "Prompt Magic" article on IBM developerWorks][ibm].  It's a well put-together article that walks you through the whole, terrifically geeky process.

Update
------

If you happen to have some strange text-wrapping problems, [I might have a solution for you][solution].  In a nutshell, end your prompt with a colour code, and use `\033` instead of `\e`.  I've updated this page accordingly; see ["Solving strange text wrapping problems in bash"][solution] for more details.

[adriano]: http://adrianocastro.net/about/
[R3]: http://sourceforge.net/projects/rthree "R3: A neat looking templating system, full of support for l10n, i18n, and many other letters and numbers."
[love]: /archive/presentation-love-the-terminal "Mike West: 'Love the Terminal'"
[ibm]: http://www.ibm.com/developerworks/linux/library/l-tip-prompt/ "Tip: Prompt Magic"
[solution]: http://mikewest.org/archive/solving-strange-text-wrapping-problems-in-bash "Mike West: 'Solving strange text wrapping problems in `bash`'"
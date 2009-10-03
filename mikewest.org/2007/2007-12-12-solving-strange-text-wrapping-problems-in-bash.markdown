---
Alias:
- http://mikewest.org/blog/id/84
Modified: '2007-12-12T16:01:38Z'
Teaser: I started having strange text wrapping problems after implementing implementing
    the beautifully colored bash prompt I discussed on Monday.  After fidgeting around
    a bit, I think I've come up with a solution.
layout: post
tags:
- Personal
title: Solving strange text wrapping problems in `bash`
---
I started having strange text wrapping problems after implementing implementing the beautifully colored bash prompt I discussed on Monday.  After fidgeting around a bit, I think I've come up with a solution.  In short, I changed two things:

*   I'm using `\033` instead of `\e` when defining the colors.
*   I'm _ending_ my prompt with a color code, even though it's redundant.

I also completely refactored the way I'm building the prompt, which makes it easier to extend it to do even more interesting things.  For example, I spend almost all my time working in subdirectories below `/my/project/directory`.  There's no reason to display that in the prompt, it's simply wasting space.  A quick `sed` command can take care of this for me, replacing `/my/project/directory/news/uk/whatever` with `.../news/uk/whatever`.  That's much easier for me to read, and makes me happy.  So my prompt now consists of:

    alias ypwd="pwd | sed -e 's#/my/project/directory#...#'";

    set_my_prompt() {
        local OPEN="\[";
        local CLOSE="\]";
        local BLUE="${OPEN}\033[1;37;44m${CLOSE}";
        local GREEN="${OPEN}\033[32m${CLOSE}";
        local WHITE="${OPEN}\033[0m${CLOSE}";
        export PS1="\[\e]2;\u@\h\a[\[\033]2;\u@\h\a${BLUE}\t${WHITE}] ${GREEN}\$(ypwd)${WHITE} \$ ${WHITE}";
    }
    set_my_prompt

The magic part happens inside of `\$(...)`.  That structure acts just like the backtick (`` ` ``) on the shell: anything inside will be executed, and it's result returned as a string.  In this case, we execute the `ypwd` alias I set up at the beginning of the script, which pushes the result of `pwd` through a `sed`-based regex.  That result is then used inside the prompt; you can do _really_ interesting things with this concept.
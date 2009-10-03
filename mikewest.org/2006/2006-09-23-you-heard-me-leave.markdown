---
Alias:
- http://mikewest.org/blog/id/33
Modified: '2006-09-23T09:23:05Z'
Teaser: '`leave` is a brilliant little utility that annoys you at a pre-specified
    time until you log out.'
layout: post
tags:
- HOWTO
title: 'You heard me: `leave`!'
---
Normally, I'd foist this off into a sidebar link, but this discovery deserves a little more: it's that brilliant.

I was reading [UNIX productivity tips][unix], and ran across the single greatest time-management command I've seen.  Running [`leave`][leave] asks "When do you have to leave?"  You enter a time in HHMM format, and `leave` then pings you 5 minutes before, reminding you that you wanted to leave.  Then it pings you the minute before.  Then it pings you every minute until you either log out, or kill the `leave` process.  This is brilliant stuff!

    $ leave
    When do you have to leave? 1830
    Alarm set for Fri Aug  4 18:30. (pid 1735)
    $ date +"Time now: %l:%M%p"
    Time now: 6:24PM
    <one minute passes>
    $
    <system bell rings>
    You have to leave in 5 minutes.

The best part?  It's built into OS X.  Thank God for BSD, eh?  :)  The [productivity tips article][unix] is worth reading anyway, if only for gems like sorting your command-line history by command, by popularity:

    $ history|awk '{print $2}'|awk 'BEGIN {FS="|"} {print $1}'|sort|uniq -c|sort -r
        103 svn
        100 cd
         75 ls
         52 exit
        ...
          1 cp
          1 chmod
          1 ack
    $

Neat, eh?

[unix]: http://www-128.ibm.com/developerworks/aix/library/au-productivitytips.html?ca=dgr-lnxw07UNIX-Office-Tips#listing4
[leave]: http://www.hmug.org/man/1/leave.php "man: leave"
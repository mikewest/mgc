---
layout:     post
title:      "I think I've bricked my iPhone"
slug:       "i-think-ive-bricked-my-iphone"
aliases:
    - http://blog.mikewest.org/post/105388319
    - http://blog.mikewest.org/post/105388319/i-think-ive-bricked-my-iphone
tags: 
    - iphone
    - brick
    - firmware
    - beta
    - iphone3
Teaser:  "I tried to install the latest iPhone 3.0 beta firmware on my decidedly-not-3G iPhone last night, and failed miserably."
---
I tried to install the latest iPhone 3.0 beta firmware on my decidedly-not-3G iPhone last night, and failed miserably.

I'm currently stuck on a pink "connect to iTunes" screen, and each new try at restoring the beta firmware throws "unknown error" 1012.  Trying to roll back to the current stable firmware doesn't work either: it throws a 1604 error.

I'm sifting through forums and the like at the moment, and I'll probably end up at the Apple Store at some point in the relatively near future so that a Genius can look at my phone, do the exact same things I'm doing now, and then shrug hopelessly and ask for my credit card.  *sigh*

I did see some amusing error messages in the console, though:

    5/9/09 9:35:38 AM com.apple.usbmuxd[485] MobileDevice:
      _MobileDeviceConnect_locked: This is not the droid you're looking for
      (is actually com.apple.mobile.restored). Move along, move along. 

    5/9/09 9:35:38 AM com.apple.usbmuxd[485] MobileDevice:
      _MobileDevicePairWorker: Pair worker (0x0xb0092000) could not connect to
      lockdownd: kAMDWrongDroidError 

`WrongDroidError`.  Ha!

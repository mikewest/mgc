---
layout: post
title:  I'm on Technikwürze
tags:
    - technikwürze
    - podcast
    - german
    - webdev
    - google
    - chrome
    - chromewebstore

Teaser:
    I sat down with Technikwürze's Marcel Böttcher way back at the beginning
    of February to talk about the exciting new release of Chrome 9 to the
    stable channel, and a few other bits and pieces of the Chrome ecosystem.
    That interview (in German) is just now seeing the light of day as
    Technikwürze 178.  After listening to it last night, I think it generally
    went pretty well, modulo a few small mistakes on my part.
---
I sat down with Technikwürze's Marcel Böttcher way back at the beginning of February to talk about the exciting new release of Chrome 9 to the stable channel, and a few other bits and pieces of the Chrome ecosystem. That interview (in German) is just now seeing the light of day as [Technikwürze 178][link].  After listening to it last night, I think it generally went pretty well.

I got a good chance to talk about the (then shiny and new) world of WebGL. It's become hugely popular in the meantime, and is supported with GPU acceleration across the board in modern browsers with generally excellent performance characteristics.  Libraries have sprung up like [Mr.doob][mrdoob]'s amazing [three.js][threejs] that make working with WebGL easy and fun. [ro.me][rome] is a great example of what can be creatively accomplished with the technology, and I'm really excited about seeing where the web will take things that it has full-speed access to OpenGL goodness from JavaScript.

I touched on the [Chrome Web Store][cws], which has had a very successful launch in the States, and is ramping up (albeit slower than I'd like) for a full international release later this year. You can see some of the results of that effort already, as the US store has been fully localized to make it accessible to users no matter what language they speak, and it's only going to get better as the year progresses.

I was able to highlight the focuses of Google's engineering center in Munich ([we're hiring!  send me CVs!][hiring]), especially those of the Chrome team that's doing exceptional work on privacy and enterprise features of the platform. I touched on some of the thought behind Chrome's release process, autoupdates, and the extension API framework. We dove briefly into some of the privacy-related work Google has done, highlighting [Keep My Opt-outs][kmoo] which we released in January, and pointing towards some future extension APIs that will enable developers to bring some great privacy protections (think TorButton and NoScript) to the Chrome platform.

These are all relatively timeless bits and pieces that I'm glad I was able to share, and I hope that listeners find it interesting, even if it's all framed in a context that's 4 months too late.  I'm a bit disappointed that it's just coming out now rather than back then when it would have been a bit more relevant.  It's amazing to see what's happened in the last 4 months (IE9 and FF4 have both been released in the meantime, we've pushed two new stable releases of Chrome, I/O happened, etc.), and pushing this interview out four months later simply doesn't reflect the things that I'd like to be focusing on now.  It sounds like I'm talking about quite old things as though they were new, which is a bit confusing for everyone involved. I'm hopeful that we can get together again in the relatively near future to talk about some of the things that are interesting today and tomorrow.

## Things I'll say differently next time.

First and foremost, listening to myself speak German is a painful experience. I mean, it's tough to listen to myself speak English; listening to myself try and fail to wrap my tongue around a few phrases (repeatedly) is a bit embarrassing. *sigh* I'll get better at it.

I'd also like to make two corrections. I'm not sure what one would call "errata" for a podcast, but that's what I'll outline here.  Let's start with the one or two things I said that jumped out at me as being clearly idiotic, even back in February:

1. I sold some of my coworkers short: of course Google has lobbyists in Berlin, but that's not at all the extent of our efforts there. Among other things, there's a large cooperation with academic institutes there to [set up a research institute focused on internet and society][institute].

2. I talked about Native Client as something that would trigger a review when uploading an item to the Chrome Web Store. I meant to refer to NPAPI plugins that can execute native code on your computer. If you write a Chrome extension or packaged application that relies on an NPAPI plugin, you'll go through a review process to verify that someone's responsible for the code, as there's no practical limit on what such a plugin can do to a user's computer (and we flag it as such in the store as being able to access "All data on your computer and the websites you visit"). These types of plugins also won't run on ChromeOS, full stop.

    While Native Client is in your head, however, I'll note that it is right now in Chrome behind a flag, and there are indeed projects written using it ([NaClBox][] being the most recent brilliant example that I'm aware of), but it's not something for  the general public at the moment. It's experimental. An amazing piece of technology that's in earnest development, but experimental. The Native Client team gave a talk at I/O (["Beyond JavaScript: Programming the Web with Native Client"][naclio]) that's worth watching if you're interested in the current status of the project.

    I also mentioned casually that Native Client supports not only C/C++ but also Java and maybe Python. Again, I should have referred to NPAPI plugins (which actually _do_ somewhat support Python via projects like [pyplugin][]). Native Client is C/C++ only at the moment. Though there's no theoretical reason the framework _couldn't_ work foremost other languages, there's no compiler, nor do I know of any effort underway to write one.

## Updates.

1. The market share numbers [from February][share] which I quoted are, of course, out of date. At I/O we talked about reaching 160 million users, and [StatCounter][stats] puts Chrome usage in their slice of the internet at right around 20% at the end of May. What I wish I had mentioned is that these numbers are nice to throw around in conversation, but the most important thing for a particular application is _its own_ demographics. Look at _your own_ logs to determine the distribution of browsers in _your_ audience.

2. The WebM project has since submitted an update to the bitstream specification (["VP8 Data Format and Decoding Guide"][vp8]) as an Internet Draft to the [IETF][].

3. With regard to the application metadata format that the Chrome Web Store uses, Mozilla's implementation of a similar idea [is progressing nicely][mozilla], but there's still a gap between the functionality it offers and the model Chrome is running with at the moment. Discussion regarding those differences, and the direction in general, are happening in public on a variety of lists ([mozilla-labs][labslist] for example).

4. Chrome's quick, multi-channel release cycle has been more successful than I thought possible. Firefox [has adopted a similar system][ffrelease], and Microsoft is [already pushing out "platform previews" of IE10][msrelease]. This is just plain good for the web.

## And that's about it...

This was the first time I've participated in a podcast of any sort. It was a good experience, modulo the gap between recording and publication, and I look forward to talking into a microphone at some point again. Thanks for inviting me onto the show, liebe Technikwürzler. Till next time... :)

[link]: http://technikwuerze.de/podcast/technikwuerze-178-im-hause-google/
[mrdoob]: http://mrdoob.com/
[threejs]: https://github.com/mrdoob/three.js
[cws]: https://chrome.google.com/webstore
[rome]: http://ro.me/
[hiring]: http://www.google.de/intl/en/jobs/germanylocations/munich/
[institute]: http://www.thelocal.de/sci-tech/20110216-33141.html
[NaClBox]: http://www.naclbox.com/
[naclio]: http://www.google.com/events/io/2011/sessions/beyond-javascript-programming-the-web-with-native-client.html
[pyplugin]: http://pyplugin.com/
[share]: http://arstechnica.com/web/news/2011/02/chrome-takes-10-usage-share-ie-continues-to-haemorrhage.ars
[stats]: http://gs.statcounter.com/
[vp8]: http://tools.ietf.org/html/draft-bankoski-vp8-bitstream-01
[IETF]: http://www.ietf.org/
[webmplugin]: http://tools.google.com/dlpage/webmmf
[mozilla]: https://developer.mozilla.org/en/OpenWebApps/The_Manifest
[labslist]: https://groups.google.com/forum/#!forum/mozilla-labs
[ffrelease]: http://blog.mozilla.com/blog/2011/04/13/new-channels-for-firefox-rapid-releases/
[msrelease]: http://ie.microsoft.com/testdrive/
[kmoo]: https://chrome.google.com/webstore/detail/hhnjdplhmcnkiecampfdgfjilccfpfoe

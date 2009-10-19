---
layout:     post
title:      "The Value of Measurement"
slug:       "the-value-of-measurement"
aliases:
    - http://blog.mikewest.org/post/105891396
    - http://blog.mikewest.org/post/105891396/the-value-of-measurement
tags: 
    - testing
    - webdev
    - a/b
    - prototyping
    - lukasmathis
    - mathis
    - ignorethecode
Teaser:    "While I agree fully with many of the conclusions Lukas Mathis draws in an excellent essay on the recent Google/Douglas Bowman split, a few bits deserve further study.  In general, engineers understand and can relate well to automated A/B testing, and designers understand and can relate well to more personal usability testing.  The two are, however, not the same, don't provide the same data, and ought not be conflated."
---
While I agree fully with many of the conclusions Lukas Mathis draws in an [excellent essay on the recent Google/Douglas Bowman split][mtui], a few bits deserve further study.  Lukas hits the central problem squarely on the head in his [footnoted claim][fn] that measurement isn't Google's problem, rather the lack of a design team capable of _balancing_ those measurements against other concerns.  I'd elaborate on this claim, and argue that the _kind_ of testing being discussed matters.  In general, engineers understand and can relate well to automated A/B testing, and designers understand and can relate well to more personal usability testing.  The two are, however, not the same, don't provide the same data, and ought not be conflated.

[fn]: http://ignorethecode.net/blog/2009/05/10/measuring-the-user-interface/#fn:google
[mtui]: http://ignorethecode.net/blog/2009/05/10/measuring-the-user-interface/ "Lukas Mathis: 'Measuring the User Interface'"

## What do A/B tests test? ##

"41 shades of blue" has become a catchphrase for those who see Google's approach as flawed; this seemingly mindless insistence on A/B testing as the sole arbiter of a design's "value" seems to me to be the point Bowman most objected to.  I have a good amount of sympathy for that viewpoint.

A/B testing is, as Lukas rightly points out, hugely valuable to any team focused on improving an established system through a series of small, iterative changes.  Serving a green button in place of a red button to 1% of your users, and discovering a statistically meaningful shift in usage patterns distinctly tells you something about your audience that no amount of surveying could.  Ignoring these user's _claims_ while carefully observing their _behavior_ can reveal interesting and useful bits of data about the way they interact with the interfaces you've built.

Especially with an audience the size of Google's, you'd have to be crazy to write off the value of building small changes incrementally, and testing those piecemeal improvements against a subset of your audience.  You'll discover that one small tweak or another has an impact, and feed that back into your design process.  Continually testing each iteration of tweaks against your audience will continually improve the quality of your pages and the overall user experience:  It's a virtuous circle of exactly the kind I'd like to encourage.

I absolutely stand behind the core of Lukas' essay: "Design is not held back by data, design is refined and perfected by data."

## The Downside ##

A/B testing is appealing because it's obvious.  It's absolutely clear what needs to be done, the results are generally clear in the direction they lead (it's either "A" or "B"), and if you have the tooling in place to make it easy (Google does), it's easy to see how it can become a central part of the way you work.

That said, you'd be just as crazy to make _every_ decision dependent on this sort of testing.  In order to isolate the effect of a change, as a true engineer-statistician ought demand, broad and sweeping suggestions should be broken down into testable components, and each served across a just-wide-enough swath of audience to return meaningful data while minimizing risk.  An insistance on A/B measurement of each change, no matter how small, means that _everything_ you measure will be "trivial" in the way that the most glaring examples of "Googlism" have been: shades of colour, or widths of border.  Only _trivial_ changes are _testable_ changes, everything else is fraught with layers of uncertainty: "Was it the new 3px border, or the new position of the button, or the completely new logo that drove traffic?" "Who knows, let's do more tests!"

Moreover, it's easy to see how a reliance on A/B testing might lead to a culture of extreme risk-aversion.  When you have a ton of data at your fingertips that help guide your decisions, your worst enemy is the black hole that a new untested/untestable/unmeasured change represents.  If a change isn't testable/tested, it's unknown.  Unknown changes might be catastrophic.  Catastrophic is bad.  Therefore untested/untestable/unmeasured changes are, in the absence of _evidence_, bad.

I suspect that Bowman isn't at all exhorting his fellow designers to abstain completely from testing; I'd interpret his remarks as cutting against an _over-reliance_ on A/B testing.  Within a primarily A/B framework, I'd consider it impossible to do _real_ design work that reevaluates a product's decisions from first principles.  Where can you begin?  What interesting set of changes can you propose when each has to be buildable in a way that allows testing against the current status quo of the product as a baseline?

I believe that Bowman is right to worry about missing "truly great" designs by getting bogged down in continual, iterative improvement of a mediocre design.  Getting wrapped up in asymptoticly approaching the _best_ shade of the _best_ button you can possibly create, and backing it all up with testing, might blind you to the fact that the action might really be better represented as a slider.  Or a dropdown box.  Or that it's completely wrong and would be better reworked entirely.

Lukas quickly notes one answer in passing.  I think it deserves more attention.

## Usability Testing and Prototypes ##

In an [interview with Salon in 2008][salon], Leander Kahney said:

<blockquote>Steve Jobs doesn't wake up one morning and there's a vision of an iPhone floating in front of his face. He and his team discovered it through this exhaustive process of building prototype after prototype.</blockquote>

Each of these prototypes functioned in one way or another, and each was put into someone's hands to play with.  This methodology of testing (especially for _new_ designs) is simply not measurable in the same way as determining whether a green link on a pre-existing page is clicked on more or fewer times than the same link in red.  A/B testing _is not_ usability testing sweeping new prototypes; it has a different purpose, and gives different data points.

Prototyping new solutions to problems, and putting them in front of real people as quickly as possible, is probably the best way to make sweeping changes while maintaining some semblance of confidence that you're moving in the right direction with regard to the audience you're aiming for.

This sort of guerilla testing designs on friends and acquaintances with something like [Silverback][] absolutely ought to be part of the design process, early and often.  Getting real feedback from people who _use_ the system you're trying to improve is critical to designing and implementing an interface that makes the right tradeoffs in the right places.

In short, I'm highly sympathetic to the [Nielsenian notion][nielsen] that users _can't_ and _won't_ tell us what they want, that we need to examine their clicks in order to measure the impact of the changes we make.  However, I think that notion needs to be tempered insofar as _never_ asking a user what she thinks is incredibly dangerous because it never allows you to break out of a certain comfort zone surrounding the product as it stands.

So.  Test.  Early, often, and persistently.  Testing gives you immense amounts of data, and data is invaluable to your designs and implementations.  But don't limit your tests to those best expressed in a spreadsheet.  Prototyping, and asking actual users actual questions, should be a part of your creative process.

Finally, to reiterate Lukas' point: you aren't Google.  Even if they're dangerously-reliant on A/B testing, you almost certainly aren't A/B testing _enough_.  I know I'm not...

[salon]: http://machinist.salon.com/blog/2008/06/09/leander_kahney/index.html
[silverback]: http://ignorethecode.net/blog/2008/08/04/silverback/
[nielsen]: https://twitter.com/iA/statuses/1752478005

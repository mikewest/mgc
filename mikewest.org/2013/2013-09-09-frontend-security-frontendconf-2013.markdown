---
layout: post
title: "Frontend Security - Frontend Conference, Zürich 2013"
tags:
  - contentsecuritypolicy
  - csp
  - hsts
  - https
  - xss
  - security
  - transcript
  - contentinjection
  - presentation

Teaser:
  "Last week, I was in Zürich to chat about client-side security. Here, I've
   wrapped up an annotated transcript, along with the slides and video. I'm
   pretty happy with how the talk turned out: I think it's a good representation
   of what I think is important in frontend security, and worth your time to
   peruse."
---
Last week, I was in Zürich attending [Frontend Conference][fec13] (talks and
slides linked up [on Lanyrd][fec13lanyrd]), and had the opportunity to chat with
the folks there about client-side security. [Content Security Policy][csp],
shockingly, was central to the discussion.

In the interests of making the presentation as accessible (and indexable) as
possible, a full transcript of the presentation is below, along with an embed of
the video and slides.

Video
-----

<iframe
  width="606"
  height="455"
  src="https://www.youtube.com/embed/fYjO5pIY1mY?rel=0"
  frameborder="0"
  title="Video: 'Frontend Security' - Frontend Conf, Zürich 2013"
  allowfullscreen="allowfullscreen"></iframe>

The video is 48m long, fully captioned, and [up on YouTube for your viewing
enjoyment][video] (I swiped the [original conference feed from UStream][original]
(with permission, thanks!)).

Slides
------

<iframe
  src="https://speakerdeck.com/player/c67a4f30f3a5013025764a2e0c7b14d8"
  allowfullscreen="true"
  mozallowfullscreen="true"
  webkitallowfullscreen="true"
  frameborder="0"
  title="Slides: 'Frontend Security' - Frontend Conf, Zürich 2013"
  width="606"
  height="516"></iframe>

The [slides are up on Speaker Deck][slides] (which is awesome), and I actually
used Speaker Deck to _present_ the slides from someone else's laptop since my
computer decided not to connect to the conference's projector. I love you,
Speaker Deck!

Transcript
----------

**>> MIKE WEST:** Thank you very much.  Before I get started, I'd like to say thanks to
[Frontend Conf][fec13] because this is the first conference I've ever been at
where the -- where everything was online less than a day after the speeches.
In fact, speeches from this morning are already online.  I think it's absolutely
incredible.  Can you give the guys up there a round of applause?  Because
that's... 

[applause]

Blows me away.

So my name is Mike West.  I work at Google on Chrome.  I do some stuff in Blink.
I do some stuff in Chrome.  If you have any questions about that, I'm happy to
answer them. What I've been doing recently has had a lot to do with security.

I'm going to talk about a couple of things today that I find really important.
The slides are at [this URL][slides], I'm actually using them right now
because my computer decided that it didn't want to hook up to the network.  So
you can follow along with me on SlideShare.  Sorry, on Speaker Deck.  I stopped
using SlideShare for good reasons, and I will tell you about them later.  I'm on
[Twitter][].  I'm on [Google+][].  You can find [my website][mikewestorg] that I
update maybe once to twice a year.  It's very exciting, very good stuff indeed.

So my brain is absolutely full.  I've been to a lot of talks over the last two
days.  This is the last talk on the last day.  I think if I tried to stuff
anything else in my head, it would explode.  I suspect that many of you are
feeling the same way. So I want to give you the one thing that I want you to
remember right now, up front, before you forget everything that I'm going to
say.

This is [an article talking about Content Security Policy][csp].  What is
Content Security Policy?  Why should I care?  I'll tell you in a minute.  But
don't worry about that right now.  Open the article, put it somewhere, find it
later.  It's something that I really think you should read.  It's something
that's well worth your time and it's written by a very handsome man.  So I
think it's really something that would be worth your time to play around with.
It's on HTML5Rocks, by the way. Does anyone know HTML5Rocks?  Does anyone not
know html5rocks.com?  Excellent. That's very good.  They're very smart people
on my team that write lots of good articles for the site.  I really think that
if you don't know about it and many if you do, it's well worth your time to take
a look at.

So how many of you have seen a page that looks like this, in either Chrome or
any other browser?  That's not enough of you.  You people are browsing really
boring websites.  You need to go into a -- just completely different corner
of the web.  You're not going to see this from cnn.com, right?  You've got to
really look for it.  This is a malware alert brought to you by the magic of
[SafeBrowsing][].  SafeBrowsing is a service that Google has put together
that's used by Chrome, used by Firefox, and a variety of other services.  It
gives us the ability to relatively rapidly show users that they could be doing
something dangerous, that we compare a list of hashes to the website that
they're about to visit.  If there's a match then we can inform the user that
they might not want to visit the site.  The site is something that we've
identified as being persistently malicious.  That is every time users go to the
site, people try to load malware onto their computers or try to direct into
phishing sites, or things along these lines.  It's persistent.  Meaning that
for every user, they're seeing this sort of behavior.

And then we've gotten really good at detecting these sorts of behaviors.  We've
gotten really good at detecting the websites that are always going to do you
harm.  What we're not so good at is detecting the more transient attacks.
Detecting attacks like content injection that only affect a single request or a
single subset of users, or perhaps only users that are logged in to a particular
site, only a particular user.  We're not that great in detecting it because
we -- when we crawl the web, we don't see these sites, because this site are
usually distributed via e-mail or via Twitter or via a wide variety of other
mechanisms by which people try to trick you into clicking on links that will do
you harm.

I mentioned -- I mentioned content injection.  Content injection is a
broad term that -- of which XSS is a specific variant.  XSS means cross-site
scripting. And generally speaking, this means that an attacker is able to trick
a server into sending code that it didn't mean to.  That is, instead of only
delivering the JavaScript that actually makes up your application.  Your server
is tricked into also delivering some sort of malicious code, code that does harm
to a user or exfiltrates their data without them even knowing about it which is
actually even worse.

Why is XSS problematic?  Generally speaking, XSS is one of the most prevalent
problems on the web.  Almost every website will have an XSS flaw of one sort
or another at one time or another, even Google.  Given that, why is it
dangerous?  What can it actually do?  What can a -- an attacker do when
they can execute code in the context of your website?

To understand why it's important, you have to understand the concept of an
[origin][].  An origin is a pairing of a scheme, a host, and a port.  That is
`http`, `example.com`, `80`. or `https`, `google.com`, `443`.  Those are
distinct origins.  And because they're distinct origins, they should and
must not have accessed to each others data. `example.com` must never have
access to `google.com`'s data.  And the browser can actually do a relatively
good job of enforcing this sort of restrictions.

There's a policy known as the Same-Origin Policy which basically means that
everything within the context of your origin has access to all of the data for
that origin.  It can access cookies, it can access `localStorage`,
`sessionStorage`, you name it.  Anything you are storing locally using any of
the wide variety of HTML5 mechanisms that are out there is accessible to any
and all code that runs within the context of your origin.  In other words, the
origin boundary is the only boundary that the browser can very effectively
enforce.

It is however the case that we generally includes script from all over the place
into our origins.  The browser allows this.  The browser really likes
JavaScript.  And basically any JavaScript it sees, it's going to execute. It
just loves JavaScript.  So every time it gets a chance to execute anything, it
executes, which is problematic, right?

What's the difference between these two `script` tags?

Exactly right.  There is no difference whatsoever.  If both of these `script`
tags are included on a page, the browser is going to go, "Yay, JavaScript.",
grab them both, execute them as fast as it possibly can because Chrome's all
about speed and bad things are going to happen, right?  Now, visually we can
inspect these two scripts.  We can say the first one is awesome, the second
one not so much.  Perhaps, I want to execute the first one that was actually
part of my application.  The second one, I have no idea how it got to my page,
I didn't write that.

Well, it might've gotten on your page like this, right?  If you're using PHP
or any other wide variety of other templating languages and you don't properly
escape output, if you just say "Hello {$name}!", and then accept whatever name,
the user gives you as their name then you're in trouble, right?  Because the --
if the user gives you a name of `<script>beEvil()</script>` and you just
blindly write that out, then you're doing yourself of disservice.

This is how a lot of cross-scripting attacks happen.  There are a lot of
variants on this, so it's not always the case that it's just coming from a GET
parameter or a POST parameter.  Things can be stored locally, things can be
reflected from various pieces of the DOM.  So attackers are really, really
clever about finding holes in your site and exploiting them.  How many people
have dedicated members of their team working on security?  That's kind of what I
suspected.

I guarantee you that if you had any sort of high value data on your website or
even medium value, even low value data on your website, there are people that
are much more interested in getting access to that data then you are in
protecting it.  Because generally speaking, your team's responsibility is to
build amazing new features and to build amazing new experiences for your users.
It's kind of assumed that you're doing security work.  And the security work is
not really ever part of your goals for a quarter.  Your goal for the quarter is
yo build this amazing new page.  It's not to make sure the other pages didn't
break in the meantime.  That should probably change, but we'll talk about how we
can mitigate the effects.

Happily, this is a absolutely trivial problem to solve. All you have to do is
perfectly escape every piece of output that you put on your site. Every piece.
Pieces that come from you and pieces that come from users.

You also have to perfectly escape it for the context in which this output will
find itself.  Here's a relatively an exhaustive list of different context in an
HTML page, you have a color exported into a `style` tag, you have a name
directly in a paragraph tag, you have a URL that's put directly into an
attribute of an HTML element, you have an ID that's put directly into script,
and you have some debug information that's put into a comment.

The rules for each of these contexts are different.  For example, inside of a
comment, two dashes will close the comment and everything else will be rendered.
Two dashes of course have no effect whatsoever inside a paragraph tag, but if
you open a script tag inside of paragraph tag then you're in trouble.  So you
need to understand the rules for each of these contexts and you need to
perfectly escape all information that you export into this contexts.

It is, honestly, trivial.

However, we are really bad at trivial things, apparently, if you look at the
history of the web.

Has anyone heard of OWASP?  O-W-A-S-P?  Excellent.  OWASP is an interesting
organization that does a lot of security research and lots of security
trainings.  They have -- as an example of the kinds of cleverness that
people can come up with for exploiting things in websites, this is an XSS
filter evasion cheat sheet][owaspxss].  It's a little bit old, it's not really
new, it hasn't really been updated since like, I don't know, 2012 or so, 2011.
But there's a lot of really interesting things in here that might make you think
again about the mechanisms by which you are filtering data that's going out to
your websites.

[Long UTF-8 encode without semicolons][owaspxss1].  Did you know that you can
have UTF-8 entities put in to your site without semicolons?  So if you're
checking for ampersand, semicolon then you're kind of screwed because you don't
need those semicolons.  Ha ha, hurray for HTML.

Has anyone heard of [JSFuck][]?

**>>** I have.

**>> MIKE WEST:** JSFuck is amazing.  It proves that you can write any line of JavaScript
using only six characters.  Open brace, close brace, open parenthesis, close
parenthesis, plus and bang.  Do your filters check for any of these characters?
They all seem relatively benign, right?  But if you put these into an attribute,
you're kind of screwed.

Does anyone know what this code does by the way?  Can you guess?  You can all
read this.  I mean, it's just JavaScript, right?  This is `alert(1)`.  Usually
you will do -- usually you will do `alert('XSS')` when you're doing a pentest
or something but `alert('XSS')` is about 6,000 characters long, so I
didn't paste it.  JSFuck is quite verbose.

Alex Russell puts this beautifully when he says, "I discount the probability of
perfection."  It's really difficult to be perfect.

I would phrase it slightly differently: "We are all idiots with deadlines."
We do the things that we think are important in the moment and it's very easy
to forget about things, these overarching things that are a critical
foundation of the work that we should be doing.  And it's very easy to make
small mistakes.  And unfortunately, small mistakes are really all that it takes.

So what I want to talk about today is what we can do inside of a browser to
mitigate the effects of our idiocy because generally speaking, there are going
to be holes in the websites that you create.  It's almost unavoidable.  It's a
question of -- it's a question of "when" not "if" there's going to be a hole in
your sites and "when" not "if" that hole is going to be exploited.  It will be
really nice if there was some sort of -- I don't know a _policy_ of some sort
that we could give to the browser that, I don't know will have an effect on the
_security_ of our _content_.  I don't know.  We'll back come back to that idea.

Does anyone what [this painting][painting] is?  This painting is [Odysseus][]
and the [Sirens][siren].  It's a really good story.  It goes something like
this. Odysseus is -- Odysseus is an amazing man.  And by that, I mean, that he
is an egomaniacal maniac and bastard.  This story goes something like this:
Sirens, they sing beautifully.  So, beautifully in fact, that they drive you to
the brink of madness, sailors in particular, they really like sailors for some
reason, who knows why.   Sailors are driven to the point that they -- all they
want to do is be near this music to hear more of the music, so they end up
throwing themselves overboard whenever they, you know, sail around the island
where these sirens find themselves.  The ship then crashes on the island then
these sirens I guess eat people, who knows.

Regardless, Odysseus decides, because he is an amazing man, that he wants to be
the only living person to have heard the song of the sirens and survived.  So,
what does he do?  Well, he tells his men to tie him to the mast.  So, they bind
him quite tightly, his hands behind his back, his legs are tied to the mast.  He
can't go anywhere.  But he can hear the music.  He simply prevented from doing
things that would be stupid, you know, acknowledging the fact that the entire
endeavor is stupid.  He then, instructs his men to put beeswax in their ears and
they, you know, wrapped things around their head, you know, primitive sorts of
earmuffs so that they can't hear the music of the sirens.  And he gives them
explicit instruction.  You know, "row next to this island", "don't go to the
island", "don't jump out of the boat", and "just keep rowing", right?   The
sirens come, they sing their beautiful songs.  He's driven to the brink of
madness but he's able to continue on his path because he's given these
instructions and then he's prevented his men from acting on these distractions.

It'd be really great if we could do something like this with the browser.
Where we could tell the browser, "Hey, this piece of code is what you want to be
executing."  These distractions, all this other beautiful JavaScript that's out
here that youreally, really want to go execute and look at it, but please do not
touch, right?  It would be nice if your application could ask the browser to tie
its hands behind its back and prevent it from doing things that it knows are
going to be bad idea.

[Content Security Policy][csp] is this thing.  It is gorgeous.  It will give you
errors like this when people try to inject code into your sites. `Refused to
execute inline script because it violates the Content Security Policy
directive: "script-src 'self'"`.  We'll talk about this in a little bit more
detail.  But the core idea I hope is clear.  Content Security Policy gives you a
mechanism by which you can whitelist certain origins of content and allow only
those origins to execute within the content -- within the context of your
origin. That is, if I want to include [Google Web Fonts][fonts] I can only
whitelist the origin from which this font should come.  I get script from that
origin, I get fonts from that origin, but I shouldn't get them from anywhere
else in the web.  This is really quite powerful.

The specification is [here][cspspec].  Content Security Policy
1.1 is currently in draft.  Content Security Policy 1.0 is a candidate
recommendation.  It's currently implemented in Chrome.  It's implemented in
Firefox 23 which just came out as an unprefix header.  We'll talk about that in
a little bit.

I edit the spec along with [Adam Barth][abarth] and [Dan Veditz][dveditz] from
Mozilla.  They are much smarter than I am, so I just kind of sit there and type
whatever they say.  It's great.

So, what could a Content Security Policy look like?  Content Security Policy is
delivered as an HTTP header.  This is the -- this is the policy that's being
used on an incredibly high value website `mikewest.org`.  Yeah.  Content
Security Policy is the name of the header, right. So, you send
`Content-Security-Policy` and then the value is a semicolon-delimited list of
directives.  Each of these directives controls a specific type of content.

Here, I've set the default of `'none'`, in other words, nothing should
be allowed on my site.  Then, I slowly open that up and start saying, "Okay.
Well, okay.  Nothing except style from my CDN.  Okay.  Nothing except style and
frames from these two places." and so on.

And you see here that I've whitelisted <https://www.speakerdeck.com>.  I did
that because Speaker Deck, being awesome, serves things over HTTPS whereas
other services do not and have no intention of doing so.  This is problematic
especially if you're on a HTTPS site because Chrome and Firefox has started
actually blocking HTTP content within the context of an HTTPS site.  So, it's
really good if you run a service of any sort and you expect people to embed
things on the web, serve it over SSL.  If you don't serve it over SSL, slowly
but surely your options are going to be limited with regards to where that
content can be embedded.  All right.

So, script -- sorry -- style, frames, script images, fonts, and so on.  This is
an exhaustive list of the directives that exist in
[Content Security Policy 1.0][csp10] which is currently available in Chrome.
There are couple of additional directives behind a flag in Chrome.  So, if you
go in to Chrome flags and then enable "Experimental Web Platform features"
(<chrome://flags/#enable-experimental-web-platform-features>), then you'll be
able to start playing around with the 1.1 stuff immediately.

And I'll talk about a little bit about what's new in 1.1 later because they are
like two important things and then a bunch of other stuff that's gotten through
for one reason or another.  What's interesting here is the last item, a report
URL or URI.  Yeah, URI.  What this does is actually gives you insight into
whether or not you're being attacked.

You can run Content Security Policy in such a way that every time there's a
violation, every time a resource is loaded that -- I'm sorry -- an attempt to
load a resource has made that goes -- that violates your policy, you'll get a
POST message from the browser.  The browser will say, "Hey, I tried to load this
thing and I blocked it.  It was on this page.  It had this URL, maybe you should
take a look at that," which is really quite useful if you're auditing websites.

What's nice here is that you can actually run kind of Content Security Policy in
a "Report Only" mode.  That is it won't actually block any content on your site.
What it will do instead is simply send these POST messages out to your web
server so that you can start cleaning up your site before you actually deploy a
Content Security Policy.  What's really nice is that you can actually run both
a Report Only mode and an Enforce Mode policy at the same time.  So, you can
have a really loose enforce policy that says `https:` only.  So I should load
everything over HTTPS and if I don't, then start telling me about that, so
that I can find these places on my site that need to be cleaned up.  Then you
can also have a Report Only mode that's more restrictive where you start saying
only this origin, only that origin, no inline script, and so on.  This gives you
a nice mechanism by which you can start rolling this out.  You start getting
information about how your site's actually behaving in the wild and it gives
you a good opportunity to start cleaning up these areas that need work.

If any of you have any questions by the way, please ask.  Did you have a
question? Okay.  I'm sorry.  Anyway, you see the report information here.
There are variety of attributes.  They do more or less what they say on the
tin. `document-uri` is the document what was being attacked.  `referrer` is
the link from which the user came and so on.  The interesting bit might be the
source file line number and column number at the end.  If the violation came
from JavaScript we'll do our best to give you some context that you can actually
find it again later on.

But what do we do about inline script?  What origin would you say that this
comes from?  It's not being loaded via a script tag, right?  It's just
inline in the page.

Ha-ha, we didn't know either.  So, we invented one, we called it `'self'`
_(I should have said `'unsafe-inline'` here... Oops!)_. Basically, inline
script is the biggest problem that we saw on the web.  And it's the core reason
the Content Security Policy is valuable.  We can instruct the browser to not to
execute inline script.  This means that even if an attacker can inject script
into your page they can't do anything.  They've just injected text, it's not
executed which means it's not dangerous.  It does mean however that if you have
inline script in your page that you're using now, you're going to have to do a
little bit of rewriting.  So, code that looks like this, where it defines a
function inline in the page and then has inline `onclick` handlers or
`javascript:` URLs or something along those lines, we have to be rewritten
something like this.

So, you externalize the script.  You put it in to an external file, you load it
from that file, and then you do some DOM manipulation in order to add event
listeners.  Quite honestly this is what you should be doing now.  I know there
are good reasons for inline script.  I know there are interesting performance
questions around it.  Generally speaking our approach with Content Security
Policy has been to throw the baby out with the bathwater and then to look in the
water and see if we can pick the baby up.  So, in 1.1 we're going to be digging
around in the water, and I'll show you a little bit of that in a moment.  For
1.0, to get something out the door that was really valuable, we simply say
inline script is banned.

You can however turn it back on by using the `'unsafe-inline'` origin.  We call
it "unsafe inline" because it's kind of unsafe and we kind of don't want you to
do it.  Regardless, here's [that article again][csp].  This article gives you
really all of the practical detail that you're going to need in order to do --
to start implementing this on your own.  I think its well worth your time.  I
really believe the Content Security Policy is one of the most effective
mechanisms to mitigate the risk of cross-site scripting that's come out in the
last several years.  It's not perfect.  There are ways to get around it.
There's an excellent paper called ["Postcards from the Post-XSS World"][postxss]
where people have already figuring out how they can attack you after you have
Content Security Policy that bans inline script.  Attackers are really, really
clever but we should make it as hard as possible for them and I think Content
Security Policy is a great way to do that.

Let's take a quick look at the [1.1 spec][cspspec] just so I can tell you about
it.  Now I'm in full screen mode.  I'm sorry.  So, I had everything open on the
other machine and then it decided not to connect.  So, we're going to go and
let's see if I can remember where it is.  Yeah, look at that.  So, Content
Security Policy 1.1.  The interesting bits of Content Security Policy 1.1 are
the inline stuff.  There's also -- there's some discussion around the JavaScript
API that might or might not go anywhere.  But let's look at -- oh, that's right.
It used to be a separate directive and now it's not.  So, we have the ability to
embed nonces as valid sources of script and... I have no idea where it is.

I just write this stuff.  I don't know where it actually is.  Give me a break.
How can I be expected to find anything? So, "valid nonces", that sounds good.
And it's a Swiss keyboard, this is sweet.

All right, you've seen something like this.  Anyway, the idea -- there are two
competing ideas that we kind of don't want to implement both of them but we want
to discuss both of them.  One of them is a nonce which basically a one-time pad.
A server, when it generates a page, should generate a unique idea along with
that page and send it in the header.  It then would embed that ID as a `nonce`
attribute on each of the scripts that are enabled.  This means that if the
server does its job and generates a new nonce every time, that an attacker
won't be able to guess it.  So, even if they inject script, it won't have the
`nonce` attribute and then won't be executed.  It has the advantage of being
very simple, it has the advantage of being transferable so that if I load a
third-party widget, I can give it the nonce as well and it can then inject code
into my page if I trust it to do that.  And ads do this all the time, so, for
ads, it's kind of an important use-case regardless of whether it's a good
use-case or not.  The other option is a hash where we would basically hash the
inline script.  And take, like, the SHA-1 or SHA-256 hash of the script and
then compare that to something that was in the header so that you could only
inject code that match this hash.  I think both of them have advantages and
disadvantages.  And they're being discussed right now on the
[`public-webappsec@`][public-webappsec] list.  I'll get there right now.  So,
the [Web Application Security Working Group][webappsec] is the group that is
doing this work.  And from this page, you'd be able to find a link to the
discussions that are going on the -- on the mailing list.  If you have opinions
and you can back them with use-cases, I'd really suggest that you get involved.
Just join the working group, join the discussion.  We're still kind of in the
formative stages of 1.1 so it's a good time to get involved.

Well. OK, cool.

So, that is Content Security Policy. That is the one thing that I want you to
remember from this talk.  I think it's incredibly important, I think it's well
worth your time to play around with. Now, we're going to talk about other stuff
because I have more time.

Some of the things that I think are important.  SSL is the first and foremost
of these. I think serving your sites over a secure channel is an absolute
prerequisite to any conception of security whatsoever.  If you're serving your
site over HTTP, you have absolutely no guarantee that the bits that leave your
server are the same bits that are getting to the -- to the client and you have
no guarantee that the bits that came from the client are the bits that actually
reached your server.

We conceive of the internet somehow like this, that I have my laptop, I send
the request directly out to a server.  I get a request or I get a response
directly back from the server.  But when we think about it, we know that that's
not at all how things work.

Instead, I go to conferences and I join the Wi-Fi network at a conference.  And
then I send all my requests through this Wi-Fi network.  Do you trust [the
people that run Frontend Conf][fecstaff]? I don't know, they look kinda shady.

Generally speaking, proxies that sit between you and the servers that you want
to talk to have complete control over every HTTP connection.  There's simply
nothing that you can do to verify anything about the connection whatsoever.
It's unencrypted, sent in the clear, which means that those proxies have a)
the ability to modify the request but also the ability to read the request and
store them and send them to exciting people like the US government.  What I
would suggest is that your conception of the world should look something like
this where there's always something in between you and the server and you
should never trust it.  You should always assume that everything going through
external servers is being tainted in some way.

You can fix that to an extent by encrypting the data that's being sent.  This
at least guarantees that the information that's leaving your computer can only
-- well, mostly only -- be read by the server that it's going to.  And mostly
only -- and you can mostly only read the responses that are coming back.  SSL
is not perfect.  There are a lot of ways in which SSL can leak information and
we discover new and exciting ways almost everyday.  However, it is the only
guarantee that we have, period, that any information you send is going to be
the same information that's going out to the -- to the server and vice versa.
Given that, I think it's highly important for any service that is doing anything
with any information that has any value whatsoever, any, to use SSL.  It's
really quite important.  And it's also really quite easy.  For example,
StartSSL (which is much bigger than 124 -- or 1024 by 768) will give you free
SSL certificates.  All you need is an IP address. StartSSL is great.  I use them
for my site.  It'll look something like this when you do.  It won't look like
this because I never touch this thing, but you'll get a nice green thing up
here.  You'll get some green stuff there.  You'll get some green things over
here which is kind of nice.  But basically, all of that is theater.  What it
means simply is that you have the ability to encrypt the connection between
you and the client and that is only a good thing.  If you start setting up SSL
and you want to make sure that you've done it correctly, there's an excellent
website called [ssllabs.com which has an SSL test][ssltest].  This will run
through a lot of tests that show you in great detail how you have screwed up
your SSL connections or how you have screwed up your SSL system in general.

I apparently still have some work to do.

Generally speaking, SSL is really quite valuable, really important, and not
that difficult to set up.  It's like [three lines in Nginx][nginxssl] and it's
probably similar in just about every other system.  The only complication is
generating a request and then sending the request off and then getting a
response back and making sure that you [concatenate things in the right
order][nginxssl2] so that Nginx will send it.  It's really quite straightforward
and really quite nice.  So, I highly recommend that you do that.

Once you do, once you've gone ahead and set up SSL, make sure that all your
users are using it all the time.  That is if someone requests an HTTP page,
redirect them to the HTTPS page.  There's a 301 permanent redirect, it's just
the location header, it's really quite straight forward.  The clever amongst you
will notice that this leaves a window of opportunity for an attacker to do
some interesting things.  They could [strip this redirect][sslstrip], for
instance.  They could man-in-the-middle you at that point and say, "Okay, I'm
going to keep you on HTTP but I'm going to do the HTTPS connection over here to
the server and then I'll just forward the information to you."  They can keep
you on HTTPS -- or HTTP by doing so.  To get back to the concept of client-side
and browser-side, you can actually instruct the browser to _only_ connect to
your website over HTTPS regardless of what the user actually types into the
address bar.  You do that by setting a [`Strict-Transport-Security`
header][sts].  What this means is that the browser will do a transparent
redirect locally before it actually goes out to the network.  So, if I type in
`mikewest.org`, or if I type in `http://mikewest.org`, the browser will actually
switch that to HTTPS for me before it goes out to the network.  This means that
there's not -- there's only one window of opportunity for an attacker to strip
the SSL connection and that's the very first time you connect to a site.  So,
connect from home in the dark with a hood over your head or something so that
you're extra secure.  And then when you go out in to the wild and dangerous
world, you'll be guaranteed that you go to HTTPS and not http.  If you'd like
to see the list of websites that is actually already set up within Chrome or
within Firefox, then go to <chrome://net-internals> and check.

So, I can look at `mikewest.org` and you'll see that it's in strict mode that
include -- doesn't include subdomains and there's some nother stuff that I'll
talk about in just a minute. So, Strict Transport Security, it's a good
thing, I highly recommend that you set it up.  This means you have SSL and all
your users use it all the time, or as close to all the time as you could possibly
get.

If you want even more security -- well, actually this is something that you
should do even if you don't want security.  Even if you don't care at all, you
should do this anyway.  `Set-Cookie`, whenever you set cookies, make sure that
you set a -- the `secure` flag, which means that they are only sent over SSL and
never sent over HTTP and you set the `HttpOnly` flag which means your cookies
are not accessible from JavaScript.  This means even if someone can inject
JavaScript into your page and, even if it gets past your policy and even if it's
executed, they still won't be able to steal users authentication tokens because
-- well, not easily anyway.  They won't be able to do it via JavaScript.
They'll have to find other ways in your site to expose the value of the cookie.

`Public-Key-Pins` is a mechanism of making your security even more secure.  So,
the weakest link in SSL right now are the people that issue SSL certificates,
the [Certificate Authorities][ca].  It's the case that any certificate authority
has the authority to issue certificates for any origin on the web.  So, I can
issue a `google.com` certificate, you can issue a `google.com` certificate, it's
just a beautiful world where we all have this ability. Google, however, would
prefer that not everyone have this ability.  Since we can't change the CA system
as it is, we can instead look to things that ensure that the certificate is only
acceptable if it meets whatever requirements we set up.  In this case,
`Public-Key-Pins` gives us the ability to send a header that says only accept
certificates whose public key matches this hash.  This means we only accept
certificates that we have signed, not that _anyone_ has signed but that _we_
have signed.  This gives you the ability to only accept _certain_ certificates
and not _all_ certificates that are valid for a particular origin.  It's really
quite valuable especially if your site is a high-value target that's under attack.

I haven't set this up on my site because it is incredibly easy to screw up.  If
I lose my keys, then people would no longer be able to access my website because
I would generate a new SSL cert but, for the max age of the pinning, which in
this case is -- I don't know, some long amount of time, I think that's a month
-- people would go to my website and then they get an SSL error even though I've
set up everything on my end.  So, you need to be really, really sure that you're
doing everything right before you start implementing this.

If you want to go a step further, you can talk to Chrome and you can talk to
Firefox about having your website [hard-coded into Chrome as being on the HSTS
list][hsts].  What this means is that there's no window of opportunity for an
attacker to strip SSL on your site.  So, `mail.google.com`, `paypal.com`, a
wide variety of sites had chosen to do this.  They're basically hard-coded into
Chrome as a list of sites that should always be HSTS, that should always use
Strict Transport Security.  And if your site is one those sites, just [file a
bug][bug] and we're happy to add any site and every site but beware
of the consequences because if you've then screwed up your SSL then no one can
get to your site, ever, with Chrome.

That is Transport Level -- [Transport Layer Security][tls].  There's one more
topic that I was going to talk about but I think I'm going to skip it because
it's not particularly important.  The slides are online so please feel free to
skim through all the `<iframe sandbox>` stuff.  It's pretty interesting but
it's not critical.

What I think is critical is, again, one more time, just so everyone remembers,
[Content Security Policy][csp].  It's really important.  I think it's the
single biggest step forward that we've made in quite some time with regard to
mitigating the risk of cross-site scripting attacks.  It's not perfect.
Attackers will still attack you after you have a policy but at least you've
raised the bar to the point where attacking you is hard as opposed to not so
hard.  Thank you for your time.

Q&A
---

Do you have any questions?  I'd be really happy to answer them.  Yeah?

I mean, maybe, depending on the question.

**>>** So, this one's going to be hopefully challenging.  So, we were on quite a big
web service and we really rely on advertising on all pages.  So, what we get a
lot is, from security web people like people in this room, is use f-ing SSL
and we cannot do that because of all the advertising.  Most advertisers do not
use SSL to serve ads.  Do you have any suggestions what we could do about it?

**>> MIKE WEST:** I -- well, the flip suggestion would be find advertisers that serve over
SSL.  The less flip suggestion is that we're moving in that direction.
Advertisers in general are starting to understand that they simply -- they can't
embed into it -- SSL sites.  And because of that, they're going to start losing
revenue.  It's not happening as quickly as I'd like, but generally speaking, the
trend is for everything on the net to be encrypted.  If you look at [SPDY][], if
you look at [QUIC][], if you look at HTTP2 which is currently in discussion, the
general trend in those discussions is starting with SSL, and that there just
isn't a non-encrypted variant.  There's some discussion around that,
specifically around caching because encryption makes caching difficult.  But
generally speaking, the trend is towards encryption and the trend, specifically
with new protocols, is to only have encryption and to simply not have a
non-encrypted channel.

So, my answer would be that it gets better but they we're going to have to wait
for that betterness.

For now, I would suggest using advertisers that can serve over SSL like Google,
for instance.  But generally speaking, I honestly believe that this is going to
be a feature that website owners are going to start asking for more and more.
And it's up to website owners and publishers to put pressure onto advertisers so
that they actually start doing the right thing.  Until that pressure, until that
market pressure exists, it's going to be very difficult to move advertisers
towards a more secure world.

**>>** Hi.  Thank you for this talk.  What's your opinion on this plugins that
came last year like [HTTPSEverywhere][] for Firefox as well as Adblock Plus
which has been, I believe, two or three months ago.  In Germany, there was a
big announcement of all these media sites serving, saying to you. You have an
Adblocker, please, please disable it because we are relying on advertising,
for example.

**>> MIKE WEST:** I think those are -- I guess I would say that those are two completely
different questions.  I think [HTTPSEverywhere][] is wonderful.  I highly
encourage that you install HTTPSEverywhere.  It's a plugin, an extension or a
plugin depending on your browser from the EFF, the [Electronic Freedom...][eff]

**>>** Foundation.

**>> MIKE WEST:**  Yes, I don't -- it's just [EFF][eff] and it's awesome. I [give them
money][donate], I just don't know their name.

Generally speaking, I would highly recommend that you install it because what
it does is -- has a list of all services or lots of services that serve things
over HTTPS but for whatever reason give you HTTP options.  It forces you onto
HTTPS.  So, it's kind of like a client-side version of the Strict Transport
Security that we talked about.  And then, I recommend that you install it but
understand that not every publisher actually expects you to use HTTPS, so, it
breaks sometimes.  You have to understand that maybe for this site, you have
to turn it off and it's a little bit more work but you're certainly more
secure because you're sending the vast majority of your traffic over HTTPS
and that's a very good thing.  AdBlock is kind of a completely different
question and I'm going to ignore it.

I won't actually.

AdBlock -- I don't understand Adblock.  I understand why people use it because
ads are often annoying. But for good or for ill, advertising is absolutely
central to financing the web, period, whether you like it or not.  Given that,
I think it's problematic if a large portion of the populace is blocking ads.
I'm not going to tell you to stop blocking ads because you're not going to.
But generally speaking, I think it's the wrong thing to do.  I think the right
thing to do is to vote with your feet and if you don't like the ads on a
particular publisher, don't visit that publisher.  I understand there are
reasons that people use it. We've talked about it yesterday or the day before.
But generally speaking, I see it as really problematic and I find that when
people complain about ads in the web, like, I find it unsympathetic, but of
course I would because I work for Google so, who knows?  Feel free to ignore
that.

We'll talk afterwards, okay? It's not really this topic so we'll talk
afterwards.

**>>** Yeah, sorry.  I quite like the reporting feature which we saw before and -- but
there was just a question on twitter.  Is there some way to prevent misuse?
Because like the URL for reporting is then public and basically everyone can
submit anything there, so, how to use a tech if it's really from a browser or...

**>> MIKE WEST:** Yeah.  So, we do -- we -- First, I would suggest that you should
already have things in place that do rate-limiting.  So, if you're being DDOS'd
then you should have mechanisms in place, and this isn't gonna make that any
worse. Second I would say, that for same-origin reporting mechanisms, so, if
`example.com` reports to `example.com`, we send cookies.  If example.com reports
to something else then we don't send cookies.  So, at that point, you can use the
cookies as some sort of authentication mechanism and say that, you know, this is
coming from this user. What you can also do is have a token, a [CSRF token][csrf] in
the reporting URL and say that for this page, you go to this URL, for this page,
you go to that URL, just with GET parameters and then verify that those
parameters are actually what you expect them to be.  So, in the same way that
you verify form submissions, you can also verify these sorts of POSTs. And I
think that would take care of most of the mechanisms.

You're making him run, that's just mean!

**>>** I'll raise about full HTTPS, what is the impact first about SEO, how Google
look about HTTPS for the website, have an impact?

**>> MIKE WEST:** I have no idea but Google serves basically everything itself over SSL,
almost everything.  And generally speaking, Google as a company wants people to
be using SSL.  I'd be shocked if SSL had a negative impact but I am not a
quote-unquote "SEO expert", so don't take my word for anything.  Talk to people
who know something about SEO.

**>>** Just a last comment, when you have a big website with lots of view, if you
use full SSL, of course, we need to have a bigger hosting environment.  How many
percentage?

**>> MIKE WEST:** Not significantly.  So, there is kind of this general common knowledge
that SSL is much slower than HTTP.  It's not that slow.  I think you're going
to -- I'm going to quote it wrong.  There's a -- there are some really smart
people at Google.  One of them is -- what's the guy's name?  Smart guy at
Google, help me out.  Violet -- SSL something -- [ImperialViolet][agl], there
we go. Oh, and look, that's like -- that's the exact article I wanted to go to.
That is sweet.  So, there's [a good article on ImperialViolet.org called
"Overclocking SSL"][overclockingssl], where it talks a little bit about the
impact of SSL.  I want to say, yeah, one -- less than 1% of the CPU load, less
than 10K of memory per connection, less than 2% of network overhead.  There is
overhead, it is minimal.  This was 2010.  My suspicion is that it's even lower
at this point.  So, if you have set things up poorly, then your site's going to
be slow.  If, however, you follow the best practices for setting up SSL
connections and do the right things with regard to [false-start][false]
and a variety of other code, weird configuration options, you're going to have a
site that's exactly as fast -- within 1% of --  non-SSL sites.

**>>** I have one more question about the SSL thing which is, are there any
disadvantages in using a free SSL provider like you were showing in comparison
to the quite expensive other ones?

**>> MIKE WEST:** Yeah.  I don't get it.  I think Thawte would love for you to believe
that their certificates are more valuable.  They are not.  You get 204 -- 2048
bits of encryption with any certificate ever.  Certs are certs.  They are a text
file that's like that long, there's no reason to pay thousands and thousands of
Euros.  It's kind of a ridiculous racket.  They can do that because people trust
them.  So, if you're doing -- the only reason -- sorry, the only reason that I would
suggest using any of these services that are, you know, widely known and widely
trusted is that some networks, especially inside of enterprises for whatever
reason, only trust certificates from certain providers.  Generally speaking,
[StartSSL][], which is the one that I recommend and the one that I use, is
well-supported across the world but you would have to test in the specific
enterprise whether they've, for whatever reason, disabled certificates from
people other than, like, the two CAs that they trust.  So, the only reason
that's valuable is because it's a racket.

**>>** You just showed us this http header was -- the pin where...

**>> MIKE WEST:** Uh-hmm.  Yeah.

**>>** Do we need a [StartSSL][] or some provider like that anyway or...

**>> MIKE WEST:** Yeah, yeah.  You'd have to have a cert before you can pin a cert, so
pinning.

**>>** Maybe somewhat, self-sign it to...

**>> MIKE WEST:** You can self-sign it and you can pin a self-signed certificate but the
browser isn't going to trust that anymore.  There's been [some discussion around
making self-signed certificates less terrible in terms of their
presentation][dnssec] but I don't think that's going to roll out to the web.

**>>** I see your point before that [EV SSL][ev] isn't worth a lot really.  Why in
browsers do -- do browser producers actually change the icon?

**>> MIKE WEST:** That is an excellent question.  You would have to talk with whoever
made that decision.

I don't think there's any value to EV certificate. Basically, the certification
means that you have a lot of money and that you paid someone.  And that gives
you your name in the URL bar and I guess that has some value, and if you're a
company then you have money to burn anyway so, hey, why not throw money at SSL.
But generally speaking, there is no difference, period, between the encryption
that you get with a self-signed certificate and a totally expensive EV
certificate.  The encryption is exactly the same.

Great. Thank you very much.

If you have any questions at all...

**>>** Thank you, Michael.  We'll follow-up with our closing keynote.  Just a moment.

[fec13]: http://2013.frontendconf.ch/
[fec13lanyrd]: http://lanyrd.com/2013/fec13/
[slides]: https://speakerdeck.com/mikewest/frontend-security-frontend-conf-zurich-2013-08-30
[Twitter]: https://twitter.com/mikewest
[Google+]: https://google.com/+MikeWest
[mikewestorg]: https://mikewest.org/
[csp]: https://mkw.st/r/csp
[SafeBrowsing]: https://developers.google.com/safe-browsing/
[origin]: http://tools.ietf.org/html/draft-abarth-origin
[owaspxss]: https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet
[owaspxss1]: https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet#Long_UTF-8_Unicode_encoding_without_semicolons
[jsfuck]: http://www.jsfuck.com/
[painting]: http://traumwerk.stanford.edu/philolog/2009/10/homers_odyssey_in_art_sirens_f.html
[Odysseus]: http://en.wikipedia.org/wiki/Odysseus
[siren]: http://en.wikipedia.org/wiki/Siren
[fonts]: http://www.google.com/fonts
[cspspec]: https://dvcs.w3.org/hg/content-security-policy/raw-file/tip/csp-specification.dev.html
[abarth]: http://www.adambarth.com/
[dveditz]: https://twitter.com/dveditz
[csp10]: http://w3.org/TR/CSP
[postxss]: http://lcamtuf.coredump.cx/postxss/
[public-webappsec]: http://lists.w3.org/Archives/Public/public-webappsec/
[webappsec]: http://www.w3.org/2011/webappsec/
[fecstaff]: http://2013.frontendconf.ch/about/
[ssltest]: https://www.ssllabs.com/ssltest/index.html
[nginxssl]: http://wiki.nginx.org/HttpSslModule
[nginxssl2]: http://www.digicert.com/ssl-certificate-installation-nginx.htm
[sslstrip]: http://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security#Applicability
[sts]: http://www.html5rocks.com/en/tutorials/security/transport-layer-security/#closing-the-open-window
[ca]: http://en.wikipedia.org/wiki/Certificate_authority
[hsts]: http://src.chromium.org/viewvc/chrome/trunk/src/net/http/transport_security_state_static.json
[bug]: http://crbug.com/new
[tls]: http://src.chromium.org/viewvc/chrome/trunk/src/net/http/transport_security_state_static.json
[eff]: https://www.eff.org/
[donate]: https://supporters.eff.org/donate
[SPDY]: http://www.chromium.org/spdy
[QUIC]: http://blog.chromium.org/2013/06/experimenting-with-quic.html
[HTTPSEverywhere]: https://www.eff.org/https-everywhere
[overclockingssl]: https://www.imperialviolet.org/2010/06/25/overclocking-ssl.html
[csrf]: http://en.wikipedia.org/wiki/Cross-site_request_forgery
[agl]: https://www.imperialviolet.org/
[false]: http://tools.ietf.org/html/draft-bmoeller-tls-falsestart
[dnssec]: https://www.imperialviolet.org/2011/06/16/dnssecchrome.html
[StartSSL]: https://www.startssl.com/
[ev]: http://en.wikipedia.org/wiki/Extended_Validation_Certificate
[video]: https://www.youtube.com/watch?v=fYjO5pIY1mY
[original]: http://www.ustream.tv/recorded/38005119

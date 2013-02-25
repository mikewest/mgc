---
layout: post
title: "Securing the Client Side"
tags:
  - contentsecuritypolicy
  - csp
  - hsts
  - https
  - xss
  - security
  - transcript
  - presentation

Teaser:
  "At the end of last year, I presented 'Securing the Client Side' at Devoxx,
   and I've been meaning to put together a more accessible version of the talk
   for those who weren't there. I think the topics are important, and worth the
   effort of updating this site for the first time in a year. *cough*."
---
In November, 2012, I attended Devoxx in Antwerp for the first time to present
some recent developments in client-side security. [Content Security
Policy][h5r-csp] of course was at the top of my list. I think the presentation
does a nice job walking through the rationale behind some practices I'd like to
see spread.

In the interests of making the presentation as accessible (and indexable) as
possible, a full transcript of the presentation is below, along with an embed of
the video and slides.

[caniuse-csp]: http://caniuse.com/#feat=contentsecuritypolicy
[caniuse-sandbox]: http://caniuse.com/#feat=iframe-sandbox
[csp10]: http://w3.org/TR/CSP/
[csp11]: http://w3.org/TR/CSP11/
[devoxx-headers]: http://devoxx.com/display/DV12/Defensible+Development+with+Secure+HTTP+Headers
[goodparts]: http://www.amazon.com/exec/obidos/ASIN/0596517742/wrrrldwideweb
[google-escaper]: http://googleonlinesecurity.blogspot.de/2009/03/reducing-xss-by-way-of-automatic.html
[h5r-csp]: http://www.html5rocks.com/en/tutorials/security/content-security-policy/
[h5r-hsts]: http://www.html5rocks.com/en/tutorials/security/transport-layer-security/
[h5r-sandbox]: http://www.html5rocks.com/en/tutorials/security/sandboxed-iframes/
[h5r]: http://www.html5rocks.com/
[handlebars]: http://handlebarsjs.com/
[jorge]: http://youtu.be/GBxv8SaX0gg?t=17m22s
[mozilla-csp]: http://blog.mozilla.org/security/2011/03/22/creating-a-safer-web-with-content-security-policy/
[nuke]: http://www.youtube.com/watch?v=aCbfMkh940Q
[owasp-xss]: https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet
[owasp]: https://www.owasp.org/
[plus]: https://plus.google.com/104437754419996754779/posts
[polp]: http://en.wikipedia.org/wiki/Principle_of_least_privilege
[public-webappsec]: http://lists.w3.org/Archives/Public/public-webappsec/
[same-origin]: http://en.wikipedia.org/wiki/Same_origin_policy
[seamless]: http://www.whatwg.org/specs/web-apps/current-work/multipage/the-iframe-element.html#attr-iframe-seamless
[srcdoc]: http://www.whatwg.org/specs/web-apps/current-work/multipage/the-iframe-element.html#attr-iframe-srcdoc
[startssl-class2]: https://startssl.com/?app=2
[startssl]: https://startssl.com/?app=0
[thinksec]: https://twitter.com/thinksec
[twitter]: https://twitter.com/mikewest
[unique-origin]: http://www.whatwg.org/specs/web-apps/current-work/multipage/origin-0.html#sandboxOrigin
[webappsec]: http://www.w3.org/2011/webappsec/

Video
-----

<iframe
  src="http://www.parleys.com/dist/share/parleysshare.swf?sv=true&pageId=3521"
  allowfullscreen="true"
  mozallowfullscreen="true"
  webkitallowfullscreen="true"
  frameborder="0"
  title="'Securing the Client Side' -- Devoxx 2012: Video"
  width="606"
  height="403"></iframe>

Slides
------

<iframe
  src="https://speakerdeck.com/player/00342360618601301a9912313d095c59"
  allowfullscreen="true"
  mozallowfullscreen="true"
  webkitallowfullscreen="true"
  frameborder="0"
  title="'Securing the Client Side' -- Devoxx 2012: Slides"
  width="606"
  height="403"></iframe>

Transcript
----------

**MIKE WEST >>** Got a cell phone in there, who knows...

The topic of today is, or, of this talk anyway, is "Securing The Client Side".
It's kind of, I think, an interesting topic for a Java conference, because most
Java programs have very little to do with actually building HTML and pushing it
out to clients.  It is, however, the case that if you want the largest market
possible, the target of your language or whatever your application is, is going
to be JavaScript, it's going to CSS and it's going to be HTML. That gives you
the ability to push your application out to a huge audience that you simply
wouldn't have access to if you tried to deploy something in a more native way.
The web is simply the largest platform out there.

And a consequence of this is that we're slowly seeing more and more of the
application logic being moved down to the client side. It's moving out of these
large back-end systems and moving down into JavaScript and executing then on a
client's computer, on an untrusted machine, as opposed to a machine, the server,
that you have complete control over. There are a couple of things that you can
do on the server side in order to ensure that your application is secure, to
ensure that no one can write things into your application that you don't want,
and to ensure that the code that your application delivers is secure when it
actually gets to the client.

We're not going to talk about that today.

Instead, we're going to focus very specifically on what you can do in the
browser, in order to ensure some measure of security for your application. It's
simply the case that the browser is an untrusted environment, so you need to be
very careful about what you're doing. But at the same time, there are some new
capabilities coming out in browsers of today, that allow you to ensure that your
application is delivered in a way that maintains some degree of security.

The web is simply a scary place. Have any of you seen a screen like this? In
Chrome or any other browser?  Most browsers today have some sort of Safe
Browsing system which tells you when you're visiting a site that we know could
be problematic. So, if we've seen a lot of malware on a site, we have mechanisms
by which we can inform the browser that a specific website might be problematic.

It's most often the case however, that the things that we're really worried
about aren't pervasive and aren't persistent on a website.

It's very difficult for someone like Google or Mozilla to detect malware on a
site, if the site itself is benign.  There are a variety of attacks that can
allow someone to inject code or inject content into a website that's otherwise
perfectly benign, nd only affects the person who is actually visiting that page
at the moment. It's called a cross-site scripting attack.  And there are a wide
variety of mechanisms that allow it to occur.

I'm going to talk about two things that you can do to reduce the capabilities of
someone who would be attacking your sites and to mitigate the effects of any
attack that did get past your defenses.

But before I start talking about things that you can do to defend, I want to
talk about one thing that I see as an absolute prerequisite for anything... for
any discussion of security on the web.

You must, _must_ send data and accept data over a secure channel.  There's
really no excuse these days for using HTTP as opposed to HTTPS to deliver an
application.  Applications _must_ be delivered over HTTPS because that's the
only mechanism by which you can ensure that there's even a modicrum of a chance
that the data that you send out and the data that the user receives are
identical.

Our view of the web kind of looks like this. We think about it.  I have a
laptop.  I go out directly to a server.  I pull some information down.  I do
something locally and then I send more information up to the server.  We think
about these direct connections, but of course it's the case that there is no
direct connection between me and a server.

Instead, I'd go to a coffee shop.  And in that coffee shop, I hook up to their
Wi-Fi network and then, in order to transmit my requests up to the server, it
hops and hops and hops through a variety of routers and a variety of different
servers until it actually hits the end point that I care about.

That's a lot of things that I have to trust.  It's a lot of different servers
that I need to ensure that I -- if I want to ensure that the information gets
from A to B intact, I need to trust each of those points in between.  If you're
sending information over HTTP, it's very likely that something like this could
happen.  It's called the man-in-the-middle attack.  I send information over
HTTP, some malicious server in between me and the end point takes that
information, modifies it in some way and then sends it on, acting as a proxy
between me and the server that I actually care about.

At this point, it's pretty much game over.  If I'm sending information over an
unencrypted channel, that man-in-the-middle can take the information, either
read it, modify it, do really whatever they want.  And there's no way to detect
this sort of thing.  Because HTTP has no sort of encryption associated with it
and no sort of signature associated with it which means that the information
that I receive, I'd simply have to blindly trust that it's the information the
server actually sent down to me.  That's something that I don't think anyone
should be doing when writing an application.  When writing an application, you
should instead be very certain that you're sending information over HTTPS.

HTTPS gives you a mechanism by which you can first encrypt the connection
between you and the server, it still hops over a wide variety of routers in
between you and the server.  But none of those routers have the ability to read
the information.  Because they don't have the private key that exists on the
server.

At that point, you have some measure of security, some measure of privacy that
is, in that the information can't be read.  Second, you have a measure of
security in that the information can't be modified as it's sent back down to you
without reencrypting the information using the same key as the server.  This is
very difficult to do.  It's not impossible.  So this isn't a completely secure
solution but it's miles better than HTTP where you have absolutely no guarantees
whatsoever.

Anyone who's running a server should still listen on HTTP ports because most
people will just type in the server name into the browser and the browser will
default to HTTP, would go out to the website and then something like this should
happen.  You should be doing a redirect -- that's kind of cut off on the side
which is annoying.

What you see at the top is a `curl`, a `HEAD` request to `mkw.st`.  It's going
over HTTP and at the bottom you'll see a location header, which redirects me to
the HTTPS server.  This is good, this means that I'll -- most of my connections
will be over HTTPS.  But it leaves the vulnerability because that first
connection is going out over HTTP.  It'd be nice if we can somehow inform the
browser that it should default to HTTPS as opposed to defaulting to HTTP, as it
turns out we can.  There's a new header called
[`Strict-Transport-Security`][h5r-hsts]. Strict Transport Security says, I'm
sending this information over HTTPS and next time you connect to the server,
forget about HTTP.  Even if the user types in `http://servername`, go over
HTTPS.  Do the redirection client side as opposed to making a request and
letting it happen server side.

There's a `max-age` associated with this, so you can say for a month, do this
sort of thing or for a year or for however long you actually trust that you'll
keep your certificates up-to-date.  And there's a mechanism by which you can
also say that all subdomains of this domain, should also be protected by Strict
Transport Security.  This is really good for you guys to be doing.  I would, so
I would very much recommend that anyone who's writing an application that's
delivered over the web, go to [startssl.com][startssl] or any of a number of
other certificate delivery websites where you can sign up, get a certificate,
associate it with your website and ensure that your application is being
delivered in a secure fashion.

Once you've done that, go ahead and set up `Strict-Transport-Security` headers
in your website, so you'll ensure that your users are always visiting your site
over HTTPS.  It's really almost a no-brainer.  StartSSL in particular, is great
for people with really small applications.  It's also good for large
applications, but for people that don't need these warranties that are
associated with larger certificate manufacturers.  StartSSL is absolutely free.
They only charge you for the work that they do.  So, if you don't care about
authentication -- no, not authentication.  If you don't care about verification,
then you can get a free certificate for your app that is -- that works on all
browsers, which is great.

If you do care about verification, or you want wild card certificates for
something on those lines.  The [level two verification][startssl-class2] is
like, 60 bucks, 60 US dollars for two years.  You get unlimited certificates
associated with that. Given this sort of thing, there's really no excuse to not
have certificates even for the smallest of projects.

With that out of the way, with that as a basis upon which we can build
everything else, let's talk about the sorts of attacks that I would like to help
you defend against.  The most common is a script injection.  So if we go to
Google.com, over HTTPS of course, we might see something like this.  An alert
box popping up that says "XSS".  This is kind of the very typical thing that if
you pay a penetration tester to go out to your website and show you the
vulnerabilities, this is most likely what you'll see. You'll see -- I was able
to inject script in to your site and that script executed and popped up an alert
box.

It isn't very scary though, right? It's just an alert box.  So, why should we
really even care about it?  What's more interesting of course, is to pop up the
user's cookies and show them that by executing script on their site, you have
access to all of the information associated with that origin.

The web is generally protected by the [same-origin policy][same-origin]. That
is, a website consists or the origin of a website consists of a scheme, a host
and a port: that is (`HTTPS`, `google.com`, 443).  It's simply the case that,
that website should never have access to information on separate origin. So,
Google should never have access to my bank's information for instance.

_[pause to resolve beard issues.]_

This of course, is the downside of beards.  Beards are generally excellent.  I
highly recommend them, but if you have a microphone on your face, it makes it
slightly difficult.

Regardless, `document.cookie` can be read by any JavaScript that's associated
with a particular domain or a particular origin. Generally, things are protected
by the same origin policy; that is Google can't directly access anything from my
bank.  But if I'm able to inject some malicious JavaScript into the context of
`google.com` or any other website, the browser has no mechanism of
distinguishing between a maliciously injected piece of content and a piece of
content that was injected intentionally by the browser or by the--by the author
of the site.

So, we see two alert boxes here and if we actually saw this when an attack was
going on, there will be some measure of protection going on.  But usually what
we see is absolutely nothing.  We visit a site it looks just like any normal
site.  We interact with it and transparently in the background, the person who's
attacking the site is either exfiltrating sensitive information pushing out my
cookies to a third party server in order to steal my session or wide variety of
other things.

Generally speaking, if someone is able to execute JavaScript on your site, it's
more or less game over.  They have complete control over the site and they have
complete control over the information associated with that site which is pretty
problematic.

This is a really excellent website to go to.  If you're interested in how a
cross-site scripting attack might look.  It's called the [XSS cheat
sheet][owasp-xss] and it's delivered by [OWASP][owasp] which is security -- an
org -- an organization of people who are interested in security and put together
a lot of documentation, a lot of trainings along these lines.  It's a really
long document because there are an incredible amount of ways of injecting code
into a site that doesn't properly escape its output.

JavaScript is really interesting in that it accepts a wide variety of syntax and
it's very difficult to insure that you escaped everything correctly such that
JavaScript doesn't execute.  If you simply echo any information that's been
delivered by a user or any user generated content in general.

There are two things that you need to do in order to protect against cross-site
scripting attacks.  And if you do these two things perfectly, you are a hundred
percent guaranteed you'll never have a cross-site scripting attack on your site.

First, you need to validate all the information that comes into your website.
So, if there's a form where you accept someone's phone number, you want to
insure that you only accept phone numbers, that you don't accidentally accept
JavaScript.  One mechanism might be scripting out everything that isn't the
number, right?  Then you're more or less guaranteed you have something that you
can safely put into your database that you can safely deal with on the back end.

The next thing you want to do is ensure that you correctly escape every piece of
output that you -- that you write to a site.  So, if you have any content that
comes from a user or any sort of untrusted source, then you want to insure that
you escape that output correctly when you write it out to the--to the screen.

I said you need to do it perfectly and unfortunately escaping output is much
more complex than it seems.  Here we have a little bit of HTML and what you --
what you notice here is that there are five different contexts in which
information could be output.  This is a more or less exhaustive list.

You have style information, you have raw HTML, that's inside the `p` tag, you
have a URL that's inside of an attribute, you have information that's been
written out directly into script, never ever do this, right?  Never write
information with the script, that's just a bad idea.  And then you have
information it's written into a comment on a site.  You usually see this as
debug information where people just write out information, so that they can
figure out what's going on, on their own site.

Unfortunately, each of these contexts has different escaping rules.  And you
need to be very sure that you're escaping content correctly for the context in
which you find yourself.  Again, if you go to that website, I pointed to
earlier, it gives you some information about these contexts and about what the
rules might be.

For instance, inside of an attribute, you need to be very sure that you'd
correctly escape quotes and it's also the case that quotes aren't actually
necessary.  So, you want to make sure that you escape the contents in a such a
way that it's interpreted as an HTML attribute as opposed to a potentially a
script.

Fortunately, this is a completely solved problem. It's been solved at least
since 2009 when Google released an [automatic context-aware
escaper][google-escaper].  There are escaping mechanisms in basically every
toolkit that people use nowadays.  So, if you use Rails or Django or whatever
Java people use.  Then there are, I guarantee you, mechanisms by which you can
escape the content, which you can guarantee that the content is being escaped
correctly when it's delivered.

As I said however, you have to be absolutely perfect about the way you do this.
You have to ensure that you perfectly escape every piece of output that goes to
the site.

Unfortunately, it's the case that attackers will spend much more time trying to
find a single tiny hole in your application than you will spend defending your
application to maintain the status quo. You're going to be busy building new
features.  You're not going to be very busy looking at every piece of HTML that
you ever generate and ensuring that the escaping that you do is correct for the
individual context.

Empirically, we see that people make mistakes, it's simply the case.  And it's
not even the case that you have to make a mistake.  A browser vendor might make
a mistake as well. If you look at old versions of IE, it's very much the case.
That strange things need to be done in order to insure that content isn't
executed as script. They're simply bugs in the way that browsers parse things.

It's a losing battle, in other words, to ensure that every piece of content is
correctly escaped for every browser that a user might come to your site with,
but it's something that's very difficult to do.

So, we make mistakes, browser vendors make mistakes.  It'd be really nice if we
could simply instruct the browser in some way that this piece of code is valid
and this piece of code is invalid.  I mean for you to execute this piece of
code, but this other thing over here, why don't you leave it alone for a little
while.

This boils down, I think to the [principle of least privilege][polp].  The idea
is that every application, or every piece of an application should have the
minimum level of privilege necessary in order to do its job correctly.  This is
really quite common in the UNIX world where you see a process start as root, set
things up, and then immediately fork and drop down with `setuid` in order to
have fewer privileges, in order to insure that it doesn't have access to things
that it shouldn't have access to.

This is why you usually end up with like the MySQL or a PHP user on a variety of
systems.  Those users have fewer privileges than root and the system make sure
that the application runs as that user as opposed to a user with higher
privileges.

The good thing here is that if you minimize the privilege that an application
has, then when an attacker finds a hole -- and it will be a "when" not an "if"
-- then the attacker has a reduced surface area with which to work. They don't
have the ability to, for instance, write directly to the disc. And in that case,
you protected yourself simply by minimizing the value of the -- of this
application as a target.

Has anyone read ["JavaScript: The Good Parts" by Douglas Crockford][goodparts]?
Yes, a good number of you.  I think this actually fits very well into the
concept of least privilege.

"JavaScript: The Good Parts" has basically the single theorem that there is a
beautiful language hidden inside of JavaScript.  The JavaScript itself is kind
of large and has become ugly in a variety of ways.  But there's a beautiful core
and if you limit yourself to this core, if you restrict yourself from using some
of the more esoteric features, then you have a much easier language to
understand but also an easier language to program in and to reason about.

My contention is that you can do the exact same thing for HTML and if you can do
the exact same thing for your applications.  You can explain to the browser that
certain things, even though you would be allowed to do them, shouldn't be
allowed within the context of this individual site.

The way that you do this is via [Content Security Policy][h5r-csp].

Content Security Policy was [originally invented by Mozilla about three, four
years ago][mozilla-csp].  It was implemented in Mozilla, I believe, Firefox 4
and has been slowly improved and steadily improved since then.  It's now on the
W3C on standards track.  I believe, actually today it will moved from working
draft to candidate recommendation which is the next step would be proposed
recommendation and at that point everyone should implement it.

Content Security Policy gives you exactly this mechanism.  It allows you to very
-- to very clearly explain to the browser which things on the page, which pieces
of content are intentional and which pieces of content should never be executed.
 It allows you then to -- well, let's look at `mikewest.org`.

So `mikewest.org` is my website and it has a variety of pieces of content.  It
has images, it uses some web fonts, it uses some script and some style.  And we
can very clearly explain to the browser that certain pieces of information or
certain sources of information are trusted. And any other source, if someone was
able to inject content into my website because it is, of course, incredibly high
value then you would be able to very clearly distinguish between the injected
information and the intentional information.

The policy is an HTTP header it can also be injected as a meta tag in Chrome. It
looks something like this, `Content-Security-Policy` is the name of the header
and then we set -- we walk through a variety of directives.  And each of these
directives allows you to very granularly control the information that is
delivered to a website or that the browser should interpret as part of the
website.

We start out by making it secure by default.  So, we set a `default-src` of
`'none'`.  This means if we left it at that, then no content would run on the
site whatsoever.  It would render HTML, so the things that are contained within
the -- excuse me, within the website itself but no images would load, the script
would execute, the style would load, no web fonts, no media, no XHR.

Basically, it turns off anything that could inject the content into the page.
Then we slowly loosen this policy by saying for instance that
`mikewestdotorg.hasacdn.net` is a valid source of style.  So, I can load a
stylesheet from this origin.  And if it comes from this origin then the browser
will allow it.  If a style sheet comes from a different origin and is somehow
injected into the page, the browser will simply not execute it, will not render
that information.

We can skip down to `script-src` which does the same thing.  It says
`mikewestdotorg.hasacdn.net` and `ssl.googleanalytics.com` are both valid
sources of script.  If I load script from these origins they're trusted.  If I
load it from any other origin, it's untrusted, so if someone was able to inject
the script tag into my site they would need to ensure that their malicious
script existed on one of these two servers which will be a very difficult
problem indeed.

This is a more or less complete list of all of the directives that are available
in [Content Security Policy 1.0][csp10].  Content Security Policy 1.0 is going
to -- as I said is going to the next step in the standards track today.  It's
implemented in Firefox.  It's implemented in Chrome.  It's implemented in Safari
6 and IE 10 implements a single directive, so they're working on it.  They're
not quite there yet.

Opera is participating very heavily in the standards process, so we expect that
Opera will probably be 13 will have something like this but at the moment, it's
[across about half the browsers that you'll see on the web][caniuse-csp].

So `default-src`, we talked about `script-src`, `object-src` allows to control
plug-ins that exist on the sites.  You could say, you know, Flash files only
from this style, images, media allows you to control HTML5 videos, so if I'm
loading video information or subtitles or something on those lines that's
controlled the via media source.  `frame-src` allows me to determine which items
I can load into frames in a website.  So, I might say that I only want to load
YouTube videos, so I would allow `https://youtube.com` as a valid frame source
and no other frame will then render on my page.

This gives you the ability to then very granularly determine which pieces of
information should be part of your site and which pieces of content or which
sources of content should never be allowed access to your website.

It has a down side however.  The main -- or not really a down side. I think it's
an up side, but a lot of people see it as a down side so I talk about it that
way.

The main vulnerability that we see in cross-site scripting attacks is inline
JavaScript. That is I write some -- I request a page in such a way that causes
it to write out the script tag or to write information into a context that gets
executed as script. Content Security Policy takes more or less a ["take off and
nuke it from orbit"][nuke] approach to inline script: that is, it bans it
completely.

This is actually, I think a good thing.  It's enforces the strict separation of
content behavior and rendering that we see in HTML, JavaScript and CSS.  We've
been talking about this for years as best practice, that you should separate
your page out into: an HTML page that has clean mark up, a JavaScript file that
enhances the behavior of the page in some way, and then a script or a CSS file
that enhances the rendering, and makes things look pretty.

What we see here is in inline `script` tag that defines some functionality.  We
see an inline event handler that associates that functionality with a click on a
`button`.  And then we see a JavaScript URL that's in a link that associates
again this functionality that we define with the click on a link.

All of these can be trivially rewritten by extracting the JavaScript out into a
separate JavaScript file, loading that JavaScript file in my HTML and
associating the handler -- the handlers of the events via JavaScript as opposed
to doing it within the content of the mark up.

This I think is a good thing regardless of whether you use Content Security
Policy.  Again, it gives you this clean separation between your mark up and your
behavior and allows you to edit each independently.  It gives you a very clear
picture of where your behavior is happening and where your mark up is happening.
 And it gives us the ability to very clearly distinguish between code that's
been maliciously injected into your site and code that exists on a trusted
source of information.

That is, if I have an external JavaScript file the browser can be very clearly
determine what the origin of that file is if on the other hand I have an inline
script.  It's simply impossible for the browser to make a distinction between
inline JavaScript that's been maliciously injected and inline JavaScript that
you intended to have on your page.

So again, Content Security Policy allows you to reduce the privilege of your
website in a way that protects you from this sort of attack.  It allows you to
say that I'm not using inline JavaScript on my site and I don't want inline
JavaScript to ever execute.  This gives you the ability to instruct the browser
to help you out.  The browser can then be your friend. It can help you ensure
that only the information that you've actually delivered is getting execute in
the context of the website.

What's also interesting about Content Security Policy is a reporting function.
It's almost never the case that you can cleanly deploy in your Content Security
Policy onto an existing application without breaking something.  Content
Security Policy gives you a mechanism of doing first a reporting mode where you
say okay.  I want to try this policy out on my application.  And you can deploy
it to actual users.

If you use Content Security Policy report only then the policy will be evaluated
by the browser and will be interpret -- or each load of a resource will be
interpreted against the policy or validated against the policy, if it passes,
great.  If it doesn't pass the load will go through, but it will send to a POST
out to an end point of your specification.  So you specify `report-uri` as
`example.com/csp-violations` and it will send some JSON to you that it'll help
you identify the things that are breaking on your website or the things that
would break based upon this policy.

So this gives you a deployment mechanism that's relatively straightforward.  You
deploy a policy as report only.  You look at the reports that are coming in.
You fix bugs on your website that are causing these reports or you tweak the
policy because perhaps there's a section of your website that you didn't
actually look at.

Once you have a policy in place that's not generating a large number of
violation reports, you can deploy that policy as an active policy.  What's nice
is that you've actually have a active policy and a reporting policy existing at
the same time, so you can have a very loose policy like this one which simply
says only load resource over HTTPS, that is no mixed content of any sort.  I'm
serving my site over HTTPS.  I don't want to load any information over HTTP.
`default-src` of `https:` will allow you to do that, simply says no source that
isn't HTTPS should be allowed to deliver content.  This is a relatively loose
policy because it says any host that's on HTTPS, so `https://evil.com` would
also match but at least it's secure, right?  So that's good.

What's nice here is that you can deploy this sort of loose policy and the loose
policy is more or less guaranteed to work on your site and you can test the
policy at the same time by setting a report only flag.  So, you can both have
headers active at the same time.

The CSP report looks like this. As you see it gives you the URL that cause
problems.  It tells you what resource it tried to load.  It tells you the policy
that was active and which directive was violated.  So, it gives you some
information that allows you to debug the problems that you'll see when you start
to deploying CSP to your website.

You can, of course also use a report in an active policy, so if you deploy a CSP
or a Content Security Policy to your site you want to know if people are
attacking your website and this allows you to send reports based on violations.

So, once you're sure that all the code that you deliver matches the policy, you
can start getting reports about attacks that are existing against your site.
And this will give you information to help figure out where those attacks are
coming from which can be quite useful.

There's a good article -- this is just really just scratching the surface of
Content Security Policy.  If you're interested and I really hope you are because
this is the most important thing that's happened in web security I think for the
last two or three years.  [Content Security Policy on HTML5Rocks][h5r-csp].  You
should go to [HTML5Rocks][h5r] anyway by the way.  It's a great website, that
gives you a lot of information about HTML5 and new features that are coming out.

There's specifically an [article about Content Security Policy][h5r-csp] that I
happen to think is relatively well written.  And it gives you some good
information about how you can start using Content Security Policy, what the
purpose is, how it works and how you can deploy of any websites.

I think this is really important and I think it's quite -- it's not easy to
deploy this on existing applications, but there's really no reason at all that
you can't deploy it on new applications that you're building.

So, anytime you start building an application think about the resources that
you're using and think about the ways in which you can restrict the browser from
loading resources that you don't want the browser to load.

[Content Security Policy 1.1][csp11] is in editor's draft right now.  I'm
working with the standards body on this so if you guys have questions at all
afterwards or if you have suggestions about things that you think could be
added to a policy like this please do let me know.  There's a -- the working
group is the [Web Applications Security working group][webappsec] if you have
any questions at all you can join [public-webappsec@w3.org][public-webappsec]
and participate in all the discussion.

So this is a place that still rapidly in development, so if you have suggestions
we'd be very interested in hearing about them.

So, that's Content Security Policy.  I think it's incredibly important; it's a
really good way to reduce the privileges of a website down to the level that you
actually need in order to do your job.

Another mechanism that HTML5 is starting to provide that does more or less the
same thing or gives you many of the same ideas is called
[Sandboxing][h5r-sandbox].  Sandboxing allows you to include an `iframe` on your
website in such a way that it runs with reduced privileges.  Again, if we think
about the single origin or the same origin model we have `example.com` and
`mybank.com`. If `example.com` frames `mybank.com` so it loads MyBank in a
frame, then it doesn't actually have any access to that frame.  It can't use
JavaScript to reach in to the frame and the bank can't reach out of the frame
into the parent's in order to do any sort of damage.

This is a good thing and it allows you to include untrusted content on your
website in a way that it can't interfere with your website.  So, the `iframe` in
and of itself can act kind of like a sandbox, but if you include same origin
content -- that is, if `example.com` includes a page from `example.com` in a
frame for example a comment or something along these lines, then, because they
exist in the same origin, the parent can reach down into the child and the child
can reach up into the parent.

Both of these might be useful, but generally speaking they're not.  Generally,
if you're including content in an `iframe` you wanted to be in someway separate
from the page that exist within. Sandboxing is an at -- or sandbox is an
attribute that you can apply to an `iframe` but does exactly this.

It works very similarly to browsers that you see these days, where you have a
brow -- well, I'll talk about this eventually.

The attribute is quite straightforward.  If you apply a `sandbox` attribute to
an `iframe` then a couple of things happen immediately.  First no plug-ins can
be loaded within this `iframe`, no script can be loaded, forms cannot be
submitted, top level navigation simply won't work. That is, if I apply
`target="_blank"` or `target="_top"` to a link within an `iframe` usually
that'll navigate my entire page, the window as opposed to the frame, sandboxing
blocks this. No pops-ups, no `window.open`, modal dialogs, things along these
lines can't be created from within the context of the sandboxed `iframe`.  No
auto-play.  So, if I have video within this link auto-play won't work, no
pointer lock and no seamless `iframe`s.

What's really important and what I failed to write here is that sandboxing
actually will push the frame into a completely separate origin, regardless of
from where it was loaded. That is if I load the page from `example.com` in a
frame it won't act as though it's `example.com` or won't act as though that's
its origin.  It will instead have what's called a "unique origin" and a [unique
origin][unique-origin] is one that matches no other origin ever.  That is, it
has no access to any data from any origin at all.

This can be quite useful because it gives you the ability to load content --
load untrusted content in a way that simply can't do any damage at all to your
website.  If script can't execute in the context, it doesn't matter if someone
can maliciously inject script because it's simply won't execute, they won't be
able to navigate your page, they won't be able to create pop-up's, they won't be
able to move or bust out of the frame and move users through an area that they
weren't trusted to do.

You can of course loosen these restrictions and this would be the minimal
sandbox that you can create.  There's still no plug-ins and there's still no
seamless `iframe`s, but everything else can be enabled.  What's nice about this
is that you can create a sandbox that gives only the minimum level of privilege
necessary to a website, in order for it to do the work that website needs to do.

This concept allows you to separate the concerns within your application, so you
can actually break your application into a variety of pieces, and now we'll come
back to the concept of the browser.

If you look at how Chrome works, you have a browser process that has all the
privileges in the world, all the privileges of a normal application running on
your system.  They can go out through the web and get information, they can go
to your disk and get information or write information to random files on your
disk, it can execute arbitrary code and so on.  It's an application with all the
privilege in the world but it's a very thin application, it doesn't do much,
instead a lot of the work is delegated out to renderer processes.  More or less
you can think of every tab is a separate renderer process.

The renderer process is ask the browser for information, the browser determines
whether or not the renderer should get the information, delivers the information
to the renderer, allows it to do its work and awaits a response.  The renderer
grabs HTML untrusted content from the web, does a lot processing on it in order
to build a render tree and then sends that tree back up to the browser once it's
verified that it's trusted.

What this means is that the renderer doesn't actually need any of these
privileges.  It doesn't need to go out to the web, the browser does that for it.
 It doesn't needs to write things to the disk--again, that's what the browser is
there for.

So, you separate the privileges of your web app or you take the application, you
break it into pieces and give each piece only those privileges that are actually
necessary in order for it to do its job.  This allows you to build applications
in such a way that each components can live inside of a sandboxed `iframe`.  So,
what you would basically end up doing is creating an API for your application
based on messaging. So it would be asynchronous API by which you pass messages
into a sandbox, allow that sandbox to do some sort of interesting work based
upon the message that you passed in.  And then ask the sandbox to send
information back up to the parent in order to delegate that work to another
process or to do some sort of rendering out to the website.  This could look
something like this, so here's a toy example of how this might work.

We have a Content Security Policy associated with this page that says
`script-src` of `'self'`, so only script that's loaded from my current origin
can be executed within the context of this page, of this protected resource.  We
load a script called `main.js` and we have an `iframe` on the page that loads
`sandbox.html`.  The sandbox allows scripts, but allows nothing else.

`main.js` looks something like this and we'll talk about it in a little bit more
detail later on, but the idea is simply that we bind an event handler to the
`button` and when I click on the `button`, we pass a message into the `iframe`
and we listen for a response, so we listen for messages on the page and we pass
messages into the `iframe`.  This is a very, very simple messaging API using
`window.` -- I'm sorry, `iframe.contentwindow.postmessage`.  So, we grab the
`iframe`, we grab its content and then we post the message to that.

The `iframe` looks something like this. The `iframe` loads in
[Handlebars][handlebars] which is a templating library.  And it's a templating
library that does a couple of things for performance reasons that are a little
bit dangerous.  Specifically it's uses `eval` in order to generate a function
and executes this function in order to actually do the work of templating.  So,
it's takes untrusted code. It evaluates in some sort of context and creates a
function which could be executed.  This is a bit dangerous and Content Security
Policy of `'self'` will actually block you from doing this. It'll block you from
using untrusted content in the context of an `eval`.  It'll block `eval`
entirely in fact.

This means that Handlebars could not execute inside the context of the page. So,
if I look at `index.html`, Content Security Policy will actually block
Handlebars from executing.  However inside the context of the sandbox there is
no Content Security Policy because I haven't set one: it's a completely separate
HTML document.  It's also a document that doesn't have access to any of the
information that was in the main page, that was in the `index.html`, so I can
more or less without issue allow JavaScript to execute in this context and allow
potentially dangerous JavaScript to execute in this context without worrying
about it stealing my information because there's no information in this context
for it to steal.

It listens for events or listens for message events, grabs the context that was
passed in and uses that context to populate a template, so Handlebars does its
work.  It uses `eval`, it uses dangerous but very performant code in order to do
some templating and then I can pass that HTML back up to my parent frame and in
the parent frame you'll see that it will actually using
`document.body.innerHTML` to write this content out to the page.

This is incredibly dangerous, you should really never do this inside the context
of an application because `innerHTML` will execute scripts, so if I have a
script tag that's pushed into a page via `innerHTML` that will execute.

The reason that I can do it in this context is because the page is protected by
Content Security Policy.  It says that even if dangerous content has been
injected into the page, no script will actually run.  The worse that an attacker
could do in this case is deface my website by making the sandbox… If they were
able to find a vulnerability in the sandbox the worst that they could do is
generate bad HTML, they couldn't generate dangerous HTML that actually execute a
script and exfiltrated information.

This gives you the ability to separate your application into pieces that need
special privileges and pieces that don't need those privileges.  It allows you
to say that the main application is protected by a very strict Content Security
Policy, the pieces of the application that wouldn't fit into that policy or that
would have issues. Maybe it's a legacy application that you have very -- that
you have a very hard time rewriting for these piece -- for this new style of
programming.  You put that into a sandbox, you allow it execute within the
context of that sandbox and you build a very thin messaging API on top of the
sandbox and on top of the application itself in order to pass messages back and
forth between these two components.

You separate out the concerns and you say that the one piece of the application
should be able to execute script, which should be able to execute potentially
dangerous scripts and the other piece of the application has no need of those
information whatsoever.  It should only rely upon this new API that you built.

This gives you a really nice way of extracting pieces of your -- pieces of your
application but you don't -- that don't need privileges and to reduce these
privileges down to the minimum level that they actually need in order to do
their job.

There's one other thing that a sandbox can potentially be useful for and this
will be available in, we'll say the near future. It's in Chrome Canary right now
but it's not quite there yet in other browsers. Specifically I'm talking about
the [`seamless` attribute][seamless] and the [`srcdoc` attribute][srcdoc].

These allow me first, to create an `iframe` that seamlessly blends in with the
content of my page.  One of the things that you see with a normal `iframe` is;
that it's a completely separate document.  So, it has its own stylesheets, has
its own JavaScript and so on. The seamless attribute allows me to create an
`iframe` in my page and allows CSS to flow down into that `iframe`.  So, if I
have a paragraph in that `iframe`, it's going to use the paragraph style from my
documents not from its own -- or it can override them of course but the CSS
flows down into that document or into the `iframe`.

The other nice thing is that the seamless `iframe` shrink wraps itself to the
size of the content on the page.  So, instead of specifying that I have an
`iframe` that's, you know, 500 by 500.  I can simply say it's a seamless
`iframe` which means it will only be as big as the content, that's been pushed
into that `iframe`.  This is really quite nice.

It works with the same-origin policy.  So, if I load content from my origin then
CSS flows down into it.  If I load content from my separate origin, CSS won't
flow into it because I can actually use CSS to extract information from that
page with some of the new selector attributes that are out.

What you also see here is a `srcdoc` attribute.  This means, instead of making
an HTTP request down to a server to get information to populate this page or
this `iframe`.  I can populate it simply by adding information to an attribute.
This means that all I have to do is correctly escape information for a single
context.  I can look at the information that the user has given me for example
for a comment on a webpage. I can escape that in such a way that it works within
the context of an attribute which is easier than trying to escape it for any
context whatsoever.  And that information is then used as the body of this
`iframe`. So, instead of making an HTTP request, I can specify the content of
the `iframe` directly within the context to the page itself.

For something like comments, this can work quite well because what I can then do
is sandbox this `iframe`.  So, that even if I completely screwed up when
escaping the information.  I can ensure that no plug-ins can run, no script can
run and so on.  But the content that's actually being delivered into this
`iframe` can be executed in a very safe way.  The sandbox attribute is supported
in WebKit quite well.  It's in -- it's been in -- it's been in Chrome for quite
some time.  It's in Safari 6 and it will be in new webkit browsers to come out.
It's just been supported inside Firefox.  So, I think, Firefox 18 now has
support for the `sandbox` attribute and it's supported in IE 10.

So, it's [in the new browsers that are coming out][caniuse-sandbox], but it has
really no downside for old applications.  They will be just as insecure as they
were before if you're using this sort of attribute.  With that, I think I'll ask
if anyone has any questions.

I'd really before -- actually before I would suggest you go out and read [the
HTML5Rocks article][h5r-csp].  I think Content Security Policy is the most
important thing that's happened again in web security for quite some time.  I
think it's really quite important and I would be thrilled if even one of you
started implementing Content Security Policy on your pages.  If you have any
questions about that at all, please drop me an email.  Please contact me [on
Twitter][twitter] or in [G+][plus] and if you have any questions right now.  I'd
be really happy to answer them.  Do we have like a mic anywhere?

**>>** Yeah.  Yeah.  Yeah.

**>> MIKE WEST:** Oh, yeah.  It's over there.  Great.

**>>** So, with the Content Security Policy, you said that you can't also have
inline JavaScript anymore.  What about style, inline styles?

**>> MIKE WEST:** It's the same story.  There is a mechanism by which you can
allow inline style if you really need it.  So, if you have a legacy application
and you simply don't have the time to rewrite it, you can allow inline style but
by default.  It's -- if you set a `style-src` then inline style will also be
removed because it's just as dangerous as inline script.

**>>** I agree.  Thanks.

**>> MIKE WEST:** Cool.  Great.  Thank you very much.  Oh, there was -- there
was another -- sorry.  There was another question.  If you have actually -- if
you have question just come up and ask.

**>>** [INDISTINCT]

**>> MIKE WEST:** The question is…

**>>** [INDISTINCT]

**>> MIKE WEST:** Yeah.  So, the question is: First of all, this looks
difficult.  So, you're talking about sandboxing, correct?  Yeah.  So, building
this sort of API is work and you have to look at your application and determine
what the APIs actually are; what the components are and then build some sort of
messaging framework that pushes messages back and forth between various frames.

You're entirely correct.  It is more difficult than writing an application in
the current style, where you just had everything in a big block that all
executes in the same context.  It is more difficult and it -- I do think it's
the case that frameworks will start to pick up that work.

We see sandbox now being deployed in enough browsers that I think it will be
interesting for frameworks to start building things out on this way.  Until now,
it's only been available in webkit which has made it less attractive for
framework developers.

But this is something, if you look at Chrome applications or Chrome extensions.
This is something that we're starting to force developers to do now.  We use it
all throughout Chrome and this is a mechanism of building applications that we
think has such good security characteristics that it's worth the effort for us
to start asking people to develop in this way.

You're entirely correct, it's more difficult.  My contention is simply that the
benefits outweigh the difficulty.

It won't be the case for every application, but a good example would be the
[office document reader inside of Chrome OS][jorge].  So, the office document
reader takes untrusted documents in `.doc` format, parses them with JavaScript
and then renders them to the page.  And it does it in exactly this style where
you have a sandbox renderer that takes information.  So, you pass a document
into that renderer.  It does this work, it uses all this untrusted code or
evaluates untrusted code and then pass this information back to it's parents in
a way that it doesn't create new security vulnerabilities.

So, it is difficult.  It's not the easiest thing in the world and I don't think
I would be ever claim that it is.  My claim is simply that the difficulty is
worth it because it gives you such good security characteristics.

You know this piece of your application, even if it's compromised, even if you
made huge mistakes, can't access the information that is secure inside the
context of the non-sandbox piece of the application.  So, it's difficult
problem, I agree with you but it's one that I think that's worth addressing.

All right.  Thank you very much for your time.

If you have any questions, I'll probably be at the Google booth downstairs for a
lot of the time.  Actually, one more thing, there's a talk in this room at I
think 4:00 -- I think 4:40 called something along the lines of [Development with
Secure HTTP headers][devoxx-headers].  I think it's going to be worthwhile.  So,
if you go -- if you're interested at all in the other things that you can do,
other things that you can do, other things that you can instruct your browser
about in order to make your applications more secure.  I'd really suggest that
you get to that talk.  I think it's been given by [Frank Kim
(@thinksec)][thinksec] and it should be really interesting.  So, 4:40, this
room, I'll be here and I hope you guys are too.

So, thank you very much!

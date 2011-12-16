---
layout: post
title: "Making Your Web Apps Accessible Using HTML5 and ChromeVox"
tags:
  - a11y
  - chromevox
  - accessibility
  - html5
  - googledeveloperday
  - gdd
  - gddil
  - gddde
  - screenreader
  - transcript
  - presentation

Teaser:
  Back in November, I presented twice at the Google Developer Day in Tel-Aviv.
  The first of those talks has been uploaded, and I spent most of the afternoon
  transcribing it to post here. I wanted to give the audience (you!) an
  introduction to screen readers, and to building accessible websites and
  applications. I think it was pretty successful, and I hope you enjoy it if you
  watch at home.
---
Back in November, I presented twice at the Google Developer Day in Tel-Aviv.
The first of those talks [has been uploaded][1], and I spent most of the
afternoon transcribing it to post here. I wanted to give the audience (you!) an
introduction to screen readers, and to building accessible websites and
applications. I think it was pretty successful, and I hope you enjoy it if you
watch at home.

I'd highly recommend that, if you're at all interested in this stuff (and you
should be), you go out and [install ChromeVox][2] to start playing around with
how your sites sound. It's trivial to get up and running, and will start to
give you a sense of what you're doing well, and what needs improvement. The
team has done a brilliant job putting it together, and it's very much worth
your time to experiment with.

The slides are available at [mkw.st/p/gdd11-berlin-a11y][3] if you'd like to
follow along at home, and here, without further adou, is the embed, followed
by the transcript:

[1]: http://www.youtube.com/watch?v=pwm73Pe5xb8
[2]: http://goo.gl/pqKpN
[3]: http://mkw.st/p/gdd11-berlin-a11y

Video
-----

<iframe
  width="606"
  height="370"
  src="https://www.youtube.com/embed/pwm73Pe5xb8?rel=0"
  frameborder="0"
  title="Google Developer Day Tel-Aviv, 2011: Making Your Web Apps Accessible Using HTML5 and ChromeVox"
  allowfullscreen="allowfullscreen"></iframe>

Transcript
----------

**MIKE WEST >>** What I'd like to discuss with you today is a topic that I
think is incredibly important. It's not a topic that I think is very sexy, and
it's something that often gets ignored when building applications. Even Google's
applications. But I think it's really important to talk about accessibility.

Making applications not only available to a wide variety of people, but usable
by those same people.

As a way of getting into this, I want you to think about the Google+ page. All
of you have probably seen this. There's a button up in the top corner that says
"Add to Circles" and the interaction model is the following. I take my mouse, I
hover it over the "Add to Circles" button, and then something pops up. And at
that point, I'm able to select circles into which I can put one of my friends or
one of my contacts. This works really, really well if I can use a mouse.

All of you close your eyes. Now grab your mouse and hover... over the... That's
kinda problematic, right? If I can't see the screen, how do I use my mouse to
hover over anything on the screen? This mode of interaction, while very
interactive and very rich, excludes a wide variety of people that either can't
or don't want to use the mouse for some reason. And in fact, when we first
launched Plus, this was completely inaccessible. It was impossible to use the
circle picker widget with anything other than a mouse. If you didn't have a
mouse, you were simply out of luck.

What I want to talk about today is how we can avoid that. How we can build
applications that are accessible and universally usable.

There are a couple of types of accessibility, and the type that I really want to
talk about today is users that use an assistive technology of some sort in order
to access a website. These users could be blind, they might be completely unable
to see the screen, in which case they're going to use something like a screen
reader or braille reader in order to get the information provided to them in a
form that they can access. They could be users with low vision, in this case they
might use a magnifier or a lens of some sort in order to make objects on the
screen bigger so they can actually interact with them well. Or they could be
motor impaired in some way. There are people that use foot pedals. There are
people who can only use individual fingers, or they might have some some sort of
mouth control, be it either with a physical object they control with their
tongue, or with speech control such that they can simulate clicks on specific
items on the page.

We want to be able to support all of these users, and what I want to talk about
today is how we can do that with HTML5 and with screen readers.

One such screen reader is called ChromeVox. ChromeVox is a screen reader built
specifically for Chrome by the Chrome Accessibility Team. This uses the
[text-to-speech API that Chrome provides][tts] as an extension API. So anyone
can write anything exactly like this, and actually all the code is open source.
So you can take a look at it and see exactly how it works. This is completely
free, you can download it. It's built directly into ChromeOS as the
accessibility mechanism for ChromeOS, and you can download it for Chrome on any
other platform. It'll work quite well, and in fact I'll demo it a little bit
today.

[tts]: http://code.google.com/chrome/extensions/tts.html

**CHROMEVOX >>** Enter your name. Choose your favorite. Screen Reader Introduction
Heading Three.

**MIKE WEST >>** This is what ChromeVox sounds like. If none of you, if one of you
hasn't used a screen reader before, this is what it sounds like: you get a very
mechanical tone.

**CHROMEVOX >>** [Beep] Enter your name. Edit text.

**MIKE WEST >>** That reads off the thing you're currently focused on on the page,
and generally speaking will give you some meta-information about that. So when
we go back up to the header, we'll hear:

**CHROMEVOX >>** Screen reader introduction. Heading three.

**MIKE WEST >>** It tells you that it's a heading, and it tells you that it's a
level three heading. What this tells you is that the semantics of your page are
really critically important. If we jump down into the form:

**CHROMEVOX >>** [Beep] Enter your name. Edit text.

**MIKE WEST >>** Here we read not only that you can type something into this field,
but we get a label for it as well. This gives you a really, kind of, a rich
visual, er, mental image of what a visual user would see on this page.

**CHROMEVOX >>** [Beep] Choose your favorite color. Red. List box one of ten.

**MIKE WEST >>** It's a list box. There are ten items. It gives you some semantics
along with it.

**CHROMEVOX >>** [Beep] Submit. Button. Having trouble, click here for help. Link.

**MIKE WEST >>** So it tells you that there's a link on the page. And there are some
other functions so you can see where that link goes and a variety of other
functionality. But that's the basics.

What I want to talk about today with that in mind are three things. First, I
want to talk about what you do when you're starting from scratch. When you have
complete control over the HTML, what's the best practice? What should you start
out with?

Second, I want to talk about the case that most of us find ourselves in, where
we have an application that isn't exactly semantic. It doesn't work quite as
well as we'd like it to in terms of the markup or in terms of the CSS, but we
still want to make sure that it's accessible. How do we go about doing that?

And finally, I'll point you to some tools and resources that you can look at
later on. There's a lot of information here. I'm not going to touch even half of
what it takes to make a website accessible, but I am going to give you some
pointers, and I hope that I give you a good basis.

So let's start out.

What's really important to understand about Chrome, er, about screen readers in
general is that all they have to work with is the DOM. They have the document
object model. This means that the semantics of your page are incredibly
important, and the visual aspect of your page is incredibly unimportant. For
instance, we can all see that this sentence here is "The rain in Spain stays
mainly on the plain." Let's see what ChromeVox thinks about it.

**CHROMEVOX >>** Example. Heading.  The plain in rain stays mainly in the Spain.

**MIKE WEST >>** That's a bit odd. I wonder why that happened. If we look at the DOM
that was used to create this, we see that what's happened is that we've simply
used absolute positioning in order to move things around on the page so that
they look like they're in a certain order. In the sentence it makes very little
sense to do that, but in our applications we do this all the time. We take
things from disparate parts of the DOM, and we jam them together visually
because that makes sense, that's how they should be. But we didn't code it that
way. In fact, we coded them at separate ends of the spectrum, and in that case,
a screen reader user, or anyone who is only able to work with the DOM, is going
to have a really hard time understanding your web page, and working with your
web page.

So it's important to understand a couple of things [CROSSTALK] about things when
working with DOM, and when creating a website. What's important, first off, is
to have logical sections of your page, and to order those sections in a way that
makes sense for someone who's trying to use this application. In other words,
the thing that's most important about your page should probably come near the
top of the DOM. The things that are much less important should probably come
near the bottom, even if it's easier for you in some way to put navigation links
all the way at the top of the DOM, those probably aren't the things people are
most interested in, so you want to put them later on the page.

It's also important to group the things on the page together that have any sort
of semantic relationship with each other. You can use any sort of HTML5 tag to
do that, for example, the `section` tag.

Last thing, yeah, it's important not to use tables. Tables are for layout. Or,
not for layout. They are for data. If you're trying to set up something on your
page with tables, then you're at the wrong conference in general. So, don't do
that.

Interactive controls. What's interesting about a lot of applications and a lot
of modern web applications that we see on the web today is that people are using
`div` and `span` to mean absolutely everything. This is a really bad practice
for a wide variety of reasons. There are are elements that actually have
semantics associated with them, and have interaction associated with them. For
instance, if I have an `onclick` event on a `div`, I have to do a lot of work in
order to make that replicate something like a `button`. If I just used the
`button` element, I get a lot of that for free. I get some keyboard
interactions. I've ensured that it has the exact same semantics as a native
button on a native web application, because the browser is doing the work for
me. I don't have to go through and build all of this out myself, I can leverage
the power of the browser, use the correct element, and in that case, get things
like keyboard accessibility almost for free. This is just good practice, there's
no reason not do this at all.

The last thing here that's really important to note is that `div`s and `span`s
are by default not focusable. If they're not focusable, they don't show up for a
screen reader. It's just that simple. You need to make sure that anything that a
person is interacting with can obtain focus on the page. I'll give you a quick
example of why that's important. In a little bit.

So if we turn ChromeVox back on [CROSSTALK].

**CHROMEVOX >>** Custom button. Live coding example. Heading three.

Click on this button.

**MIKE WEST >>** So, there's probably a button coming up. I've just heard some text
that said "button", that's important. So let's jump to the next element on the
page.

**CHROMEVOX >>** Send.

**MIKE WEST >>** Send. Ok. Let's hit a button. Well, nothing seems to be happening.
I wonder why that is. If I click on "send", of course, I get an alert. Hrm.
Something's going wrong here, what could it be?

The most important thing is to simply change this to a `button`.

If we change it to a button, and then refresh.

**CHROMEVOX >>** [Beep] Send. Button.

**MIKE WEST >>** Send, button. ChromeVox now recognizes this as a semantic element.
If I hit enter again, I get the alert. In other words

**CHROMEVOX >>** Send. Button.

**MIKE WEST >>** Enter will simulate a click, if the element is a button. The
browser will do the work for you. If it wasn't a button, you would have to do
things like `onkeydown`, and then, have an event handler for `onkeydown` in
order to make sure that you replicated all of the functionality that a browser
would.

This is something that you simply don't want to do on your own. You want
to make sure that you use the right elements.

**CHROMEVOX >>** Labeling. Label your.

**MIKE WEST >>** What's also important, specifically with regard to forms, is to
make sure that every element on the page that users are going to interact with
in some way has a label. This is incredibly important, and it's difficult to
overemphasize how important this is. If you don't have labels, then you simply
have text boxes on the page. A text box is completely meaningless without
context. I know that I'm supposed to enter some information into this text box,
but I have no idea what it is, and I have no idea why it might be important for
my interaction with this application. If, on the other hand, I have a label, and
the label syntax is absolutely trivial: You simply say "label", and then use an
ID in order to say what this thing is labeling. If I do that, then the screen
reader will understand that there is a semantic relationship between the text
and the element on the page. It will bind those together when it reads them out
to me. In other words, I will get good semantic information about what this
thing on the page is that I'm meant to interact with.

Again, and this should be really really basic, every image on your page should
have an `alt` tag. There's no reason at all that an image shouldn't have an alt
tag. There are two types, however, of images on your page. There are images that
replicate information that is already available, in other words they are purely
decorative. And there are images that are, in and of themselves, informative.

For the former type, you should have a blank `alt` tag. If you have a blank
`alt` tag, that means "I've thought about this. This image exists on the page,
it's visually important, but it has absolutely no semantic meaning." In that
case the screen reader will simply ignore it. A blank `alt` tag means "ignore
this image."

A missing `alt` tag is, however, something completely different, and we'll look
at exactly what that does in a moment. For the normal use case, you have an
image on the page that's informative in some way, you should have alt-text
associated with that that says "This image has some meaning, here's what it is."
Otherwise, it's completely useless for a person who can't see the page.

So, again, let's take a quick look at what a form sounds like when you don't do
things correctly.

**CHROMEVOX >>** Edit text.

**MIKE WEST >>** Edit text.

There's nothing here. I know that there's a text box. I should probably type
something, but I have no idea what it is.

Oops.

**CHROMEVOX >>** Password. Edit text.

**MIKE WEST >>** Password. Edit text. That's interesting. It doesn't really help me.
I know that it's a password, and that's better, but it really doesn't help very
much.

Now let's look at the image. What's really interesting about this is that I have no
alt text here at all. What this means [CROSSTALK]. This means that the browser is
going try to figure out something for me. And usually it does an absolutely
miserable job.

**CHROMEVOX >>** Nine zero one d three n nine four t three. Image.

**MIKE WEST >>** So it reads the name of the image. Especially when you have these
sorts of big CMS systems that automatically generate images in a variety of
sizes and a variety of contexts, the name of the image is never informative. But
it's just common practice that a screen reader will try to give you any
information that it has. And in this case, the only information it has is the
name of the image. This is really really bad behavior, and it's something that
you should avoid to whatever extent possible when building your own
applications.

Let's look at how we would solve this problem.

The first thing we would need to do is change these `span`s to `label`s.

By doing so, we give each of the, each of the elements on the page, or each of
the form elements, semantic information. We tell it that the first label is
pointing to the first form element.

I can't talk and type at the same time, as we're finding out. For user.

I just can't type at all, I think is the problem.

So.

**CHROMEVOX >>** User name. Edit text.

**MIKE WEST >>** So this time, when I click on it, or if I'd given it focus in some
other way it would have behaved the same, when I click on it, it not only reads
out that it's an edit text box, it also tells me the label associated with it so
that I know that here I'm supposed to type my user name. That's excellent
behavior.

Now let's fix the image.

**CHROMEVOX >>** User name. P I N. Password. Edit text. Golden Gate.

**MIKE WEST >>** Excellent. So now I know that there is information associated with
this image. In that case, I'm actually able to use it to understand the page. So
again, big lesson here: use an `alt` tag, use `label`s. Both of them are
absolutely critically important, and really very basic. If you're not doing this
already, you're doing the wrong thing.

What we've talked about and what we've seen here is that focus is really
important. You see a big outline on the page of what the focused element is. The
focused element is exactly what the user is currently interacting with. If they
have a mouse, they might be hovering over something completely different, or
they might be clicking on things that can't accept focus. That simply isn't the
case when you're dealing with someone who's using a screen reader. In this case,
you need to make sure that you provide focus hooks within your application.

First of all, so that the important elements the user is supposed to interact
with are focusable. And second, that you not only accept, um, you not only
accept things like hover and, um, onkeydown and a variety of other things along
those lines.

What will become important later, what we'll see later on is that it's not only
important to ensure that each element can be focused, but also important to
manage focus on the page. If, for instance, I have a dialog box that pops up, I
want to make sure that the focus stays within that dialog box if it's modal.

I'll show a quick example of how that might work.

So here I have "Buy more printer ink". I get a modal dialog box. I see that it's
modal because the screen has been darkened, so I have some sort of visual
feedback that I should click on one of these two buttons before I do anything
else. I'll click on that. Let's see how it sounds.

**CHROMEVOX >>** Popup dialog. [Beep] Buy more printer ink. Button.

**MIKE WEST >>** So it's a button. That's good. I hit a button.

What happened?

According to the screen reader, absolutely nothing, because the focus didn't
move. I hit enter, or I clicked on it, but the focus stayed on the button
because nothing told the focus to move. What really needs to happen here,
probably the best case scenario, is to move the focus programmatically to the
first focusable element within the context of this dialog box.

Let's see what we can do about that.

Happily, moving focus around is incredibly trivial. You simply have to call
`.focus()` on the correct element. Let's look at it again.

**CHROMEVOX >>** O K. Button.

**MIKE WEST >>** What we see here is that focus was automatically moved inside the
context of this dialog box. That's great. However, there's another aspect that
we need to think about. What happens when I click on one of these two buttons?
What happens in that scenario, if I hit enter, focus is dropped on the floor. In
other words, nothing on this page has focus anymore, which means the screen
reader is going to start back up at the top of the page. That's really bad
experience.

What we instead want to happen is to bring the user directly back to where they
were when they activated this dialog box. We can do that relatively trivially.
So here we see that the button is called "confirm", so I can simply associate
focus with confirm.

If I refresh this:

**CHROMEVOX >>** O K. Button.

**MIKE WEST >>** Jumps me in.

**CHROMEVOX >>** Buy more printer ink. Button.

**MIKE WEST >>** Jumps me back out. This is good experience. This means that I move
directly from the dialog, directly back onto the page where I was. I know where
I am, I understand the context, and I'm able to deal with that.

What we

**CHROMEVOX >>** O K. Button.

**MIKE WEST >>** What is problematic, however, is that if I keep hitting Tab, I can
jump outside of this dialog box. Visually, I understand that I'm not supposed to
do that, the page is dark. However, that doesn't really work when dealing with a
screen reader. Instead, we need to manage focus for the user in order to show
them that they should stay within this context. They need to make a decision,
yes or no. That's the only time you should use a modal dialog.

So how can we go about doing that ... [CROSSTALK]

**CHROMEVOX >>** Buy more printer ink. Button. [CROSSTALK]

**MIKE WEST >>** ... and type, so I will copy.

I am cheating, and it's awesome.

There we go.

So now, I'm hitting tab, and trying to get out of the box. Shift-tab would bring
me to the previous focus item. I'm not able to. I've thrown in some code that
makes it possible for me to intercept `blur` events and `focus` events, and make
sure that I'm only focusing on one of the two items that should be focusable
within the context that I currently find myself.

This isn't that difficult, basically, I'm really just adding event listeners and
dealing with it.

Um.

And now Chrome is crashing. Ha ha.

You know what's awesome? [Dev version of Chrome][dev].

[dev]: http://www.chromium.org/getting-involved/dev-channel

I really recommend that you use the dev version of Chrome. I do not recommend
that you demo with the dev version of Chrome because it causes small problems
like this.

Good times. Let's see if I can get out of this.

Regardless.

Um.

Doo, doo doo, doo doo. Ha ha. Good times.

Ah, my good friend Force Quit.

My good friend Force Quit. There we go, hey look at that.

Now let's open this back up.

So what you might not know about Chrome is that we have three different
channels. Actually we have four, but three are important.

We have a stable channel, that's what every user actually gets. And it is, as
the name implies, stable.

We have a beta channel, the beta channel is a little bit less stable than
stable. Stable gets built about every six weeks, beta gets built probably about
every three weeks. Dev, on the other hand, is built on a weekly basis, sometimes
more than weekly. More than weekly is actually awesome, because it shows you
exactly what's happening on trunk. But. It's slightly problematic in that
sometimes it's broken. Like now. Ha ha.

Anyway.

The last thing I'd point out when dealing with applications that you have
complete control over are keyboard shortcuts. It's really quite useful to give
users the ability to control the application in a controlled way with a
keyboard. For instance, if you go to GMail, you might not know that you're able
to use Vim keybindings, so J and K, in order to jump between messages. You're
able to use keybindings in order to archive, and jump back to the inbox. It
actually makes you much more efficient.

For specific types of applications, keyboard shortcuts can be incredibly useful.
There are three types that I list up here. I don't really think it's incredibly
important to talk about them, and I'm running out of time, so I'll move on.

We've talked about the ideal world. When you have complete control, you want to
use semantic elements, and you want to make sure that you manage focus
correctly, and that you only use those elements that kinda do all the work for
you. That you use `button`s instead of `div`s and so on.

What we usually end up with, in the real world, is code that kinda looks like
this. It's just a jumble of random crap thrown onto the page. You need to figure
out first what it is, and then you need to change it to do something useful and
accessible.

Generally this means that you're trying to build an interactive control that
HTML simply doesn't provide for you. So if we look back to the circle picker
that we looked at before, there's no native HTML widget that says "When I hover
over this thing, pop something up and do some sort of checkboxy goodness." That
simply doesn't exist as part of HTML; It's something you need to build on your
own.

When we find ourselves in these sorts of situations, we need to figure out how
we implement that in a way that is actually accessible. One thing that we can
use is something new called ARIA.

ARIA is part of the HTML5 specification, kinda, depending on who you ask, and it
gives more semantic information, or it allows you to create semantic
relationships first of all between elements on the page, but also to add
semantics to an element like a `div` that, by itself, means absolutely nothing.

If we look at something like this, this is kinda what the widget looks like, you
have two pieces. You have a button and a popup, and we need to figure out how to
make those accessible. The HTML that we're stuck with for whatever reason looks
like this. We've got some `div`s, we've got some `span`s. There's really nothing
here that a user can actually do anything with, the screen reader.

So what do we do about it?

The first thing we need to do is to make sure that the elements that a user
interacts with are focusable. `div`s, as I said before, by themselves are not
focusable. They simply get ignored by the screen reader, and instead it jumps to
their content.

What we can do, however, in order to make it focusable, is to add a `tabindex`.
`tabindex` means, when you are tabbing through the page, when you're using the
tab key to jump between the focusable elements, first of all this element should
be in the tab, uh, in the tab order, and second of all, perhaps it has a
specific position.

I have never actually used tab order to say that an element has a specific
position. Instead, I set a tab order of zero, which means
this element is focusable, and this element should appear wherever it appears in
the DOM.

A `tabindex` of -1 is also sometimes useful for specific scenarios. This means
that if you're tabbing through the page, this element doesn't get focus, but if
you're using a screen reader or if you're, if you want to programmatically
assign focus in some way, you can.

**AUDIENCE >>** _[UNINTELLIGIBLE]_

Sorry?

**AUDIENCE >>** _[UNINTELLIGIBLE]_

Sure, we can talk about details and stuff later on.

Um, right.

So, we talked a little bit earlier about the keyboard, and about the fact that
the keyboard is an incredibly important mechanism for interacting with a web
page. You need to make sure that you support it. This means that your custom
controls should respond to the keyboard in the same way that a native control
does. This means, if for example, I tab over to a link on the page, and I hit
enter, that link is going to be executed. I'm going to jump to that link. If I'm
on a button and I hit enter, it's going to do something.

I need to make sure that my custom elements do the exact same thing, and there's
a lot of work associated with this. I first of all need to figure out what the
semantics are, and second I need to replicate those semantics within the context
of my JavaScript.

This is why it's better to simply use the correct to begin with, because then
you avoid a lot of work. But if you can't avoid that work for whatever reason,
you need to make sure that you deal with the `keydown` or the `keyup` event, or
a `keypress` event, depending on the interaction that you want.

You need to make sure that you deal with things like enter and escape, in
interesting, and, you know, normal ways, ways that a user would expect.

The code for that might look something like this: you intercept the `keydown` or
a `key` event of some sort, you look at the event, and then you look at the
`keyCode`, and you need to figure out what the `keyCode` actually is. This is
space, this is enter.

It's generally better practice not to use magic numbers in your code, but
instead to set up some sort of constants so that you actually read "space" or
"enter", but I didn't have space, so I did this.

Also important to note is that [the W3C has a document that documents a couple
of common keyboard patterns][keyboard]. Things like "Escape should cancel a
dialog box." Things like that are documented relatively well, but the W3C, the
only problem with that is that it's relatively Windows-specific. It's not the
case that all keyboard shortcuts are the same on all platforms. So, keep that
in mind, and make sure that you are tuning your keyboard shortcuts to the
platform that most of your users are actually using.

[keyboard]: http://www.w3.org/TR/wai-aria-practices/#aria_ex

If we look at the first part of this widget, I said it was in two parts, look at
the button first. And this actually acts very much like a button, even though
the user has to hover over it. That's not the usual button behavior, but the
conceptual behavior is very similar. I interact in some way with this thing, and
then a modal dialog pops up, and I have to interact with that dialog.

So here we're going to act as though this `div` is a `button`. We do that first
of all by giving it `tabindex` such that I can tab to it on the page. This means
that enter for instance, I'll be focused on it, I'll press enter, that will
simulate a click, and I'll get some sort of interaction with this button.

What we don't have, however, is the label semantic. What we instead have to do
is to put text into the `div` such that it actually gets read out when the user
focuses on this `div`. Again, there's no `label` that can be associated with
anything other than an input element or select element or form element of some
sort. That behavior simply doesn't exist. So you have to make sure that there's
textual content in everything that you have on the page. Even if it's like a
gear, because you're doing some sort of settings menu, you can't simply have a
gear as like a background image. It's much much better to have a `div`, actually
a `button`, but if you have to have a `div`, then make sure that `div` has
textual content so that a screen reader can actually read it.

If we look at the dropdown that pops up when I hover over this thing, it acts
much like a modal dialog, so a modal dialog is what we should emulate. We should
make sure that when I'm tabbing through, that I can't tab out of the dialog. I
have to make a decision here before I can interact with something else on the
page. We should make sure that it's focusable, and we should make sure that the
elements in particular are focusable. If you look, there are checkboxes up
there, um, it's a little bit light... but there are checkboxes up there. Those
are implemented as `div`s, so we need to make sure that those also are
focusable, and that when I do something with them, they behave exactly like a
checkbox would.

What we can then layer on top of all of this backend work, so I do all of the
event handling, I do all of the markup, what I can then do to add more semantics
is to layer on ARIA. ARIA is a mechanism by which I can say that this `div` is
not only a `div`, it actually has a role on the page. In this case it might be a
role of button. This means that when I use a screen reader, or anything that
would extract semantic information from the page, it can look at this `div` and
understand that this `div` is actually a `button`. This means that the screen
reader would read "Add to Circle. Button." and then the user would understand
that they could interact in some way with this thing that they've been presented
with.

What's important to note is that this isn't a panacea. This doesn't do the work
for you of dealing with the keyboard or of making elements on the page
focusable. It simply adds a semantic layer. You still have to do the work of
intercepting keyboard events, and you still have to do the work of making sure
that these elements are, um, potentially interactable.

So, these are a couple of examples of ARIA roles that you can have. You can have
a `button`, and this means that it is a button on the page. You can click on it
or use the keyboard in order to interact with it. It invites interaction in that
case. A menu item is another example, and search are, kinda, is a landmark on
the page so a screen reader can give you some information about the semantics of
the page itself. Not simply specific elements, but the things that exist on the
page. So there is a search widget somewhere, I can jump to that, potentially.
There are sections of the page that have, are, that bind content together in an
interesting way. I can jump to those.

Screen readers, by and large, at the moment, don't support ARIA landmarks as
well as they could. What they generally support are headings. This means that if
you have a good heading structure on your page, a screen reader user can easily
jump from one heading to the next, and get a good understanding of what's on the
page. What will be happening in the future is that screen readers will have
better support for ARIA landmarks, and then you'll be able to jump to specific
landmarks on the page as well.

This is already the case in some screen readers. But it's not really across the
board quite yet. But it's something that we should start thinking about now, and
experimenting with now in things like ChromeVox, so that we can use them in the
future when they become more ubiquitous.

It's not only the case, however, that ARIA describes roles on the page. So it's
not only the case that I can say "It's a button." I can also say that this
button, or that this checkbox, for instance, has been checked. This means that
the `div` has a role of checkbox, it acts as through it was a checkbox, but it
has properties associated with that. In this case, `aria-checked`. This allows
me to determine programmatically whether or not this item is in a checked state.
So if the box should show a check mark or not. It also enables the screen reader
then to read that out to me, so that when I hover, when I focus on this element
on the page, the screen reader can tell me it is a checkbox, and that the
checkbox is checked.

Using this sort of state information in order to give the user more semantic
information about how the page is put together, and what state it current finds
itself in, is incredibly useful.

The last thing I note here is ARIA live region. A live region of the page. If
you've ever used Twitter, and probably most of you have, you know that when
you're typing in your status message, there's a, there's a number next to it
that counts down from 140. As you're typing, it tells you, you have, you know,
20 characters left. It's really quite useful to mark this region as updating, as
something that screen reader should pay attention to, even if I'm not directly
focused on it. This means, if I mark it as a "live" region, I can type a little
but, and then, in a lull, the screen reader can tell me that this thing on the
page updated itself. So I type a little bit, I wait, the screen reader tells me
I have 20 characters left.

`aria-live` is the attribute that allows the screen reader to understand that
this piece of the page is going to update itself, and that it's important to pay
attention to.

So, if we jump back to the add to circles widget, we could implement it
something like this, where we have the `div` for the button, we tell the browser
that it's a button, we tell the browser to make sure it's focusable by giving it
a `tabindex` of 0, and we have some text inside of it such that, when I focus on
it, the screen reader tells me something interesting.

We can set up this thing here as a dialog, and the ARIA, the screen reader will
tell me that this is a dialog that I need to interact with before I move
further. We can make sure that these checkboxes are interactable by giving them
`role` of checkbox, I didn't put a `tabindex` of 0 here. I should have. I need
to. And I need to make sure that there's an `aria-checked` attribute in order to
tell me whether or not this is checked.

So, at this point, I would just say that there are two tools that I think are
really quite useful when testing your own applications for accessibility.

The first is [ChromeVox][2]. It's a completely free screen reader that's
relatively easy to use for people who have never used a screen reader before.
There's good documentation, it's an extension for Chrome, you can go to the
Chrome Web Store, download it, install it into Chrome on any platform, and it
will read text to you.

This gives you kind of a quick and dirty mechanism for testing the accessibility
of your page. It's not going to be exactly like a blind user using your page,
because they use screen readers simply differently than I do, for instance. But
it's a good sanity check. You can look at your page, make sure that things more
or less work the way that you would expect them to when you're tabbing through.
That things are in the right order, that things are focusable.

That is really useful information.

[ChromeShades][shades] is an accessibility tool that basically turns off all CSS on your
page, and makes it, makes it very obvious when you have a DOM that makes no
sense. So if you look at your page, you read through it, and you have no idea
what's going on, then you know that the styles that you've made, that you've
applied to your page, are more than presentation, they are in fact semantic. And
you need to fix that. You need to make sure that the DOM that you present to a
user is usable and semantic.

[shades]: https://chrome.google.com/webstore/detail/hlklboladblmgfpkenhlgbhoojdlfoao

Another screen reader that is quite useful is [NVDA][]. NVDA is, I think it's
Windows only, for Firefox. It's a really great screen reader. It's free, so if
you just pop open a VM and start using it, it's really quite good. VoiceOver on
Mac is also quite good, but not quite as good, I think, as NVDA.

[NVDA]: http://www.nvda-project.org/

There are a couple of libraries with accessibility support within their UI
components. jQueryUI is doing quite a good job. GWT is getting there, Dojo has
done an excellent job.

At this point, I think I'm running out of time, so I would ask if any of you
have any questions.

I'll pop up some final thoughts that you can read while you're asking.

Yeah?

Q&A
---

**AUDIENCE >>** _[UNINTELLIGIBLE]_

**MIKE WEST >>** The question is whether ARIA is part of HTML5 or is a separate
namespace. To be perfectly honest, I don't know. I know that there was a lot of
argument about it. And honestly, I don't care, because it's supported in
browsers, so whether it's part of HTML5 or a separate standard is kinda
irrelevant. Browsers generally support it, screen readers generally support it,
and it is the only mechanism by which you can add this sort of semantic layer to
the page. So, I would suggest that you use it, regardless of what a standards
body tells you.

**AUDIENCE >>** _[UNINTELLIGIBLE]_

**MIKE WEST >>** The role element, whether... I think the role element is in fact
part of HTML5, that it validates if you go to [validator.nu][valid]. Um, whether it's
part of the spec or not, I don't know.

[valid]: http://validator.nu/

**AUDIENCE >>** What's the state of ARIA support?

**MIKE WEST >>** The question was what the state of ARIA support is. Modern browsers
generally support ARIA, and generally make the information available to
accessibility, uh, tools. So, I know Chrome, excuse me, Chrome is working on it.
Chrome has relatively decent accessibility support now. If you look at the dev
version of Chrome, it's relatively good. It exposes the sort of semantic
information, like a role of button. That wasn't the case as of, like, Chrome 12
and 13. We made a lot of effort in 14 and 15, and we've made even more effort
since then. So Chrome is getting there.

The support in Firefox has been better over time, they're generally doing quite
a good job of leading in terms of accessibility support within the browser, and
the combination of Firefox and NVDA is quite excellent.

So, we're getting there with Chrome. ChromeVox, I think, is a really good step
in that direction. As I said, it's embedded into ChromeOS, so we're making sure
that when we roll out new, new iterations of Chrome, that we add accessibility
support.

IE also has generally quite good accessibility support, or at least, it exposes
all of the right things to the operating system layer. That said, IE6 and IE7
don't understand ARIA at all. IE8 has a little bit of understanding, IE9 is
really starting to get there.

So, I would say modern browsers have pretty good support for ARIA, and the
support will only get better as time goes on.

**AUDIENCE >>** Is there any, um, is there any connection between accessibility
_[UNINTELLIGIBLE]_.

**MIKE WEST >>** So the question was, something along the lines of whether things
like alt tags not being there can be validated by tools, or whether that could
be part of HTML validation. Is that a correct...

**AUDIENCE >>** W3C. You want to have HTML5, HTML4, validate _[UNINTELLIGIBLE]_.

**MIKE WEST >>** The question, ok, the question is whether `alt` can be associated
in some way with valid HTML5 and valid HTML4. If you don't have an `alt` tag
then it would simply be invalid.

I think that's unlikely to happen for a variety of reasons. What I would suggest
is.

I'll. You can tell me about it in a moment.

What I would suggest, before we get there, is that there are tools that will
help you determine whether your page is accessible. None are really exceptional,
it really requires some human interaction. But I wouldn't necessarily rely on a
validation tool to tell me whether my site is accessible. That's kind of two
separate questions entirely.

**AUDIENCE >>** _[UNINTELLIGIBLE]_

**MIKE WEST >>** There are, there are, well, accessible pages will validate. I mean,
that's the case. If you use ARIA, and you use the new, validator.nu, it
understands all the ARIA syntax, and will validate your page for you. It will
also give you warnings for things like `alt` tags not existing.

What I would suggest is that you look at things like [WCAG][]. There are documents
that declare what it means to be accessible. I don't find them necessarily
convincing, but they work really well for people like government who have to
have a checklist of things that they go through to say "this page is
accessible."

[WCAG]: http://www.w3.org/TR/WCAG/

I really think it requires human interaction and human testing, but there are
tools out there that purport to tell you whether your page is accessible.

Real quick, over here.

**AUDIENCE >>** _[UNINTELLIGIBLE]_

**MIKE WEST >>** I'm told that images will not validate without `alt` tags. So, yay
world.

**AUDIENCE >>** What about access keys? They seem to be gone?

**MIKE WEST >>** About access keys? I don't actually know if access keys are
supported in any browsers. Generally speaking, the support, as I understand it,
wasn't very good, and everybody implemented it themselves anyway. My
understanding is that the best thing for you to do is to build the keyboard
support into your application that actually makes sense for your application.

GMail doesn't use access keys. GMail does everything via JavaScript.

**AUDIENCE >>** _[UNINTELLIGIBLE]_

**MIKE WEST >>** Yeah. The comment is that nobody uses access keys anymore. I don't
think anyone ever used access keys, or at least they they were never well
supported.

Ok, well. You did. So that's good.

I would suggest that you use JavaScript in order to script your page.

**AUDIENCE >>** _[UNINTELLIGIBLE]_

**MIKE WEST >>** I wouldn't say that it's more accessible to have access keys. To be
perfectly honest, I don't know what the support is for access keys, for that
attribute.

**AUDIENCE >>** I'm a strong advocate for accessibility, but my product manager not
so much. How can I push it to my product manager?

**MIKE WEST >>** So, the questions is how can a strong advocate for accessibility
convince business people that accessibility is important.

This is a problem that everyone faces. Google faces it. You see some of the apps
that we have aren't as accessible as they should be. We're really working to
make them more accessible, but it hasn't always been a priority.

I think the single most important thing you can do is to look at your current
user base. Generally speaking, the number of people who can't access a webpage
is relatively low. There aren't an amazing number of disabled people in the
world. It is a large number, not probably not large enough in and of itself to
convince a business person that this is a really important group.

What's more important are the PR benefits, or, not even benefits, but PR harm of
people saying that they simply cannot use your website.

It's good to look at past legal cases. If we were in the USA, I'd say look at
[the Target case][target], which was problematic for a variety of reasons. If
you're in Israel, I'm told that there is a law coming up that will enforce
accessibility in some way for sites that are used for certain groups of people.
I know nothing about it, and I am not a lawyer, so everything I'm saying is
probably wrong.

[target]: http://en.wikipedia.org/wiki/National_Federation_of_the_Blind_v._Target_Corporation

I would suggest that you look at the laws in your country. Laws are usually a
good way of convincing people that don't otherwise want to be convinced.

I think it's probably the worst argument, but it is an effective argument for
that type of person.

**AUDIENCE >>** _[UNINTELLIGIBLE]_

**MIKE WEST >>** That's a bad thing.

Anything else?

Great, if there are any other questions, come up. Thanks!

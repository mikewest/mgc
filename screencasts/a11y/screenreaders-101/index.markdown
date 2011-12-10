>> MIKE: Hello, Internet!

I'm Mike West, a developer advocate on the chrome team, and, in the next five or so minutes, I'd like to introduce you to screen readers as a first step towards talking about accessibility on the web.

A screen reader is a piece of software that takes the textual content of a web page, and renders it into synthesized speech so that a person who can't see the page can nonetheless interact with it in a practical way.

The screen reader I'm using here is called ChromeVox. It's the accessibility system at the core of ChromeOS, and it's available as an extension to desktop Chrome. It's really easy to get up and running, and it's a great way to start playing around with the world of screenreaders.

I've got a demonstration page here, let's reload it and see how it sounds.

>> CHROMEVOX: A ChromeVox demonstration.

>> MIKE: So, entering a page, ChromeVox (and most screenreaders), will read you the title of that page in order to give you some context as to what it is you're about to see. Now, as I mentioned, a screen reader user most likely can't use a mouse. So, a system of keyboard shortcuts has been set up to allow them to navigate through a page. Let's use one now.

>> CHROMEVOX: Hello, World! Heading One.

>> MIKE: So it reads me "Hello, World", which is obvious, and then it tells me some additional semantic information: in this case "Heading one". It can do that because I've used semantic HTML in order to structure this document. This is an H1 element, it's a heading on the page, and the screen reader knows that. It can tell me about it to give me some extra context for the text that it's just read me.

Let's move on to the next element and see how that sounds.

>> CHROMEVOX: I'm [Beep] ChromeVox Link. Comma. the DOM Document Object Model is all I know. Period.

>> MIKE: Interesting. ChromeVox has read something that's actually different from what I see here. Let's hop into the DOM and figure out why that is.

Well, as we can see here, I've actually wrapped individual pieces of this sentence in spans, and moved them around with relative positioning. This confuses the screen reader, because all that it has access to is the DOM. If something comes first in the DOM, it's going to get read first by the screen reader. The screen reader simply doesn't understand the CSS that you've applied. And we do- we see this happening all the time in applications and web pages. We take things from the bottom of the DOM and move them all the way to the top of the page, visually, because it makes sense there. But, given the way the DOM is structured, it can be difficult to navigate to those things just using a screen reader.

Two other things to note within the context of this sentence: first, "ChromeVox" is a link, and the screen reader read it to me differently so that I would know it's a link. It changed the pitch, and it said "link" after the word, meaning that I can use this to go somewhere else. That's nice. Also, if you look at the  word "DOM", it's actually an abbreviation. And if we look at the DOM, we'll see, hey, it's an abbreviation with title "Document Object Model". This means that the screen reader takes the additional semantic information that's available within the context of HTML, and reads it to me in a way that is, uh, that's usable for someone who can't use the mouse to simply hover over this word and get the tooltip.

Let's move on to the form and see how that sounds.

>> CHROMEVOX: [Beep] What is your name? Edit text.

>> MIKE: So I hop into the form, and a couple of things happened. First, it plays a sound, a beep, that tells me I'm in an input field of some sort. Then it reads the label for that input field. And then it says "edit text", meaning that I can start typing something to interact with this form field. It's really important to ensure that all of the fields in every form that you create have labels. Otherwise the screen reader would just say "edit text", which isn't very useful. It tells me that I can type text, but doesn't give me any hint at all as to what text I should type.

Let's move on to the next field.

>> CHROMEVOX: [Beep] What is your quest? Password.

>> MIKE: This is a password field and it tells me that. Apparently quests are very secretive. In this case, it again takes extra semantic information, and renders it to me in a way that I can hear, and interact with.

>> CHROMEVOX: [Beep] What is your favorite color? Blue. List box one of two.

>> MIKE: So a list box, or a select element, is, uh, contains multiple options, and here it tells me that there are two options. If blue isn't my favorite color, for instance…

>> CHROMEVOX: Yellow. Two of two.

>> MIKE: I can choose yellow, which is, ah, a much more beautiful color. Let's hop down to the button and see how that works.

>> CHROMEVOX: Right, off you go. Button.

>> MIKE: So it tells me that it's a button, and I know that with a button, I can click on it. What I can also do is use the enter key to submit this form. 

[pause]

>> MIKE: And when I submit the form, it amazingly takes me to ChromeVox in the Chrome Web Store. If you want to get involved in screen readers, and start playing around with them yourself, I'd highly recommend that you hop over to the web store, you type in "ChromeVox", and you install it. It's a one-click install, it's free, and it's really easy to get up and running. It gives you a good introduction to screen readers, and something that we can build on later on when we start talking about ARIA, custom, uh, custom widgets on a page, and a variety of other things that you'll need to think about when building accessible websites. So please, head out, download ChromeVox, and start making your sites accessible.

Thanks. 

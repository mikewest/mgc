---
layout: post
title: Content Security Policy
tags:
  - http
  - security
  - contentsecuritypolicy
  - xss

Teaser:

---
> The browser is not a safe programming environment. It is
> inherently insecure. -- Douglas Crockford, ["Ajax Security"][crock]

[crock]: http://www.slideshare.net/webdirections/douglas-crockford-ajax-security-presentation

The web's security model is fundamentally broken, and has been since the beginning. Browsers trust the code they receive from a website completely, meaning that each chunk of JavaScript that executes on a page runs with access to the entire origin's data. Cross-site scripting attacks exploit this trust, injecting malicious code into a site in a wide variety of ways. At best, sites are defaced. At worst, user session data is compromised.

It is, of course, possible to completely eliminate this class of attacks by properly escaping every bit of data that makes it onto the site. A brief glance at history shows that this defense is unlikely to be effective; given the convoluted set of escaping rules in various HTML contexts, differences in cross-browser implementation, and browser bugs (like [UTF-7 support][utf7]), it's simply a Hard Problem™. Even with solid understanding of the problems, and a variety of secure frameworks, it remains trivial to accidentally create a hole, and one hole is all it takes.

Content Security Policy is relatively new addition to the web platform that promises to mitigate the risk of XSS attacks by giving administrators fine-grained control over the data and code that ought to be allowed to run on their site. The feature boils down to a whitelisting mechanism for images, script, style, and a variety of other resource types. A site declares an acceptable list of origins for each data type via a straightforward HTTP header, and browsers that support [the draft specification][spec] simply refuse to load resources that aren't listed. A quick example should make this clear.

## mkw.st's Policies

On [mkw.st][mkwst], I'm using one stylesheet, hosted on `mkw.st`, one of Google's web fonts, and a few inlined `data:` images. I'd like to ensure that that remains the case, and that I don't accidentally load script from my friends at `evil.com`.

I've configured my server to generates the following headers when loading the site:

    $ curl -Ik https://mkw.st/
    HTTP/1.1 200 OK
    Server: nginx/1.0.8
    Date: Sat, 08 Oct 2011 10:38:40 GMT
    Content-Type: text/html; charset=UTF-8
    Content-Length: 7940
    Last-Modified: Sat, 08 Oct 2011 05:07:16 GMT
    Connection: keep-alive
    Vary: Accept-Encoding
    Strict-Transport-Security: max-age=604800
    X-WebKit-CSP: default-src 'self'; img-src 'self' data:; font-src https://themes.googleusercontent.com;
    X-Content-Security-Policy: default-src 'self'; img-src 'self' data:; font-src https://themes.googleusercontent.com;
    Accept-Ranges: bytes

The interesting headers are `X-Content-Security-Policy` and `X-WebKit-CSP`[^1], both of which contain a simple, semicolon-separated list of policy directives. Each directive consists of a type followed by a set of one or more "source expressions" that define the policy's limitations. These expressions generally consist of scheme/host/port groupings, but can also contain wildcards and special keywords like `'self'` (which expands to the current site's origin) and `'none'` (which ought to be self-explanatory). Let's look at each in turn.

`default-src` specifies a catch-all for unspecified content types. I haven't listed a policy for objects (`object-src`), for example, so any request for video or Flash content would fall back to this default. In this case, the default is `'self'`[^2], so objects can only be loaded from the same origin as the page itself.

[^2]: Note the single-quotes around `'self'` and `'none'`. These are required. Without them, the policy would refer to a server named `self` or `none`, which almost certainly isn't what you mean.

The last policy, for example, allows the site to load font resources from `https://themes.googleusercontent.com/`, which is taken quite literally and exclusively. Fonts can _only_ be loaded from `themes.googleusercontent.com`, and _only_ over HTTPS. Any request for a font from a different host or scheme would throw an error. At the rise of  that policy directives override the value of `default-src` completely: `'self'` isn't acceptable unless it's explicitly listed.

[^1]: Firefox is [confident enough][ff4] in the draft spec to use the canonical header, WebKit (and therefore Chrome) are a little more cautious, and have prefixed the header just in case: the details are the same, however. Both teams are working from the same spec, and both are pretty much feature complete. To follow their progress, CC yourself on either the [Bugzilla #663566][mozbug], or [WebKit #53572][wkbug].

## Source Expressions




##  The trade-off

cross site scripting attacks are effective because script can be injected arbitrarily almost anywhere on a webpage. 2 provide guarantees of protection, content security policy significantly limits the developer's ability to script a page without extra resources. In short in-line script and in-line style our band. This can be a bit inconvenient, but honestly it's good practice. A large part of the web standards discussion has been focused upon separating areas of responsibility. Markup is responsible for semantics, CSS is responsible for style, and JavaScript is responsible for behavior. Each of these can and should exist separate from the other. In-line JavaScript, and especially in-line event handlers, muddy the waters. Content security policy requires that all in-line JavaScript the moved out of line. Ensuring the JavaScript only exists in external resources means that the browser interestingly determine whether resources should be allowed or not. If in-line JavaScript is allowed, they were right back where we started.

## Reports

Even if


[owasp]: https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet
[ff4]: http://blog.mozilla.com/security/2011/03/22/creating-a-safer-web-with-content-security-policy/
[spec]: https://dvcs.w3.org/hg/content-security-policy/raw-file/tip/csp-specification.dev.html
[mkwst]: https://mkw.st/
[mozbug]: https://bugzilla.mozilla.org/show_bug.cgi?id=663566
[wkbug]: https://bugs.webkit.org/show_bug.cgi?id=53572
[utf7]: http://en.wikipedia.org/wiki/UTF-7#security

and the desire for mashed-up and widgetified 

 hello. This is a test to see whether works in I a writer. Dictation. It looks like it does. But it's a bit odd. Stirring should.
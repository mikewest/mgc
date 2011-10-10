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

The web's security model is fundamentally broken, and has been since the beginning. Browsers trust the code they receive from a website completely, so each chunk of JavaScript that executes on a page runs with access to the entire origin's data. Cross-site scripting attacks exploit this trust, injecting malicious code into a site in a wide variety of ways. At best, sites are defaced. At worst, user session data is compromised.

It is, of course, possible to completely eliminate this class of attacks by properly escaping every bit of data that makes it onto the site. A brief glance back at the web's history shows that this defense is unlikely to be effective; given the convoluted set of escaping rules in various HTML contexts, differences in cross-browser implementation, and browser bugs (like [UTF-7 support][utf7]), it's simply a tough problem. Even with our solid, modern understanding of the issue, and a variety of secure frameworks, it remains trivial to accidentally create a hole, and one hole is all it takes.

Content Security Policy is a relatively new addition to the web platform that promises to mitigate the risk of XSS attacks by giving administrators fine-grained control over the data and code that ought to be allowed to run on their site. The feature boils down to a whitelisting mechanism for images, script, style, and a variety of other resource types. A site declares an acceptable list of origins for each data type it cares about via a straightforward HTTP header, and browsers that support [the draft specification][spec] simply refuse to load resources that aren't listed. A quick example should make this clear.

## mkw.st's Policies

On [mkw.st][mkwst], I'm using one stylesheet, hosted on `mkw.st`, one of Google's web fonts, and a few inlined `data:` images. I'd like to ensure that that remains the case, and that I don't accidentally load script from my friends at `evil.com`.

I've configured my server to generate the following headers when loading the site:

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

The interesting bits are `X-Content-Security-Policy` and `X-WebKit-CSP`[^1], both of which contain a simple, semicolon-separated list of policy directives. Each directive consists of a type followed by a set of one or more "source expressions" that define the policy's limitations. These expressions generally consist of scheme/host/port groupings, but can also contain wildcards and special keywords like `'self'` (which expands to the current site's origin) and `'none'` (which ought to be self-explanatory). Let's look at each in turn.

The first directive is of type `default-src`, which specifies a catch-all for content types that aren't explicitly listed. I haven't created a policy for objects (`object-src`), for example, so any request for video or Flash content would use the policy specified here. In this case, I'm specifying a single source: `'self'`[^2]. This means that resources that hit `default-src` can only be loaded from the same origin as the page itself. You may see references to `allow` in older CSP documentation: `default-src` replaces that keyword.

You likely won't be shocked to learn that the next directive,`img-src`, whitelists sources for image resources. Here, images are limited to `data:` URLs, and to `'self'`.

Equally unsurprisingly, the directive of type `font-src` allows the site to load font resources from `https://themes.googleusercontent.com/`, which is taken quite literally and exclusively. Fonts can _only_ be loaded from `themes.googleusercontent.com`, and _only_ over HTTPS. Any request for a font from a different host or scheme would throw an error. It's important to note here that the value of the `font-src` overrides `default-src` completely. They aren't merged: I won't be able to load fonts from `'self'` unless I explicitly add it to `font-src`'s definition.

[^1]: Firefox is [confident enough][ff4] in the draft spec to use the canonical header, WebKit (and therefore Chrome) are a little more cautious, and have prefixed the header just in case: the details are the same. Both teams are working from the same spec, and both are pretty much feature complete. To follow their progress, CC yourself on either [Bugzilla #663566][mozbug], or [WebKit #53572][wkbug].

[^2]: Note the single-quotes around `'self'` and `'none'`. These are required. Without them, the policy would refer to a server with a hostname of `self` or `none`, which almost certainly isn't what you mean.

##  Nothing's free.

In order to function properly, Content Security Policy imposes a [few restrictions][restrictions] on sites that make use of it. Two in particular are worth calling out here.

1. CSP enforces a strict separation of behavior and semantics by refusing to execute inline script, and an equally strict separation of presentation and semantics by refusing to apply inline styles. This follows directly in line with the general recommendation of the web standards community, and allows CSP to clearly identify the source of each piece of data on a page. This identification is essential, as without it the whitelisting mechanism is ineffective. In addition, banning inline script and style substantially reduces the effect of cross-site scripting attacks that rely on JavaScript or CSS [reflection][]: attackers will be forced to compromise a whitelisted resource, which is a much higher bar.

    It's fairly obvious that this restriction would block execution of code contained within `<script>` blocks, but also note that it prevents event handlers from being written inline (`<a … onclick="JAVASCRIPT">` ought to be rewritten to use `el.addEventListener(…)`). Likewise, `javascript:` URLs won't work.

	It's also the case that `data:` URLs are blocked by default, as they can contain arbitrary content that can't be easily verified as being safe, or as really being intentionally written by your server. If you'd like to allow `data:` URLs, you'll have to do so on a type-by-type basis. See above, for example, where I'm explicitly allowing `data:` URLs for image resources, but not for any other resource type.

2. Relatedly, raw strings will not be converted to code. This means that `eval` is right out, as are a variety of other `eval`-like mechanisms (`setTimeout` with a string argument, `new Function(…)`, and so on). Since [`eval` is evil][evil], this isn't a particularly onerous restriction, but it does mean that you'll need to parse JSON content without simply executing it, either with something like [json.js][json] or with a built-in JSON object.

[evil]: http://www.jslint.com/lint.html#evil
[json]: http://www.json.org/js.html

## Further Reading

The list of resource types that Content Security Policy supports is extensive. This example touched on supports images, fonts, and objects, and [a complete list can be found in the specification][list]. 

[list]: https://dvcs.w3.org/hg/content-security-policy/raw-file/tip/csp-specification.dev.html#directives

[owasp]: https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet
[ff4]: http://blog.mozilla.com/security/2011/03/22/creating-a-safer-web-with-content-security-policy/
[spec]: https://dvcs.w3.org/hg/content-security-policy/raw-file/tip/csp-specification.dev.html
[mkwst]: https://mkw.st/
[mozbug]: https://bugzilla.mozilla.org/show_bug.cgi?id=663566
[wkbug]: https://bugs.webkit.org/show_bug.cgi?id=53572
[utf7]: http://en.wikipedia.org/wiki/UTF-7#security
[restrictions]: http://people.mozilla.com/~bsterne/content-security-policy/details.html#restrictions
[reflection]: http://google-gruyere.appspot.com/part2#2__reflected_xss

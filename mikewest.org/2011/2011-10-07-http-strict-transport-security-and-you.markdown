---
layout: post
title: HTTP Strict Transport Security and You
tags:
  - chrome
  - http
  - https
  - encryption
  - security
  - firesheep
  - hsts

Teaser:
  With a simple Wi-Fi packet-sniffer, intercepting login
  cookies over the air is far easier than it ought to be. 
  Happily, clever people have put together solid mitigation 
  techniques, one of which is HTTP Strict Transport Security.
  I've implemented it on a personal site, this article
  describes what it is, why it's important, and how you can use 
  it yourself.
---
With a simple Wi-Fi packet-sniffer, intercepting login cookies over the air is far easier than it ought to be. [Firesheep][] demonstrated this vulnerability definitively, showing the public exactly how trivial it is to hijack unencrypted HTTP sessions. So, we learned an important lesson: running HTTPS on your servers mitigates a large chunk of risk, as encrypting the traffic between your site and its users prevents attackers from grabbing cookies, and thus from hijacking a user's session. Encryption also ensures that your content is delivered without modification, which reduces the ability of man-in-the-middle attackers to intercept your users' traffic when they're using untrustworthy networks. To whatever extent possible, you should use HTTPS, and ensure that you force encryption for important cookies by marking them as `Secure`.

Unfortunately, this isn't a complete solution. Users generally don't type `https://example.com/` into their browser's address bar. They generally either type `example.com` or `http://example.com/`, and you're going to have a hard time reminding them to consistently use `https` when visiting your site. You can redirect users from HTTP to HTTPS, but that leaves a window of opportunity for attackers: your request to the HTTP site is unencrypted, and potentially vulnerable to attack _before_ you can be redirected. It would be significantly safer if you could avoid that HTTP request. This is the problem that [HTTP Strict Transport Security (HSTS)][spec][^1] is meant to address.

Adding a `Strict-Transport-Security` header to your server's HTTPS responses will inform browsers that your website should _only_ be accessed via HTTPS. Normal HTTP connections will be rewritten client-side, _before_ any network traffic is generated. Sending the following header:

    Strict-Transport-Security: max-age=31556926; includeSubDomains

would instruct a browser that supported the draft standard that it shouldn't touch your site (or any of its subdomains) over HTTP for a year. This substantially reduces the surface exposed to attack: as long as the very first HTTP request went through correctly, your users will never use an insecure connection to your website again, regardless of what they type in the address bar.

You will need to ensure that you can actually _serve_ HTTPS responses for every request (on any port) to your host, however, as HTTP simply won't be an option anymore. This is a Good Thing™, even if it might mean a little work for you up front.

None of this is new (just new to me), so browser support is already relatively good: HSTS is supported in [Firefox 4+][ff], and Chrome[^2]. [Opera appears to be waiting][opera] for [issues open against the draft standard][issues] to be resolved, and for the draft to move to RFC status. Looking at the list, I don't see any significant upcoming changes to the header structure: I'd recommend implementing it for your sites now.

## Sound interesting?

As an example, I've just implemented this for [mkw.st][mkwst] (where I'll likely be moving this site at some point in the relatively near future). It took about a half-hour, all told, and most of that was waiting for the certificate to be mailed to me. Here's what I needed to do to set things up:

1. I generated a certificate request on my server, which also involved creating a new private key. Both were trivial, and [RapidSSL's detailed walkthrough][csr] was helpful.

2. Using the newly generated CSR, I purchased a certificate via [CheapSSLs][]. They seem a bit… well… cheap, so I'm not sure I'd recommend them for a high-risk site. For my not particularly valuable site, however, they're brilliant. A 3-year cert ([from RapidSSL][cheaprapid]) was $27 (paid via PayPal), and showed up in my inbox within 20 minutes of purchase.

3. I configured my server to use the certificate. For Nginx, this just meant recompiling the server with SSL support, and adding a new server definition that listened on port 443, and had reference to both the private key and certificate generated above. [Nginx's documentation][nginx] is better than I remembered it being.

For a single-server site like mine, this is a piece of cake, and certainly worth playing around with.

[Firesheep]: http://codebutler.github.com/firesheep/
[spec]: http://tools.ietf.org/html/draft-ietf-websec-strict-transport-sec-02
[preloaded]: http://codesearch.google.com/codesearch#OAMlx_jo-ck/src/net/base/transport_security_state.cc&exact_package=chromium&q=kPreloadedSTS
[add]: http://www.chromium.org/sts
[ff]: http://hacks.mozilla.org/2010/08/firefox-4-http-strict-transport-security-force-https/
[opera]: http://my.opera.com/community/forums/topic.dml?id=838822&t=1317981165&page=1#comment10176262
[issues]: http://trac.tools.ietf.org/wg/websec/trac/report/1?asc=1&sort=ticket
[mkwst]: https://mkw.st/
[CheapSSLs]: http://www.cheapssls.com/
[cheaprapid]: https://www.cheapssls.com/geotrust-ssl-certificates/rapidssl.html
[csr]: https://knowledge.rapidssl.com/support/ssl-certificate-support/index?page=content&id=SO6506
[nginx]: http://wiki.nginx.org/HttpSslModule
[barth]: http://www.schemehostport.com/

[^1]: Adam Barth co-wrote the HSTS spec, and he's coincidentally just started a cleverly titled web security blog that I suspect will be very much worth reading: [Scheme/Host/Port][barth]

[^2]: Chrome actually attempts to avoid even the initial one-time HTTP request for websites that have requested extra protection. Sites like PayPal and Twitter are hard-coded as requesting HSTS (the complete list is [visible in `net/base/transport_security_state.cc`][preloaded]).

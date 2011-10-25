---
layout: post
title: Applying Content Security Policy to Chrome Extensions
tags:
  - CSP
  - contentsecuritypolicy
  - chrome
  - extensions
  - security
  - manifest

Teaser:
    Based on the Content Security Policy primer I wrote last week, you should
    have a good idea of what CSP can offer a website developer. What might not
    be clear is that the policies can extend beyond HTTP, a bit more deeply
    into the browser. Chrome offers Content Security Policy support for
    extensions that substantially reduce the possibility of permission leakage;
    this article describes how it works, and how you can use it in your
    extensions.
---
After reading the [Content Security Policy primer][primer] that I wrote earlier this month, you should have a good idea of the benefits that CSP can offer a website developer. Whitelisting known-good resource origins, refusing to execute potentially dangerous inline JavaScript, and banning the use of `eval` are all effective mechanisms for mitigating cross-site scripting attacks. Implementing and enforcing such policies is simply a good idea.

Recognizing these advantages, Chrome's engineers have extended CSP's reach beyond websites into other areas of the browser where policies can serve as a defense against attacks. Most notably, policies can be applied to [packaged applications][pack] and [Chrome extensions][ext]. Extensions are powerful and modular, giving developers expanded capabilities above and beyond what it makes sense for the web platform to offer. To whatever extent possible, developers need to ensure that those additional capabilities aren't leaked out to the broader web. Content Security Policies mitigate this risk.

[pack]: http://code.google.com/chrome/extensions/apps.html
[ext]: http://code.google.com/chrome/extensions/index.html

## Next Steps

We're working to set a better example by updating the 70 or so sample extensions and applications that Chromium makes available to include the new `content_security_policy` manifest entry. You can follow our progress on that effort at [crbug.com/92644][92644]: star the bug if you're interested in 

[92644]: http://crbug.com/92644

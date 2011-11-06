---
layout: post
title: 'Secure Chrome extensions: Content Security Policy'
tags:
  - CSP
  - contentsecuritypolicy
  - chrome
  - chromium
  - extensions
  - security
  - manifest
  - introduction
  - tutorial
  - header
  - x-content-security-policy
  - x-webkit-csp

suggestions:
  - url: /2011/10/content-security-policy-a-primer
    title: "Content Security Policy: A Primer"

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

Recognizing these advantages, Chrome's engineers have extended CSP's reach beyond websites into other areas of the browser where policies can serve as a defense against attacks. Most notably, policies can be applied to [packaged applications][pack] and [extensions][ext]. Both can make use of Chrome's powerful and modular set of [extension APIs][api], which give developers capabilities above and beyond what it makes sense for the web platform to offer normal websites. To whatever extent possible, therefore, developers need to ensure that those additional capabilities aren't leaked out to the broader web. Content Security Policies mitigate this risk by helping developers ensure that the only code that runs with elevated privileges is their own.

Defining policies for an extension is quite straightforward, and we're working to add them to all the sample extensions in the Chromium project. Walking through one of these samples together should give you a good idea of how it all works.

[primer]: http://mikewest.org/2011/10/content-security-policy-a-primer
[pack]: http://code.google.com/chrome/extensions/apps.html
[ext]: http://code.google.com/chrome/extensions/index.html
[api]: http://code.google.com/chrome/extensions/api_index.html

## Implementation

The [Mappy][] sample extension injects a content script into every page a user visits, searches the page for addresses, and passes them back to the extension so that a map can be displayed in the extension's popup. This is exactly the sort of dangerous scenario in which we need to worry about malicious websites exploiting the extension's permissions, perhaps by cleverly embedding JavaScript into the address which might then be executed if we're not careful when it's passed back to the extension's context. A content security policy is absolutely necessary.

The first step towards securing the extension is to define exactly which resources it needs to load. Mappy's needs are pretty simple: it loads CSS and JavaScript from the local extension package, connects to `https://maps.googleapis.com` to geolocate an address, and finally displays a static map image from `https://maps.google.com`.[^1] A sufficiently paranoid policy would use a `default-src` policy directive to deny access to _everything_ by default, and then specifically whitelist only those resources via `style-src`, `script-src`, `connect-src`, and `img-src` directives. I've annotated Mappy's definition (which does exactly that) below:

    # Block everything, then whitelist from there.
    default-src 'none';

    # Accept CSS from the extension's package.
    style-src 'self';

    # Accept JavaScript from the extension's package.
    script-src 'self';

    # Allow XHR connections over HTTPS to Google Maps APIs.
    connect-src https://maps.googleapis.com; 

    # Allow images from Google Maps to load over HTTPS.
    img-src https://maps.google.com;

For normal websites, content security policies are delivered via an HTTP header. Chrome extensions use the same policy syntax, but define policies in the package's [manifest JSON][manifest] as a simple key-value pair. Simply take the policy you've defined, and add it to `manifest.json`: you can see how Mappy's CSP is defined by visiting [Chromium's source repository][manifestsvn].

With the [manifest changes][manifestdiff] in place, the next step is to take a close look at the extension's code to make sure we comply with the new restrictions we're defining. Generally speaking, this means ensuring that CSS and JavaScript is moved out from the extension's background page and popup into separate files. Most of the time, this is a straight copy/paste job, simply moving code wholesale from an inline `<script>` block into a `background.js` file. For Mappy, the `background.html` change is [captured in this diff][backgrounddiff], and the `popup.html` change is [visible in this diff][popupdiff].

That's it! Once you've defined a policy, and adjusted your extension's code to match it, just test the extension locally, bump the version number, and push the update to your users. They'll be more secure, and the world will be a (slightly) better place.

[manifest]: http://code.google.com/chrome/extensions/manifest.html
[manifestdiff]: http://codereview.chromium.org/8311007/diff/9001/chrome/common/extensions/docs/examples/extensions/mappy/manifest.json
[manifestsvn]: http://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/extensions/docs/examples/extensions/mappy/manifest.json?view=markup
[Mappy]: http://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/extensions/docs/examples/extensions/mappy/
[backgrounddiff]: http://codereview.chromium.org/8311007/diff/9001/chrome/common/extensions/docs/examples/extensions/mappy/background.html
[popupdiff]: http://codereview.chromium.org/8311007/diff/9001/chrome/common/extensions/docs/examples/extensions/mappy/popup.html

## Next Steps

Your task is clear: update the extensions you own! It's very straightforward work, and a real win for security. Content Security Policy support was added to Mappy in [revision 106043][commit]; take a look at [the code review][review] to get some implementation ideas for your own extensions.

At the same time you're working on your extensions, the Chromium team is working to set a better example by updating the 70 or so sample extensions and applications that Chromium makes available to include the new `content_security_policy` manifest entry. It's easy work -- following the steps listed above takes less than half-hour on average -- but 70 is a big number, so we're a bit behind. You can follow our progress on that effort at [crbug.com/92644][92644]: star the bug if you're interested in updates, and pitch in if you're interested! [Patches are welcome][patch]: just send any code reviews my way (`mkwst@chromium.org`).

[^1]: Whenever possible, load resources over HTTPS rather than unencrypted HTTP. This has a number of benefits for privacy and security, most importantly (for our current context) a guarantee that the code you're loading hasn't been modified since it left the server. Active network attackers need to do a _lot_ more work to inject code into a HTTPS stream, wheres it's a trivial task via HTTP.

[commit]: http://crrev.com/106043
[review]: http://codereview.chromium.org/8311007
[92644]: http://crbug.com/92644
[patch]: http://www.chromium.org/developers/contributing-code

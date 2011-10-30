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

Recognizing these advantages, Chrome's engineers have extended CSP's reach beyond websites into other areas of the browser where policies can serve as a defense against attacks. Most notably, policies can be applied to [packaged applications][pack] and [Chrome extensions][ext]. Both can make use of Chrome's powerful and modular set of [extension APIs][api], which give developers capabilities above and beyond what it makes sense for the web platform to offer normal websites. To whatever extent possible, developers need to ensure that those additional capabilities aren't leaked out to the broader web. Content Security Policies mitigate this risk by helping developers ensure that the only code that runs with elevated privileges is their own.

[pack]: http://code.google.com/chrome/extensions/apps.html
[ext]: http://code.google.com/chrome/extensions/index.html
[api]: http://code.google.com/chrome/extensions/api_index.html

## Implementation

Defining policies for an extension is quite straightforward, and we're working to add them to all the sample extensions in the Chromium project. Walking through one together should give you a good idea of how it all works.

The [Mappy][] sample extension injects a content script into every page a user visits, searches for addresses, and passes them back to the extension so that a map can be displayed in the extension's popup. This is exactly the sort of dangerous scenario in which we need to worry about malicious websites exploiting the extension's permissions (perhaps by cleverly embedding JavaScript into the address).

The first step towards securing the extension is to define exactly what resources it needs to load. It loads CSS and JavaScript from the extension package, connects to `https://maps.googleapis.com` to locate an address, and finally displays a static map image loaded from `https://maps.google.com`. A sufficiently paranoid policy would use `default-src 'none'` to deny access to everything, and then specifically whitelist those resources via `script-src`, `style-src`, `connect-src`, and `img-src` policies.

For normal websites, content security policies are delivered via an HTTP header. Chrome extensions use the same policy syntax, but define policies in the package's [manifest][]. Mappy's definition looks like this:

    {
      "name": "Mappy",
      "version": "0.6.1",
      ...
      "content_security_policy": "default-src 'none'; style-src 'self'; script-src 'self'; connect-src https://maps.googleapis.com; img-src https://maps.google.com"
    }

With the manifest changes in place, the next step is to take a close look at the extension's code to make sure we comply with the new restrictions we're defining. Generally speaking, this means ensuring that CSS and JavaScript is moved out from the extension's background page and popup into separate files. Most of the time, this is a straight copy/paste job, simply moving code wholesale from an inline `<script>` block into a `background.js` file.

That's it! Once you've defined a policy, and adjusted your extension's code to match it, just test the extension locally, bump the version number, and push the update to your users. They'll be more secure, and the world will be a (slightly) better place.

[manifest]: http://code.google.com/chrome/extensions/manifest.html
[Mappy]: http://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/extensions/docs/examples/extensions/mappy/
[commit]: http://crrev.com/106043
[review]: http://codereview.chromium.org/8311007

## Next Steps

Your task is clear: update the extensions you own! It's very straightforward work, and a real win for security. Content Security Policy support was added to Mappy in [revision 106043][commit]; take a look at [the code review][review] to get some implementation ideas for your own extensions.

At the same time you're working on your extensions, the Chromium team is working to set a better example by updating the 70 or so sample extensions and applications that Chromium makes available to include the new `content_security_policy` manifest entry. It's easy work -- following the steps listed above takes less than half-hour on average -- but 70 is a big number, so we're a bit behind. You can follow our progress on that effort at [crbug.com/92644][92644]: star the bug if you're interested in updates, and pitch in if you're interested! [Patches are welcome][patch]: just send any code reviews my way (`mkwst@chromium.org`).

[92644]: http://crbug.com/92644
[patch]: http://www.chromium.org/developers/contributing-code

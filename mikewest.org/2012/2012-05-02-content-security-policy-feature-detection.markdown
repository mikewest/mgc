---
layout: post
title: "Content Security Policy: Feature Detection"
tags:
  - contentsecuritypolicy
  - security
  - csp
  - eval
  - angular
  - featuredetection
  - modernizr

Teaser:
  "AngularJS has recently implemented support for Content Security Policy that 
   restricts the use of `eval()`, `new Function()`, and other such text-to-JS
   conduits. This is a huge win, as CSP is one of the best protections modern
   browsers provide against XSS attacks. However, Angular's implementation
   reveals a need for feature detection that the spec currently doesn't address.
   This is my proposal for such an API."
---
[AngularJS][angular]'s [latest release candidate][angularrc7] is the first
framework I've seen that cleanly supports a [content security policy][csp]
that restricts usage of `eval()`, `new Function()`, and the like. I'm thrilled
to see this happening, and it's a testament to the priority that the Angular
developers place on security. CSP is quite simply one the best XSS-protection
mechanisms available to developers these days in modern browsers. The more
frameworks that hop on board, the faster sites can start adopting CSP, and
the safer we'll all be on the net.

All that said, the implementation isn't as complete as it could be. Angular
requires that the developer manually opt into CSP-friendly mode via the
[`ng-csp`][ngcsp] directive. This is error-prone at best, and introduces
complexity that would be better hidden away inside the framework. The Angular
developers recognize this shortfall, and are [explicitly requesting][igor]
some sort of feature detection API that would allow frameworks to query the
currently active policy to determine its boundaries, and fork their
implementation accordingly.

This does seem like a great addition to the spec; I'd suggest the following
implementation:

Add `document.[prefix]contentSecurityPolicy` as an object that exists in
browsers that support CSP. This would enable trivial feature detection of CSP
as a whole, which would enable frameworks to make intelligent decisions about
how to proceed through the following use cases:

1.  Is a policy enabled? If not, perhaps I’d like to set one via `meta`
    injection.

    `document.contentSecurityPolicy.active` is a boolean property: `true` if
    a policy is set, `false` otherwise.

2.  Can I execute `eval()` or use `new Function()`?
 
    `document.contentSecurityPolicy.isWhitelisted('script-src', 'unsafe-eval')`
    returns `true` if `unsafe-eval` has been defined for the `script-src`
    directive.
  
3.  Can I embed a `data:` image or frame?

    `document.contentSecurityPolicy.isWhitelisted('image-src', 'data:')` and
    `document.contentSecurityPolicy.isWhitelisted('frame-src', 'data:')`

4.  Can I include Google Analytics?

    `document.contentSecurityPolicy.isWhitelisted('script-src', 'https://ssl.google-analytics.com')`
    (Note that `isWhitelisted` should do the hard work of dealing with
    wildcards. This example should return `true` if `*.google-analytics.com`
    is whitelisted.)

5.  Are reports being sent? If so, where are they going?

    The `document.contentSecurityPolicy.reportUri` property is either
    `undefined` if no `report-uri` directive is set, and a URI if the
    directive is set.

This seems like a reasonable first pass at a strawman for discussion. Thanks to
[Paul Irish][irish], [Eric Bidelman][bidelman], and [Pete LePage][lepage] for
walking through this with me.

What do you think?

[angular]: http://angularjs.org/
[angularrc7]: https://groups.google.com/forum/?fromgroups#!topic/angular/NUT9q_fjMJQ
[csp]: https://mikewest.org/2011/10/content-security-policy-a-primer
[ngcsp]: http://docs.angularjs.org/api/angular.module.ng.$compileProvider.directive.ngCsp
[igor]: https://twitter.com/#!/IgorMinar/status/197329318249111552
[irish]: http://paulirish.com/
[bidelman]: http://ericbidelman.com/
[lepage]: http://petelepage.com/

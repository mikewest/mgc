---
layout: post
title:  "Continuous Integration with Hudson and JSLint"
Teaser: "Running tests automatically is the best way to ensure that they're run at all; this is just as true for static code analysis tools like JSLint as it is for your own unit tests.  Integrating JSLint tests for JavaScript and CSS into a CI server like Hudson is hugely beneficial, I'll show you how in this article."
tags:
    -   hudson
    -   testing
    -   development
    -   continuousintegration
    -   integration
    -   staticanalysis
    -   jslint
    -   javascript
    -   css
    -   workflow

---

The first step is to get JSLint running locally on the command line.  The easiest way to make that happen is to use Mozilla's [Rhino][], an implementation of JavaScript written in Java.  [Download the most recent version of Rhino][dlrhino] from the project site, unzip the archive, and move the `js.jar` file you'll find inside somewhere safe.  We'll need it later on.

After a bit of trial and error on a project at work, I've gotten [JSLint][] running 

Running tests automatically is the best way to ensure that they're run at all; this is just as true for static code analysis tools like [JSLint][] as it is for your own unit tests.  After a bit of trial and error on a project at work, I've gotten JSLint running against a large set of JavaScript and CSS files every time I commit changes.  This makes it more possible to find bugs early in the process of development, and to enforce some basic coding standards 

In this article, I'll walk through setting up JSLint so that 


[JSLint]:   http://jslint.com/
[Rhino]:    http://www.mozilla.org/rhino/
[dlrhino]:  http://www.mozilla.org/rhino/download.html

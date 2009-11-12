---
title:  "My Jekyll Fork"
layout: post
Teaser: "Jekyll is a well-architected throwback to a time before Wordpress, when men were men, and HTML was static.  I like the ideas it espouses, and have made a few improvements to it's core.  Here, I'll point out some highlights of my fork in the hopes that they see usage beyond this site."
tags:
    -   mikewest.org
    -   jekyll
    -   git
    -   github
    -   fork
    -   webdev
    -   blog
    -   architecture
    -   design
    -   tags
    -   archive
    -   programming
    -   ruby
---
[Jekyll](http://jekyllrb.com/) is an interesting project, a well-architected throwback to a time before unnecessary dynamism reigned supreme.  In contrast to blog engines like Wordpress or Textile, Jekyll doesn't attempt to do anything other than push raw content through a few simple filters out into the world in the form of static HTML files.  Jekyll's [publication philosophy][blh] is very much in line with my own, and I appreciate the work that's gone into it.  It's relatively widely used, and therefore much more stable and well-tested than anything I'd write on my own.  Given my [recent experience][yesterday], I want something that will Just Work™, and this looks like it.  I finished moving this site to Jekyll yesterday, and I'm quite happy with how it's working...

It doesn't fit me perfectly, though.  Here, I'll point to a few features that I think are missing, and a few design decisions that I think are worth reconsideration.  Happily, it's an open source project, so I'll also be able to point to my fork of the project where I'm busy addressing these shortcomings.

"Generated" Pages: Tags and Archives
------------------------------------

The biggest gap I see in Jekyll's feature set is support for "generated" pages (covered in [Issue #16][i16]).  HTML that Jekyll produces is tied one-to-one with files you create on the filesystem.  This has the appeal of simplicity, fails in a number of ways to support two quasi-dynamic things that I consider essential to the kind of sites Jekyll aims to produce: tags, and archives.

[i16]: http://github.com/mojombo/jekyll/issues#issue/16

**Tags** are a nice way of grouping content on a site, and surfacing that content to readers in an unobtrusive way.  Jekyll, out of the box, does a miserable job of making them available in templates.  `site.tags` gives you a list of _all_ the site's tags, `page.tags` gives you the tags for the current page, and that's it.  That's simply not enough structured data to do anything useful with; I want more.  "More", in my case, meaning two things: a separate page for each tag at `/tags/[TAG]`, listing each article that fits; and a page listing out all the tags on the site (in cloud form, if only because I'm _so_ Web 2.0).  The latter is (painfully) possible out of the box, the former is not.

My solution (based heavily on [Matt Flores][]' [fork][mffork]) is available in the [tag_index branch][tagindex] of my Jekyll fork.  The implementation is very low-impact: simply add a `tag_detail.html` layout to your site's `_layouts` directory.  Jekyll will auto-generate pages using that layout for each tag on your site, providing `page.tag` as a variable inside each as they're rendered.  This allows you to dive into `site.tags` to pull out lists of articles in a very straightforward way.  Once rendered into HTML, the result is placed into a directory you specify via a configuration variable (`tag_root`).  This has worked brilliantly for me here on this site.

[Matt Flores]:  http://matflores.com/
[mffork]:       http://github.com/matflores/jekyll/commit/abd0491c451b77bd119a0071457a362c35e6c2f6
[tagindex]:     http://github.com/mikewest/jekyll/tree/tag_index

**Archive pages** listing out content written during a certain period are another nice way of dividing up posts on a site.  Especially useful for sites with more than a few posts, it's a mechanism for showing users posts that fit together temporally.  It's nice to be able to see [all of 2007's posts][a2007], for instance.  Or [all posts from November of 2008][a200811].  

Again, I borrowed a bit of code from Matt Flores, brought it up to date with the latest Jekyll tag (0.5.4 at the time I'm writing this), and check it into the [archive branch][archive] of my fork.  Similarly to the tagging system above, archives depend on adding a few extra layouts.  `archive_yearly.html`, `archive_monthly.html`, and `archive_daily.html` are supported, and offer `page.year`, `page.month`, and `page.day`, which can be used to reference posts in `site.collated_posts`.  My [`archive_monthly.html`][am] is indicative of how this can work.

Generated pages are written to `/[YEAR]/index.html`, `/[YEAR]/[MONTH]/index.html`, and `/[YEAR]/[MONTH]/[DAY]/index.html` if posts exist over the specified time period.

[a2007]:    /2007
[a200811]:  /2008/11
[archive]:  http://github.com/mikewest/jekyll/tree/archive
[am]:       http://github.com/mikewest/mikewest.org/blob/master/_layouts/archive_monthly.html

Filters
-------

Jekyll uses the [Liquid][] templating engine, which isn't exactly my first choice.  It's a solid engine, as far as it goes, but it's no [Jinja2][].  Regardless, Jekyll has built in a number of useful filters that can be used to perform operations on text before it's rendered.  `textilize()` is a good example of this, running text through a Textile parser, then writing the output instead of the original text.  It's great!

Except, of course, for the fact that Textile is hideous.  :)  I much prefer to write Markdown formatted text (it's just easier for me to read, really), so I was a bit miffed when I discovered that a Markdown counterpart to `textilize()` was simply missing.

A more robust system is being discussed (slowly) in [Issue #19][i19].  I decided not to wait for a perfect solution, and simply added `markdownize()` in the [filters branch][filters] of my fork.  A trivial, but _very_ necessary change. 

[filters]:  http://github.com/mikewest/jekyll/tree/filters
[Jinja2]:   http://jinja.pocoo.org/2/
[i19]:      http://github.com/mojombo/jekyll/issues#issue/19

Default Configuration Values
----------------------------

I really like the way that Jekyll expects posts to be formatted.  Each post lives in it's own file, and each file begins with a YAML block specifying metadata such as titles, teasers, and layout style.  This allows you to configure each post separately, and lends quite a bit of flexibility to the end product.

As [Issue #25][i25] points out, it'd be nice if layout in particular could be specified at the site level as a default value.  Posts that need different layouts are (generally) few and far between, and a global configuration would make the most common case a bit simpler.

Henrik [took a stab at a solution][hcommit] to the problem, which I ran off with and improved upon in the [post_defaults branch][postdefaults] of my fork.  I'm waiting on someone to take a look at this work now, but I'm not holding my breath for it to be merged into the official release.

[hcommit]:      http://github.com/henrik/jekyll/commit/77bf31c42c25c2f87c215348a816b730104fe820
[postdefaults]: http://github.com/mikewest/jekyll/tree/post_defaults
[i25]:          http://github.com/mojombo/jekyll/issues#issue/19

Problematic Design
------------------

Beyond gaps in the feature set, Jekyll does one or two things that I simply disagree with.

Jekyll tightly couples content and layout by assuming that both will exist together in a defined directory structure.  Leaving a bit of complexity to the side, a typical Jekyll site contains a `_posts` subdirectory filled to the brim with lovely raw content, and a `_layouts` directory filled with [Liquid][]-based HTML templates.  The former is exclusively concerned with content, the latter exclusively with layout.

For the same reasons that we eventually started building websites without inline style information, separating the concerns of the site's semantics from it's layout and behavior, I don't believe that these bits belong in the same repository.  At a minimum, I'd like to be able to deploy a version of my website's look and feel without worrying about whether or not I tagged the release before or after adding a post.  The one activity has nothing to do with the other, and both ought be able to proceed in parallel.  Jekyll's current implementation encourages mixing the two, which I don't appreciate.  Instead, I prefer to run two distinct repositories: one containing [pure content][mgc], the other containing [site-specific layout and configuration][org].  This feels cleaner to me.

The solution I've hacked together is available in the [contentpath branch][contentpath] of my Jekyll fork.  I've added a single configuration variable (`content_root`) that contains an absolute path to the directory containing the site's content.  That directory will be parsed in it's entirety (e.g. no `_posts` subdirectory is required).  If a `_posts` directory exists in the usual location (`[SITE_ROOT]/_posts/`) it will be parsed as well to ensure backwards compatibility.  

I don't expect this change to make it into the main tree, as it's probably not interesting for Jekyll's main audience of GitHub Pages users who _do_ in fact very much want to deal with a single repository.  Moreover, when dealing with potentially malicious users, it's not a brilliant idea to give them the ability to generate publicly accessible pages from _any_ readable directory on a system.  For my use, however, it's more or less perfect, and I'll do my best to keep it rebased on top of the latest Jekyll tags for anyone else who's of the same mind.

[contentpath]: http://github.com/mikewest/jekyll/tree/contentpath

[blh]: http://tom.preston-werner.com/2008/11/17/blogging-like-a-hacker.html
[yesterday]: http://twitter.com/mikewest/status/4605321990
[Liquid]: http://www.liquidmarkup.org/
[mgc]: http://github.com/mikewest/mgc/
[org]: http://github.com/mikewest/mikewest.org/

[Jekyll][] is an interesting project, a well-architected throwback to a time before unnecessary dynamism reigned supreme.  In contrast to blog engines like Wordpress or Textile, Jekyll doesn't attempt to do anything other than push raw content through a few simple filters out into the world in the form of static HTML files.  Jekyll's [publication philosophy][blh] is very much in line with my own, and I appreciate the work that's gone into it.  It's relatively widely used, and therefore much more stable and well-tested than anything I'd write on my own.  Given my [recent experience][yesterday], I want something that will Just Work™, and this looks like it.

It doesn't fit me perfectly, though.  Here, I'll point to a few features that I think are missing, and a few design decisions that I think are worth reconsideration.  Happily, it's an open source project, so I'll also be able to point to my fork of the project where I'm busy addressing these shortcomings.

Missing Features
----------------

Problematic Design
------------------

Jekyll tightly couples content and layout by assuming that both will exist together in a defined directory structure.  Leaving a bit of complexity to the side, a typical Jekyll site contains a `_posts` subdirectory filled to the brim with lovely raw content, and a `_layouts` directory filled with [Liquid][]-based HTML templates.  The former is exclusively concerned with content, the latter exclusively with layout.

For the same reasons that we eventually started building websites without inline style information, separating the concerns of the site's semantics from it's layout and behavior, I don't believe that these bits belong in the same repository.  At a minimum, I'd like to be able to deploy a version of my website's look and feel without worrying about whether or not I tagged the release before or after adding a post.  The one activity has nothing to do with the other, and both ought be able to proceed in parallel.  Jekyll's current implementation encourages mixing the two, which I don't appreciate.  Instead, I prefer to run two distinct repositories: one containing [pure content][mgc], the other containing [site-specific layout and configuration][org].  This feels cleaner to me.

Here's my stab at a solution: [contentpath][].

[contentpath]: http://github.com/mikewest/jekyll/tree/contentpath





It doesn't require a database, it doesn't require server configuration, it doesn't require much of anything at all, really.  It's a simple system designed for one thing only, which I can appreciate.  

I've more or less settled upon [Jekyll][] as the base publishing system for this website. 


It's reason for being is outlined clearly in [Blogging Like a Hacker][blh], and after sifting through the code, I'm pretty happy with how it meets the goals it has set.  It's missing a few things that I think are important, however.

[blh]: http://tom.preston-werner.com/2008/11/17/blogging-like-a-hacker.html
[yesterday]: http://twitter.com/mikewest/status/4605321990
[Liquid]: http://www.liquidmarkup.org/
[mgc]: http://github.com/mikewest/mgc/
[org]: http://github.com/mikewest/mikewest.org/

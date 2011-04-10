---
layout: post
title:  A Quick git/vim Workflow Tip
tags:
    - git
    - vim
    - editor
    - development

Teaser:
    Git makes it incredibly easy to work on a lot of a project's features at
    once, hopping quickly back and forth between branches. I love this
    ability, but I hate remembering what exactly it was that I was working on
    in a particular branch. I know it had something to do with a particular
    bug, but I've no idea anymore which files I was fiddling around with to
    fix it. Here's my solution to that problem.
---
Git makes it incredibly easy to work on a lot of a project's features at once,
hopping quickly back and forth between branches. I love this ability, but I
hate remembering what exactly it was that I was working on in a particular
branch. I know it had something to do with a particular bug, but I've no idea
anymore which files I was fiddling around with to fix it.

Enter `git vim`. I've set up two trivial alias in my `~/.gitconfig` file to
either show me a list of files effected by a particular revision or range, and
to directly open them in my editor of choice so that I'm back to work as
quickly as possible.

    [alias]
      ...
      fshow = ! sh -c 'git show --pretty="format:" --name-only $1 | grep -v "^$" | uniq | sed -e "s#^#`git rev-parse --show-toplevel`/#"' -
      vim   = ! sh -c 'vim `git fshow $1`' -
      mate  = ! sh -c 'mate `git fshow $1`' -
      edit  = ! sh -c '$EDITOR `git fshow $1`' -

The first alias calls `git show` to get a list of all the files touched by a
revision or range, filters out empty lines, and ensures that the paths are
absolute after deduplicating the list of files. Any
[valid revision or range][1] will work: `HEAD`, `37ad159`, `master..`, etc.

To see a list of files changed over the last four revisions, I could type:

    $ git fshow HEAD~5..
    lib/rocco/layout.rb
    lib/rocco/layout.mustache
    lib/rocco.rb
    rocco.gemspec
    test/helper.rb
    test/test_reported_issues.rb

To open those files for editing, I'd use the second alias:

    $ git vim HEAD~5..

If I wanted to open the files in TextMate instead, I'd use the third:

    $ git mate HEAD~5..

Or, if I was clever enough to set up an `$EDITOR` environment variable (which
I should do, given that it's used all over the place on the shell), I could
use the last alias to open the files in whatever program that was set to:

    $ git edit HEAD~5..

I can hop from branch to branch, and open all the relevant files quickly and
easily. It's a small thing, but it's made a big difference in my workflow
over the last week or three. 

[1]: http://www.kernel.org/pub/software/scm/git/docs/gitrevisions.html

---
Alias:
- http://mikewest.org/blog/id/88
Modified: '2008-01-20T20:47:35Z'
Teaser: After a brief mishap with a hard drive, I've gone backup-crazy.  This article
    looks how I'm using Parchive to give myself an extra bit of confidence in my backups.
layout: post
tags:
- Personal
title: Safegarding your data with Parchive
---
So, the disk on which I keep the main copy of my Aperture library started
making strange clicking noises when plugged into my powerbook.  It makes these
noises _instead of_ the expected whirring and humming and actual _reading of
data_.  This, as you may suspect, is a Bad Thing.

Thankfully, it works perfectly when plugged into my work laptop, so I've spent
the majority of the day descending into full-blown backup paranoia.  I've
consolidated all my important and cloned them onto three separate hard drives.
Now I'm beginning the process of burning a million DVDs.  Of course, the
aforementioned paranoia forces me to recognize that DVDs degrade; I can't
_trust_ them, you see.  What to do?

This is thankfully a solved problem.

Usenet posters have used something called [Parchive][] for years now to post
binary files with some guarantee of completeness in the intrinsically lossy
world of globally mirrored newsgroups.  Along with the actual data that's
written to a newsgroup, the poster will upload a number of `PAR` files
containing _parity information_ that allows you to _regenerate_ any lost data.
Without going into the details of [Reed-Solomon error correction][error], this
means that if a few pieces of the data you're downloading are missing, you can
generate them yourself, ensuring that the original signal gets through.

[Parchive]: http://parchive.sourceforge.net/
[error]: http://en.wikipedia.org/wiki/Reed-Solomon_error_correction "Wikipedia: 'Reed-Solomon error correction'"

The same theory applies to DVDs.  I don't particularly trust the medium to
_guarantee_ successful backups over time, but I _do_ trust that they'll
probably retain 99% of the bits I care about.  Parchive, therefore, looks like
a great solution.

Installing `parchive`
---------------------

Installing Parchive is trivial.  You can grab binaries off sourceforge, or
check out the CVS tree and compile it yourself, like so:

    cvs -d:pserver:anonymous@parchive.cvs.sourceforge.net:/cvsroot/parchive login
    cvs -z3 -d:pserver:anonymous@parchive.cvs.sourceforge.net:/cvsroot/parchive co -P par2cmdline
    cd par2-cmdline/
    ./configure --prefix=/usr/local
    make
    sudo make install

Using `parchive`
----------------

The main thing I want to do with Parchive is create `PAR` files that contain
vital parity information about my data.  when doing so, there are two options
that are important to consider:  **% redundancy**, and **block size**.

The former option controls how much parity information is generated, that is,
how much data you can _lose_ while still being able to regenerate the whole.
I've settled on **10%** as being stupendously beyond the amount of bad sectors
I'd expect to see on a DVD within a reasonable amount of time, and therefore
"safe".

The latter option only makes sense if you know a little about how parchive
works: in a nutshell, it breaks your files up into smaller pieces, and
generates parity information for each block separately.  If you lose _one bit_
of a block, the whole thing is invalid, and has to be regenerated.  In an
ideal world, then, you'd set the block size equal to the sector size of
whatever medium you're using for backup.  In that case, you've got the best
protection against a single sector dying; you don't waste any space.  This
efficiency, however, is impractical for two reasons: first, the smaller the
block size, the longer it takes to process the data, and second, parchive's
algorithm is limited to a maximum of 32,768 (coincidentally, that's
2<sup>15</sup>) blocks.  If you set a 2k block size to _maximize_ efficiency,
you'd only be able to process ~65M before parchive fell over and died.  I need
to write parity information for up to a whole DVD's worth of data, ~4Gb
(~4.7Gb total capacity - 10% redundancy).  4 millionish kilobytes / 32768
blocks = about 123kb per block.  I'll double that (and round to the nearest
power of two, because I suspect that makes things easier internally), and
end up with a block size of 262,144 bytes.

So, creating `PAR` files for a directory is just a matter of plugging these
values into the `par2create` command:

    par2create -s262144 -r10 [NameOfParFile.par2] [FilesToRead]

Easy, eh?

Verifying the files in a directory is equally trivial, using `par2verify`:

    par2verify [NameOfParFile.par2]

If `par2verify` tells you that you've got corruption in your data, you can
repair it with `par2repair`:

    par2repair [NameOfParFile.par2]

When that's finished, parchive will have magically regenerated your data from
the parity files you have at hand.  Brilliant.
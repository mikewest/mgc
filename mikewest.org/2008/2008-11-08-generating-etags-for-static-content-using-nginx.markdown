---
Alias:
- http://mikewest.org/blog/id/94
Modified: '2008-11-08T20:34:44Z'
Teaser: 'Nginx is a brilliant little HTTP server that I''m using on this website to
    quickly serve static content.  It bothers me a (very) little that it doesn''t
    correctly generate Etag headers for static content, however.  I''m attempting
    to remedy that oversight by releasing an Nginx module: `nginx-static-etags`.'
layout: post
tags:
- mikewest.org
- nginx
- etag
- caching
- http
- headers
- performance
- exceptionalperformance
- y!
- yahoo
- static
- webdev
- development
- fallow
- server
- module
- nginx-static-etags
title: Generating Etags for static content using Nginx
---
[Nginx][] is a brilliant little HTTP server that I'm using on this website to quickly serve static content, and quickly proxy traffic through to the [ruby backend][fallow] when static content just won't do.  It's been a breeze to set up, and quite stable in my (limited) experience.  There's just one thing bothering me about it at the moment: it doesn't completely support the content-based cache headers I'd like to see.  Specifically, it doesn't do `Etag`s for content it serves, and it [doesn't look like Igor's going to implement it][igor].

I see the complete lack of `Etag` support as an oversight.  It's more granular than `Last-Modified`, which is only accurate to the second, and only measures change along the axis of _time_; `touch`ing a file doesn't change it's content, but would force a cache miss when the cache is based on nothing but timestamp.  `Etag`s, on the other hand, are _content_-based identifiers that provide a mechanism for confirmation that the content of the file you're reading is accurate, regardless of inconsequential fiddling or deployment on the server.

That said, it isn't catastrophic to rely entirely on `Last-Modified` when serving truly static content.  If you set `Cache-Control` and `Expires` headers correctly, your users' browsers and upstream proxies should cache the static content correctly.  You'll all be seeing the right thing at more or less the right time.  It's not optimal, however, and I'm using that as an excuse to play around with C again.

## Introducing `nginx-static-etags`

It appears that the only way to add the functionality I'd like to see is to write an Nginx module (in C) and compile it into the server.  I'm in the process of doing that now, and I'm making relatively good progress on [`nginx-static-etags`][module] over on GitHub.  It's been much harder than I expected, actually.  [Evan Miller][evan] has put together an [epic Nginx module-building tutorial][module] that I've had up constantly all week, but it turns out that I remember less C than I thought I did (and that the "C" that I remember is generally C++, which isn't quite the same).

I certainly wouldn't recommend that anyone run this in production yet, as, let's be honest, the code's likely a joke.  But after a week of tinkering and banging my head against GCC, it's finally actually doing what it promises: generating valid `Etag` headers for static content.  There's very little configuration available right now, but the goal is to get it up to feature parity with the [equivalent Apache configuration option][apache].

It's been a good learning experience for me, and it's [keeping me sane][sanity] (as side projects are wont to do).  [Follow along on GitHub][github] if you're interested.

## Installation

Download the module however you like.  I'd recommend pulling it down with Git by simply cloning this repository:

    mkdir ~/src
    cd    ~/src
    git clone git://github.com/mikewest/nginx-static-etags.git ./nginx-static-etags

To use the module, you'll have to compile it into Nginx.  So, download the Nginx source, configure it with the module path, and compile:

    mkdir ~/src
    cd ~/src
    curl -O http://sysoev.ru/nginx/nginx-0.6.32.tar.gz
    tar -zxvf ./nginx-0.6.32.tar.gz
    cd ./nginx-0.6.32
    ./configure --add-module=/Users/mikewest/Repositories/nginx-static-etags
    make
    sudo make install
    
And you're done!

## Configuration

Add `FileEtag` to the relevant `location` blocks in your `nginx.conf` file:

    location / {
        ...
        FileETag on;
        ...
    }

## Caveat

[Brad's][intranation] kinda right to [question the value][comment] of implementing `Etag`s at all: if you don't generate them correctly you'll do more harm than good.  Yahoo!'s Exceptional Performance team [explicitly recommends against using the `Etag` header][yahoo] unless you know what you're doing (which really boils down to ensuring that Apache doesn't use the file's `inode` to generate the key).  I think they've painted with a _really_ broad brush, though, as YSlow's admonitions against `Etag`s really only apply to the default configurations of Apache and IIS.  `Etag` can be a very valuable addition to the caching arsenal if you think about them; Yahoo!'s throwing the baby out with the bathwater. 

[nginx]:    http://nginx.net/
[fallow]:   http://github.com/mikewest/fallow/tree
[igor]:     http://markmail.org/message/xiungpgciwvocl4w
[yahoo]:    http://developer.yahoo.com/performance/rules.html#etags
[github]:   http://github.com/mikewest/nginx-static-etags/tree
[evan]:     http://emiller.info/
[module]:   http://emiller.info/nginx-modules-guide.html
[apache]:   http://httpd.apache.org/docs/1.3/mod/core.html#fileetag
[sanity]:   /2008/10/fallow-fields-and-new-beginnings
[comment]:  http://github.com/mikewest/nginx-static-etags/commit/7dc32e124a8ba70d7bab733d68a8ef75f1b7d3b8#comments
[intranation]: http://intranation.com/
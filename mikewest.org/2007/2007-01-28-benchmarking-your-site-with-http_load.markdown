---
Alias:
- http://mikewest.org/blog/id/53
Modified: '2008-04-07T16:48:44Z'
Teaser: http_load is a great benchmarking utility that gives you a quick overview
    of your web server's performance.  This article describes how to install and use
    it.
layout: post
tags:
- HOWTO
title: Benchmarking Your Site with `http_load`
---
[`http_load`][http_load] is a stunningly useful HTTP benchmarking utility that gives you a rough idea of how many hits per second a server is capable of serving.  You simply tell it what pages to grab, and how many "clients" it should run in parallel; it gives you back useful information about the average fetches per second and the average, minimum, and maximum response times.  It's no substitute for a solid profiler to dig into the hows and whys of your application's performance, but it's great at telling you when you're "good enough" to launch.

## Installing `http_load` on OS X ##

Installation is not tough, it's the typical `make`, then `make install` process that you'll use just about any time you install a *nix application from source.  It even defaults to `/usr/local/bin`, perfect.

So, here we go:

    mkdir ~/http_load_src
    cd ~/http_load_src
    curl -O http://www.acme.com/software/http_load/http_load-12mar2006.tar.gz
    tar -xzvf ./http_load-12mar2006.tar.gz
    cd http_load-12mar2006
    make
    sudo make install
    cd ~
    rm -rf ~/http_load_src
    
You'll end up with the application installed at `/usr/local/bin/http_load`, and if you've [set your `PATH` to include `/usr/local`][path], then you're good to go.

    
[http_load]: http://www.acme.com/software/http_load/
[path]: http://hivelogic.com/narrative/articles/using_usr_local "Using /usr/local"

## Using `http_load` to Benchmark Your Site ##

Once installed, using `http_load` for quick benchmarking is really quite straightforward.  You call the program, tell it how many requests to make concurrently, and how long to run (either in number of seconds, or total fetches), and finally pass in a file full of URLs to request.

To see how many requests your server can take care of over a 5 second period, run:
    
    http_load -parallel 10 -seconds 5 ./omg_its_full_of_urls.txt
    
You'll get back a response that looks something like:

    3587 fetches, 10 max parallel, 6.97698e+06 bytes, in 5.00052 seconds
    1945.07 mean bytes/connection
    717.325 fetches/sec, 1.39525e+06 bytes/sec
    msecs/connect: 0.674328 mean, 20.771 max, 0.045 min
    msecs/first-response: 12.4517 mean, 389.405 max, 1.978 min
    HTTP response codes:
      code 200 -- 3587

The numbers you'll want to look at in more detail are "fetches/sec" and "msecs/first-response".  These are critical in terms of really understanding what your site is doing.

It's important to note the difference between "benchmarking" and "profiling".  What we're doing here with `http_load` is the former: we're getting a feel for a specific page's overall performance.  We know that it serves X pages per second, and generally takes about Y milliseconds to response.  What we don't know yet is __why__ either of these is the case.  You'll have to dig in more detail into your PHP code and server configuration to determine _what to tweak_ to bring up your site's performance to an acceptable level.  `http_load` doesn't, and can't, do that for you.  

## A Tip for Shell Scripters ##

Generally speaking, I'm only testing one URL at a time to determine the performance of a specific script on a site.  For this case, creating a file with a single URL inside is a little annoying, so I whipped up a quick bash script to make it happen for me.  Add the following function to your `.bash_profile`, and you can simply type "httpload [url] [clients] [seconds]" to run a quick benchmark.

    httpload() {
        STAMP=`date +"%s"`;
        echo "http://$1" > /var/tmp/$STAMP.http_load_temp_file
        http_load -parallel $2 -seconds $3 /var/tmp/$STAMP.http_load_temp_file
        rm -f /var/tmp/$STAMP.http_load_temp_file
    }
    
Hooray for bash scripting!

## Troubleshooting ##

It looks like Leopard introduces some quirks to the process.  If you're getting an error like:

    rm -f /usr/local/bin/http_load
    cp http_load /usr/local/bin
    rm -f /usr/local/man/man1/http_load.1
    cp http_load.1 /usr/local/man/man1
    cp: /usr/local/man/man1: No such file or directory
    make: *** [install] Error 1
    
Then do the following to fix up the problem:

    sudo rm /usr/local/bin
    sudo mkdir -p /usr/local/bin/
    sudo mkdir -p /usr/local/share/man/man1/
    sudo ln -s /usr/local/share/man/ /usr/local/man
    make clean
    make
    sudo make install
    
In a nutshell, Leopard doesn't come with a `/usr/local/bin` directory, and seems to have moved the location of local manual pages from `/usr/local/man/` to /usr/local/share/man/`.  The commands above will create the binary and manual page directories you'll need, and sets up a [symlink][symlink] mapping the old directory structure to the new one.

Magic!

[symlink]: http://arstechnica.com/reviews/os/mac-os-x-10-5.ars/14#symlinks-and-hard-links
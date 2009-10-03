---
Alias:
- http://mikewest.org/blog/id/57
Modified: '2007-04-16T12:18:31Z'
Teaser: '`libgd` is a pain in the ass to install from source.  Here''s a step by step
    guide in case I ever have to do it again.'
layout: post
tags:
- HOWTO
title: Installing `libgd` from source on OS X
---
Using Matías Giovannini's [great instructions][instructions], I was (finally)
able to get the GD library installed on OS X so I can build some charts in
Perl.  I've condensed his instructions into the shell commands that I actually
needed to get everything installed, and record them here just in case I ever
have to do it again.  :)

[instructions]: http://www.paginar.net/matias/articles/gd_x_howto.html "Compiling GD on Mac OS X HOWTO"

## 1. Install `zlib` ##

    curl -O http://www.zlib.net/zlib-1.2.3.tar.gz
    tar -xzvf ./zlib-1.2.3.tar.gz
    cd zlib-1.2.3
    ./configure --shared && make && sudo make install

## 2. Install `libjpeg` ##

    curl -O ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v6b.tar.gz
    tar -xzvf ./
    cd jpeg-6b
    ln -s `which glibtool` ./libtool
    export MACOSX_DEPLOYMENT_TARGET=10.4
    ./configure --enable-shared && make && sudo make install

## 3. Install `libpng` ##

    curl -O ftp://ftp.simplesystems.org/pub/libpng/png/src/libpng-1.2.16.tar.gz
    tar -xzvf ./libpng-1.2.16.tar.gz
    cd libpng-1.2.16
    ./configure && make && sudo make install

## 4. Install `freetype2` ##
    
    curl -O http://download.savannah.gnu.org/releases/freetype/freetype-2.3.4.tar.gz
    tar -xzvf freetype-2.3.4.tar.gz
    cd freetype-2.3.4
    ./configure && make && sudo make install
    
## 5. Install `libgd` ##

    curl -O http://libgd.org/releases/gd-2.0.34.tar.gz
    tar -xvzf ./gd-2.0.34.tar.gz
    cd gd-2.0.34
    sudo ln -s /usr/X11R6/include/fontconfig /usr/local/include
    ./configure && make && sudo make install
    
## 6. Celebrate! ##

I celebrated by installing `GD::Graph` via CPAN, you might prefer something
more suitably exciting.  :)
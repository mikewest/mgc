---
Alias:
- http://mikewest.org/blog/id/20
Modified: '2006-06-18T10:27:57Z'
Teaser: SQLite is a nice little database engine that can be incredibly fast as a website
    backend.  Installing it on OS X is equally quick.
layout: post
tags:
- HOWTO
title: Install SQLite Locally on OS X
---
SQLite is a self-contained, embeddable, zero-configuration SQL database engine that performs admirably in a variety of applications. 

Of course, there's a [nice binary distribution][binary] that you can install, but it's trivial to compile yourself from source and install into `/usr/local`.  Simply drop into Terminal, and type the following:

        curl -O http://www.sqlite.org/sqlite-3.3.6.tar.gz
        tar xzvf ./sqlite-3.3.6.tar.gz
        cd sqlite-3.3.6
        ./configure --prefix=/usr/local
        make
        sudo make install

Other configuration options are spelled out [at the SQLite website][compilation].  I don't think any are very relevant to your locally-hosted development copy of SQLite, but if you're curious, there they are.

## Using SQLite with PHP 5.1.X ##

SQLite is built into php 5.1.X, so you can simply install [Marc Liyanage's excellent PHP distribution][entropy], and start going with code like:

    <?php
        $db = new SQLiteDatabase(":memory:");
        $db->query("
            BEGIN;
                CREATE TABLE hello_world (text varchar(12));
                INSERT INTO hello_world VALUES ('Hello World!');
            COMMIT;
        ");
        $result = $db->query("SELECT * FROM hello_world");
        $row = $result->current();
        print $row[0];
    ?>

Unfortunately, my [PHP distribution of choice][entropy] seems to have dropped the PDO drivers for SQLite in the [5.1.4 release][entropy_5_1_4].  That's a shame, as [TextDrive][textdrive] wants me to use the PDO drivers to access SQLite 3+ databases.  

Reverting to the [5.1.2 release][entropy_5_1_2] gives me back my the precious PDO support, but I'm still looking around for a simple way of bringing the PDO drivers to the party in a more recent release of PHP.  I'll update this post as soon as I figure something out.

## Further Reading ##

*   [The SQLite website][sqlite] is, of course, a great resource for SQLite
    development in general.
*   Zend has a [good SQLite introduction][intro] avaliable for your reading
    pleasure.

[sqlite]: http://www.sqlite.org/ "SQLite"
[binary]: http://www.sqlite.org/download.html "SQLite Download Page"
[compilation]: http://www.sqlite.org/compile.html "Compilation Options for SQLite"
[entropy]: http://www.entropy.ch/software/macosx/php/ "Marc Liyanage's excellent PHP distribution for OS X"
[entropy_5_1_4]: http://www2.entropy.ch/download/entropy-php-5.1.4-5.tar.gz "PHP 5.1.4 :: Marc Liyanage's Binary Distribution for OS X"
[entropy_5_1_2]: http://www2.entropy.ch/download/Entropy-PHP-5.1.2-1.dmg "PHP 5.1.2 :: Marc Liyanage's Binary Distribution for OS X"
[intro]: http://www.zend.com/php5/articles/php5-sqlite.php "Zend :: SQLite Introduction"
[textdrive]: http://textdrive.com/
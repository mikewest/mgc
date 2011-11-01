---
layout: post
title:  Intro to IndexedDB
tags:
    - indexeddb
    - api
    - mozilla
    - chrome
    - presentation
    - gtug
    - google
    - javascript
    - webdev
    - development
    - html5
    - offline

Teaser:
    Yesterday at the Silicon Valley GTUG meetup, I gave a presentation
    introducing the IndexedDB API.  I've thrown the slides on Slideshare,
    but the transcription there is absolutely miserable.  I'll reproduce
    it here in a readable format, and add a few notes where appropriate.
---
Yesterday at the Silicon Valley GTUG meetup, I gave a presentation introducing the IndexedDB API.  I've thrown the slides on Slideshare, but the transcription there is absolutely miserable.  I'll reproduce it here in a readable format, and add a few notes where appropriate.

Video
-----

<iframe
  class="youtube-player"
  height="370"
  src="https://www.youtube.com/embed/yRo2hVoHWdQ?start=382"
  title="'Intro to IndexedDB' on YouTube"
  type="text/html"
  width="606"
  frameborder="0"></iframe>

Embedded Slides
---------------

<iframe
  frameborder="0"
  height="506"
  src="http://www.slideshare.net/slideshow/embed_code/6162787"
  title="'Intro to IndexedDB' on Slideshare"
  width="606"
  scrolling="no"></iframe>

Slide Transcript
----------------

1.  *IndexedDB*: Mike West, [@mikewest][twitter], <mkwst@google.com>,
    [SV GTUG][sv-gtug], 2010.12.14

2.  *Beta*: The IndexedDB API is incredibly beta.  It’s only implemented in
    Firefox 4 and Chrome dev channel, so it’s not anything that can be used for
    production projects in the near future.  Microsoft and Opera are
    contributing to the spec, however, and Google is working on pushing the
    code upstream to Webkit itself, so this looks like something that will be
    more and more relevant going forward.  

    Since the spec’s not finished, and everything’s in dev mode, this is a
    _great_ time to examine the API, and experiment.  We need to play around
    with this code, and feed our experience back into the standards bodies and
    browser vendors: that’s the best way to ensure that things work the way we
    want them to when everything’s solidified.

3.  *Offline*: One of the most exciting recent realizations in web development
    is that the offline bits of the HTML5 suite of specifications are _really
    ready_ for widespread use.  It's possible to store arbitrary amounts of
    information on a user's computer without resorting to opaque hacks like
    Flash storage, while at the same time making that information available in
    useful ways to your program's code.  This opens up a whole new world of
    sites and applications which we're only just beginning to appreciate.
    Offline's important, and not just because of the Web Store.

4.  *Storage Options*: What I'd like to do here is take a very brief survey of
    the landscape for context, and then dive into one particular feature that I
    think will become important in the near future: IndexedDB.

5.  *Cookies*:  These aren't offline at all, but they're relevant to the general
    context of how web applications store data at the moment.  The image on this
    slide is [Luigi Anzivino's "Molasses-Spice cookies"][slide5bkg] (which look
    delicious).

6.  *Cookies*

    *   Simple, key-value pairs, "shared' between server and client.
    
    *   Excellent for maintaining state, poor for anything else, as they are
        unstructured, and incur a signiﬁcant overhead for each HTTP request.

7.  *Local Storage*:  The image on this slide is [Evan Leeson's
    "Toasters"][slide7bkg].

8.  *Local Storage*
    
    *   The simplicity of cookies, tuned for higher-capacity,
        client-side-only storage.

    *   Dead simple API:

            localStorage.setItem( ‘key’, ‘value’ );
            localStorage.getItem( ‘key’ ); // ‘value’

    *   Values are unstructured strings:
        
        *  Filtering and search are _O(n)_, unless you layer some indexing
           on top.
        
        *  Structure requires `JSON.stringify` & `JSON.parse`


9.  *WebSQL*: The image on this slide is [Nick P's "file cabinet to
    heaven"][slide9bkg], which is a pretty accurate representation of life with
    WebSQL.  Stacking file cabinets on top of each other certainly provides you
    with the possibility of well organized storage, but that doesn't mean it's
    a good idea.

10. *WebSQL*
     
    *   A real, relational database\n implementation on the client (SQLite)
    *   Data can be highly structured, and `JOIN` enables quick, ad-hoc
        access
    *   Big conceptual overhead (`SQL`), no finely grained locking
    *   Not very JavaScripty, browser support is poor (IE and Firefox won't
        implement it), and [the spec][websql] has been more or less abandoned.

11. *File API*: The image on this slide is [Davide Tullio's "Hard Disk in
    B&W][slide11bkg].

12. *File API*: I know nothing about the File API, but Seth does!  And his
    presentation is right after mine, so I'll be all ears.  :)

13. *IndexedDB*: The image on this slide is [Robin Riat's "Kanuga library card
    catalog"][slide13bkg]

14. *IndexedDB*:  
    
    *   Sits somewhere between full-on SQL and unstructured key-value pairs
        in localStorage.
    *   Values are stored as structured JavaScript objects, and an indexing
        system facilitates filtering and lookup.
    *   Asynchronous, with moderately granular locking
    *   Joining normalized data is a completely manual process.

15. *IndexedDB Concepts*

16. Practically everything is asynchronous. Callbacks are your friends.

17. Databases are named, and contain one or more named *Object Stores*

18. A diagram of how a database might look, containing a single object store
    and a set of objects.

19. Object stores define a property (similar to a primary key) which every
    stored object must contain, explicitly or implicitly (autoincremented).

20. The same diagram as #18, with IDs added.

21. Values in an Object Store are structured, but don’t have a rigidly defined 
    schema.  Think document database, CouchDB.  Not MySQL.

22. The same diagram as #20, with differing data added for various objects.

23. Object Stores can contain one or more *Indexes* that make filtering and
    lookup possible via arbitrary properties.

24. The same diagram as #22, with a subset highlighted (as though they were
    filtered out).

25. *IndexedDB API*: Now we'll dive into some JavaScript.  Lovely, lovely
    JavaScript.

26. It's beta.  Again.  This is a reminder.  :)

27. *Vendor Prefixes*:  `webkitIndexedDB` & `moz_indexedDB`

28. *Code:*

        // Deal with vendor prefixes
        if ( "webkitIndexedDB" in window ) {
          window.indexedDB      = window.webkitIndexedDB;
          window.IDBTransaction = window.webkitIDBTransaction;
          window.IDBKeyRange    = window.webkitIDBKeyRange;
          // ...
        } else if ( "moz_indexedDB" in window ) {
          window.indexedDB = window.moz_indexedDB;
        }
        if ( !window.indexedDB ) {
          // Browser doesn’t support indexedDB, do something
          // clever, and then exit early.
        } 

29. *Database Creation*

30. *Code:*

        var dbRequest = window.indexedDB.open(
          “AddressBook”,        // Database ID
          “All my friends ever” // Database Description
        );

        // The result of `open` is _not_ the database.
        // It’s a reference to the request to open
        // the database.  Listen for its `success` and
        // `error` events, and respond appropriately.
        dbRequest.onsuccess = function ( e ) { ... };
        dbRequest.onerror   = function ( e ) { ... };

31. *Databases are versioned...* 

32. *Code:*

        // The `result` attribute of the `success` event
        // holds the communication channel to the database
        dbRequest.onsuccess = function ( e ) {
          var db = e.result;
          // Bootstrapping: if the user is hitting the page
          // for the first time, she won’t have a database.
          // We can detect this by inspecting the database’s
          // `version` attribute:
          if ( db.version === “” ) {
            // Empty string means the database hasn’t been versioned.
            // Set up the database by creating any necessary
            // Object Stores, and populating them with data
            // for the first run experience.
          } else if ( db.version === “1.0” ) {
            // 1.0 is old!  Let’s make changes!
          } else if ( db.version === “1.1” ) {
            // We’re good to go!
          }
          // ...
        };

33. *... and versioning is asychronous.*

34. *Code:*

        dbRequest.onsuccess = function ( e ) {
        var db = e.result;
        if ( db.version === “” ) {
          // We’re dealing with an unversioned DB.  Versioning is, of
          // course, asynchronous:
          var versionRequest = db.setVersion( “1.0” );
          versionRequest.onsuccess = function ( e ) {
            // Here’s where we’ll set up the Object Stores
            // and Indexes.
          };
        }
        // ...
      };

35. *Creating Object Stores and Indexes*

36. *Code:*

        dbRequest.onsuccess = function ( e ) {
        var db = e.result;
        if ( db.version === “” ) {
          var versionRequest = db.setVersion( “1.0” );
          // Setting a version creates an implicit Transaction, meaning
          // that either _everything_ in the callback succeeds, or
          // _everything_ in the callback fails.
          versionRequest.onsuccess = function ( e ) {
            // Object Store creation is atomic, but can only take
            // place inside version-changing transaction.
            var store = db.createObjectStore(
              "contacts",  // The Object Store’s name
              "id",        // The name of the property to use as a key
              true         // Is the key auto-incrementing?
            );
            // ...
          };
        }
        // ...
      };

37. *More code:*

        dbRequest.onsuccess = function ( e ) {
          var db = e.result;
          if ( db.version === “” ) {
            var versionRequest = db.setVersion( “1.0” );
            versionRequest.onsuccess = function ( e ) {
              var store = db.createObjectStore( "contacts", "id", true );
              store.createIndex(
                “CellPhone”,  // The index’s name
                “cell”,       // The property to be indexed
                false         // Is this index a unique constraint?
              );
            };
          }
          // ...
        };

38. *Writing Data (is asynchronous)*

39. *Code:*

        // Assuming that `db` has been set somewhere in the current
        // scope, we use it to create a transaction:
        var writeTransaction = db.transaction(
          [ “contacts” ],           // The Object Stores to lock
          IDBTransation.READ_WRITE  // Lock type (READ_ONLY, READ_WRITE)
        );
        // Open a contact store...
        var store = writeTransaction.objectStore( “contacts” );
        // ... and generate a write request:
        var writeRequest = store.add( {
            “name”:  “Mike West”,
            “email”: “mkwst@google.com”
        } );
        writeRequest.onerror = function ( e ) {
            writeTransaction.abort();
        };
        // Transactions are “complete” (not “committed”?) either when
        // they fall out of scope, or when all activities in the
        // transaction have finished (whichever happens last)
        writeTransaction.oncomplete = function ( e ) { ... };

40. *Reading Data (is asynchronous)*

41. *Code:*

        // Assuming that `db` has been set somewhere in the current
        // scope, we use it to create a transaction:
        var readTransaction = db.transaction(
          [ “contacts” ],           // The Object Stores to lock
          IDBTransation.READ_ONLY   // Lock type (READ_ONLY, READ_WRITE)
        );
        // Open the `contact` store...
        var store = readTransaction.objectStore( “contacts” );
        // ... and generate a cursor to walk the complete list:
        var readCursor = store.openCursor();
        // Setup a handler for the cursor’s `success` event:
        readCursor.onsuccess = function ( e ) {
          if ( e.result ) {
            // You now have access to the key via `e.result.key`, and
            // the stored object via `e.result.value`.  For example:
            console.log( e.result.value.email ); // mkwst@google.com
          } else {
            // If the `success` event’s `result` is null, you’ve reached
            // the end of the cursor’s list.
          }
        };

42. *Querying (is asynchronous)*

43. *Code:*

        var t = db.transaction( [ “contacts” ], IDBTransation.READ_ONLY );
        var s = t.objectStore( “contacts” );
        // ... and generate a cursor to walk a bounded list, for example
        // only those names between M and P (inclusive)
        var bounds = new IDBKeyRange.bound(
          “M”,  // Lower bound
          “Q”,  // Upper bound
          true, // Include lower bound?
          false // Include upper bound?
        );
        var readCursor = store.openCursor( bounds );
        // Setup a handler for the cursor’s `success` event:
        readCursor.onsuccess = function ( e ) {
          // process `e.result`
        };

44. *Further Reading:*

    * [The IndexedDB Spec](http://www.w3.org/TR/IndexedDB/)
    * [Firefox 4: An Early Walkthrough of IndexedDB](http://hacks.mozilla.org/2010/06/comparing-indexeddb-and-webdatabase/)
    * [Mozilla Developer Docs](https://developer.mozilla.org/en/IndexedDB)

45. *Questions?*, Mike West, [@mikewest][twitter], <mkwst@google.com>,
    http://mikewest.org/

[twitter]:    http://twitter.com/mikewest
[sv-gtug]:    http://sv-gtug.blogspot.com/
[slide5bkg]:  http://www.flickr.com/photos/ilmungo/65345233/in/photostream/
[slide7bkg]:  http://www.flickr.com/photos/ecstaticist/4743121155/
[slide9bkg]:  http://www.flickr.com/photos/nickperez/2569423078/
[websql]:     http://www.w3.org/TR/webdatabase/
[slide11bkg]: http://www.flickr.com/photos/daddo83/3406962115/
[slide13bkg]: http://www.flickr.com/photos/31408547@N06/4671916278/

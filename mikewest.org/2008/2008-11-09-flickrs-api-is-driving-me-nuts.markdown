---
Alias:
- http://mikewest.org/blog/id/95
Modified: '2008-11-09T17:00:13Z'
Teaser: I'm trying to do something with the Flickr API that I consider to be relatively
    trivial. I have the impression that the API is fighting me every step of the way.
    Why, oh why, can't the wonderful people who designed Del.icio.us's new API hop
    over to Flickr and slap together something that makes sense from the perspective
    of the end user?
layout: post
tags:
- mikewest.org
- projects
- fallow
- flickr
- api
- webdev
- development
title: Flickr's API is driving me nuts
---
I'm trying to do something with the Flickr API that I consider to be relatively trivial. I have the impression that the API is fighting me every step of the way. Why, oh why, can't the wonderful people who designed Del.icio.us's new API hop over to Flickr and slap together something that makes sense from the perspective of the end user?

## Basics

I'd like to have a list of my flickr sets as a block on my homepage, displaying the most recent sets in the order they were published, along with some simple metainformation and a thumbnail.  I'd also like to display photosets in my [archive pages][archive], interspersed throughout the rest of the content at the proper point in the timeline.

Most of this is easy to get with a single call to [`flickr.photosets.getList`][getList].  The XML that's returned looks something like:

    <?xml version="1.0" encoding="utf-8" ?>
    <rsp stat="ok">
    <photosets>
        <photoset id="[ID GOES HERE]" primary="2914968443" secret="[SECRET GOES HERE]" server="3007" farm="4" photos="2" videos="0">
            <title>2008-10 - Driving</title>
            <description />
        </photoset>
        ...
    </photosets>
    </rsp>
    
Simple enough to parse, and in combination with Flickr's [standardized url structure][urls], this gets me relatively close to the data that I'm looking for.  The small bit that's missing is an actual publication date, which is significant for my plans.  Without it, I can't correctly insert the photosets into my archive pages, and so far as I can tell, the data simply isn't exposed via the API.  So let's dig around a bit.

Since I know what the primary photo is for the photoset, I can grab it via [`flickr.photos.getInfo`][getInfo], which gets me the photo's dates:

    <?xml version="1.0" encoding="utf-8" ?>
    <rsp stat="ok">
    <photo id="2914968443" secret="[SECRET GOES HERE]" server="3007" farm="4" dateuploaded="1223227911" isfavorite="0" license="3" rotation="0" originalsecret="c87ab26ef7" originalformat="jpg" media="photo">
    	...
    	<dates posted="1223227911" taken="2008-10-04 18:12:42" takengranularity="0" lastupdate="1223283362" />
        ...
    </photo>
    </rsp>

Leaving aside the strange change of [timestamp format][time], and the nonsensical lack of timezone information, I can mash those into the photoset data to get an approximation of it's creation date.  That works pretty well, actually.  It means, however, that I have to make an additional API request for _each_ photoset.  That's more than a little annoying.

But now I have all the information I need, so putting the code together is straightforward.  Straightforward, that is, until I start thinking about the necessity to automatically update this data periodically.

## Updates

The [Del.icio.us API][delicious] is really good about handling this scenario:
[`posts/all`][posts_all] returns all the your bookmarks, and allows you to _filter_ the list by tag or date range.  If I know, for instance, that I last polled for changes at 10:00 this morning, I can ask Del.icio.us to send me only the bookmarks that came in _after_ that point in time.  This makes the update-handling code on my end quite simple: I ask for all the updates since the last bookmark I've stored locally, and when I get a response, I treat the whole thing as new.

Flickr doesn't, so far as I can tell, support the same mechanisms.  This has the effect of pushing validation down to my layer: I grab a list of all my photosets and then walk through the list, checking locally to see if I've already got the information stored.  This is stupendously inefficient, and actually becomes _more_ inefficient as time goes on and I add more photosets.

The closest Flickr comes to the Del.icio.us level of efficiency is [`flickr.photos.getRecent`][getRecent], which returns a list of up to 500 recent photos.  It doesn't, however, provide the same benefit as the Del.icio.us feed, as it doesn't allow you to specify what "Recent" means.  It simply pulls a set number of photos off the top and throws them back over the wall.

I would _love_ to see something like the Del.icio.us functionality added to the Flickr API. It would make my particular use case quite a bit simpler, and if applied across the board, it would make the entire Flickr API better suited to the polling-based tasks it's being put to.

[archive]: /archive
[getList]: http://www.flickr.com/services/api/flickr.photosets.getList.html
[urls]: http://www.flickr.com/services/api/misc.urls.html
[getInfo]: http://www.flickr.com/services/api/flickr.photos.getInfo.html
[delicious]: http://delicious.com/help/api
[posts_all]: http://delicious.com/help/api#posts_all
[time]: http://www.flickr.com/services/api/misc.dates.html
[getRecent]: http://www.flickr.com/services/api/flickr.photos.getRecent.html
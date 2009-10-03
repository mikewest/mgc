---
Alias:
- http://mikewest.org/blog/id/93
Modified: '2008-11-02T11:34:15Z'
Teaser: Hopefully, you didn't notice a thing yesterday when I moved the site off my
    shared accelerator at Joyent, and onto a custom built slice at Slicehost.  That
    was very much the goal.  Briefly, I'll go through the steps I took to make the
    transition as smooth as possible both before the launch and directly afterwards.
layout: post
tags:
- mikewest.org
- projects
- migrations
- server
- dns
- dnsmadeeasy
- webdev
- development
- howto
- bestpractice
- performance
- sysadmin
- logfiles
title: Smoothly Migrating to a New Server
---
Hopefully, you didn't notice a thing yesterday when I moved the site off my shared accelerator at Joyent, and onto a custom built slice at Slicehost.  That was very much the goal.  Briefly, I'll go through the steps I took to make the transition as smooth as possible both before the launch and directly afterwards.

## DNS and TTL ##

I read in a cookbook once that the first step in _any_ recipe is to boil water.  It doesn't really matter what you're making; there's a very high probability that you'll need boiling water at some point in the process, and since it takes _forever_ to boil, you'll want to get it started as soon as possible.  So, when you find yourself mildly hungry, just walk into the kitchen, fill a pot with water, set it on the stove, and then start thinking about what you want to eat.  Worst case, you can make yourself some tea afterwards.

In exactly the same way, you need to think about your site's DNS situation as early as possible, even if you're not sure where the site will end up when you're done.  DNS changes can take _days_ to propagate, depending on local ISPs cache settings, so it's really in your best interest to start thinking about this part of the migration first, well before you're ready to launch.

Most people don't pay too much attention to DNS.  They'll use their hosting service's DNS servers, or, worse yet, their domain registrar's.  These generally provide very basic service, and very few offer the granularity you'd get with a service like [DNSMadeEasy][], who I've [talked about before][iseasy] and highly recommend.

In particular, the feature that's most important for smooth migration is the ability to set the <abbr title="Time to Live">TTL</abbr> for a particular DNS record.  TTL prescribes the length of time (in seconds) a particular DNS lookup ought be cached before asking a domain's authoritative server for an update.  Generally speaking, your IP address doesn't change, so there's no point in asking your users to look it up every time they come to your site.  That lookup accounts for a good bit of overhead, hovering somewhere around 20-120 milliseconds per request, [according to Yahoo!'s exceptional performance team][dnsperformance].  Normally, then, you'll want to keep your TTLs relatively long; I leave mine at about a day (86,400 seconds).

Migrations, however, require much more rapid reaction times.  You'll want to minimize the time between pointing the domain to the new IP address, and the time at which your users actually start hitting the new site.  As soon as you think you might be moving to a new server, or changing your server's IP (to add an SSL certificate, for instance), your first step should be to dial down the TTL on your domains so that the change gets to your users as quickly as possible.  As I said, I leave my TTL sitting at one day, which means I need to dial it down at _least_ 24 hours before the changeover.  And since ISPs are notoriously bad about caching DNS lookups longer than you've actually recommended, it'd be best to reduce your TTL as early in the process as possible.

For yesterday's migration, I dropped `mikewest.org`'s TTL down to an hour about a week ago, and then down to 30 seconds a few hours before I made the cutover.  Today or tomorrow, when I'm sure everything's working correctly on the new server, I'll dial that back up.

[DNSMadeEasy]:  http://dnsmadeeasy.com/
[iseasy]:       /2007/12/dns-made-easy-is-actually-pretty-easy  "Mike West: 'DNS Made Easy is actually pretty easy'"
[dnsperformance]: http://developer.yahoo.com/performance/rules.html#dns_lookups

## Staging ##

A big advantage of moving to a new server is that you simply don't have to worry about breaking anything on the live site while you're rolling out changes.  I'm using a completely different stack on the new slice than I was on Joyent's box, and getting that running on the same machine as the old site would have been... interesting to say the least.  A new server gives you the opportunity to stage your work somewhere, get it tested and running on the production hardware, and then make the cutover when you're reasonably confident that things will go well.

Make sure you take advantage of this opportunity by pointing a domain at the server while you're still in development: `test.mikewest.org`, for example.  This allows you to hit the new box from a variety of client machines without the necessity of screwing with `/etc/hosts` files.

Just before launch, however, it's a good idea to adjust your hosts file to point the "live" domain at the new server to make sure that you've set things up correctly.  It's easy during development to create an environment that works perfectly under the test domain, but fails spectacularly under the live domain.  Setting your hosts file and hitting the site that way gives you assurance that you haven't made that sort of mistake.

## Content Feeds ##

The vast majority of people who read this site do so through RSS feeds.  There's simply no reason to type `mikewest.org` into a browser every day when you can get the content pushed to you.

I use [feedburner][] to distribute my feeds, which made it much simpler to seamlessly migrate from one server to the next.  I created three new feeds for this iteration of the site: [one feed for posts][postfeed], [one feed for links][linkfeed], and [one feed for a combination of both][bothfeed].  I pointed each of these at my staging server's domain to verify that they correctly retrieved content and that nothing was wrong with the new feeds I was building (this is another advantage of a publicly accessible staging server: third-party integrations are _much_ simpler to test).

When I made the cutover yesterday, I simply changed the location at which each of the feeds looks for content.  I kept an eye on each via my trusty NetNewsWire to make sure that the transition was successful, and it seems to have gone off without a hitch.

[postfeed]: http://feeds.mikewest.org/just_posts
[linkfeed]: http://feeds.mikewest.org/just_links
[bothfeed]: http://feeds.mikewest.org/omg_everything_ever
[feedburner]: http://www.feedburner.com/

## Redirects for old content ##

It's important to maintain consistency for your users, especially if you're changing URL structure as part of your migration.  I've [written about this problem][modrewrite], way back in 2006 when I last made major changes to mikewest.org, and I think the advice there has held up really quite well.  In a nutshell, set up redirects for your old content that cleanly map to the new page structures, and make sure that you pay attention to your access logs to get an understanding for the way your content is being linked to from the outside world.  If you haven't read ['Leveraging mod_rewrite'][modrewrite] yet, I think that it's worth a few minutes of your time.

[modrewrite]: /2006/05/leveraging-modrewrite

## `tail -f` your access log ##

Directly after the launch, it's important to keep an eye on the access log to identify issues that you missed in your own testing.  For example, I haven't gotten around to building an archive overview page yet, so the `/archive` link currently ends up as a redirect to the current yearly overview: `/2008`.  This worked perfectly in the tests I did, so I was happy.

Right after the launch, however, I started seeing a whole lot of 4-request sequences for `/archive/`, which 301'd to `/archive`, which 302'd to `/2008/`, which 301'd to `/2008`.  That's a bit much.  As it turns out, when I made the decision to strip ending `/` characters to standardize the site's URLs, I'd inserted the rule in the wrong place, so it was running _before_ any of the redirects I'd coded into the site.  I'd also made the mistake of hard-coding `/archive/` into the link on the homepage, and `/#{year}/` as the redirect link.  This meant that instead of a single 302 temporary redirect, the user was running through _three_ redirects to get to the end goal.  This showed up clearly in the logs, and was an easy bug to fix.  This sort of thing popped up pretty often in the first hour or two after the switch.  They're small things that can make a big difference to the user experience, but you can't fix them unless you look for them.

Running through the log periodically with something like: `tail -n500 ./access.log | grep ' 50[0-9] '` gives you a quick overview of the most recent server errors (and there will probably be some...).  Likewise, `tail -n500 ./access.log | grep ' 40[0-9] '` gives you a feel for what content is being requested that you're not providing anymore, which you can use to set up appropriate redirects, or to bring back or update old content that your users want to see.
---
layout: post
title: "Nerdy New Year"
tags:
  - resolutions
  - ssl
  - cdn
  - certificate
  - hsts
  - startssl
  - cookies
  - webdev

Teaser:
  "New Year's resolutions come in all shapes and sizes; if you're a web
  developer stuck for good ideas of things you could do to improve the world
  (or at least the tiny chunk of it that's concerned with web performance and
  security) I'd like to propose two: secure all your websites, and use a
  cookieless domain for static assets."
---
New Year's resolutions come in all shapes and sizes; if you're a web
developer stuck for good ideas of things you could do to improve the world
(or at least the tiny chunk of it that's concerned with web performance and
security) I'd like to propose two: secure user's connections to all your
websites, and use a cookieless domain for static assets.

## SSL Everywhere.

If you look closely, you'll notice that `mikewest.org` is being served via a
secure connection: `https` rather than `http`. This is a Good Thing™, for
reasons which I explored [earlier this year][4]. I'd like to suggest that each
of you pop open Firefox (yes, Firefox) and head to [StartSSL][5] where you can,
_for free_, create an account, verify your ownership of a domain, and generate
an SSL certificate.

I've moved to StartSSL for every domain I own that hosts a website. It's
trivially easy, very well supported (I've never waited more than 18 hours for a
response to a support request), and works well in every browser I care about.
Moreover, it's run by real people who you can email. I've gotten responses from
the founder himself at two in the morning; the service is brilliant.

I'd suggest, actually, going through the extra step of verifying your identity
with them so that you can generate wildcard certificates, and certificates
with DNS alt names: both will make it easier for you to host SSL websites
without the annoyance of setting up separate IP addresses for each host.
They charge $59.90 for the verification, at which point you can create as many
certificates as you like. It's a heck of a deal.

And hey, while you're at it, start serving [`Strict-Transport-Security`][4]
headers too!

[4]: https://mikewest.org/2011/10/http-strict-transport-security-and-you
[5]: https://www.startssl.com/

## Cookieless domains for static assets

You've probably heard at some point in the past that it's a [good][1] [idea][2]
to serve static assets from a domain that doesn't set cookies. Yesterday, I
finally got around to doing that here. If you hop into devtools or Firebug,
you'll see that this page's CSS, JavaScript, and images are all being served
not from `mikewest.org`, but from `mikewestdotorg.hasacdn.net`. Setting up an
alias like this is trivial in any server. Here's how I made it work in Nginx:

My websites all have specific directories in which static assets live,
`/home/mkwst/public_html/mikewest.org/public/static` for example. I simply set
up a server listening for requests to `mikewestdotorg.hasacdn.net`, and use
the static asset directory as the `root`. With that in place, I ensure that all
files are served with [far-future expiry headers][3], and then set up some
trivial versioning magic by ignoring the first chunk of the URL:
`https://mikewestdotorg.hasacdn.net/20111231/style.css` serves the same file
as `https://mikewestdotorg.hasacdn.net/1/style.css`, but because the 
paths are different, the file can be loaded and cached anew when something
changes.

That setup looks like this:

    server {
      listen 80;
      server_name mikewestdotorg.hasacdn.net;

      # Turn off logging for static assets:
      access_log  off;
      error_log   /dev/null crit;

      # Set the root from which Nginx reads files for this domain:
      root /home/mkwst/public_html/mikewest.org/public/static;

      location / {
        add_header Expires "Thu, 31 Dec 2037 23:55:55 GMT";
        add_header Cache-Control "public, max-age=315360000";
        
        if (-f $request_filename) {
          break;
        }

        rewrite ^/\d+/(.*) /$1 break;
      }
    }
  
Easy! I've thrown [the whole config file up on GitHub][gh] if you're curious. 

[1]: http://code.google.com/speed/page-speed/docs/request.html#ServeFromCookielessDomain
[2]: http://developer.yahoo.com/performance/rules.html#cookie_free
[3]: http://developer.yahoo.com/performance/rules.html#expires
[gh]: https://github.com/mikewest/hasacdn.net/blob/master/private/nginx.conf

So there you have it; enjoy the end of your holidays with these two resolutions
that you can bang out over the weekend. You'll be ahead of the game, and the
envy of all your friends and neighbors when you compare notes at the end of
2012.

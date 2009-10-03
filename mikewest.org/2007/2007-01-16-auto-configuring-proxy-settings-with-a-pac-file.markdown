---
Alias:
- http://mikewest.org/blog/id/49
Modified: '2007-01-21T00:23:54Z'
Teaser: Configuring a browser's proxy settings manually is inflexible; proxy auto-config
    (PAC) files are much more flexible.
layout: post
tags:
- HOWTO
title: Auto-configuring Proxy Settings with a PAC File
---
At work, resources meant only for super-secret internal use are locked away
behind a homegrown authentication system.  To get at, for example, a piece of 
documentation, we connect through a proxy, get bounced around through a
single-signon system, and finally end up where we're trying to get.  This is
great for security, but not so wonderful for performance.  The proxy's just
not as fast as direct access, especially when accessing the internet at large.

I've taken to the hacky solution of setting Firefox up with the necessary
proxy settings, and using Safari to do all my browsing and testing.  This
works, but it's a bit of a pain in the ass.  Safari is not, for me, a browser
that's conducive to development.  I need a way to load up the super-secret AND
the not-so-secret sites in Firefox, passing the former through the proxy, and 
hitting the latter directly.

As it turns out, this is a problem that's really quite solved; there's no need
to dig around through a series of Firefox extensions that do way more than I
want them to; I can simply set up a [proxy auto-config (PAC) file][pac] that gives
me quite fine-grained control over when the proxy kicks in.

In a nutshell, the auto-config file is a JavaScript file that defines a single
function (`FindProxyForURL`) that accepts two arguments (`url` and `host`).  This function is called just before the browser requests a page, and, as you
might expect, tells the browser whether it should hit a proxy or grab the
page directly.  If you write an auto-config file, and host it on a server
somewhere, then you're good to go with regard to proxy configuration in any
browser that supports the standard (read: all browsers ever).

[pac]: http://en.wikipedia.org/wiki/Proxy_auto-config "Wikipedia: Proxy Auto-config"

The Proxy Auto-Config File Format
---------------------------------

In the simplest case, you need to use a basic proxy server for every request
your browser makes.  Assuming you connect through port 8080 of
`my.proxy.server.com`, the corresponding auto-config file is trivial:

    function FindProxyForURL(url, host) {
        return "PROXY my.proxy.server.com:8080";
    }
    
Easy, right?  No matter what `url` gets passed to the function, you return a 
string containing the connection method ("PROXY", we'll talk about others in
a second) and the server.

But let's say you're in my situation.  You need to use the proxy server for 
_some_ sites, and directly connect to others.  Let's say
`super-secret.website.com` hid behind the proxy, and you could connect to
everything else directly:

    function FindProxyForURL(url, host) {
        if (
            localHostOrDomainIs(host, "super-secret.website.com")
        ) {
            return "PROXY my.proxy.server.com:8080";
        } else {
            return "DIRECT";
        }
    }

We use the `localHostOrDomainIs` function to compare the requested host to a
string.  If `host` is "super-secret.website.com", we return the proxy, if not,
we tell the browser to connect directly.

Finally, let's put together a more complex example.  Let's say that we need to
connect to some servers with one proxy, others through a Socks server, and
everything else directly.  Further, let's assume that our network design is 
strange enough to dictate that we access a particular server _differently_ 
based on the URL requested.  This is a strange scenario indeed, but is
relatively straightforward to implement:

    function FindProxyForURL(url, host) {
        //
        //  Here's a list of hosts to connect via the PROXY server
        //
        var proxy_1 = array(
            "super-secret.website.com",
            "mostly-secret.website.com",
            "my-secret.other-website.com",
            "our-secret.other-website.com"
        );
        
        for (var i = 0, var count = proxy_1.length; i < length; i++) {
            if (
                localHostOrDomainIs(host, proxy_1[i])
            ) {
                return "PROXY my.proxy.server.com:8080";
            }
        }
        
        //
        //  Here's a list of hosts to connect via the SOCKS server
        //
        var proxy_2 = array(
            "i-need-socks.website.com",
            "socks-are-warm-and-fuzzy.other-website.com"
        );
        
        for (var i = 0, var count = proxy_2.length; i < length; i++) {
            if (
                localHostOrDomainIs(host, proxy_1[i])
            ) {
                return "SOCKS my.socks.server.com:1080";
            }
        }
        
        //
        // Connect through a SOCKS server for everything on
        // `strange.server.com` under the `socks` subdirectory
        //
        if (
            shExpMatch(url, "strange.server.com/socks/*")
        ) {
            return "SOCKS my.socks.server.com:1080";
        //
        //  And through a normal PROXY server for everything
        //  on `strange.server.com` under the `proxy` subdirectory
        //
        } elseif (
            shExpMatch(url, "strange.server.com/proxy/*")            
        ) {
            return "PROXY other.proxy.server.com:8080";            
        }
        //
        // Directly connect to everything else
        //
        return "DIRECT";
    }
    
The `shExpMatch` function we added to this example allows you a lot of
flexibility by matching the `host` or `url` against a string with wildcards.
`shExpMatch(url, '*.domain.com/proxy/*')` would, for example, match any
request for a page under the `proxy` subdirectory of any subdomain of
`domain.com`. while `shExpMatch(host, 'secret.*.com')` would match any request
for any page on a server whose lowest-level domain is "secret".


Hosting The PAC File
----------------------------

Once you've written a proxy auto-config file using the techniques above, you
can either put it somewhere on your local disk and simply point the browser to
it, or host it remotely on a server you have access to.  You can name it
whatever you like, but conventionally it's named `proxy.pac`.

If you choose the latter method, you'll have to ensure that you serve the file
with the correct [MIME type][mime]: `application/x-ns-proxy-autoconfig`.  If
you're running Apache, you can simply add the following line to your
`.htaccess` file to send the correct headers for any file with the `.pac`
extension:

    AddType application/x-ns-proxy-autoconfig .pac

[mime]: http://en.wikipedia.org/wiki/Mime_type "Wikipedia: Internet Media Type"

More Resources
--------------

These examples outline everything I've ever needed when putting together my 
proxy configuration.  There are more functions out there for you to play with
if your configuration is more complex than what I've needed to deal with,
and documentation is fairly plentiful.

*   Netscape has good documentation of the various functions available for use
    in your auto-config file in their [documentation for proxy auto-config
    scripts][netscape_pac].
    
*   [Automatic proxy HTTP server configuration in web browsers][tesco] 
    contains, surprisingly enough, more detailed information about the inner
    workings of the proxy system in the browser engine.

[netscape_pac]: http://wp.netscape.com/eng/mozilla/2.0/relnotes/demo/proxy-live.html "Navigator Proxy Auto-Config File Format"
[tesco]: http://homepages.tesco.net/J.deBoynePollard/FGA/web-browser-auto-proxy-configuration.html "Automatic proxy HTTP server configuration in web browsers"

---
Alias:
- http://mikewest.org/blog/id/47
Modified: '2007-01-12T16:02:46Z'
Teaser: ''
layout: post
tags:
- HOWTO
title: Setting Up an OpenID Server with phpMyID
---
Sam Ruby's "[OpenID for non-SuperUsers][sam_openID]" distills the process of
[setting up one's own OpenID server][setup] with [phpMyID][] in such a clear and
concise manner, that I couldn't help but [implement it myself][my_server].  I've taken his
instructions, and turned them into a cut and past operation for anyone whose
website is hosted on a server with access to Subversion.  When you're
finished, you'll be the proud owner of a bleeding-edge OpenID server running
at http://yourdomain.com/open_id/.

To begin, SSH into your server, and change to the document root of your
website.  For example:

    cd ~/web/public/

Then run the following (very long) command:

    clear;mkdir ./open_id/;cd ./open_id/;read -p "Username: " USER;read -sp "Password: " PASS;echo;echo "Loading up the Files from the remote repository:";echo "t" > ./temp_file_to_accept_cert_non-interactively;svn export -q https://www.siege.org/svn/oss/phpMyID/trunk/MyID.php < ./temp_file_to_accept_cert_non-interactively > /dev/null 2>&1;echo 'Success.';echo 'The username and password you entered will be used to configure the OpenID server:';HASH=`echo -n "$USER:phpMyID:$PASS" | openssl md5`;NICE="\$new='\$profile=array(\"auth_username\"=>\"$USER\",\"auth_password\"=>\"$HASH\");';if (/^\#\\\$profile/) { \$_ = \$new; }";perl -pi.bak -e "$NICE" MyID.php;USER='';PASS='';mv MyID.php index.php;rm temp_file_to_accept_cert_non-interactively;rm MyID.php.bak;echo 'Success.';

You'll be prompted for a username, and a password.  Enter each in turn, and then sit back and relax while the script runs.

That's it!

Next Steps
----------

Once you've got the server installed correctly, [test it out][test].  Then
[head back over to Sam's article][next_steps] to set up a clean delegation to
your server from your main blog or homepage URL.  You'll have to edit your
site's template a bit, which isn't something I can write a generic script for.
But it's easy, so you'll do fine without me.

Troubleshooting
---------------

*   __Error__: "Missing expected authorization header."  If you get this
    error, you're probably running PHP as a CGI, and not as an Apache module.
    In this case, the authentication headers don't get created correctly, and
    the phpMyID server can't understand the login requests.
    
    To fix the problem, we'll write a corrective `.htaccess` file by running
    the following commands in the same directory where your phpMyID server
    lives (`~/web/public/open_id/` in our example):
    
        echo 'RewriteEngine on' >> .htaccess
        echo 'RewriteCond %{HTTP:Authorization} !^$' >> .htaccess
        echo 'RewriteCond %{QUERY_STRING} openid.mode=authorize' >> .htaccess
        echo 'RewriteCond %{QUERY_STRING} !auth=' >> .htaccess
        echo 'RewriteCond %{REQUEST_METHOD} =GET' >> .htaccess
        echo 'RewriteRule (.*) %{REQUEST_URI}?%{QUERY_STRING}&auth=%{HTTP:Authorization} [L]' >> .htaccess

[sam_openID]: http://www.intertwingly.net/blog/2007/01/03/OpenID-for-non-SuperUsers "Sam Ruby: 'OpenID for non-SuperUsers"
[setup]: http://www.intertwingly.net/blog/2007/01/03/OpenID-for-non-SuperUsers#MasterOfYourDomain
[next_steps]: http://www.intertwingly.net/blog/2007/01/03/OpenID-for-non-SuperUsers#claimYourBlog
[phpMyID]: http://siege.org/projects/phpMyID "phpMyID: A standalone, single user, OpenID Identity Provider"
[test]: http://www.openidenabled.com/resources/openid-test/checkup "Test your OpenID Setup"
[my_server]: https://mikewest.org/open_id/ "Mike West's OpenID Server"
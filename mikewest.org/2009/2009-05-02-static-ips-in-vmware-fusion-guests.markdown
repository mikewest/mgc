---
layout:     post
title:      "Static IPs in VMWare Fusion Guests"
slug:       "static-ips-in-vmware-fusion-guests"
aliases:
    - http://blog.mikewest.org/post/102662931
    - http://blog.mikewest.org/post/102662931/static-ips-in-vmware-fusion-guests
tags: 
    - vmware
    - virtualization
    - networking
    - staticip
    - dhcp
---
Generally speaking, your guests will pick up the same IP from VMWare every time.  You write some scripts assuming that those IPs will remain stable, and everything's good.  Then, for whatever reason, VMWare's DHCP server decides that your VM really ought to sit on 192.168.65.131 instead of 192.168.65.135, where it had been happy and comfortable for _weeks_.  Annoying.

The solution's simple: you need to tell Fusion to assign the same IP to a particular guest every time.  That's a trivial process:

1.  Log into your VM, and type `ifconfig -a | grep HWaddr | awk '{print $5}`.  That will spit out a string that looks something like "00:0c:29:f8:9d:61".  This string is your VM's <abbr title="Media Access Control">MAC</abbr> address that uniquely identifies this VM when it requests an IP address.  Write it down; you'll need it shortly.

2.  Back on your mac, open up VMWare's DHCP server config.  It sits in `/Library/Application Support/VMware Fusion/vmnet8/dhcpd.conf`, and is a simple text file that you can edit with something like TextMate or VIM.

        mate /Library/Application\ Support/VMware\ Fusion/vmnet8/dhcpd.conf

3.  Add a block for each of your VMs in the form:

        host [HOSTNAME] {
            hardware ethernet [MAC ADDRESS];
            fixed-address [STATIC IP OF YOUR CHOICE];
        }

    The address you choose needs to be in the same subnet as the previously assigned DHCP addresses.  Mine, for example, was 192.168.65.131, so I can pick any address in 192.168.65.*.  It's best to pick a number between 3 and 127, as VMWare has reserved that range for static IPs.

4.  Reboot VMWare's DHCP server so that it picks up the new assignments you've made:

        sudo /Library/Application\ Support/VMware\ Fusion/\boot.sh --restart

5.  Grab new addresses on your VMs.  The simplest way to do this is simply to reboot the machines.  If you're not into rebooting, you can either bring the ethernet interface down and back up again (on linux) with:

        sudo ifdown eth0 && sudo ifup eth0

    Windows has a similar set of commands:

        ipconfig /release
        ipconfig /renew

    Make sure you're not trying to perform this switch if you're SSHed into the machine.  I suspect turning off the network would have some adverse effects on your connection... :)

Enjoy your (dynamically) static IPs!

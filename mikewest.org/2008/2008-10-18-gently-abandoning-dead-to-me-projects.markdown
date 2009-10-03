---
Alias:
- http://mikewest.org/blog/id/91
Modified: '2008-10-18T13:25:43Z'
Teaser: I've had a few bits of code floating around on the site for 2-3 years now
    without any serious investment of effort on my part.  It's time to throw in the
    towel, admit that I'm never actually going to touch them again, and set those
    loose.
layout: post
tags:
- DataRequestor
- Personal
title: Gently abandoning dead (to me) projects
---
I've had a few bits of code floating around on the site for 2-3 years now without any serious investment of effort on my part.  It's time to throw in the towel, admit that I'm never actually going to touch them again, and set those loose under a liberal license.

## [DataRequestor][dr_code] ##

DataRequestor was a tiny project started in 2004 to solve some user interface issues we ran into while I was working at [Dallas Airmotive][].  It's a simple Ajax library, written before Ajax had a name.  Despite well intentioned statements to the contrary, I simply haven't touched the code since early 2005.  I'm proud of it's heritage, but it's not something I use anymore, and it's well outclassed and out-debugged by the frameworks that have become available in the meantime.

So, I'm [releasing the code][dr_code] under the [MIT license][].  It's up on GitHub (which I'm beginning to _love_) now.  It's yours for the forking.

[Dallas Airmotive]: http://www.bbaaviationero.com/node/5
[dr_code]: http://github.com/mikewest/datarequestor/tree/master  "GitHub: 'DataRequestor'"
[MIT license]: http://en.wikipedia.org/wiki/Mit_license "Wikipedia: 'MIT License'"

## [mcw_templates][mcw_code] ##

`mcw_templates` is a solid Textpattern plugin that enables the export and import of Textpattern templates, something so basic that I'm still shocked it's not officially part of the distribution.  I'm using Textpattern less and less, and now that I'm in the process of writing my own blog software, it's pretty clear that I'm never going to touch this plugin ever again.

So, I'm [releasing the code][mcw_code] under the [MIT license][].  It's up on GitHub now, and it's yours for the forking.  

[mcw_code]: http://github.com/mikewest/mcw_templates/tree/master "GitHub: 'mcw_templates'"

## [PerfectTime][pt_code] ##

Could PerfectTime have been more pompously named?  Blame _why, [it was his idea][why].  This is a small JavaScript library that automatically converts timestamps on a page into the user's timezone.  Useful, but not to me.  I've developed [doubts about it's accessibility][abbr], and even more doubts about it's widsom in general.  That said, it's a decent little tool that I'm never going to touch again.

So, I'm [releasing the code][pt_code] under the [MIT license][].  It's up on GitHub now, and it's yours for the forking.

[pt_code]: http://github.com/mikewest/perfecttime/tree/master "GitHub: 'PerfectTime'"
[why]: http://redhanded.hobix.com/inspect/showingPerfectTime.html "Whytheluckystiff: 'Showing Perfect Time'"
[abbr]: http://www.isolani.co.uk/blog/access/AccessibilityOfDateTimeMicroformat "Mike Davies: 'The accessibility of the date-time pattern in Microformats'"
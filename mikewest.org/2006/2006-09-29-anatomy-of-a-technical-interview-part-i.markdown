---
Alias:
- http://mikewest.org/blog/id/36
Modified: '2006-09-29T13:20:04Z'
Teaser: ''
layout: post
title: 'Anatomy of a Technical Interview: Part I'
---
Interviews for technical positions are tough, both for the interviewer and the interviewee.  The interviewer has the impossible task of evaluating someone's competence on a wide range of complex subjects in just a few hours.  The interviewee has the equally impossible task of proving that she's smarter than the average bear within the same tight time constraints.  Really, it's a wonder anyone ever gets hired at all.

There are no hard and fast rules you can follow to guarantee success in an interview.  

------------------------------------------------------------------------------

The Anatomy of a Web Development Interview
------------------------------------------

Interviews are tough, especially interviews for technical positions.  The interviewer wants to get a good feel for your problem-solving ability, and you want to answer questions as quickly and correctly as possible so that you give the best possible impression.  I interviewed for a web development position a little while back, and in this brief series of articles, I want to talk a little bit about a few of the more interesting questions I got asked, and the process by which I came up with an answer.

The first task focuses on JavaScript and the DOM, here it is: "__Write a function that returns an array containing all the elements on a page having a specified attribute.__"  Given that, where do you start?

## Prove That You're an Expert ##

The first thing to realize when you've in a good technical interview is that the answer you come up with probably matters less than you think.  It's important that you end up with some code that works, but the interviewer is typically more concerned with _how_ you get to the answer, and _why_ you went that route.  

When you get a question, don't start by grabbing a marker and scribbling on the whiteboard.  Step back a bit, and talk about the problem with the interviewer.  Make sure that you understand the task, and that the interviewer _knows_ that you understand it, before diving in.  If nothing else, this discussion is a good opportunity for you to point out everything you _do_ know, even if you're (for the moment) clueless as to how to solve the actual question at hand.

So, we might begin by talking about the similarities between the function we've been asked for and some built in DOM methods:  "Well, Ms. Interviewer, we've got `getElementsByTagName` which gives us an array of all the elements of a specific type, and we've got `getElementById` to get a specific element.  But neither of those seems immediately useful, so it looks like we'll have to write some code to hit every element on the DOM tree and test whether it has the attribute we're looking for."  We haven't gotten much closer to the goal, but we're _talking intelligently_ about the DOM.  We're giving the clear impression that we _know what we're talking about_ (hey, he knows that the DOM is a [tree][]!), which counts for a lot in the interview.

[tree]: http://en.wikipedia.org/wiki/Tree_%28data_structure%29 "Wikipedia: 'Tree (Data Structure)'"

From there, we need to come up with a plan of attack, so start discussing the algorithms you might choose to solve the problem you've just described.  You need to hit every DOM node on the tree... How could you do it?  In my interview, I latched onto [recursion][], both because it was the first thing that came to mind, and because [smart people][] consider recursion to be an important skill to test for:  "Well, generally speaking, we need to traverse a tree, hitting every node on the way.  It makes sense to do that recursively, starting at the top, and walking the tree depth-first, then sticking all the results into a big array to give back to the function's caller."

[recursion]: http://en.wikipedia.org/wiki/Recursion "Wikipedia: 'Recursion'"
[Steve Yegge]: http://steve-yegge.blogspot.com/ "Steve Yegge: 'Stevey's Blog Rants'"

## Apply Your Expertise ##

At this point, we've established that we more or less know what we're talking about, and outlined the general process by which we'll attack the problem.  Now we need to turn that general algorithm into a specific solution for our problem.
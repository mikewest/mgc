---
Alias:
- http://mikewest.org/blog/id/31
Modified: '2006-09-04T10:47:55Z'
Teaser: 'The interview articles I found yesterday had more than a few common "phone
    screen" questions that I decided to make sure I could answer:  here''s what I
    came up with.'
layout: post
tags:
- Personal
title: Answers to Common Technical Interview Questions
---
In an effort to convince myself that I really do know what I'm doing with this "web" thing, I've walked through some of the example interview questions from the articles I [mentioned yesterday][yesterday].  A few were simply inapplicable to the work I'd be doing, but actually doing the few minutes of work for the questions that matter is so much more worthwhile than simply looking at them and thinking "Yup.  I could do that."  I'm posting JavaScript implementations and explanations here in the hopes that someone out there is in a similar position and could use the help, or that a genius passing through will point out some silly mistake or cool optimization I missed.  So, here goes:

1.  __Write a function to return the _Nth_ [Fibonacci number][fib]__:  This is
    _the_ quintessential recursion problem.  Even though the recursive
    implementation is O(2<sup>n</sup>), it's almost certainly the answer your
    interviewer is looking for.  Here's one way of writing it:
    
        function fib(n) {
            return (n <= 1)?n:fib(n-1) + fib(n-2);
        }
    
    Easy, right?  The _Nth_ number is either the number itself (if it's 0 or
    1), or the sum of the previous two numbers.  Recursion is built right into
    the definition, no need to look farther afield for a "correct" answer.
    
    But in a technical interview, this is almost certainly the beginning of a
    larger question: how do we make this computation _fast_?  Recursion,
    though applicable here, is simply a slow way to calculate the values
    because it's doing just that: _calculating_ every value for `fib(n-1)`,
    over and over again.  We can vastly improve the code's performance by
    caching results as we calculate them in an iterative fashion, for example:
    
        function fib(n) {
            var cache   = [];
            cache[0]    = 0;
            cache[1]    = cache[2]  = 1;
            for (var i=3; i<=n; i++) {
                cache[i] = cache[i-2] + cache[i-1];
            }
            return cache[n];
        }
    
    This runs in something closer to O(n): the number of calculations
    increases linearly, a huge improvement over the recursive version's
    exponential explosion.
    
2.  __Print out a multiplication table, up to 12x12__:  Do you understand
    `for` loops?  Have you heard of `printf`?  Good, because that's about all
    that this question tests.  JavaScript, unfortunately, has no native
    `printf` function to pad out the results is probably a more interesting
    test than the question itself...
    
            function mult_table() {
                var theString = "";
                for (var i=1;i<13;i++) {
                    for (var j=1;j<13;j++) {
                        theString += pad(i*j, 4);
                    }
                    theString += "\n";
                }
                return theString;
            }
                function pad(str, len) {
                    var padding = (arguments[2] == "0" || arguments[2])?arguments[2]:" ";
                    str = str.toString();
                    while (str.length < len) {
                        str = padding + str;
                    }
                    return str;
                }
    
    The `mult_table` function is trivial: two `for` loops, one nested inside
    the other, to calculate 1x1, 1x2, 1x3, ..., 12x12.  The `pad` function
    takes the answer that was calculated, and pads it out to a certain length,
    using either " ", or the third argument (if one was provided).
    
3.  __Print all the odd numbers from 1 to N__:  Again, this is a fairly simple
    question with a fairly predictable answer.  Happily, we're able to reuse
    the `pad` function we just wrote to make the string prettier:
    
        function print_odds() {
            var theString = "";
            for (var i = 0; i < 100; i++) {
                if (i & 1) {
                    theString += pad(i.toString(), 3);
                }
            }
            return theString;
        }
        
    The only bit of trickery I've thrown into this implementation is the `if`
    condition, which eschews the typical `(i % 2 == 1)` test for the more
    esoteric bitwise and: "`&`".  In a nutshell, we can use `and` in this case
    to determine if the "ones" bit of a number is set, meaning that it's odd
    (if you're not up on binary, take a look at Dave Stewart's great article 
    "[Get a Speed Boost from the Bitwise Operator][bitwise]").  That's a bit
    faster than using modulus, though for a problem like this it's barely
    noticeable.
    
4.  __Determine how many bits are "on" in a given integer__:  Continuing with
    the bitwise theme, an answer to this question is to use bitwise `and` to
    act as a filter for our integer:

        function howManyBits(num) {
            var numBits = 0,
                i       = 1,
                theAnd  = Math.pow(2, i);
            do {
                numBits += (num & theAnd)?1:0;
                theAnd  = Math.pow(2, ++i)
            } while (theAnd <= num);
            return numBits;
        }
        
    We generate a test value with a single bit "on" by exploiting the fact
    that binary numbers with a single bit set are all powers of two (e.g.
    `00000001` = 1, `00000010` = 2, `00000100` = 4, etc.).  We'll simply
    generate filters until we've exceeded our number, and use each filter to
    test a single bit.  This is an easy solution, but I can't help but think
    that there must be a better way to do this...
    
5.  __Find the largest value in an array of integers__: There's not a
    straightforward way to do this without looking at each of the values in
    the array, so the easy solution (which is O(n)) is probably the best.  The
    only 'trick' is that you can skip evaluation of the first item in the
    array by using it as the initial value for `max`.  Otherwise, the code is
    very easy to sift through:
    
        function largest_int(theArray) {
            var max = theArray[0];
            for (var i=1;i<theArray.length;i++) {
                if (theArray[i] > max) {
                    max = theArray[i];
                }
            }
            return max;
        }

6.  __Implement [binary search][binary]__: This question simply tests whether
    or not you were paying attention in class when your prof waxed poetic
    about the virtues of O(n log(n)) search algorithms.  The basic premise of
    a binary search is this: given a sorted array, a particular value can be
    found by starting in the middle.  If the sought-after value is greater
    than the middle value, look in the middle of the _second_ half of the
    array.  If it's less, look in the middle of the _first_ half of the array.
    This question, therefore, is both testing your general knowledge of common
    algorithms, but also sneakily getting at your recursive chops as well:
    
        function binary_search(needle, haystack) {
            return binary_search_helper(needle, haystack, 0, haystack.length-1);
        }
            function binary_search_helper(needle, haystack, top, bottom) {
                var middle = Math.floor((bottom + top)/2);
                if (top > bottom) { return -1; }
                    if (haystack[middle] > needle) {
                        return binary_search_helper(needle, haystack, top, middle-1);
                    } else if (haystack[middle] < needle) {
                        return binary_search_helper(needle, haystack, middle+1, bottom);
                    } else {
                        return middle;
                    }
                }
            }
            
7.  __Implement [`atoi`][atoi] and [`itoa`][itoa]__:  Ok, honestly?  I had to look up
    what `atoi` and `itoa` meant.  This probably means that I'm completely
    disqualified from a C++ programming position.  That said, I'm not
    interviewing for C++, so hopefully that won't be a terrible strike against
    me.  The point, of course, is not _just_ to test whether you know C++
    vocabulary, but also whether you can implement something like `.toString`
    for integers in a reasonable way.  The "trick" here is to understand that
    each characters has a numerical code associated with it, and that each
    number character's code is defined to be one more than the previous number
    character's code.  In other words, if you calculate the character code for
    "0", you can simply subtract that from any other number's code to convert
    the character to an integer.  So, `'8'.charCodeAt(0) - '0'.charCodeAt(0)`
    gets you the integer `8`.  All you have to do is multiply that by the
    relevant power of 10, and you've got yourself an integer:

        function atoi(str) {
            var cur     = 0;
            var sign    = 1;
            var value   = 0;
            var zero    = '0'.charCodeAt(0);
            var nine    = '9'.charCodeAt(0);
            switch (str[0]) {
                case "-":
                    cur++;
                    sign = -1;
                    break;
                case "+":
                    cur++;
                    sign = 1;
                    break;
            }
            while (
                (cur < str.length) &&
                (str.charCodeAt(cur) >= zero && str.charCodeAt(cur) <= nine)
            ) {
                value = (value * 10) + (str.charCodeAt(cur++) - zero);
            }
            return sign * value;
        }
        
    The same idea, of course, applies in reverse.  Adding an integer to zero's
    character code gives you the character code for that integer's character,
    and a simple call to `String.fromCharCode` gets you the relevant character
    itself.
            
        function itoa(num) {
            var cur     = 1;
            var sign    = (num < 0)?-1:1;
            var str     = "";
            var zero    = '0'.charCodeAt(0);
            while (num) {
                str     = String.fromCharCode((num % 10)+zero)+str;
                num     = Math.floor(num/10);
            }
            return str;
        }

8.  __Reverse a string (in place?)__:  Ah, strings.  How exciting.  Reversing
    a string is, of course, trivial in JavaScript (`.reverse()`, anyone?), but
    that, of course, is probably not really the answer your interviewer is
    looking for.  "Ha, ha.", she'll say, "Now tell me how `.reverse()` works."
    
    The critical piece of information you need here is the ability to get at
    particular characters within a string, in order.  Of secondary importance
    is enough understanding of the algorithm to know when to _stop_ reversing,
    lest you inadvertently re-reverse the string before returning.
    
        function reverse_string(thestring) {
            var len     = thestring.length,
                last    = len-1,
                middle  = parseInt(len/2),
                newStr  = new Array();
            for (var i = 0; i < middle; i++) {
                newStr[last-i]  = thestring[i];
                newStr[i]       = thestring[last-i];
            }
            return newStr.join('');
        }
    
    My initial pass at the solution didn't use the `newStr` buffer array, 
    instead opting for a temp variable to facilitate a direct swap between
    `thestring[i]` and `thestring[last-i]`, but it seems that the array
    representation of a string in JavaScript is somehow distinct from the
    string itself.  I need to play around with this a little more, because I
    don't really understand that result (This is what happens when you spend
    your life using regular expressions to do every string manipulation you
    ever need).  In case you have some good ideas, here was my initial stab at
    things:
    
        function reverse_string(thestring) {
            var len     = thestring.length,
                last    = len-1,
                middle  = parseInt(len/2);
            for (var i = 0; i < middle; i++) {
                var temp            = thestring[i];
                thestring[i]        = thestring[last-i];
                thestring[last-i]   = temp;
            }
            return thestring;
        }
    
These questions are all pretty straightforward evaluations that would probably
be appropriate for a phone interview.  I'd expect questions in a real, live
technical interview to be a little deeper, and a little more impossible to 
"correctly" solve off the top of your head.  I'll be sifting through a few of
the puzzles at [techInterview][] in a valiant attempt to get my brain wrapped
around itself in such a way as to make the "Ah ha!" moments for puzzles like 
[Switches][].  [Joel Spolsky's article I linked yesterday][joel] also has good
advice for the "impossible questions" interviewers seem to love.

So.  How about you?  What are your "critical" interview questions, what
information do they look for, and how would you answer them?
                
[yesterday]: http://mikewest.org/archive/articles-about-interviewing "Mike West: 'Articles about Interviewing'"
[fib]: http://en.wikipedia.org/wiki/Fibonacci_number "Wikipedia: 'Fibonacci Number'"
[bitwise]: http://www.easy-designs.net/articles/theBitwiseOperator/ "Dave Stewart: 'Get a Speed Boost from the Bitwise Operator'"
[binary]: http://en.wikipedia.org/wiki/Binary_search "Wikipedia: 'Binary Search Algorithm'"
[atoi]: http://en.wikipedia.org/wiki/Atoi "Wikipedia: 'atoi'"
[itoa]: http://en.wikipedia.org/wiki/Itoa "Wikipedia: 'itoa'"
[techInterview]: http://www.techinterview.org/ "techInterview - puzzles and interview questions"
[Switches]: http://www.techinterview.org/puzzles/Switches.html "techInterview: 'Switches'"
[joel]: http://www.joelonsoftware.com/articles/fog0000000073.html "Joel Spolsky: 'The Guerrilla Guide to Interviewing'"
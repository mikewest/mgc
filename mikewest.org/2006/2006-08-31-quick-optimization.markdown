---
Alias:
- http://mikewest.org/blog/id/29
Modified: '2006-09-04T00:41:47Z'
Teaser: DOM calls are expensive; this article walks through one quick way to optimize
    them out of your code.
layout: post
tags:
- JavaScript
title: Quick Optimization
---
Accessing and manipulating the DOM is slow.  The speed of your JavaScript execution will very often depend entirely on the number, and the nature, of DOM calls that you make.  

For example, a common problem when writing unobtrusive JavaScript is to loop through a group of elements (say, each cell in a table), doing _something interesting_ to each in turn.  An initial pass at this code might look something like:

    var theTable    = document.getElementById('sought_after');
    var rows        = theTable.getElementsByTagName('tr');
    for (var rowNum=0;rowNum<rows.length;rowNum++) {
        var cells   = rows[rowNum].getElementsByTagName('td');
        for (var colNum=0;colNum<cells.length;colNum++) {
            var theValue = cells[colNum].innerHTML;
            
            //
            // do some processing here.
            //
        }
    }
    
The code's fine, and on small data sets, it'll run quickly enough.  That said, "quickly enough" is relative, and if the interesting something that you're doing to each cell takes much time, then you'll quickly find yourself running into performance problems.

One quick way to squeeze a few milliseconds of processing time is to avoid the expensive `getElementsByTagName` call inside the `rows` loop.  Instead of grabbing a list of the cells in each row as we pass, we can grab _all_ the cells, and process them as a flat array:

    var theTable    = document.getElementById('sought_after');
    var cells       = theTable.getElementsByTagName('td');
    for (var cellNum=0;cellNum<cells.length;cellNum++) {
        var theValue = cells[cellNum].innerHTML;
            
        //
        // do some processing here.
        //
    }

This code avoids the overhead of the internal `for` loop, and additionally replaces `rows.length` DOM calls with a single, larger call.  The performance increase is non-trivial (and it's even faster if you replace the `for` loop with the native `Array.forEach` method that newer versions of Firefox provide.  Take a look at Dean Edward's [Enumerating JavaScript Objects][foreach] for ideas in that regard).  The downside is that we no longer have access to the `rowNum` and `colNum` variables that were used in the initial algorithm.  If we want to do some calculations that require knowing where we are in our dataset, we'll run into problems.

[foreach]: http://dean.edwards.name/weblog/2006/07/enum/ "Dean Edwards: 'Enumerating JavaScript Objects'"

Simple arithmetic, however, can give us that information.  In essence, what we've done to our dataset is a transformation of a table that looks like:

    1   2   3   4   5
    6   7   8   9   10
    11  12  13  14  15
    
into an array that looks like:

    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15

If we know how many columns were in the original table (5), then we can use division and modulus to calculate the mapping between the cell array, and the position in the table:

    var numCols = 5;
    var colNum  = cellNum % numCols;
    var rowNum  = Math.floor(cellNum / numCols);
    
Of course, that requires a modulus, a division, and a call to `Math.floor`.  We can drop out the latter two in favour of a less-expensive `if` by simply incrementing `rowNum` at loop's end when `colNum` is equal to `numCols - 1`.  The whole thing, then, looks like:

    var theTable    = document.getElementById('sought_after');
    var numCols     = theTable.getElementsByTagName('tr')[0].childNodes.length;
    var cells       = theTable.getElementsByTagName('td');
    var rowNum      = 0;
    for (var cellNum=0;cellNum<cells.length;cellNum++) {
        var colNum = cellNum % numCols;

        //
        // do some processing here.
        //
        
        if (colNum == (numCols-1)) { rowNum++; }
    }
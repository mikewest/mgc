---
Alias:
- http://mikewest.org/blog/id/21
Modified: '2006-06-21T20:08:24Z'
Teaser: Your code can be faster!  Here are a few tips to help you speed up the toughest
    pieces of your JavaScript.
layout: post
tags:
- HOWTO
- JavaScript
title: Pimp My JavaScript &#8212; Duff&#8217;s Edition
---
I think we can all agree that JavaScript isn't exactly a speed demon.  It's wonderful at what it does (really), but it simply doesn't perform like we might want it to.  This is never more true than when we're trying to gather and process a lot of information from the DOM in the pursuit of some unobtrusive improvements to a website's UI.

Let's say that you're processing an HTML table, reading numeric data out of each cell to build a JavaScript array that you can work with later on.  A first pass at that system might look something like:
    
    var _data = [];
    
    var theTable = document.getElementById('table_id');
    
    var rows = theTable.getElementsByTagName('tr'); 
    for (rowNum = 0; rowNum < rows.length; rows++) {
        _data[rowNum] = [];
        var cols = rows[rowNum].getElementsByTagName('td');
        for (colNum = 0; colNum < cols.length; cols++) {
            _data[rowNum][colNum] = parseFloat(cols[colNum].innerHTML);
        }
    }

Great!  We've looped through all the rows and columns in order, and dumped the data into the `_data` array, and it went so fast we barely even noticed it working.  We're done!

Of course, if you're working with a data set of any significant size (say, 1000 rows and 10 columns), that code's going to eat up a huge chunk of the precious 5 seconds you've got before Firefox starts throwing "Unresponsive Script" warnings.  Over 5 runs, it averaged 2634 milliseconds to process a 1000x10 table of random numbers.  

With some clever scripting techniques, we'll shave almost a second off that time.  Doesn't sound like a whole lot, but it can easily be the difference between a site that holds a user's attention during processing, and one that drives them away with inadvertent errors.

We can bump up the speed with 3 specific improvements:

1.  Replace the repeated `getElementsByTagName('td')` calls with a more
    efficient algorithm.
2.  Use reversed `do...while` loops instead of `for` loops.
3.  Unroll the loops.

## Replace Repeated DOM Queries ##

The first rule of optimizing your code is to work "globally to locally", meaning that you should examine your overall architecture before you dive into loop unrolling and bit-shifting.   The most supercharged, pimped-out Pinto in the world is going to get beaten by a stock Ferrari, so make sure you've chosen the right vehicle before getting under the hood.

In this case, let's take a closer look at what we're doing with the DOM.  We know that DOM queries aren't very fast at all, and yet we're performing one to grab all the `TR` elements in the table, and then looping through each one and performing another query _every time_ to grab all the `TD` elements.  It's a logical enough way of getting our data, but it's really heavy on the DOM.

Instead of querying the DOM for each row's set of `TD`s, let's grab them all at once:

    var cells = theTable.getElementsByTagName('td');
    
This gives us a big, flat array of all the cells in our table.  What it doesn't give us is a clean way of figuring out where a cell is in terms of the table's columns and rows.  To make that happen, we'll first need to figure out how many rows and columns there are.  If we can get that information, we're just a simple modulus and division from mapping our array elements to positions in the table.

Happily, we can get the totals quite simply.  We get the total number of columns by examining the first cell's `parentNode` (a `TR` element), and asking it how many `TD` children it has:

    var totalCols   = cells[0].parentNode.getElementsByTagName('td').length;
    
And then we can calculate the number of rows by dividing the total number of cells we have by the total number of columns:

    var totalRows    = cells.length / totalCols;

All that's left is to map our flat array to the two-dimensional table structure.  This probably makes more sense visually, so, imagine a 5x5 table.  If we grab a flat array of all the cells in the table, the array indexes map onto the table as follows:

                col col col col col
                0   1   2   3   4
            ------------------------
            |
    row 0   |   0   1   2   3   4
    row 1   |   5   6   7   8   9
    row 2   |   10  11  12  13  14
    row 3   |   15  16  17  18  19
    row 4   |   20  21  22  23  24

The first 5 cells are in the first row, the next 5 cells are in the second row, etc.  This means that simply dividing the cell's index by the total number of columns and dropping the remainder will give us that cell's row index (e.g. cell 8 / 5 = 1.6, so it's in row #1).

Moreover, every 5th cell from the first is in the first column.  Every 5th cell from the second is in the second columns.  So taking the modulus of the cell index and the total number of columns gives us the column index (e.g. cell 8 % 5 = 3, so it's in col #3).

This means that we can rewrite our `for` loop as:
    
    for (rowNum = 0; rowNum < totalRows; rowNum++) {
        _data[rowNum] = [];
    }
        
    for (index=0; index<cells.length; index++) {
        _data[parseInt(index / totalCols)][index % totalCols] =
            parseFloat(cells[index].innerHTML);
    }

The initial `for` loop is required, since we're not able to create the row's array on the fly anymore (well, we could, but it would require an `if` inside the loop, and that'd be a bit slower than the extra `for` loop).

So our new algorithm looks like:


    var table = document.getElementById('theTable');
                
    cells        = table.getElementsByTagName('td');
    totalCols   = cells[0].parentNode.getElementsByTagName('td').length;
    totalRows    = cells.length/totalCols;

    for (rowNum = 0; rowNum < totalRows; rowNum++) {
        _data[rowNum] = [];
    }
    
    for (index=0; index<cells.length; index++) {
        _data[parseInt(index / totalCols)][index % totalCols] = parseFloat(cells[index].innerHTML);
    }
    
Let's see what else we can tweak...

## Reversed `for` Loops ##

Generally speaking, counting _down_ from the end of your loop is faster than counting _up_ from zero.  Apparently, comparing a number to zero is quicker than comparing a number to any other number, so this:

    for (i=length-1; i>=0; i--) {
        // something
    }

is generally going to execute faster than:

    for (i=0; i<length; i++) {
        // something
    }
    
It's a trivial change, but it can make a real difference in a long-running loop.

## Unrolling Loops ##

We can reduce the overhead of running through a loop by executing our code multiple times in one loop execution instead of just once, or [unrolling the loop][unroll].  A trivial example is something like:

    total = 0;
    for (i=0;i<100;i++) {
        total += i;
    }

turning into something like this:

    total = 0;
    for (i=0;i<100;i += 5) {
        total += i;
        total += i+1;
        total += i+2;
        total += i+3;
        total += i+4;
    }

We're doing 5 iterations of our code every time we go through the loop, so we avoid the `if` test at the top, as well as the increment.  This works really well, as long as you know that your loop is going to run an even multiple of 5 times.

What if you don't know ahead of time how many iterations you need to go through?  In that case, you need this article's namesake: [Duff's Device][duff].  It's a stunningly ugly (or beautiful, I suppose, if you're into crazy obsfucation) mechanism for unrolling a loop with an arbitrary number of iterations.  We can't implement the "`do...while` inside a `switch`" of the original, but we can come pretty close.  Our example above looks something like this, once Duffed:

    var i           = 0;
    var iterations  = 100;

    // first we take care of the remainder
    var counter     = iterations % 5;
    if (counter>0) {
        do {
            total += i++;
        } while (--counter);
    }
    
    // now we're evenly divisible
    counter = parseInt(iterations / 5);
    if (counter>0) {
        do {
            total += i++;
            total += i++;
            total += i++;
            total += i++;
            total += i++;
        } while (--counter);
    }
    
It's a little verbose, but I think it's fairly clear what's going on.  Let's apply this to our table parsing code, and see what we get.  We've got two loops, so we'll unroll both like so:

    var rowNum        = 0;
    var iterations    = totalRows;
    var counter        = iterations % 8;
    if (counter>0) {
        do {
            _data[rowNum++] = [];
        } while (--counter);
    }
    counter = parseInt(iterations / 8);
    if (counter>0) {
        do {
            _data[rowNum++] = [];
            _data[rowNum++] = [];
            _data[rowNum++] = [];
            _data[rowNum++] = [];
            _data[rowNum++] = [];
            _data[rowNum++] = [];
            _data[rowNum++] = [];
            _data[rowNum++] = [];
        } while (--counter);
    }

    var cellNum    = 0;
    iterations    = cells.length;
    counter        = iterations % 8;
    if (counter>0) {
        do {
            _data[parseInt(cellNum/totalCols)][cellNum%totalCols] = parseFloat(cells[cellNum++].innerHTML);
        } while (--counter);
    }
    n = parseInt(iterations / 8);
    if (counter>0) {
        do {
            _data[parseInt(cellNum/totalCols)][cellNum%totalCols] = parseFloat(cells[cellNum++].innerHTML);
            _data[parseInt(cellNum/totalCols)][cellNum%totalCols] = parseFloat(cells[cellNum++].innerHTML);
            _data[parseInt(cellNum/totalCols)][cellNum%totalCols] = parseFloat(cells[cellNum++].innerHTML);
            _data[parseInt(cellNum/totalCols)][cellNum%totalCols] = parseFloat(cells[cellNum++].innerHTML);
            _data[parseInt(cellNum/totalCols)][cellNum%totalCols] = parseFloat(cells[cellNum++].innerHTML);
            _data[parseInt(cellNum/totalCols)][cellNum%totalCols] = parseFloat(cells[cellNum++].innerHTML);
            _data[parseInt(cellNum/totalCols)][cellNum%totalCols] = parseFloat(cells[cellNum++].innerHTML);
            _data[parseInt(cellNum/totalCols)][cellNum%totalCols] = parseFloat(cells[cellNum++].innerHTML);
        } while (--counter);
    }
    
Over 5 runs, it averaged 1728 milliseconds to process a 1000x10 table of random numbers: a 44% improvement over the initial pass.  Nice work.  

There's probably more we could do to speed up the code.  Maybe there's a way of reading table data that I've missed.  

[unroll]: http://en.wikipedia.org/wiki/Loop_unrolling "Wikipedia: 'Loop Unrolling'"
[duff]: http://en.wikipedia.org/wiki/Duff%27s_device "Wikipedia: 'Duff's Device'"
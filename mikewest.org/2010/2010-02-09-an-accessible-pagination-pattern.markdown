---
layout: post
title:  "An Accessible Pagination Pattern"
Teaser: "Pagination is a basic building block of the web, but it's often implemented with markup that makes it less accessible than it ought to be.  Here, I've outlined my preferred solution to the problem."
tags:
    -   html
    -   accessibility
    -   aria
    -   a11y
    -   markup
    -   pagination
    -   paging
    -   patterns
    -   flickr
    -   cnn

---
Pagination is a basic building block of the web, appearing practically everywhere content is displayed.  From a UI perspective, a pagination widget generally ends up being presented in a very straightforward manner as a horizontal list of links, framed by "previous" and "next" links to give the user clear calls to action.  Flickr and CNN provide good examples of this general pattern:

![Pagination widgets on Flickr and CNN](/static_content/2010-02-pagination-pattern.png)

Flickr marks this up as a flat series of `a` tags inside a `div`, CNN as a `ul`, containing one `li` for each page.  And those certainly aren't the only options: while doing a bit of research for a project at work, I came across a much wider than expected variety of markup, and no clear "best practice."

After thinking about it a bit, and grilling my more intelligent friends, I've settled on a pattern that I think works pretty well.  It's nothing at all groundbreaking, but is certainly worth documenting as a markup pattern I'd advocate.  The HTML is straightforward (and an [example][] is available):

    <p id="paginglabel" class="audible">Pagination</p>
    <ul role="navigation" aria-labelledby="paginglabel">
        <li><a href="#"><span class="audible">%TYPE% Page</span>1</a></li>
        <li><a href="#" rel="prev"><span class="prev">Previous<span class="audible">: %TYPE% Page</span></span>2</a></li>
        <li><p><span class="audible">You're currently reading %TYPE% page </span>3</p></li>
        <li><a href="#" rel="next"><span class="next">Next<span class="audible">: %TYPE% Page</span></span>4</a></li>
        <li><a href="#"><span class="audible">%TYPE% Page </span>5</a></li>
    </ul>

I see a few advantages to this markup:

1.  **Clear signposting**
    
    The widget uses the [`aria-labelledby` attribute][labelledby] to instruct
    capable browsers to use the contents of the preceding paragraph as a
    label, and the [`role` attribute][role] to demarcate the `ul` as a
    navigation landmark on the page.
    
    These are especially important for visitors making use of screenreaders or 
    other assistive technologies, as they typically have the option of 
    navigating through a page's content by jumping directly from one list to 
    the next, or from one landmark to the next.  In such a scenario, the label 
    and role will be announced before reading the contents of the list, 
    providing essential information about its context and purpose which would 
    otherwise be lacking.
    
    Likewise, the previous and next pages are given [`rel` attributes][rel],
    making their relationship to the current page crystal clear, and available 
    to any capable parser.

2.  **Clear link text**
    
    A link containing only the text "1" is more or less useless to a visitor
    who can't visually link the text to it's context.  Adding that context is
    simply done, however, by placing some additional text inside the link.  An 
    addition as trivial as "Page 1" makes a huge difference in comprehension.
    This text can be hidden for sighted users by wrapping it in a `span`, and
    [positioning it offscreen][offscreen] via CSS.  The current page is called 
    out in the same way, providing the visitor with additional context.

3.  **Deduplication**
    
    CNN and Flickr made the same choice when marking up the widget's "Previous"
    and "Next" links.  Even though these both link off to items which are also
    available in the list, the link has been duplicated, breaking the
    relationship between the visible page number, and the textual label.  I'd
    argue that it's better to group the two into the same `a` element, using one
    link for both elements.
    
    The markup above does just that, placing the textual labels inside the link
    element itself, making it clear that the previous page is page 2.  The
    presentation of the "previous" and "next" links to the left and right of
    the list, respectively, can be handled by positioning their containing
    `span`s absolutely.  This requires approximate knowledge of the text's
    size, and can usually be accommodated even in multi-language environments.

4.  **Sound over Semantics**
    
    For pagination, it seems like it would make perfect sense to use an ordered
    list rather than the unordered list I've chosen here.  It's almost
    certainly semantically correct, as the list of pages is indeed ordered, and
    that order is indeed meaningful.
    
    In this case, however, I think it's the wrong choice.  [NVDA][] (which is
    the only screen reader I have access to at the moment) reads ordered lists
    as "One.  [List item content]  Two.  [List item content] ..."  An unordered
    list, on the other hand, doesn't number the items as they're read. Since I'm
    explicitly including the page number in the link, an `ol` simply sounds
    strange and repetitive: "One.  Example Page one. Link.  Two. Example page
    two. Link. ..."  Assuming other readers like [Jaws][] and [WindowEyes][]
    behave similarly, an unordered list simply _sounds_ better.
    
    _(Thanks to [Gareth][] for the good [question][] that I'd neglected to
    address.)_

I've put together a [quick example of this markup at work][example].  I hope you
reach for it next time you need a pagination widget.

[rel]: http://www.w3.org/TR/REC-html40/struct/links.html#h-12.1.2
[labelledby]:   http://www.w3.org/TR/2009/WD-wai-aria-20091215/states_and_properties#aria-labelledby
[role]: http://www.paciellogroup.com/blog/?p=106
[offscreen]: http://accessibilitytips.com/2008/03/05/avoiding-visibility-hidden/
[example]: /static_content/2010-02-pagination-pattern.html
[NVDA]: http://www.nvda-project.org/
[Jaws]: http://www.freedomscientific.com/products/fs/jaws-product-page.asp
[WindowEyes]: http://www.gwmicro.com/Window-Eyes/
[Gareth]: http://morethanseven.net/
[question]: http://twitter.com/garethr/status/9292593418

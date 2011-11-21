---
layout: post
title: "GDD Keynote: The HTML5 Demos"
tags:
  - gdd
  - gddde
  - gdd11
  - keynote
  - demos
  - webgl
  - svg
  - d3
  - mrdoob
  - fluxslider
  - css3
  - webaudio
  - mikebostock
  - joelambert
---
I had the opportunity to present a few demos during the Chrome section of 
Saturday's Google Developer Day in Berlin (which, incidentally, was a blast).
I expect a video to go up at some point in the vaguely near future, but, since
I got more than a few questions about it, I'll throw the links up here with a
bit of background and credit for each.

* The [first demo][demo1] was pulled from a talk [Mike Bostock][bostock] gave
  just last week, highlighting the power of the impressive [D3.js][d3]. D3 is a
  free JavaScript library that makes it easy to bind data to a DOM, and then
  generate stunning visualizations based on those bindings. His [entire
  presentation][pres1] is well worth checking out, and really highlight what an
  often overlooked technology like SVG is capable of.

[demo1]: http://mbostock.github.com/d3/talk/20111116/transitions.html
[bostock]: http://bost.ocks.org/mike/
[d3]: http://mbostock.github.com/d3/
[pres1]: http://mbostock.github.com/d3/talk/20111116/#0

* Next, I pulled out an oldie-but-goodie: [Joe Lambert's][joe] [Flux
  Slider][flux]. It's a quick demonstration of the power of CSS-based
  transitions, and really well suited to venues like GDD, as it makes the
  capabilities of modern browsers immediately visually apparent. If you haven't
  seen it yet, take a look. It's another open-source library, so fiddle with
  [the code][code] as well.

[joe]: http://blog.joelambert.co.uk/
[flux]: http://www.joelambert.co.uk/flux/transgallery.html
[code]: https://github.com/joelambert/Flux-Slider/tree/master/js/src

* Obviously, no HTML5 demo is complete without WebGL, and no WebGL demo is
  complete without [Mr.doob][mr] and [three.js][three]. I introduced the topic
  by throwing a [huge, Kinect-driven Mr.doob][kinect] onto the wall behind me.
  <img src="https://lh5.googleusercontent.com/-us34i7oWZ-o/Tsd3OkzyuiI/AAAAAAAAHhI/EMzADuFJMik/s640/IMG_20111119_103025.jpg" alt="">
  I followed up the introduction with a [beautiful terrain rendering][terrain]
  from [AlteredQualia][altered]. What I liked most about that demo is the fact
  they they've pulled pieces from the [ro.me][rome] project to save time and
  effort. Open source is brilliant.

[mr]: http://mrdoob.com/
[three]: http://mrdoob.github.com/three.js/
[kinect]: http://mrdoob.com/lab/javascript/webgl/kinect/
[terrain]: http://alteredqualia.com/three/examples/webgl_terrain_dynamic.html
[altered]: http://alteredqualia.com/
[rome]: http://ro.me/

* Finally, I pulled the [HTML5 Wow Visualizer][viz] from [Eric][e] and
  [Arne][a]'s excellent [I/O 2011 presentation][wow]. It's still the best
  WebAudio API demo out there, clearly demonstrating the power of the analyzer
  and showing off things that simply aren't possible with the `audio` tag.

[viz]: http://www.htmlfivewow.com/demos/audio-visualizer/index.html
[e]: https://plus.sandbox.google.com/118075919496626375791/
[a]: http://blog.roomanna.com/
[wow]: http://www.htmlfivewow.com/

And that's it. Fiveish quick demos in about five minutes. I enjoyed it! What did
you think?

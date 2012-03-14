/**
 * @fileoverview This file implementes the SlideController object, which
 * wraps a DOM element with logic that makes an otherwise flat page appear
 * to be a cleverly designed presentation.
 */

/**
 * Given an element on the page, handles user input to scroll through a set
 * of slides, adjusting the browser history correctly, and doing clever
 * things with simple transitions along the way.
 *
 * @param {string} id The ID of the DOM element at the root of the slides.
 * @constructor
 */
function SlideController(id) {
  this.id_ = id;
  this.title_ = document.title,
  this.root_ = document.getElementById(id);
  this.slides_ = document.querySelectorAll('#' + id + ' > section, ' +
                                           '#' + id + ' > header, ' +
                                           '#' + id + ' > aside, ' +
                                           '#' + id + ' > h2, ' +
                                           '#' + id + ' > figure, ' +
                                           '#' + id + ' > footer');
  this.HASH_REGEX = RegExp(this.HASH_PREFIX + '([0-9]+)' );
  this.init_();
}

/**
 * The keyCodes that we're interested in, mapped to meaningful names.
 *
 * @enum {number}
 */
SlideController.KeyCodes = {
  SPACE: 32,        // Next slide.
  PAGE_UP: 33,      // Previous slide.
  PAGE_DOWN: 34,    // Next slide.
  LEFT_ARROW: 37,   // Previous slide.
  RIGHT_ARROW: 39,  // Next slide.
  UPPERCASE_B: 66   // This is the only other button on my remote: It ought
                    // to blank the screen.
};

SlideController.prototype = {
  /**
   * The prefix added to the hash value at the end of the URL as the 
   * user navigates through the presentation.
   *
   * @type {!string}
   */
  HASH_PREFIX: '#slide-',

  /**
   * Are all the slides hidden (perhaps in response to a user pressing
   * "hide all" on his remote?)
   *
   * @type {!boolean}
   * @private
   */
  allHidden_: false,

  /**
   * The index of the currently visible slide.
   *
   * @type {number}
   * @private
   */
  current_: 0,

  /**
   * The ID of a currently-running timer.
   *
   * @type {number}
   * @private
   */
  timer_: 0,

  /**
   * @return {!number} The number of slides that can be scrolled through.
   */
  get length() {
    return this.slides_.length;
  },

  /**
   * @return {!string} The page title appropriate for the current slide.
   */
  get title() {
    return this.title_ +  " -- Slide #" + this.current;
  },

  /**
   * @return {!number} The current slide's index.
   */
  get current() {
    return this.current_;
  },

  /**
   * We push one or two things out-of-band in order to keep the slide
   * transitions smooth. This setter encapsulates the timer logic, ensuring
   * that only one timer is running, and that previous timers are cancelled.
   *
   * @param {!number} num The ID of the timer that's been generated.
   */
  set timer(num) {
    if (this.timer_)
      clearTimeout(this.timer_);

    this.timer_ = num;
  },

  /**
   * This setter has side effects, and in fact drives most of the page's
   * logic. When an index is set, that slide's `aria-hidden` attribute is
   * set to `false`, and the previously current slide's attribute to `true`.
   * Additionally, the URL is updated, as well as the page's title, and   *
   * `focus` is placed upon the newly visible slide.
   *
   * @param {!number} num The index of the current slide.
   */
  set current(num) {
    // Hide the currently displayed slide, and remove the currently previous
    // slide's class.
    if (this.current !== null && this.current !== num)
      this.slides_[this.current].setAttribute('aria-hidden', 'true');
    if (this.current !== null && this.current - 1 >= 0)
      this.slides_[this.current - 1].classList.remove('previous');

    if (num >= 0 && num < this.length) {
      this.current_ = num;
      document.title = this.title;
      // Push the URL update out a few seconds to avoid 
      this.timer = setTimeout(function () {
        history.pushState(
            this.current,
            'Slide ' + this.current, '#slide-' + this.current);
      }.bind(this), 2000);
    }

    // Show the current slide
    this.slides_[this.current].setAttribute('aria-hidden', 'false');
    this.slides_[this.current].classList.remove('next');

    // Set the previous and next slides
    if (this.current + 1 < this.length)
      this.slides_[this.current + 1].classList.add('next');
    if (this.current - 1 >= 0)
      this.slides_[this.current - 1].classList.add('previous');

    // Move focus to the current slide
    this.slides_[this.current].focus();
  },

  /**
   * @return {!boolean} Are all the slides hidden?
   */
  get allHidden() {
    return this.allHidden_;
  },

  /**
   * @param {!boolean} val Should all slides be hidden?
   */
  set allHidden(val) {
    this.allHidden_ = val;
    this.slides_[this.current].
        setAttribute('aria-hidden', val ? 'true' : 'false');
  },

  /**
   * Advances to the next slide, if there is a next slide.
   *
   * @return {!boolean} True if there was a next slide, false if we're
   *     already at the end.
   */
  next: function() {
    if (this.current < this.length) {
      if (!this.buildNextItem_())
        this.current++;
      return true;
    }
    return false;
  },

  /**
   * Retreats to the previous slide, if there is a previous slide.
   *
   * @return {!boolean} True if there was a previous slide, false if we're
   *     already at the beginning.
   */
  prev: function() {
    if (this.current > 0) {
      this.current--;
      return true;
    }
    return false;
  },

  /**
   * Kicks things off by hiding all slides, then determines which slide
   * should be shown by either reading it from the hash value, or 
   * defaulting to the first element. After displaying the correct item,
   * event handlers are bound for keyboard/back-button navigation.
   *
   * @private
   */
  init_: function () {
    for (i=0; i < this.slides_.length; i++)
      this.slides_[i].setAttribute('aria-hidden', 'true'); 

    var match = this.HASH_REGEX.exec(window.location.hash);
    if (match && !isNaN(parseInt(match[1], 10)))
      this.current = parseInt(match[1], 10);
    else
      this.current = 0;

    this.markBuilds_();
    this.bindHandlers_();
  },

  /**
   * Adds `to-build` class to all items on the page with a `build` class, so
   * that it can be removed for dramatic effect.
   *
   * @private
   */
  markBuilds_: function () {
    var b = document.querySelectorAll('.build');
    for (var i = 0; i < b.length; i++) {
      b[i].classList.remove('build');
      b[i].classList.add('to-build');
    }
  },

  /**
   * If the current slide contains an item waiting to be built, build it and
   * return the item built. Otherwise return null.
   *
   * @return {Element}
   * @private
   */
  buildNextItem_: function () {
    var b = this.slides_[this.current].querySelector('.to-build');
    if (b) {
      b.classList.remove('to-build');
      b.classList.add('built');
      if (!this.slides_[this.current].querySelector('.to-build')) {
        this.slides_[this.current].classList.add('fully-built');
      }
      return b;
    }
    return null;
  },

  /**
   * Binds event handlers for keyboard/back-button navigation: left-arrow
   * and page-up both take me to the previous slide. Right-arrow, page-down,
   * and space all take me to the next slide. Uppercase B hides all slides,
   * focusing everyone's attention on whatever it is that you'd like to say.
   *
   * @private
   */
  bindHandlers_: function () {
    document.addEventListener(
        'keydown',
        (function (e) {
          switch (e.keyCode) {
            case SlideController.KeyCodes.PAGE_UP:
            case SlideController.KeyCodes.LEFT_ARROW:
              this.prev();
              break;

            case SlideController.KeyCodes.PAGE_DOWN:
            case SlideController.KeyCodes.RIGHT_ARROW:
            case SlideController.KeyCodes.SPACE:
              this.next();
              break;

            case SlideController.KeyCodes.UPPERCASE_B:
              this.allHidden = !this.allHidden;
              break;
          }
        }).bind(this),
        false);
    window.addEventListener(
        'popstate',
        (function (e) {
          if (e.state !== null)
            this.current = e.state;
        }).bind(this),
        false);
  }
};


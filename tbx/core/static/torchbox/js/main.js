// Load in required functions
$(document).ready(function() {
    tbx.heroImages();
    tbx.mobileMenu();
    tbx.loadMore();
    tbx.team();
    tbx.clipThru();
    tbx.scrollEvents();
    tbx.signUp();
    tbx.jobs();
});

var tbx = {

  // Hero image carousel/slider
  heroImages: function() {

    var $heroButton       = $( '.featured-case-studies li' ),
        $heroContainer    = $( '.home-hero' ),
        $heroList         = $( '.feature-images' ),
        $heroImage        = $( '.feature-image' ),
        activeClass       = 'active',
        initialLoad       = 'initial-load',
        currentItem       = null;    

      // On load we're forcing the second item to appear (via CSS)
      // but once the user interacts with the hero we need to 
      // revert this behaviour to default
      function resetHero() {
        $heroContainer.removeClass( initialLoad );
      }

      function hideHeroItems( $item ) {
        $heroButton.not( $item ).removeClass( activeClass );
        $heroImage.removeClass( activeClass );
      }

      function showHeroItem( $item ) {
        currentItem = $item.data( 'name' );
      
        // Set hover state on button/link            
        $item.addClass( activeClass );

        // Show corresponding image
        $heroList.find( '[data-name="' + currentItem + '"]' ).addClass( activeClass );      
      }

      // Reset but only on first hover
      $heroButton.one( 'mouseenter', function() {
        resetHero();
      });

      $heroButton.on( 'mouseenter', function() {
        hideHeroItems( $(this) );
        showHeroItem( $(this) );
      });
  },


  // Mobile menu functionality
  mobileMenu: function() {
    var $bleed            = $( '.bleed' ),
        $bleedItem        = $bleed.find( 'li' ),
        $menuButton       = $( '.menu-button' ),
        twist             = 'twist',
        bleedVisible      = 'visible out-animation',
        showItem          = 'show';

    function close() {

      $bleedItem.removeClass( showItem ); 
      $menuButton.removeClass( twist );

      setTimeout(function() {
        $bleed.removeClass( bleedVisible );
      }, 500);

    }

    function open( $item ) {

      // Open tray
      $bleed.addClass( bleedVisible )
      $menuButton.addClass( twist );

      // Fade in nav items
      $bleedItem.each(function() {
        $item = $(this);
        $item.addClass( showItem ); 
      });
    }

    $menuButton.click(function() {

      if ( $menuButton.hasClass( twist ) ) {
        close();
      } 

      else {
        open($(this));
      }

    });

    // Reset/close on resize
    $( window ).on( 'resize', function(){
        close();
    });
  },


  // 'Load more' functionality (show/hide)
  loadMore: function() {
    var $clients          = $( '.clients' ),
        $clientsButton    = $clients.find( 'button' ),
        $list             = $( '.clients ul' ),
        visible           = 'visible',
        moreLabel         = 'Load more',
        lessLabel         = 'Show less';

    $clientsButton.click(function() {

      var $clientsButton  = $(this);
      
      // If already open
      if ( $list.hasClass( visible ) ) {
        $list.removeClass( visible )

        setTimeout(function() {
          $clientsButton.html( moreLabel );
        }, 900);
      } 

      // If already closed
      else {
        $list.addClass( visible );

        setTimeout(function() {
            $clientsButton.html( lessLabel );
        }, 1300);
      }
    });
  },


  // Team filtering
  team: function() {

    var $textFilter   = $( '.js-text-view' ),
        $imageFilter  = $( '.js-image-view' ),
        $peopleList   = $( '.people-list' ),
        textView      = 'people-list--text',
        active        = 'active';

    $textFilter.on( 'click', function(){
      $( this ).addClass( active );
      $imageFilter.removeClass( active );
      $peopleList.addClass( textView );
    });

    $imageFilter.on( 'click', function(){
      $( this ).addClass( active );
      $textFilter.removeClass( active );
      $peopleList.removeClass( textView );
    });
  },


  // Scroll events
  scrollEvents: function() {
    if ( $( window ).width() > 768 ) {
      $( window ).on( 'scroll', function(){

          var $aboutText              = $( '.about-text' ), 
              $heroText               = $( '.hero-text' ),
              scrollTop               = $(window).scrollTop(),
              stopClass               = 'stop';

          // Stop hero text
          ( function() {
             if ( scrollTop >= 335 ) {
                 $heroText.addClass( stopClass );
             } else {
                 $heroText.removeClass( stopClass );
             }
          }());

          // Stop about text
          ( function() {
            if ( scrollTop >= 465 ) {
                $aboutText.addClass( stopClass );
            } else {
                $aboutText.removeClass( stopClass );
            }
          }());

          // Add padding as page is scrolled
          ( function() {
            var paddingStart          = 0,
                paddingStop           = 285,
                textContent           = $( '.js-text-content' ),
                offset                = Math.abs( $(document).scrollTop() + 60 ),
                paddingStop           = 340,
                paddingTop            = null;

            if ( textContent.length ) {
              
              if ( offset <= paddingStop ) {
                paddingTop = offset;
              }

              textContent.css({
                'paddingTop' : paddingTop,
              });
            }
          }());
       });
    }
  },


  // Clip Thru
  // https://github.com/salsita/jq-clipthru
  clipThru: function() {
    if ( $( '#tester-unique' ).length ) {
      $( '#tester-unique' ).clipthru({
        autoUpdate: true,
        autoUpdateInterval: 30
      });
    }
  },


  jobs: function() {
    if ( $( '.jobs-carousel' ).length ) {
      $('.jobs-carousel').each(function (index, item) {
        var carouselId = "carousel" + index;
        this.id = carouselId;

          $(this).slick({
            slide: '#' + carouselId + ' li',
            slidesToShow: 1,
            slidesToScroll: 1,
            slidesPerRow: 1,
            infinite: false,
            vertical: true,
            verticalSwiping: true
          });
      });

      /*
       * Check for window resize and reinitialise Slick
       * because it doens't calculate height correctly.
      */
      var resizeId;
      $(window).resize(function() {
        clearTimeout(resizeId);

        resizeId = setTimeout(function() {
          $('.jobs-carousel').slick('setPosition');
        }, 500);

      });
    }
  },


  // SignUp form
  signUp: function() {
    function bindSignUpFormPageForm(element) {
      $(element).on('submit', function(e) {
          e.preventDefault();
          e.stopImmediatePropagation();
          $(".sign-up-form-button").html("Submitting...");
          $.ajax({
            url: $(this).attr('action'),
            type: "POST",
            data: $(this).serialize(),
            success: function(data) {
              // Google Tag Manager voodoo
              window.dataLayer = window.dataLayer || [];
              window.dataLayer.push({
                  'event': 'formSubmissionSuccess',
                  'formId': 'sign-up-form'
              });
              // end voodoo
              $(".sign-up-form").html(data);
              $('.page-signupformpage form.sign-up-form').each(function() {
                  bindSignUpFormPageForm(this);
              });
            }
          });
      });
    }
  }
};

// OLD/NON-REFACTORED JS
// // hero hover on li change background image
// $('.featured-case-studies li:nth-child(1)').hover(
//     function() {
//         $('.home-hero').addClass('first-feature');
//     },
//     function() {
//         $('.home-hero').removeClass('first-feature');
//     }
// );

// $('.featured-case-studies li:nth-child(3)').hover(
//     function() {
//         $('.home-hero').addClass('third-feature');
//     },
//     function() {
//         $('.home-hero').removeClass('third-feature');
//     }
// );


// // hero hover on li change background image
// $('.featured-case-studies li:nth-child(1)').hover(
//     function() {
//         $('.home-hero').addClass('first-feature');
//     },
//     function() {
//         $('.home-hero').removeClass('first-feature');
//     }
// );

// $('.featured-case-studies li:nth-child(3)').hover(
//     function() {
//         $('.home-hero').addClass('third-feature');
//     },
//     function() {
//         $('.home-hero').removeClass('third-feature');
//     }
// );

// end redesign


//     var inOutState = function( trigger, target, speed ){

//         var $trigger    = $( trigger ),
//             inClass     = 'mouseEnter',
//             outClass    = 'mouseLeave',
//             resetClass  = 'reset',
//             speed       = speed ? speed : 500,
//             state        = {
//                 busy : false
//             }

//         $trigger.each(function(){

//             var $item    = $( this ),
//                 $target = $item.find( target );

//             $item.on( 'mouseenter', function(){
//                 if( state.busy ){ return false; };
//                 $target.addClass( inClass );
//             });

//             $item.on( 'mouseleave', function(){

//                 state.busy = true;
//                 $target.addClass( outClass );

//                 $target.removeClass( inClass );
//                 setTimeout(function(){
//                     $target.addClass( resetClass );
//                     $target.removeClass( outClass );
//                     setTimeout(function(){
//                         $target.removeClass( resetClass );
//                         setTimeout( function(){
//                             state.busy = false;
//                         }, 10);
//                     }, 5);
//                 }, speed)

//             });

//         });

//     };


//     inOutState( 'button', '.rule' );

// });

// $(function() {
//     var $window = $(window);
//     var breakpoints = {
//         medium: 'screen and (min-width: 45em)',
//         large: 'screen and (min-width: 96em)'
//     }

//     Harvey.attach(breakpoints.medium, {
//         on: function(){
//             $('body').addClass('breakpoint-medium');
//         },
//         off: function(){
//             $('body').removeClass('breakpoint-medium');
//         }
//     });
//     Harvey.attach(breakpoints.large, {
//         on: function(){
//             $('body').addClass('breakpoint-large');
//         },
//         off: function(){
//             $('body').removeClass('breakpoint-large');
//         }
//     });


//     // Scroll all anchor links
//     $('a[href*=#]:not([href=#])').click(function() {
//         if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {

//             var target = $(this.hash);
//             target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
//             if (target.length) {
//                 $('html,body').animate({
//                     scrollTop: target.offset().top
//                 }, 1000);
//                 return false;
//             }
//         }
//     });

//     // Menu toggle
//     $(".menu-button").click(function() {
//         $('nav ul').toggleClass('visible');
//     });

//     // Share hide
//     $(".share a").click(function() {
//         $('.share ul').toggleClass('visible');
//     });

//     // News-letter PLAY toggle
//     $('.sign-up').on('click', function() {
//       $('.newsletter-wrapper-top').toggleClass('show');
//     });

//     // News-letter PLAY height container
//     $('.sign-up').on('click', function() {
//       $('header.container').toggleClass('taller');
//     });

//     // newsletter signup form
//     $('.newsletter-signup').on('submit', function(e) {
//         e.preventDefault();
//         $(".newsletter-button").html("Signing up...");
//         $(".newsletter-email").animate({
//             width: "0px"
//         });
//         $(".newsletter-email").hide("slow");
//         $.ajax({
//             url : $(this).attr('action'),
//             type: "GET",
//             data: $(this).serialize(),
//             success: function (data) {
//                 // Google Tag Manager voodoo
//                 window.dataLayer = window.dataLayer || [];
//                 window.dataLayer.push({
//                     'event' : 'formSubmissionSuccess',
//                     'formId' : 'newsletter-signup'
//                 });
//                 // end voodoo
//                 $(".newsletter-button").html("Thanks!");
//             }
//         });
//     });

//     // Google ad grant application form
//     $('.grant-application').on('submit', function(e) {
//         e.preventDefault();
//         e.stopImmediatePropagation();
//         $(".grant-application-button").html("Submitting...");
//         $.ajax({
//             url : $(this).attr('action'),
//             type: "POST",
//             data: $(this).serialize(),
//             success: function (data) {
//                 $(".grant-application").html(data);
//             }
//         });
//     });

//     $('.page-signupformpage form.sign-up-form').each(function() {
//         bindSignUpFormPageForm(this)
//     });

//     // main blur // Slows down the browser too much
//     //$('.sign-up').on('click', function() {
//     //  $('main').toggleClass('blur');
//    //});

//     // Dropdown menus for mobile
//     $('.dropdown').click(function() {
//         $('.dropdown').toggleClass('open');
//         $('.popular-tags .closed').slideToggle();
//     });
//     var querystring = window.location.search;
//     if ((querystring.indexOf('tag') > 0) && ($('.dropdown').css('display') == 'block')) {
//         $('.dropdown').addClass('open');
//         $('.popular-tags .closed').slideToggle();
//     }

//     // Sticky elements
//     $('.pick').each(function(){
//         var $stickyEl = $('.pick');
//         var elTop = $stickyEl.length && $stickyEl.offset().top - 4;

//         $stickyEl.toggleClass('fixed', $window.scrollTop() > elTop);

//         $window.scroll(function() {
//             $stickyEl.toggleClass('fixed', $window.scrollTop() > elTop);
//         });
//     });

//     $('.nextprev').each(function(){
//         var $stickyEl = $('.nextprev');
//         var elTop = $stickyEl.length && $stickyEl.offset().top - 10;

//         $stickyEl.toggleClass('sticky', $window.scrollTop() > elTop);

//         $window.scroll(function() {
//             $stickyEl.toggleClass('sticky', $window.scrollTop() > elTop);
//         });
//     });

//     // fitVids
//     $('.responsive-object').fitVids();

//     // get some stats about the video
//     $('.responsive-object').each(function() {
//         var $this = $(this);
//         var iframe = $('iframe', $this)[0];
//         var player = $f(iframe);

//         $(document).on('click tap', '.poster, .play', function(){
//             player.api('play');
//         });

//         player.addEvent('ready', function() {
//             player.addEvent('play', function(id){
//                 $('.play').hide();
//                 $('.breakpoint-medium header, .breakpoint-medium .hero-video h1').animate({
//                     opacity: 0,
//                 }, 500, function() {});
//                 $('.poster').fadeOut(300);
//                 ga('send', 'event', 'video', 'played', id);
//             });
//             player.addEvent('pause', function(id){
//                 $('header').animate({
//                     opacity: 1,
//                 }, 500, function() {});
//                 ga('send', 'event', 'video', 'paused', id);
//             });
//             player.addEvent('finish', function(id){
//                  $('header').animate({
//                     opacity: 1,
//                 }, 500, function() {});
//                 $('.poster').fadeIn(500);
//                 ga('send', 'event', 'video', 'finished', id);
//             });
//         });
//     });

//     //featherlight used for lightboxes in streamfield-enabled pages
//     $('.gallery').featherlightGallery();

//     $(function(){

//         var inOutState = function( trigger, target, speed ){

//             var $trigger    = $( trigger ),
//                 inClass     = 'mouseEnter',
//                 outClass    = 'mouseLeave',
//                 resetClass  = 'reset',
//                 speed       = speed ? speed : 500,
//                 state        = {
//                     busy : false
//                 }

//             $trigger.each(function(){

//                 var $item    = $( this ),
//                     $target = $item.find( target );

//                 $item.on( 'mouseenter', function(){
//                     if( state.busy ){ return false; };
//                     $target.addClass( inClass );
//                 });

//                 $item.on( 'mouseleave', function(){

//                     state.busy = true;
//                     $target.addClass( outClass );

//                     $target.removeClass( inClass );
//                     setTimeout(function(){
//                         $target.addClass( resetClass );
//                         $target.removeClass( outClass );
//                         setTimeout(function(){
//                             $target.removeClass( resetClass );
//                             setTimeout( function(){
//                                 state.busy = false;
//                             }, 10);
//                         }, 5);
//                     }, speed)

//                 });

//             });

//         };


//         inOutState( 'button', '.rule' );

//     });
// });
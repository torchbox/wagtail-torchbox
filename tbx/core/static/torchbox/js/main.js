/**
 * Type some JavaScript here and click either
 * fix or diff.
 */
// Sign up form page form
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

$(function() {

    // new for redesign

    // Add active to second mainstage item on load
    $(window).on('load', function() {
        $('.featured-case-studies li:nth-child(2)').addClass('active');
    });

    // hero hover on li change background image
    $('.featured-case-studies li:nth-child(1)').hover(
        function() {
            $('.home-hero').addClass('first-feature');
        },
        function() {
            $('.home-hero').removeClass('first-feature');
        }
    );

    $('.featured-case-studies li:nth-child(3)').hover(
        function() {
            $('.home-hero').addClass('third-feature');
        },
        function() {
            $('.home-hero').removeClass('third-feature');
        }
    );

    $('.menu-button').click(function() {
        $('.bleed').toggleClass('visible out-animation');
        $('.menu-button').toggleClass('twist');
    });

    // load more logos
    $('.clients button').click(function() {
        var $button = $(this);
        var $list   = $( '.clients ul' );
        var visible = 'visible';

        // If already open
        if ( $list.hasClass( visible ) ) {
          $list.removeClass( visible )

          setTimeout(function() {
            $button.html( 'Show more' );
          }, 900);
        } 

        // If closed
        else {
          $list.addClass( visible );

          setTimeout(function() {
              $button.html( 'Show less' );
          }, 1300);
        }
    });

        // load either desktop or mobile
        if ($(window).width() < 768) {
            // load on mobile
        }
        else {
            // load on desktop

           // clip thorugh
           // https://github.com/salsita/jq-clipthru
           $(document).ready(function() {
               $('#tester-unique').clipthru({
                   autoUpdate: true,
                   autoUpdateInterval: 30,
                   debug: true
               });
           });

           // stop work page title
           $(window).scroll(function() {
               var scroll = $(window).scrollTop();

               if (scroll >= 335) {
                   $(".hero-text").addClass("stop");
               } else {
                   $(".hero-text").removeClass("stop");
               }
           });

           // grow #work-content padding top on scroll
           $(window).bind('scroll', function(){
               var paddingStart = 0,
               paddingStop = 285,
               element = $('#work-content'),
               offset = $(document).scrollTop(),
               paddingTop = 340;

               if ( offset <= paddingStop ) {
                   paddingTop = (60+(offset));
               }

               element.css({
                'paddingTop' : paddingTop
               });
           });

        };

          // stop about page title
          $(window).scroll(function() {
              var scroll = $(window).scrollTop();

              if (scroll >= 465) {
                  $(".about-text").addClass("stop");
              } else {
                  $(".about-text").removeClass("stop");
              }
          });

           //grow #about-content padding top on scroll
           $(window).bind('scroll', function(){
               var paddingStart = 60,
               paddingStop = 300,
               element = $('#about-content'),
               offset = $(document).scrollTop(),
               paddingTop = 350;

               if ( offset <= paddingStop ) {
                   paddingTop = (60+(offset));
               }

               element.css({
               'paddingTop' : paddingTop
               });
           });

        // match height
        // $('.jobs li .content').matchHeight();

});

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
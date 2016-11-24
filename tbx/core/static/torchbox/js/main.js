// Load in required functions
$(document).ready(function() {
    tbx.onLoad();
    tbx.heroImages();
    tbx.mobileMenu();
    tbx.loadMore($('.clients'));
    tbx.loadMore($('.blog-listing'));
    tbx.jobs();
    tbx.scrollEvents();
    tbx.servicesScrollEvents();
    tbx.servicesAvatar();
    tbx.servicesCarousel();
    tbx.particles();
    tbx.newsletterSignUp();
});

var tbx = {

    onLoad: function() {
        
    },

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
            $header           = $( '.container-header' ),
            headerFixed       = 'container-header--fixed',
            twist             = 'twist',
            bleedVisible      = 'visible out-animation',
            showItem          = 'show';

        function close() {

            $( 'body' ).removeClass( 'menu-open' );
            $bleedItem.removeClass( showItem );
            $menuButton.removeClass( twist );
            $header.removeClass( headerFixed );

            setTimeout(function() {
                $bleed.removeClass( bleedVisible );
            }, 500);

        }

        function open( $item ) {

            // Open tray
            $bleed.addClass( bleedVisible );
            $menuButton.addClass( twist );

            // Fade in nav items
            $bleedItem.each(function() {
                $item = $(this);
                $item.addClass( showItem );
            });

            // Fix header
            // Delay for animation
            setTimeout(function() {
                $( 'body' ).addClass( 'menu-open' );
                $header.addClass( headerFixed );
            }, 300);
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
    loadMore: function($parent) {
        var $clients          = $parent,
            $button           = $parent.find( 'button' ),
            $list             = $parent.find( 'ul' ),
            visible           = 'visible',
            moreLabel         = 'Show more',
            lessLabel         = 'Show less';

        $button.click(function() {
            var $button  = $(this);

            // If already open
            if ( $list.hasClass( visible ) ) {
                $list.removeClass( visible )
                $button.html( moreLabel );
            }

            // If already closed
            else {
                $list.addClass( visible );
                $button.html( lessLabel );
            }
        });
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

    map: function() {

        var zoomMin         = 5,
            mapZoom         = null;
        markers         = [],

        // Define locations and labels
        locations       = [
            [51.858469, -1.480863, 'Oxford'],
            [51.454814, -2.597802, 'Bristol'],
            [39.950865, -75.145590, 'Philadelphia']
        ],

        // Define basic map options
        mapOptions = {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoom: 4,
            scrollwheel: false,
            styles: [{"featureType":"all","elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#000000"},{"lightness":40}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#000000"},{"lightness":16}]},{"featureType":"all","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"lightness":"69"}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":17},{"weight":1.2}]},{"featureType":"administrative.country","elementType":"geometry","stylers":[{"lightness":"35"}]},{"featureType":"administrative.country","elementType":"geometry.fill","stylers":[{"lightness":"1"}]},{"featureType":"administrative.province","elementType":"geometry.fill","stylers":[{"weight":"3.94"},{"lightness":"45"}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":21}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":16}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":19}]},{"featureType":"water","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":17}]}]

        },

        // Build map
        map = new google.maps.Map(document.getElementById( 'map' ), mapOptions);


        // Set up markers    
        function setMarkers(map, locations) {

            for (i = 0; i < locations.length; i++) {

                var lat             = locations[i][0],
                    long            = locations[i][1],
                    title           = locations[i][2],
                    markerLocation  = new google.maps.LatLng(lat, long),
                    infowindow      = new google.maps.InfoWindow(),
                    markerInfo      = '<div class="map-infobox">' + title + '</div>';

                // Create markers    
                var marker = new google.maps.Marker({
                    map:        map,
                    position:   markerLocation,
                    title:      title,
                    icon:       '{% static "torchbox/images/pin.png" %}'
                });

                // Add each marker to the markers array
                markers.push(marker);

                // Upon marker click, show info box
                google.maps.event.addListener( marker, 'click', ( function( marker, markerInfo, infowindow ) {
                    return function() {
                        infowindow.setContent( markerInfo );
                        infowindow.open( map, marker );
                    };
                })( marker, markerInfo, infowindow ));
            }
        }

        // Position map to display within bounds of the markers
        function positionMap(){

            var bounds = new google.maps.LatLngBounds();

            for (var i = 0; i < markers.length; i++) {
                bounds.extend(markers[i].getPosition());
            }

            map.fitBounds(bounds);
        }

        // Hide a single marker/list of markers
        // Refactor to pass location name
        function hideMarkers() {
            markers[1].setMap(null);
        }

        // Show all markers
        function showAllMarkers() {
            for (var i = 0; i < locations.length; i++) {    
                markers[i].setMap(map);
            }
        }

        // On user zoom change
        function zoomChange() {
            google.maps.event.addListener(map, 'zoom_changed', function() {

                mapZoom = map.getZoom();

                // When zoomed out
                if ( mapZoom < zoomMin ) {
                    hideMarkers();
                }

                // When zoomed in
                else {
                    showAllMarkers();
                }
            }); 
        }

        setMarkers(map, locations)
        hideMarkers();
        zoomChange();
        positionMap();

    },

    scrollEvents: function() {
        var $specifications     = $( '.specifications' );

        if ($specifications.length > 0) {
            var $client             = $( '.specifications .client' ),
                offset              = $specifications.offset().top,
                fixedClass          = 'specifications--fixed',
                showClient          = 'client--show';

            $( window ).on( 'scroll', function() {
                // Stick the specs bar
                if ( $( window ).scrollTop() >= offset ) {
                    $specifications.addClass( fixedClass );
                    $client.addClass( showClient )
                } 

                // Un-stick
                else {
                    $specifications.removeClass( fixedClass );
                    $client.removeClass( showClient )
                }  
            });
        }
    },

    servicesScrollEvents: function() {

        if ( $( '.js-services-inner' ).length ) {

            var $window         = $( window ),

            // Avatar
            $avatarContainer    = $( '.services-avatar-container' ),
            avatarClass         = 'services-avatar-container--fixed',
            avatarOffset        = $avatarContainer.offset().top - 40,

            // Reason list
            $reasonItem         = $( '.services-reasons-list__item' ),
            reasonClass         = 'services-reasons-list__item--show',

            // Process list
            $processItem        = $( '.services-grid__item--hidden' ),
            processClass        = 'services-grid__item--show',

            // Speeds
            delayDuration       = 200;

            $( window ).on( 'scroll', function() {

                // Stick avatar
                if ( $window.scrollTop() >= avatarOffset ) {
                    $avatarContainer.addClass( avatarClass );
                } else {
                    $avatarContainer.removeClass( avatarClass );
                } 

                // Fade in reasons
                // if ( $reasonItem.length ) {

                //     var reasonItemOffset = $reasonItem.offset().top - 650;

                //     if ( $window.scrollTop() >= reasonItemOffset ) {

                //         // Fade in each item with a delay
                //         $reasonItem.each( function(i) {
                //             var $item = $(this);

                //             setTimeout( function() {
                //                 $item.addClass( reasonClass );
                //             }, delayDuration * i );
                //         });
                //     }
                // }

                // Fade in process items
                if ( $processItem.length ) {

                    var processItemOffset   = $processItem.offset().top - 650,
                        processItemDefault  = $processItem.offset().top + 100;

                    if ( $window.scrollTop() >= processItemOffset ) {

                        // Fade in each item with a delay
                        $processItem.each( function(i) {
                            var $item = $(this);

                            setTimeout( function() {
                                $item.addClass( processClass );
                            }, delayDuration * i );
                        });
                    }

                    // Show/hide 'fly-in' CTA
                    if ( $window.scrollTop() >= processItemDefault ) {
                        $( '.services-avatar-container' ).removeClass( 'services-avatar-container--move-left' );
                    } else {
                        $( '.services-avatar-container' ).addClass( 'services-avatar-container--move-left' );
                    }
                }

            });
        }
    },

    servicesAvatar: function() {

            // Avatar containers
        var $avatar                 = $( '.services-avatar' ),
            $avatarContainer        = $( '.services-avatar-container' ),

            // Avatar components
            $avatarLink             = $( '.services-avatar-container__button' ),
            $avatarTitle            = $( '.services-avatar-container__find-out-more' ),
            $avatarInfo1            = $( '.services-avatar-container__contact-info' ),
            $avatarInfo2            = $( '.services-avatar-container__contact-details' ),

            // Avatar classes
            avatarInfo2Show         = 'services-avatar-container__contact-details--show',
            avatarTitleAlt          = 'services-avatar-container__find-out-more--alt',
            avatarContainerAlt      = 'services-avatar-container--alt',
            avatarContainerLeft     = 'services-avatar-container--move-left',
            avatarContainerHide     = 'services-avatar-container--hide',

            // Close avatar
            $closeButton            = $( '.services-avatar-container__close' );

        $avatar.on( 'mouseenter', function() {
            $avatarContainer.addClass( avatarContainerLeft );
        });

        $avatarLink.on( 'click', function() {
            $avatarTitle.addClass( avatarTitleAlt );
            $avatarTitle.text( 'Contact Will' );
            $avatarContainer.addClass( avatarContainerAlt );
            $avatarInfo1.hide();
            $avatarInfo2.addClass( avatarInfo2Show );
       });

        $closeButton.on( 'click', function() {
            $avatarContainer.addClass( avatarContainerHide );
        });
    },

    servicesCarousel: function() {

        if ( $( '.services-slider ul' ).length ) {
            $( '.services-slider ul' ).owlCarousel({
                loop: true,
                margin: 20,
                items: 1,
                autoplay: 5000,
                autoplayTimeout: 500000,
                slideSpeed: 500,
                paginationSpeed: 500,
                nav: true,
                responsive: {
                    0: {
                        items: 1
                    },
                    1100: {
                        items: 1,
                        stagePadding: 100
                    }   
                }
            });
        }
    },

    particles: function() {
        particlesJS("particles-js", {
          "particles": {
            "number": {
              "value": 50,
              "density": {
                "enable": true,
                "value_area": 800
              }
            },
            "color": {
              "value": "#ffffff"
            },
            "shape": {
              "type": "circle",
              "stroke": {
                "width": 0,
                "color": "#000000"
              },
              "polygon": {
                "nb_sides": 5
              },
            },
            "opacity": {
              "value": 0.9,
              "random": false,
              "anim": {
                "enable": false,
                "speed": 2,
                "opacity_min": 0.1,
                "sync": false
              }
            },
            "size": {
              "value": 2.5,
              "anim": {
                "enable": false,
                "speed": 50,
                "size_min": 0.1,
                "sync": false
              }
            },
            "line_linked": {
              "enable": true,
              "distance": 150,
              "color": "#ffffff",
              "opacity": 0.4,
              "width": 1
            },
            "move": {
              "enable": true,
              "speed": 2.5,
              "direction": "none",
              "random": false,
              "straight": false,
              "out_mode": "out",
              "bounce": false,
              "attract": {
                "enable": false,
                "rotateX": 600,
                "rotateY": 1200
              }
            }
          },
          "interactivity": {
            "detect_on": "canvas",
            "events": {
              "onclick": {
                "enable": true,
                "mode": "push"
              },
              "resize": true
            },
            "modes": {
              "grab": {
                "distance": 140,
                "line_linked": {
                  "opacity": 1
                }
              },
              "bubble": {
                "distance": 400,
                "size": 40,
                "duration": 2,
                "opacity": 8,
                "speed": 3
              },
              "repulse": {
                "distance": 200,
                "duration": 0.4
              },
              "push": {
                "particles_nb": 4
              },
              "remove": {
                "particles_nb": 2
              }
            }
          },
          "retina_detect": true
        });
    },

    // SignUp form
    signUp: function(element) {
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
                }
            });
        });
    },

    // Newsletter signup
    newsletterSignUp: function() {
        $('.newsletter-signup').on('submit', function(e) {
            e.preventDefault();
            $(".newsletter-button").html("Signing up...");
            $(".newsletter-email").animate({
                width: "0px"
            });
            $(".newsletter-email").hide("slow");
            $.ajax({
                url : $(this).attr('action'),
                type: "GET",
                data: $(this).serialize(),
                success: function (data) {
                    $(".newsletter-button").html("Thanks!");
                }
            });
        });
    }
};

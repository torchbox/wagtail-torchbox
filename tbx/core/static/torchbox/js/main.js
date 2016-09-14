// Load in required functions
$(document).ready(function() {
    tbx.heroImages();
    tbx.mobileMenu();
    tbx.loadMore();
    tbx.signUp();
    tbx.jobs();
    tbx.scrollEvents();
    tbx.newsletterSignUp();
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
    loadMore: function() {
        var $clients          = $( '.clients' ),
            $clientsButton    = $clients.find( 'button' ),
            $list             = $( '.clients ul' ),
            visible           = 'visible',
            moreLabel         = 'Show more',
            lessLabel         = 'Show less';

        $clientsButton.click(function() {

            var $clientsButton  = $(this);

            // If already open
            if ( $list.hasClass( visible ) ) {
                $list.removeClass( visible )
                $clientsButton.html( moreLabel );
            }

            // If already closed
            else {
                $list.addClass( visible );
                $clientsButton.html( lessLabel );
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

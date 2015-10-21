$(function() {

  $('.jobs-listing li > a').matchHeight();

  $('.jobs-carousel').each(function (index, item) {
    var carouselId = "carousel" + index;
    this.id = carouselId;
    $(this).slick({
      slide: '#' + carouselId + ' li',
      slidesToShow: 1,
      slidesToScroll: 1,
      slidesPerRow: 1,
      appendArrows: "#" + carouselId + " .slick-buttons",
      infinite: false,
      vertical: true,
      verticalSwiping: true
    });
  });
});


// On slide change.
$('.jobs-carousel').on('afterChange', function(event, slick, direction){
  // Move buttons to next slide.
  $('.jobs-carousel').find('.slick-buttons').css('opacity', 0).remove();
  $('.jobs-carousel .slick-active .slide-caption-container').append('<div class="slick-buttons"></div>');
  $('.jobs-carousel .slick-active .slide-caption-container .slick-buttons').css('opacity', 0);
  $('.jobs-carousel .slick-active .slide-caption-container .slick-buttons').animate({'opacity': 1}, 250);
  $('.jobs-carousel').slick('reinit');
});

/*
 * Check for window resize and reinitialise Slick
 * because it doens't calculate height correctly.
*/
var resizeId;
$(window).resize(function() {
  clearTimeout(resizeId);
  resizeId = setTimeout(function() {
    $('.jobs-carousel').slick('reinit');
  }, 500);
});

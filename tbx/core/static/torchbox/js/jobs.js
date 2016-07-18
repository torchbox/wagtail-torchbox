$(function() {

  // $('.jobs-listing li > a').matchHeight();

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

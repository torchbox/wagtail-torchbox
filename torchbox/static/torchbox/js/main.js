$(document).ready(function() {
    // Menu toggle
    $(".menu-button").click(function() {
        $('nav ul').toggleClass('visible');
    });

    // Share hide
    $(".share a").click(function() {
        $('.share ul').toggleClass('visible');
    });
    
    // fitVids
    $(".responsive-object").fitVids();
});

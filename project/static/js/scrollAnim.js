
$(document).ready(function() {
$(window).scroll(function() {
    var scroll = $(window).scrollTop();
    var mediaQuery = window.matchMedia('(min-width: 577px)');
    // Check if the screen size is larger than 576px (not a mobile device)
    if (mediaQuery.matches) {
    if (scroll > 200) {
        $("#topnav").css("background", "transparent");
    } else {
        $("#topnav").css("background", "rgb(29, 29, 29)");
    }
    }
});
});

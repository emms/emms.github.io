$(document).ready(function() {

    //smooth scrolling
    $('a[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top
                }, 1000, 'easeInOutExpo');
                return false;
            }
        }
    });


    //show hamburger menu when scrolled 100vh
    var $nav = $('.menu');
    var $win = $(window);
    var winH = $win.height(); // Get the window height.

    $win.on("scroll", function() {
        $nav.toggleClass("hidden", $(this).scrollTop() < winH);
    }).on("resize", function() { // If the user resizes the window
        winH = $(this).height(); // you'll need the new height value
    });

    $(".menu-link").click(function(e) {
        e.preventDefault();
        $(".menu").toggleClass("open");
        $(".menu-overlay").toggleClass("open");
    });

    $(".menu-overlay a").click(function(e) {
        $(".menu").toggleClass("open");
        $(".menu-overlay").toggleClass("open");
    });

});

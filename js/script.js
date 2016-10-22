$.backstretch("img/v2/bg_2.jpg", { centeredY: false });

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


    //show hamburger menu when scrolled 100vh but always on mobile
    var $nav = $('.menu');
    var $win = $(window);
    var winH = $win.height(); // Get the window height.
    var vinW = $win.width();

    var mobile = (vinW > 768) ? false : true;

    if (mobile) {
        $nav.removeClass("hidden");
    }

    $win.on("scroll", function() {
        if (!mobile) {
            $nav.toggleClass("hidden", $(this).scrollTop() < winH);
        } else {
            $nav.removeClass("hidden");
        }
    }).on("resize", function() { // If the user resizes the window
        winH = $(this).height(); // you'll need the new height value
        vinW = $(this).width();
        mobile = (vinW > 768) ? false : true;
        if (mobile) {
            $nav.removeClass("hidden");
        } else if ($(this).scrollTop() < winH){
            $nav.addClass("hidden");
        }
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

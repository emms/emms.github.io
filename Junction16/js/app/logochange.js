/*if (window.innerWidth > 480) {
    $(".main-logo").hover(
        function() {
            //if ($(".main-logo").css('opacity') === 1) {
            $(this).animate({
                opacity: 0
            });
            $('.buzz_wrapper').animate({
                opacity: 1
            });

            //}
        },
        function() {
            //if ($(":animated").length === 0) {
            $('.buzz_wrapper').animate({
                opacity: 0
            }).promise().done(function() {
                $(".main-logo").animate({
                    opacity: 1
                });
            });
            //}
        }
    );
}*/
/*
$(".buzz_wrapper").hover(
    function() {
        if ($(".buzz_wrapper").css('opacity') === 1) {
            $(this).animate({
                opacity: 0
            }).promise().done(function() {
                $('.main-logo').animate({
                    opacity: 1
                });
            });
        }
    },
    function() {
        if ($(":animated").length === 0) {
            $('.main-logo').animate({
                opacity: 0
            }).promise().done(function() {
                $(".buzz_wrapper").animate({
                    opacity: 1
                });
            });
        }
    }
);*/

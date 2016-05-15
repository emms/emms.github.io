$(document).ready(function() {

    var w = $(window).width(),
        h = $(window).height();
    $('#video-block').css({
        height: '' + h + '',
        width: '' + w + ''
    });

    var videoheight = parseInt($('#video-block').css('height')) + 50 + 'px';
    $('.dark-overlay').css('height', videoheight);

    $(window).resize(function() {
        var w = $(window).width(),
            h = $(window).height();
        $('#video-block').css({
            height: '' + h + '',
            width: '' + w + ''
        });

        var videoheight = parseInt($('#video-block').css('height')) + 50 + 'px';
        $('.dark-overlay').css('height', videoheight);
    });

});

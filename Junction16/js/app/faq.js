/*$('.faq-arrow').on('click', function() {
    var $faqContainer = $(this).closest('.faq-container');
    var answerHeight = $faqContainer.find('.faq-a').css("height");
    var boxHeight = $faqContainer.find('.faq-box').css("height");
    var newHeight = parseFloat(answerHeight) + parseFloat(boxHeight) + 'px';
    if (!$faqContainer.hasClass('opened')) {
        $faqContainer.addClass('opened');
        $faqContainer.find('.faq-box').animate({
            height: newHeight
        }).promise().done(function() {
            $faqContainer.find('.faq-a').animate({
                opacity: 1
            });
        });
    } else {
        $faqContainer.removeClass('opened');
        $faqContainer.find('.faq-a').animate({
            opacity: 0
        }).promise().done(function() {
            $faqContainer.find('.faq-box').animate({
                height: parseFloat(boxHeight) - parseFloat(answerHeight) + 'px'
            });
        });
    }
});*/

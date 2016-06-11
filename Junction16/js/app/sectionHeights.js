 function sectionHeights() {
     var sectionHeight = parseInt($('.text-content').outerHeight(true)) + 'px';
     $('.section-img').css('height', sectionHeight);
     console.log(sectionHeight);
 }

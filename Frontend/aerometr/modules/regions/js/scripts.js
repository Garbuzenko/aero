$('body').on('change', '.jsChangeSelect', function() {
   var btn = $(this).attr('data-btn');
   $('.jsSearchSelect').attr('placeholder','Поиск региона');
   $('.jsSearchSelectSvg').remove();
   $('#'+btn).click();
});
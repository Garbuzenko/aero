$('body').on('click', '.jsDelReportBtn', function() {
        var t = $(this);
        
        var inputId = t.attr('data-id');
        var value = t.attr('data-value');
        var btn = t.attr('data-btn');
        
        $('#'+inputId).val(value);
        $('#jsRemoveElement').val('jsDelReportTr'+value);
        $('#'+btn).click(); 
});
function initializeDataTable() {
    if ($.fn.DataTable.isDataTable('#ecommerce-list')) {
        $('#ecommerce-list').DataTable().destroy();
    }
    
    ecommerceList = $('#ecommerce-list').DataTable({
    headerCallback:function(e, a, t, n, s) {
                e.getElementsByTagName("th")[0].innerHTML=`#`
   },
   "dom": "<'dt--top-section'<'row'<'col-12 col-sm-6 d-flex justify-content-sm-start justify-content-center'l><'col-12 col-sm-6 d-flex justify-content-sm-end justify-content-center mt-sm-0 mt-3'f>>>" +
   "<'table-responsive'tr>" +
   "<'dt--bottom-section d-sm-flex justify-content-sm-between text-center'<'dt--pages-count  mb-sm-0 mb-3'i><'dt--pagination'p>>",
     "oLanguage": {
     "oPaginate": { "sPrevious": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-left"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>', "sNext": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-right"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>' },
     "sInfo": "Страница _PAGE_ из _PAGES_",
     "sSearch": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-search"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
     "sSearchPlaceholder": "Поиск...",
     "sLengthMenu": "Топ :  _MENU_",
   },
   "stripeClasses": [],
   "lengthMenu": [10, 20, 30, 40, 50,100],
   "pageLength": 10 
 });
}
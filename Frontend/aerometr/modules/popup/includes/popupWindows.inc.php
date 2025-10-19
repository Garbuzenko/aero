<!--------------------------------------------------- Затемнение экрана --------------------------------------------------------->
<div id="opaco" class="text-center hidden">
<div class="containerLoader">
  <div class="cloud front">
    <span class="left-front"></span>
    <span class="right-front"></span>
  </div>
  <span class="sun sunshine"></span>
  <span class="sun"></span>
  <div class="cloud back">
    <span class="left-back"></span>
    <span class="right-back"></span>
  </div>
</div>
</div>
<!------------------------------------------------------------------------------------------------------------------------------->

<!---------------------------------------------------- Всплывающее окно --------------------------------------------------------->
<div class="modal" id="jsPopupWindow" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="jsPopupWindowTitle"></h5>
                <button type="button" class="btn-close jsClosePopupWindow">
                  <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>
            <div class="modal-body" id="jsPopupWindowSubDiv">
                
            </div>
            <div class="modal-footer">
                <!--<button class="btn btn btn-light-dark jsClosePopupWindow" data-bs-dismiss="modal"><i class="flaticon-cancel-12"></i> Закрыть</button>-->
                <button type="button" class="btn btn-primary jsClosePopupWindow">Закрыть</button>
            </div>
        </div>
    </div>
</div>
<!------------------------------------------------------------------------------------------------------------------------------->
<div class="row layout-top-spacing">
  <div class="col-xxl-12 col-xl-12 col-lg-12 col-md-12 col-sm-12 mb-4">
     <div class="single-post-content">
        <div class="post-content">
           <h4><?=$modArr[$component]['h1'];?></h4>
           <p><?=$modArr[$component]['descr'];?></p>
                                    
           <hr class="my-2">
           <h4 class="my-4">Базовый URL</h4>

             <div class="code-section-container show-code">
               <div class="code-section text-left fs-6">
                  <pre class="hljs xml" style="color: #fff !important;"><?=$modArr[$component]['baseUrl'];?></pre>
               </div>
             </div>

             <h4 class="mb-3 mt-5">Пример запроса</h4>

             <div class="code-section-container mb-3 show-code">
                <button class="btn toggle-code-snippet _effect--ripple waves-effect waves-light"><span>Code</span> <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down toggle-code-icon"><polyline points="6 9 12 15 18 9"></polyline></svg></button>

                <div class="code-section text-left">
                   <pre class="hljs xml"><?=$modArr[$component]['query'];?></pre>
                </div>
            </div>
            
            <form method="post" action="" id="form_jsGetQueryApi" class="mb-3">
              <input type="hidden" name="module" value="gis" />
              <input type="hidden" name="component" value="component" />
              <input type="hidden" name="api" value="<?=$component;?>" />
              <input type="hidden" name="callbackFunc" value="jsGetQueryAllApi" />
              <input type="hidden" name="alert" value="" />
              <input type="hidden" name="opaco" value="1" />
              <button class="send_form btn btn-primary" id="jsGetQueryApi">
                Выполнить запрос
              </button>
            </form>
            
            <div id="jsResultQuery" class="mt-2 hljs xml hidden" style="max-height: 400px; overflow-y: auto;"></div>

        </div>
                                
                                
        <div class="post-info">
                                    
        <hr>

      </div>
    </div>
  </div>
</div>
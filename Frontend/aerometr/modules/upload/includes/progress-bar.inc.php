<div id="jsProgressBarMessage" class="mt-3 mb-2">0% - загрузка файла на сервер</div>
<div id="jsProgressBarHtml" >
<div class="progress br-30">
  <div class="progress-bar bg-primary progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%"></div>
</div>
</div>
<script type="text/javascript">
  $(document).ready(function(){
     setInterval( function() {
       $.ajax({
        type: "GET",
        url: "https://aerometr.ru/upload/progress",
        cache: false,
        contentType: false,
        processData: false,
        success: function (data){
            if (data == '-1') {
                $('#jsEditUploadStatus').html('');
                return false;
            }
            var myArr = $.parseJSON(data);
            $('#jsProgressBarMessage').html(myArr['progress']);
            $('#jsProgressBarHtml').html('<div class="progress br-30"><div class="progress-bar bg-primary progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="'+myArr['percent']+'" aria-valuemin="0" aria-valuemax="100" style="width: '+myArr['percent']+'%"></div></div>'); 
            $('#uploadTerminal').append(myArr['terminal']);
            var block = document.getElementById('uploadTerminal');
            block.scrollTop = block.scrollHeight;
            
            if (myArr['percent'] == '100.00') {
                $('#jsEditUploadStatus').html('');
                return false;
            }
        }
      });       
     }, 3000 );
  });
</script>
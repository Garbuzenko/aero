<script>
 var block = document.getElementById('uploadTerminal');
 block.scrollTop = block.scrollHeight;
</script>

<!-- BEGIN PAGE LEVEL PLUGINS -->
<script src="<?=$xc['tmp_url'];?>/src/assets/js/scrollspyNav.js"></script>
<script src="<?=$xc['tmp_url'];?>/src/plugins/src/filepond/filepond.min.js"></script>
<script src="<?=$xc['tmp_url'];?>/src/plugins/src/filepond/FilePondPluginImageExifOrientation.min.js"></script>
<script src="<?=$xc['tmp_url'];?>/src/plugins/src/filepond/FilePondPluginImagePreview.min.js"></script>
<script src="<?=$xc['tmp_url'];?>/src/plugins/src/filepond/filepondPluginFileValidateSize.min.js"></script>

<!-- END PAGE LEVEL PLUGINS -->
<script>
FilePond.registerPlugin(
    FilePondPluginImagePreview,
    FilePondPluginImageExifOrientation,
    FilePondPluginFileValidateSize
);
  
var multifiles = FilePond.create(
   document.querySelector('.file-upload-multiple'),
   {
       // Кастомные тексты на русском языке
       labelIdle: 'Перетащите файлы сюда или <span class="filepond--label-action">нажмите для выбора</span>',
       labelInvalidField: 'Поле содержит недопустимые файлы',
       labelFileWaitingForSize: 'Расчет размера',
       labelFileSizeNotAvailable: 'Размер недоступен',
       labelFileLoading: 'Загрузка',
       labelFileLoadError: 'Ошибка при загрузке',
       labelFileProcessing: 'Загрузка на сервер',
       labelFileProcessingComplete: 'Загрузка завершена',
       labelFileProcessingAborted: 'Загрузка отменена',
       labelFileProcessingError: 'Ошибка при загрузке',
       labelFileProcessingRevertError: 'Ошибка при отмене',
       labelFileRemoveError: 'Ошибка при удалении',
       labelTapToCancel: 'Нажмите для отмены',
       labelTapToRetry: 'Нажмите для повтора',
       labelTapToUndo: 'Нажмите для отмены',
       labelButtonRemoveItem: 'Удалить',
       labelButtonAbortItemLoad: 'Отменить',
       labelButtonRetryItemLoad: 'Повторить',
       labelButtonAbortItemProcessing: 'Отменить',
       labelButtonUndoItemProcessing: 'Отменить',
       labelButtonRetryItemProcessing: 'Повторить',
       labelButtonProcessItem: 'Загрузить'
   }
);
</script>
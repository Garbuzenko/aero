<?php defined('DOMAIN') or exit(header('Location: /'));

$xc['bread_crumbs'] = array(
  0 => array('anchor' => 'Загрузка файла', 'url' => '', 'status' => 1)
);

// вытаскиваем сообщения о последних загрузках
$lastUploads = db_query("SELECT * FROM log ORDER BY id DESC LIMIT 200");

if ($lastUploads != false) {
    $reversedArray = array_reverse($lastUploads);
}

$processedFiles = null;

$pf = db_query("SELECT * FROM processed_files ORDER BY id DESC");

if ($pf != false) {
    ob_start();
    include $_SERVER['DOCUMENT_ROOT'].'/modules/upload/includes/result.inc.php';
    $processedFiles = ob_get_clean();
}
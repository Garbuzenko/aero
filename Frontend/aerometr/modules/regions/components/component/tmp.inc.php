<?php defined('DOMAIN') or exit(header('Location: /'));?>

<?if (!empty($flightsStat)):?>
<button class="btn btn-success mt-3" onclick="captureFullPage('jsContent','#060818','<?=$title;?>')">Скачать графики</button>
<div class="row layout-top-spacing">
<?=$regionStat;?>
</div>
<?endif;?>
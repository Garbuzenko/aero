<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, shrink-to-fit=no">
    <title><?=$xc['title'];?></title>
    <meta name="description" content="<?=$xc['description'];?>">
    <meta name="keywords" content="">
    
    <link rel="apple-touch-icon" sizes="180x180" href="<?=DOMAIN;?>/img/fav/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="<?=DOMAIN;?>/img/fav/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="<?=DOMAIN;?>/img/fav/favicon-16x16.png">
    <link rel="manifest" href="<?=DOMAIN;?>/img/fav/site.webmanifest">
    
    <link href="<?=$xc['tmp_url'];?>/layouts/vertical-dark-menu/css/light/loader.css" rel="stylesheet" type="text/css" />
    <link href="<?=$xc['tmp_url'];?>/layouts/vertical-dark-menu/css/dark/loader.css" rel="stylesheet" type="text/css" />
    <script src="<?=$xc['tmp_url'];?>/layouts/vertical-dark-menu/loader2.js"></script>
    
    <!-- BEGIN GLOBAL MANDATORY STYLES -->
    <link href="https://fonts.googleapis.com/css?family=Nunito:400,600,700" rel="stylesheet">
    <link href="<?=$xc['tmp_url'];?>/src/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <link href="<?=$xc['tmp_url'];?>/layouts/vertical-dark-menu/css/light/plugins.css" rel="stylesheet" type="text/css" />
    <link href="<?=$xc['tmp_url'];?>/layouts/vertical-dark-menu/css/dark/plugins.css" rel="stylesheet" type="text/css" />
    <link href="<?=$xc['tmp_url'];?>/src/assets/css/light/components/modal.css" rel="stylesheet" type="text/css" />
    <link href="<?=$xc['tmp_url'];?>/src/assets/css/dark/components/modal.css" rel="stylesheet" type="text/css" />
    <link href="<?=$xc['tmp_url'];?>/src/assets/css/light/forms/switches.css" rel="stylesheet" type="text/css" />
    <link href="<?=$xc['tmp_url'];?>/src/assets/css/dark/forms/switches.css" rel="stylesheet" type="text/css" />
    <!-- END GLOBAL MANDATORY STYLES -->

    <link rel="stylesheet" href="<?=DOMAIN;?>/css/<?=$xc['style'];?>" />
    <?=$xc['head'];?>
    
    <?if($xc['ya_map']==true):?>
    <script src="https://api-maps.yandex.ru/<?=$xc['yaMapsVer'];?>/?apikey=<?=YANDEX_API_KEY;?>&lang=ru_RU"></script>
    <?endif;?>
</head>

<body class="dark">

 <?if($xc['noMainTmp'] == false):?>
 <!-- BEGIN LOADER -->
 <div id="load_screen"> <div class="loader"> <div class="loader-content">
  <img src="<?=DOMAIN;?>/img/loader2.gif" />
 </div></div></div>
 <!--  END LOADER -->

   <?=$xc['header'];?>
   <!--  BEGIN MAIN CONTAINER  -->
    <div class="main-container" id="container">
       <div class="overlay"></div>
       <div class="search-overlay"></div>
       
       <?=$xc['menu'];?>
       
       <!--  BEGIN CONTENT AREA  -->
        <div id="content" class="main-content">
          <div class="layout-px-spacing">
            <div class="middle-content container-xxl p-0">
              <?require $_SERVER['DOCUMENT_ROOT'].'/modules/bread-crumbs/tmp.inc.php';?>
              <?=$xc['content']?>
            </div>
          </div>
          <?=$xc['footer'];?>
        </div>
        <!--  END CONTENT AREA  -->
    </div>
    <!-- END MAIN CONTAINER -->
   
<?else:?>
   
   <?=$xc['content']?>
   
<?endif;?>

<?=$xc['js'];?>
<?=$xc['body'];?>

<?=$xc['popup'];?>

<?if($xc['no_metrika']==false):?>
<?=$xc['counter'];?>
<?endif;?>


</body>
</html>
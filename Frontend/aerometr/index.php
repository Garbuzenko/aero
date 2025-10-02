<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

//date_default_timezone_set("UTC"); // Устанавливаем часовой пояс по Гринвичу
header('Content-Type: text/html; charset=utf-8'); // устанавливаем кодировку
setlocale(LC_ALL, 'ru_RU', 'ru_RU.UTF-8', 'ru', 'russian');
session_start();

require_once $_SERVER['DOCUMENT_ROOT'] . "/config.php";

// если идёт запрос на домен с www
if (preg_match('/www\./is', DOMAIN)) {
    $redirect = str_replace('www.', '', DOMAIN . $_SERVER['REQUEST_URI']);
    exit(header('Location: ' . $redirect));
}
// -----------------------------------------------------------------------------

require_once $_SERVER['DOCUMENT_ROOT'] . "/lib/db.php";
require_once $_SERVER['DOCUMENT_ROOT'] . "/lib/functions.php";

if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/popup/functions.php')) {
  include $_SERVER['DOCUMENT_ROOT'] . '/modules/popup/functions.php';
}

$xc['url'] = substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?') + 1);
parse_str($xc['url'], $xc['url']);

// для всплывающих окон, которые показываются сразу после загрузки страницы
$xc['message'] = null;

if (!empty($_COOKIE['message'])) {
    $xc['message'] = $_COOKIE['message'];
    setcookie("message", "", time() - 9999999, "/");
}
// ------------------------------------------------------------------------

// определение мобильного браузера
$xc['mobile'] = 0;
if (!empty($_SERVER['HTTP_USER_AGENT'])) {
    define('MOBILE', is_mobile($_SERVER['HTTP_USER_AGENT'])); //is_mobile($_SERVER['HTTP_USER_AGENT'])
  
    if (MOBILE == true) {
      $xc['mobile'] = 1;
    }
}
// ----------------------------------------------------------------------------------------------------------------------

// ----------------------------------------- Ajax запросы ---------------------------------------------------------------
if (isset($_POST['action']) && $_POST['action'] == 'ajax' && !empty($_POST['module'])) {
    
    $xc['module'] = clearData($_POST['module'], 'get');
    $xc['component'] = null;

    if (!empty($_POST['component']))
        $xc['component'] = 'components/' . clearData($_POST['component'], 'get') . '/';
    
    if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'ajax.php'))
        require_once $_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] .'ajax.php';

    exit();
}
// ----------------------------------------------------------------------------------------------------------------------

// собираем css и js файлы со всех модулей и объединяем их в один (1 css и 1 js файл)
$xc['style'] = get_file('css', $xc['update']);
$xc['scripts'] = get_file('js', $xc['update']);
// ---------------------------------------------------------------------------------------------------------------------

// если в url не указано название модуля, то по умолчанию загружается модуль главной страницы
if (empty($_GET['mod']))
  $xc['module'] = 'main';
    
  else
  $xc['module'] = clearData($_GET['mod'], 'get');
// ---------------------------------------------------------------------------------------------------------------------

// если указанный в url модуль не существует, то по умолчанию загружается общий модуль
if (!file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] .'/index.php')) {
      $xc['module'] = 'module';
}
// ---------------------------------------------------------------------------------------------------------------------

// если включен вход по паролю
if ($xc['close'] == true && empty( $xc['open_modules'][ $xc['module'] ] )) {
    require_once $_SERVER['DOCUMENT_ROOT'] . "/modules/login/index.php";
}
// ----------------------------------------------------------------------------------------------------------------------


// определение компонента модуля
$xc['component'] = null;

if (!empty($_GET['com']) && is_numeric($_GET['com']) == false)
  $xc['component'] = clearData($_GET['com'],'guid');

// ---------------------------------------------------------------------------------------------------------------------


// подключение файлов модуля
if (!empty($xc['component'])) {
    $xc['component'] = 'components/' . $xc['component'] . '/';

    if (!file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'index.php')) {
        $xc['component'] = 'components/component/';

        if (!file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'index.php'))
           exit(header('Location: /'));
    }
}

if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'index.php'))
    require_once $_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'index.php';

if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'config.php'))
    require_once $_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'config.php';

// html шаблон модуля
ob_start();

require_once $_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'tmp.inc.php';

$xc['content'] = ob_get_clean();
// --------------------------------------------------------------------------------------------------------------

// для поддключениее css и js файлов отдельного модуля
$xc['head'] = null;
$xc['body'] = null;

if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'head.php')) {
    ob_start();
    include $_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] .'/' . $xc['component'] . 'head.php';
    $xc['head'] = ob_get_clean();
}

if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] . '/' . $xc['component'] . 'body.php')) {
    ob_start();
    include $_SERVER['DOCUMENT_ROOT'] . '/modules/' . $xc['module'] .'/' . $xc['component'] . 'body.php';
    $xc['body'] = ob_get_clean();
}
// ---------------------------------------------------------------------------------------------------------------

// подключаем модуль для всплывающих окон
$xc['popup'] = null;

if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/modules/popup/includes/popupWindows.inc.php')) {
    ob_start();
    include $_SERVER['DOCUMENT_ROOT'] . '/modules/popup/includes/popupWindows.inc.php';
    $xc['popup'] = ob_get_clean();
}
// ---------------------------------------------------------------------------------------------------------------


// элементы главного шаблона
$xc['header'] = null;
$xc['footer'] = null;
$xc['menu'] = null;
$xc['js'] = null;
$xc['counter'] = null;
$xc['404'] = null;

$tmpBlocks = @scandir($_SERVER['DOCUMENT_ROOT'].'/tmp');

if ($tmpBlocks != false) {
    foreach($tmpBlocks as $tmpBlock) {
        if ($tmpBlock != '.' && $tmpBlock != '..' && $tmpBlock != 'tmp.inc.php' && $tmpBlock != 'mob.inc.php' ) {
            if (@filesize($_SERVER['DOCUMENT_ROOT'].'/tmp/'.$tmpBlock) > 0) {
                
                $tmpBaseName = str_replace('.inc.php','',$tmpBlock);
                
                ob_start();
                include $_SERVER['DOCUMENT_ROOT'].'/tmp/'.$tmpBlock;
                $xc[$tmpBaseName] = ob_get_clean();
            }
        }
    }
}
// ---------------------------------------------------------------------------------------------------------------

// подключение главного шаблона
require_once $_SERVER['DOCUMENT_ROOT'] . '/tmp/tmp.inc.php';
// ----------------------------------------------------------------------------------------------------------------

?>
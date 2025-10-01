<?php defined('DOMAIN') or exit(header('Location: /'));

// выход из админки
if (!empty($_POST['exit']) or !empty($xc['url']['exit'])) {
    $a = db_query("UPDATE users  
    SET hash='' 
    WHERE id='" . intval($_SESSION['user_id']) ."' 
    LIMIT 1", "u");
    
    setcookie("hash", "", time() - 9999999, "/");
    session_destroy();
    
    exit(header('Location: '.DOMAIN));
}
// ---------------------------------------------------------------------------------------------------------------
    
// автоматическая авторизация
if (!empty($_COOKIE["hash"])) {

    $hash = clearData($_COOKIE['hash'], 'guid');
    $loginMess = 'Вам нужно авторизоваться';

    $login = db_query("SELECT u.*, 
    users_role.role  
    FROM users AS u 
    JOIN users_role ON u.role_id = users_role.id
    WHERE hash='".$hash."' 
    LIMIT 1");

    if ($login != false) {
        
        $_SESSION['user_id'] = $login[0]['id'];
        $_SESSION['role_id'] = $login[0]['role_id'];
        $_SESSION['role'] = $login[0]['role'];
        // имя пользователя
        $_SESSION['name'] = null;
        
        if (!empty($login[0]['first_name'])) {
           $_SESSION['name'] = $login[0]['first_name'].' ';
        }
        
        if (!empty($login[0]['last_name'])) {
            $_SESSION['name'] .= $login[0]['last_name'];
        }
        // --------------------------------------------------------------
        
        // аватар
        $_SESSION['avatar'] = DOMAIN.'/img/users/no_avatar.png';
        
        if (!empty($login[0]['avatar']) && file_exists($_SERVER['DOCUMENT_ROOT'].'/img/users/'.$login[0]['avatar'])) {
            $_SESSION['avatar'] = DOMAIN.'/img/users/'.$login[0]['avatar'];
        }
        // --------------------------------------------------------------
        
        
        if ($_SESSION['role_id'] > 1) {
            if (!empty($xc['close_modules'][ $xc['module'] ])) {
                exit(header('Location: '.DOMAIN));
            }
        }
        
        
    } 
        
    else {
        
       if (isset($_POST['action']) && $_POST['action'] == 'ajax') {
           $html = popup_window($loginMess,''); 
           exit($html);
       } 
        
        else {
          $xc['module'] = 'login';
          $xc['component'] = null;
        }
    }
} 

else {
    
    if (isset($_POST['action']) && $_POST['action'] == 'ajax') {
        $html = popup_window($loginMess,'');
        exit($html);
    } 
    
    else {
        $xc['module'] = 'login';
        $xc['component'] = null;
    }
}
// ---------------------------------------------------------------------------------------------------------------

?>
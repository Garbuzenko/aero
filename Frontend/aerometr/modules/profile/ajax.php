<?php defined('DOMAIN') or exit(header('Location: /'));

if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsEditRole') {
    
    $role_id = intval($_SESSION['role_id']);
    $url = $_POST['url'];
    
    ob_start();
    require_once $_SERVER['DOCUMENT_ROOT'].'/modules/profile/includes/editRoleForm.inc.php';
    $form = ob_get_clean();
    
    $h = popup_window($form,'Смена режима работы',400,400,10000);
    exit($h);
}

if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsSwitchEditRole') {
    
    $role_id = intval($_POST['userRole']);
    $url = $_POST['url'];
    
    $upd = db_query("UPDATE users 
    SET role_id=".$role_id."
    WHERE id=".intval($_SESSION['user_id'])."
    LIMIT 1","u");
    
    if ($upd == true) {
        $r = json_encode( array( 0 => 'redirect', 1 => DOMAIN.$url ) );
        exit($r);
    }
    
}

<?php defined('DOMAIN') or exit(header('Location: /'));

// авторизация
if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_signIn') {
  
    $remember = 0;
    $login = clearData($_POST['login']);
    $pass = encrypt_pass($_POST['pass']);
    $url = $_POST['url'];
    
    if (isset($_POST['remember']))
      $remember = intval($_POST['remember']);
    
    $a = db_query("SELECT id 
    FROM users 
    WHERE `login`='".$login."' 
    AND `pass`='".$pass."' 
    LIMIT 1");
    
    if ( $a == false ) {
        $html = popup_window('Неправильный логин или пароль','Что-то не так...'); 
        exit($html);
    }
    
    $hash = sha1($login);
    //$hash = get_hash($login);
   
    $b = db_query("UPDATE users    
    SET hash='" . $hash . "' 
    WHERE id=" . $a[0]['id'] ." 
    LIMIT 1", "u");
    
    if (empty($remember))
       setcookie('hash', $hash, time() + 3600 * 24, '/');
       
    else
      setcookie('hash', $hash, time() + 3600 * 24 * 30, '/');
    
    if (preg_match('/login/',$url)) {
        $url = '';
    }
      
    $r = json_encode( array( 0 => 'redirect', 1 => DOMAIN.$url ) );
    exit($r);
    
}
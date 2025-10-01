<?php

function popup_window($html, $title, $width = null, $height = null, $zIndex = null) {

    if (empty($html))
        return false;
    
    if (empty($zIndex))
      $zIndex = 5500;
    
    if (empty($width) && empty($height)) {
        
        if (MOBILE == true) {
          $width = '90%';
          $height = '50%';
        }
        
        else {
            $width = 400;
            $height = 300;
        }
    }
    
    // определяем есть ли в переменной html тэги
    $h = strip_tags($html);

    // если тэгов нет, то нужно задать стили текста
    if ($h == $html) {
       $html = '<p>' . $html . '</p>';
    }

    $zIndex = intval($zIndex);

    $arr = array(
        0 => 'popup',
        1 => $html,
        2 => $title,
        3 => $width,
        4 => $height,
        5 => $zIndex);

    $arr = json_encode($arr);

    return $arr;
}
<?php defined('DOMAIN') or exit(header('Location: /'));

function overpassQuery() {
    $overpassUrl = "https://overpass-api.de/api/interpreter";
    
    // ID Москвы (административный округ)
    $moscowId = 102269; // Это ID Москвы как субъекта РФ
    
    // Overpass QL запрос для Москвы по ID
    $query = "
        [out:json][timeout:30];
        rel({$moscowId});
        out geom;
    ";
    
    // Подготовка запроса
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $overpassUrl);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, "data=" . urlencode($query));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30); // Уменьшил таймаут до 30 сек
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/x-www-form-urlencoded'
    ]);
    
    // Выполнение запроса
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    if ($error) {
        throw new Exception("Ошибка cURL: " . $error);
    }
    
    if ($httpCode !== 200) {
        throw new Exception("HTTP ошибка: " . $httpCode);
    }
    
    // Декодируем JSON ответ
    $data = json_decode($response, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Ошибка декодирования JSON: " . json_last_error_msg());
    }
    
    $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    
    return $json;
}

if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsGetQueryApi') {
    
    if ($_POST['api'] == 'skyarc') {
      $url = 'https://skyarc.ru/features/atpoint?lat=80&lng=80';
    }
    
    if ($_POST['api'] == 'opensky') {
        $url = 'https://opensky-network.org/api/states/all';
    }
    
    if ($_POST['api'] == 'skyarc' || $_POST['api'] == 'opensky') {
        $data = file_get_contents($url);
        $arr = json_decode($data,true);
        $json = json_encode($arr, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        exit('<pre>'.$json.'</pre>');
    }
    
    if ($_POST['api'] == 'overpass') {
        try {
            
          // По ID
          $result = overpassQuery();
          
          exit('<pre>'.$result.'</pre>');
    
        } catch (Exception $e) {
         echo "Ошибка: " . $e->getMessage() . "\n";
       }
    }
    
    exit();
}
<?php defined('DOMAIN') or exit(header('Location: /'));

require_once($_SERVER['DOCUMENT_ROOT'].'/lib/TCPDF-main/tcpdf.php');

$start_date = '2025-01-01';
$end_date = '2025-07-31';

if (!empty($xc['url']['start_date']) && !empty($xc['url']['end_date'])) {
    $start_date = clearData($xc['url']['start_date'],'date');
    $end_date = clearData($xc['url']['end_date'],'date');
}

function convertPageToPDF($url) {
    global $start_date, $end_date;
    
    // Загружаем страницу
    $html = file_get_contents($url);
    if ($html === false) {
        throw new Exception("Не удалось загрузить страницу: $url");
    }

    // Парсим HTML для извлечения нужных данных
    $dom = new DOMDocument();
    libxml_use_internal_errors(true);
    @$dom->loadHTML('<?xml encoding="UTF-8">' . $html);
    libxml_clear_errors();

    $xpath = new DOMXPath($dom);

    // Извлекаем заголовок из тега <h1>, <h2>, <h3>, <h4>, <h5>, <h6>
    $title = '';
    for ($i = 1; $i <= 6; $i++) {
        $titleNodes = $xpath->query("//h{$i}[contains(@class, 'text-center') or contains(@class, 'title') or contains(@class, 'header')]");
        if ($titleNodes->length > 0) {
            $title = trim($titleNodes->item(0)->textContent);
            break;
        }
    }
    
    // Если не нашли по классам, ищем любой h1-h6
    if (empty($title)) {
        for ($i = 1; $i <= 6; $i++) {
            $titleNodes = $xpath->query("//h{$i}");
            if ($titleNodes->length > 0) {
                $title = trim($titleNodes->item(0)->textContent);
                break;
            }
        }
    }

    // Извлекаем изображение
    $imageHTML = '';
    $images = $xpath->query('//img');
    if ($images->length > 0) {
        $img = $images->item(0);
        $src = $img->getAttribute('src');
        $alt = $img->getAttribute('alt') ?: 'Logo';
        
        // Обрабатываем относительные пути
        if (strpos($src, 'http') !== 0) {
            $baseUrl = parse_url($url, PHP_URL_SCHEME) . '://' . parse_url($url, PHP_URL_HOST);
            if (strpos($src, '/') === 0) {
                $src = $baseUrl . $src;
            } else {
                $src = $baseUrl . '/' . $src;
            }
        }
        
        $imageHTML = '
        <div class="cover-page">
            <div class="logo-container">
                <img src="' . htmlspecialchars($src) . '" alt="' . htmlspecialchars($alt) . '" class="cover-image">
            </div>
            <div class="cover-title">' . htmlspecialchars($title) . '</div>
        </div>';
    }

    // Извлекаем таблицу
    $tableHTML = '';
    $tables = $xpath->query('//table');
    if ($tables->length > 0) {
        $table = $tables->item(0);
        $tableHTML = $dom->saveHTML($table);
    }

    // Создаем чистый HTML для PDF
    $cleanHTML = '
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <style>
            /* Стили для обложки (первая страница) */
            .cover-page {
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                page-break-after: always;
            }
            .logo-container {
                margin-bottom: 40px;
            }
            .cover-image {
                max-width: 300px;
                height: auto;
            }
            .cover-title {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #333;
            }
            .cover-period {
                font-size: 16px;
                margin-bottom: 10px;
                color: #666;
            }
            .cover-date {
                font-size: 14px;
                color: #999;
                margin-top: 20px;
            }
            
            /* Стили для контента (вторая страница) */
            body { 
                font-family: dejavusans, sans-serif; 
                font-size: 9px; 
            }
            .title { 
                text-align: center; 
                font-size: 14px; 
                font-weight: bold; 
                margin-bottom: 15px;
                padding: 10px;
            }
            table { 
                width: 100%; 
                border-collapse: collapse; 
                table-layout: fixed;
            }
            th { 
                background-color: #f8f9fa; 
                border: 1px solid #dee2e6; 
                padding: 8px 4px !important; 
                font-weight: bold;
                text-align: center;
                vertical-align: middle;
            }
            td { 
                border: 1px solid #dee2e6; 
                padding: 6px 4px !important; 
                word-wrap: break-word;
                vertical-align: middle;
            }
            /* Выравнивание чисел по центру */
            .number-cell { 
                text-align: center;
            }
            /* Выравнивание первой колонки по центру */
            .index-cell {
                text-align: center;
            }
            /* Ширины колонок */
            .col-1 { width: 5%; }
            .col-2 { width: 25%; }
            .col-3 { width: 12%; }
            .col-4 { width: 14%; }
            .col-5 { width: 15%; }
            .col-6 { width: 13%; }
            .col-7 { width: 16%; }
        </style>
    </head>
    <body>
        ' . $imageHTML . '
        <div class="content-page">
            ' . $tableHTML . '
        </div>
    </body>
    </html>';

    return $cleanHTML;
}

// Функция для обработки таблицы и добавления классов выравнивания
function processTableHTML($html) {
    // Добавляем классы для выравнивания
    $html = preg_replace_callback('/<table[^>]*>(.*?)<\/table>/is', function($matches) {
        $tableContent = $matches[1];
        
        // Обрабатываем строки
        $tableContent = preg_replace_callback('/<tr[^>]*>(.*?)<\/tr>/is', function($trMatches) {
            $rowContent = $trMatches[1];
            $colIndex = 1;
            
            // Обрабатываем ячейки
            $rowContent = preg_replace_callback('/<(td|th)[^>]*>(.*?)<\/(td|th)>/is', function($cellMatches) use (&$colIndex) {
                $tag = $cellMatches[1];
                $content = $cellMatches[2];
                $currentColIndex = $colIndex;
                $colIndex++;
                
                $classes = "col-{$currentColIndex}";
                
                // Добавляем классы выравнивания
                if ($currentColIndex == 1) {
                    $classes .= " index-cell"; // № - по центру
                } elseif ($currentColIndex == 2) {
                    // Регион - оставляем по левому краю
                } else {
                    $classes .= " number-cell"; // Числовые колонки - по центру
                }
                
                return "<{$tag} class=\"{$classes}\"><br><br>{$content}<br></{$tag}>";
            }, $rowContent);
            
            return "<tr>{$rowContent}</tr>";
        }, $tableContent);
        
        return "<br><table>{$tableContent}</table>";
    }, $html);
    
    return $html;
}

// Основной код
try {
    $url = 'https://aerometr.ru/report?start_date='.$start_date.'&end_date='.$end_date;
    
    $pdfHTML = convertPageToPDF($url);
    
    // Обрабатываем таблицу для добавления классов выравнивания
    $pdfHTML = processTableHTML($pdfHTML);
    
    // Создаем PDF
    $pdf = new TCPDF('L', 'mm', 'A4', true, 'UTF-8');
    $pdf->SetFont('dejavusans', '', 9);
    $pdf->SetAutoPageBreak(true, 15);
    
    // Первая страница создается автоматически при вызове writeHTML
    // благодаря page-break-after: always в CSS
    
    $pdf->AddPage();
    $pdf->writeHTML($pdfHTML, true, false, true, false, '');

    $filename = 'aerometr_report_'.time().'.pdf';
    // Устанавливаем заголовки для скачивания
    header('Content-Type: application/pdf');
    header('Content-Disposition: attachment; filename="'.$filename.'"');
    header('Content-Transfer-Encoding: binary');
    header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
    header('Pragma: public');
    
    // Прямой вывод PDF в браузер
    $pdf->Output($filename, 'D');
    
    exit(); 

} catch (Exception $e) {
    echo "Ошибка: " . $e->getMessage() . "\n";
}
exit();
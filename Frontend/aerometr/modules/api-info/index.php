<?php defined('DOMAIN') or exit(header('Location: /'));
/*
$xc['bread_crumbs'] = array(
  0 => array('anchor' => 'Интеграция API', 'url' => '', 'status' => 1)
);

$allowed_tables = ['aircraft_type',  'aircraft', 'grid_hexagon', 'grid_square', 'points', 'regions', 'processed_flights'];

$table = $_GET['table'] ?? null;
$id = $_GET['id'] ?? null;

if (!$table || !in_array($table, $allowed_tables)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid or missing table name']);
    exit;
}

$table = preg_replace('/[^a-zA-Z0-9_]/', '', $table);

try {
    if ($id !== null) {
        if (!ctype_digit($id)) {
            http_response_code(400);
            echo json_encode(['error' => 'ID must be a positive integer']);
            exit;
        }
        $stmt = $pdo->prepare("SELECT * FROM `$table` WHERE id = ?");
        $stmt->execute([$id]);
        $row = $stmt->fetch();

        if ($row) {
            echo json_encode($row, JSON_UNESCAPED_UNICODE);
        } else {
            http_response_code(404);
            echo json_encode(['error' => 'Record not found']);
        }
    } else {
        // Пагинация
        $page = (int)($_GET['page'] ?? 1);
        $limit = (int)($_GET['limit'] ?? 100);
        $limit = max(1, min($limit, 1000)); // от 1 до 1000
        $page = max(1, $page);

        $offset = ($page - 1) * $limit;

        // Получаем общее количество записей
        $countStmt = $pdo->prepare("SELECT COUNT(*) FROM `$table`");
        $countStmt->execute();
        $total = (int)$countStmt->fetchColumn();
        $pages = ceil($total / $limit);

        // Получаем данные
        $stmt = $pdo->prepare("SELECT * FROM `$table` LIMIT :limit OFFSET :offset");
        $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
        $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
        $stmt->execute();
        $rows = $stmt->fetchAll();

        echo json_encode([
            'data' => $rows,
            'meta' => [
                'total' => $total,
                'page' => $page,
                'limit' => $limit,
                'pages' => $pages
            ]
        ], JSON_UNESCAPED_UNICODE);
    }

} catch (PDOException $e) {
    error_log("API DB Error: " . $e->getMessage());
    http_response_code(500);
    echo json_encode(['error' => 'Database query failed']);
}
*/
?>
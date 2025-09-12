<?php
$data_file = "uploads/parsed_output.json";

$data = [];
if (file_exists($data_file)) {
    $json = file_get_contents($data_file);
    $data = json_decode($json, true);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Parsed STDF Data</title>
</head>
<body>
    <h2>Parsed STDF Data</h2>

    <?php if (!empty($data)): ?>
        <table border="1" cellpadding="5">
            <tr>
                <th>Test Number</th>
                <th>Site Number</th>
                <th>Result</th>
                <th>Test Text</th>
                <th>Head Number</th>
            </tr>
            <?php foreach ($data as $row): ?>
                <tr>
                    <td><?= htmlspecialchars($row['test_number']) ?></td>
                    <td><?= htmlspecialchars($row['site_num']) ?></td>
                    <td><?= htmlspecialchars($row['result']) ?></td>
                    <td><?= htmlspecialchars($row['test_text']) ?></td>
                    <td><?= htmlspecialchars($row['head_num']) ?></td>
                </tr>
            <?php endforeach; ?>
        </table>

        <form action="export_excel.php" method="post">
            <input type="submit" value="Export to Excel">
        </form>

    <?php else: ?>
        <p>No data to display.</p>
    <?php endif; ?>
</body>
</html>

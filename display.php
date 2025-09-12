<?php
// display.php

if (!isset($_GET['json'])) {
    die("No data to display");
}

$jsonFile = $_GET['json'];
if (!file_exists($jsonFile)) {
    die("Data file not found");
}

$data = json_decode(file_get_contents($jsonFile), true);
?>

<!DOCTYPE html>
<html>
<head><title>STDF Parsed Data</title></head>
<body>

<h1>Parsed STDF Data</h1>

<table border="1" cellpadding="5" cellspacing="0">
<thead>
<tr><th>Device</th><th>Test Time</th><th>Test Result</th></tr>
</thead>
<tbody>
<?php foreach ($data as $part): ?>
<tr>
    <td><?= htmlspecialchars($part['device']) ?></td>
    <td><?= htmlspecialchars($part['test_time']) ?></td>
    <td><?= htmlspecialchars($part['test_result']) ?></td>
</tr>
<?php endforeach; ?>
</tbody>
</table>

<form method="post" action="export_excel.php">
    <input type="hidden" name="json" value="<?= htmlspecialchars($jsonFile) ?>">
    <button type="submit" name="export">Export to Excel</button>
</form>

</body>
</html>

<?php
require 'vendor/autoload.php';

use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;

$data_file = "uploads/parsed_output.json";

if (!file_exists($data_file)) {
    die("No data to export.");
}

$data = json_decode(file_get_contents($data_file), true);

$spreadsheet = new Spreadsheet();
$sheet = $spreadsheet->getActiveSheet();

// Set headers
$headers = ['Test Number', 'Site Number', 'Result', 'Test Text', 'Head Number'];
$sheet->fromArray($headers, NULL, 'A1');

// Set data rows
$row_num = 2;
foreach ($data as $row) {
    $sheet->fromArray([
        $row['test_number'],
        $row['site_num'],
        $row['result'],
        $row['test_text'],
        $row['head_num']
    ], NULL, 'A' . $row_num++);
}

// Output to browser
header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
header('Content-Disposition: attachment;filename="parsed_data.xlsx"');
header('Cache-Control: max-age=0');

$writer = new Xlsx($spreadsheet);
$writer->save('php://output');
exit;

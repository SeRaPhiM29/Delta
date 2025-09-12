<?php
// export_excel.php

require 'vendor/autoload.php';

use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;

if (isset($_POST['export']) && isset($_POST['json'])) {
    $jsonFile = $_POST['json'];

    if (!file_exists($jsonFile)) {
        die("Data file not found");
    }

    $data = json_decode(file_get_contents($jsonFile), true);

    $spreadsheet = new Spreadsheet();
    $sheet = $spreadsheet->getActiveSheet();

    $sheet->setCellValue('A1', 'Device');
    $sheet->setCellValue('B1', 'Test Time');
    $sheet->setCellValue('C1', 'Test Result');

    $row = 2;
    foreach ($data as $part) {
        $sheet->setCellValue("A$row", $part['device']);
        $sheet->setCellValue("B$row", $part['test_time']);
        $sheet->setCellValue("C$row", $part['test_result']);
        $row++;
    }

    header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    header('Content-Disposition: attachment;filename="stdf_data.xlsx"');
    header('Cache-Control: max-age=0');

    $writer = new Xlsx($spreadsheet);
    $writer->save('php://output');
    exit;
}
?>

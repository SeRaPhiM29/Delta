<?php
// process_upload.php

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['stdf_file'])) {
    $uploadDir = __DIR__ . '/uploads/';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }

    $tmpName = $_FILES['stdf_file']['tmp_name'];
    $filename = basename($_FILES['stdf_file']['name']);
    $targetFile = $uploadDir . $filename;

    // Move uploaded file to uploads folder
    if (move_uploaded_file($tmpName, $targetFile)) {
        // Path for output JSON
        $jsonOutput = $uploadDir . pathinfo($filename, PATHINFO_FILENAME) . '.json';

        // Run Python script
        $command = escapeshellcmd("python3 parse_stdf.py " . escapeshellarg($targetFile) . " " . escapeshellarg($jsonOutput));
        exec($command, $output, $return_var);

        if ($return_var === 0) {
            // Redirect to display page with the JSON file path (or include display inline)
            header("Location: display.php?json=" . urlencode($jsonOutput));
            exit;
        } else {
            echo "Error parsing STDF file.";
        }
    } else {
        echo "Failed to upload file.";
    }
} else {
    echo "No file uploaded.";
}
?>

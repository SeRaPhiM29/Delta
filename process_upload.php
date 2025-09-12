<?php
$target_dir = "uploads/";
if (!file_exists($target_dir)) {
    mkdir($target_dir, 0777, true);
}

$uploaded_file = $target_dir . basename($_FILES["stdf_file"]["name"]);

if (move_uploaded_file($_FILES["stdf_file"]["tmp_name"], $uploaded_file)) {
    $output_json = $target_dir . "parsed_output.json";
    $python_path = "/home/pi/myenv/bin/python";
    $cmd = escapeshellcmd("$python_path parse_stdf.py $uploaded_file $output_json");
    $output = shell_exec($cmd . " 2>&1");

    if (!file_exists($output_json)) {
        echo "Error running parser:<br><pre>$output</pre>";
        exit;
    }

    header("Location: display.php");
    exit;
} else {
    echo "Failed to upload file";
}
?>

<!-- upload.php -->
<!DOCTYPE html>
<html>
<head><title>Upload STDF File</title></head>
<body>

<h2>Upload STDF File</h2>

<form action="process_upload.php" method="post" enctype="multipart/form-data">
    Select STDF file to upload:
    <input type="file" name="stdf_file" accept=".stdf" required />
    <button type="submit">Upload & Parse</button>
</form>

</body>
</html>

<!DOCTYPE html>
<meta charset="UTF-8">
<html>
<head>
    <title>CodeSanitizer Pro</title>
    <style>
        .container { max-width: 800px; margin: 50px auto }
        .alert { color: #dc3545 }
    </style>
</head>
<body>
<div class="container">
    <h1>🔒 CodeSanitizer Pro</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <div id="result" class="alert"></div>
</div>

<script>
    document.getElementById('uploadForm').onsubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', e.target.file.files[0]);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.text();
        document.getElementById('result').innerHTML =
            response.ok ? `✅ 消毒完成: ${result}` : `❌ 错误: ${result}`;
    };
</script>
</body>
</html>

<?php
highlight_file(__FILE__);
$admin_hash = '0e215962017';
echo "<form action='index.php' method='POST'>";
echo"    <input type='text' name='user' placeholder='Username'>";
echo"    <input type='password' name='pass' placeholder='Password'>";
echo"    <button>Enter Magic Portal</button>";
echo"</form>";
if ($_POST['user'] === 'admin') {
    $pass_hex = $_POST['pass'];
    if($pass_hex == $admin_hash)
    {
        die("I don't want you to pass");
    }
    // 新增十六进制解码层
    if (!ctype_xdigit($pass_hex)) {
        die("hex you know?");
    }
    $raw_data = hex2bin($pass_hex);

    if (md5($raw_data) == $admin_hash) {
    echo @highlight_file('flag.php', true);
    }
}
?>
<!DOCTYPE html><!--STATUS OK--><html>
<head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script>
        window.alert = function()
        {
            window.location.href="64f3b8dbf7b0bd405247a1be615e3a00af1a481b13d0eb749346079cd0890c42.php";
        }
    </script>
    <title>未过滤的评论陷阱</title>
</head>
<body>
<h1 align=center>未过滤的评论陷阱</h1>
<?php
    ini_set("display_errors", 0);
    $str = strtolower($_GET["keyword"]);
    echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
    <form action=index.php method=GET>
    <input name=keyword  value="'.$str.'">
    <input type=submit name=submit value=搜索 />
    </form>
    </center>';
?>
</body>
</html>
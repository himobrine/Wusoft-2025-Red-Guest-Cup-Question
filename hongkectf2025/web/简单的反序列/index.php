<?php
error_reporting(0);
class Secret {
    private $filename;
    public function __construct($file) {
        $this->filename = $file;
    }

    public function __destruct() {
        if (file_exists($this->filename)) {
            echo @highlight_file($this->filename, true);
        }
    }
}

if (isset($_GET['data'])) {
    $data = $_GET['data'];
    unserialize(base64_decode($data));
} else {
    highlight_file(__FILE__);
}
?>

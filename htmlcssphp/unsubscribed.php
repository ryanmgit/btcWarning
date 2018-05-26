<html>
<head>
<link rel="stylesheet" type="text/css" href="btcstyle.css">
</head>

<body>
<div class="background">
  <div class="fullform">
    <div class="welcometext">
      If you miss us feel free to sign back up at any time &#60;3 
    </div>
  </div>
</div>
<?php

  error_reporting(E_ALL);
  ini_set('display_errors', '1');

  DEFINE('DB_USERNAME', 'btcwarning');
  DEFINE('DB_PASSWORD', 'P6iC2i7iNbn5Gci5yusheg6473ehu489eu8r');
  DEFINE('DB_HOST', '127.0.0.1:8889');
  DEFINE('DB_DATABASE', 'email_list');

  $mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE);
  
  $email = $_POST['emailinput'];
  
  //escape entries to prevent tomfoolery
  $email = $mysqli->real_escape_string($email);
  
  $query = "DELETE FROM `email_list`.`email_list` WHERE `email_list`.`email` = '$email';";
  
  $mysqli->query($query); 
  $mysqli->commit();
  $mysqli->close();
  
?>
</body>
</html>
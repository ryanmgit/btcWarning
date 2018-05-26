<html>
<head>
<link rel="stylesheet" type="text/css" href="btcstyle.css">
</head>

<body>
<div class="background">
  <div class="fullform">
    <div class="thanks">
      Thank you for registering. 
    </div>
  </div>
</div>
<?php

  error_reporting(E_ALL);
  ini_set('display_errors', '1');

  DEFINE('DB_USERNAME', 'btcwarning');
  DEFINE('DB_PASSWORD', 'P6iC2i7iNbn5Gci5');
  DEFINE('DB_HOST', '127.0.0.1:8889');
  DEFINE('DB_DATABASE', 'email_list');

  $mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE);

 
  $users_email = $_POST['emailinput'];
  $users_rsi = $_POST['rsiwarning'];
  $up_5 = $_POST['up5'];
  $up_10 = $_POST['up10'];
  $up_15 = $_POST['up15'];
  $up_20 = $_POST['up20'];
  $up_25 = $_POST['up25'];
  $up_30 = $_POST['up30'];
  $down_5 = $_POST['down5'];
  $down_10 = $_POST['down10'];
  $down_15 = $_POST['down15'];
  $down_20 = $_POST['down20'];
  $down_25 = $_POST['down25'];
  $down_30 = $_POST['down30'];

  
  //escape entries to prevent tomfoolery
  $users_email = $mysqli->real_escape_string($users_email);
 
  
  //see which form its from
  //$articleid = $_GET['id'];

  //kill if id is modified
  //if( ! is_numeric($articleid))
  //  die('invalid article id');
  
  //check if email is in use
//  if(!filter_var($_POST['email'], FILTER_VALIDATE_EMAIL)){
//    alert("Invalid email"); // Use your own error handling
//  }
//    $select = $mysqli->query("SELECT `email` FROM `game` WHERE `email` = '".$_POST['email']."'") or exit($mysqli->error());
//  if(mysqli_num_rows($select)){
//    exit("This email is already being used");
//  }
  
  $query = "INSERT INTO `email_list`.`email_list`
    (`email`, `lastmodified`, `rsi`, `up5`, `up10`, `up15`, `up20`, `up25`, `up30`, `down5`,`down10`,`down15`,`down20`,`down25`,`down30`)
    VALUES ('$users_email',  CURRENT_TIMESTAMP, '$users_rsi', '$up_5', '$up_10', '$up_15', '$up_20', '$up_25', '$up_30', '$down_5', '$down_10', '$down_15', '$down_20', '$down_25', '$down_30');";  

  //query sql and close connection
  $mysqli->query($query);
  $mysqli->commit();
  mysqli_close($mysqli);
  
?>
</body>
</html>

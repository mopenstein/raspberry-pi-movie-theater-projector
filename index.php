<?php
$t = localtime();

$t[1] = str_pad($t[1], 2, "0", STR_PAD_LEFT);
$t[2] = str_pad($t[2], 2, "0", STR_PAD_LEFT);
$t[3] = str_pad($t[3], 2, "0", STR_PAD_LEFT);
$t[4] = str_pad($t[4], 2, "0", STR_PAD_LEFT);

//echo $t[2] . ":" . $t[1] . " " . $t[4] . "/" . $t[3] . "/" . (1900+$t[5]) . "<br />";

if(isset($_POST["shutdown"])) {
	$result = exec('sudo shutdown now');
	header("Location: / \n\n");
	die();
}

if(isset($_POST["resume"])) {
	$contents = file_get_contents('/mnt/mydisk/resume.txt');
	$lines = explode("\n", $contents);
	file_put_contents("/mnt/mydisk/play.txt", $lines[0]."\n".$lines[1]);
	$result = exec('sudo ./kill.sh');
	header("Location: / \n\n");
	die();
}


if(isset($_POST["movie"]) && isset($_POST["start_time"])) {
	//save time and movie
	
	if(isset($_POST["schedule"])) {
		$date = (1900+$t[5]) . '-' . ($t[4]+1) . '-' . $t[3] . ' ' . $_POST["start_time"] . ':00';
		$timestamp = strtotime($date);
		file_put_contents("/mnt/mydisk/movie.txt", "$timestamp\n".$_POST["movie"]);		
		$result = exec('sudo ./kill.sh');
	} elseif(isset($_POST["play"])) {
		file_put_contents("/mnt/mydisk/play.txt", "0\n".$_POST["movie"]);
		$result = exec('sudo ./kill.sh');
	}
	
	header("Location: / \n\n");
	die();
}

?>
<!doctype html>
<title>Movie Projector</title>
<head>
	<meta charset="utf-8">
	<meta name="HandheldFriendly" content="True">
	<meta name="MobileOptimized" content="320">
	<meta name="viewport" content="width=device-width">
	<meta http-equiv="cleartype" content="on">
	<link rel="apple-touch-icon-precomposed" sizes="114x114" href="favicon.png">
	<link rel="apple-touch-icon-precomposed" sizes="72x72" href="favicon.png">
	<link rel="apple-touch-icon-precomposed" href="favicon.png">
	<link rel="shortcut icon" href="favicon.png">
	<link rel="icon" type="image/png" href="favicon.png" />
  	<link rel="stylesheet" href="style.css">
	<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
	<script src="//code.jquery.com/jquery-1.10.2.js"></script>
	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
  
  <style>
	input,select,div {
		width:100%;
		font-size:250%;
	}
  </style>
 </head>
 <body>
<?php

//youtube-dl -f 22 --output "/mnt/mydisk/trailers/%(title)s.%(ext)s" 4PdTapNIr-k

$t = localtime();

$t[1] = str_pad($t[1], 2, "0", STR_PAD_LEFT);
$t[2] = str_pad($t[2], 2, "0", STR_PAD_LEFT);
$t[3] = str_pad($t[3], 2, "0", STR_PAD_LEFT);
$t[4] = str_pad($t[4], 2, "0", STR_PAD_LEFT);

//echo $t[2] . ":" . $t[1] . " " . $t[4] . "/" . $t[3] . "/" . (1900+$t[5]) . "<br />";



$fileList = glob('/mnt/mydisk/films/*');
 
echo '
<form method="POST">
<h3>Movie:</h3>
<select name="movie">
';
//Loop through the array that glob returned.
foreach($fileList as $filename){
   //Simply print them out onto the screen.
   echo '<option value="'.$filename.'">'.basename($filename, ".mp4"), '</option>'; 
}
echo '
</select><br />
<br />
<input type="submit" name="play" value="Play Now" /><br />
<br />
';

echo '<h3>Start time:</h3>
<input type="time" id="start_time" name="start_time" value="'.$t[2].':'.$t[1].'" /><br />
<br />
<input type="submit" name="schedule" value="Schedule" /><br />
</form>


<form method="POST">
';

$contents = file_get_contents('/mnt/mydisk/resume.txt');
$lines = explode("\n", $contents);

echo '<h3>Resume Movie:</h3>
<div>
Time: '.gmdate("H:i:s", $lines[0]).'<br />
Movie: '.basename($lines[1]).'<br />
</div>
<input type="submit" name="resume" value="Resume" />
</form>
<br />
<br />
<br />
<br />
<br />
<br />
<form method="POST">
<input type="submit" name="shutdown" value="Shutdown" style="background-color: #AF4C50;   border: none;  color: white;  padding: 15px 32px;  text-align: center;  text-decoration: none;  display: inline-block;" />
</form>';
 ?>
</body>

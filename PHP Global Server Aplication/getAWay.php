<?php





// If get the upadted new ip save it

try {

    // GET Request from outside

    // https://trackingpackage.000webhostapp.com/?ID=221397455373948

    if ( isset($_GET['ID'] ) ) {

        $requestCODE = $_GET["ID"];

        if($requestCODE == 221397455373948) {

            $myLatestIP = $_SERVER['REMOTE_ADDR'];

        	$myfile = fopen("latestIP.txt", "w") or die("Unable to open file!");

        	fwrite($myfile, $myLatestIP);

        	fclose($myfile);

        	echo "SAVED";

        	exit();

        }

    }

} catch (Exception $e) {

    echo $e;

}











// If you have the request o show the video get the saved ip an continue with her

// https://trackingpackage.000webhostapp.com

try {

    if( ! isset($_GET['ID']) ) {

        $myfile = fopen("latestIP.txt", "r") or die("Unable to open file!");

        $myLatestIP = fread($myfile,filesize("latestIP.txt"));

        fclose($myfile);

        echo '<script>window.open ("http://' . $myLatestIP . ':5000/stream", "_self")</script>';

    }

} catch (Exception $e) {

    

}

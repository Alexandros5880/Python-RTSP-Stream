<?php






try {


    if ( isset($_GET['ID'] ) && isset($_GET['action'] ) ) {

        $requestCODE = $_GET["ID"];
        $action = $_GET["action"];



        if($requestCODE == 221397455373948) {

            // GET Request from outside update Global Ip
            if ($action == "update") {  // https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=update
                $myLatestIP = $_SERVER['REMOTE_ADDR'];
                $myfile = fopen("latestIP.txt", "w") or die("Unable to open file!");
                fwrite($myfile, $myLatestIP);
                fclose($myfile);
                echo "SAVED";
                exit();
        	}

        	// Gte the local html file with all the cameras
            if ($action == "getAll") {  // https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=getAll
                $myfile = fopen("latestIP.txt", "r") or die("Unable to open file!");
                $myLatestIP = fread($myfile,filesize("latestIP.txt"));
                fclose($myfile);
                echo '<script>window.open ("http://' . $myLatestIP . ':5000/stream", "_self")</script>';
            }

            // Gte the local html file with all the cameras
            if (strpos($action, "video_feed") !== false) {  // https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_1
                $myfile = fopen("latestIP.txt", "r") or die("Unable to open file!");
                $myLatestIP = fread($myfile,filesize("latestIP.txt"));
                fclose($myfile);
                echo '<script>window.open ("http://' . $myLatestIP . ':5000/' . $action . '", "_self")</script>';
            }



        }


    }

} catch (Exception $e) {

    echo $e;

}

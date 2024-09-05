<?php
// connecting to database
$conn = mysqli_connect("localhost", "root", "", "bot") or die("Database Error");

$getMesg = mysqli_real_escape_string($conn, $_POST['text']);

// checking user query against database queries
$check_data = "SELECT replies FROM chatbot WHERE queries LIKE '%$getMesg%'";
$run_query = mysqli_query($conn, $check_data) or die("Error");

// if user query matched to database query it will show the reply, otherwise it goes to the else statement
if(mysqli_num_rows($run_query) > 0){
    // fetching reply from the database according to the user query
    $fetch_data = mysqli_fetch_assoc($run_query);
    $reply = $fetch_data['replies'];
    echo $reply;
}else{
    echo "Sorry, I can't understand you!";
}
?>

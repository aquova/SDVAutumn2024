<!DOCTYPE html>
<html>
    <head>
        <title>SDV Halloween Event 2024</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="assets/pumpkin_emoji.webp" type="image/webp">
        <link rel="stylesheet" href="css/index.css" type="text/css">
    </head>
    <body>
        <?php include 'leaderboard.php'; ?>
        <div class="title">
            <img src="assets/leaf_emoji.webp">
            <h1 class="center">SDV Halloween Event 2024</h1>
            <img src="assets/ghost_emoji.webp">
        </div>
        <div id="leaderboard">
            <div id="container">
                <div class="list">
                    <?php tricks_received_leaderboard(); ?>
                </div>
                <div class="list">
                    <?php treats_recieved_leaderboard(); ?>
                </div>
                <div class="list">
                    <?php tricks_sent_leaderboard(); ?>
                </div>
                <div class="list">
                    <?php treats_sent_leaderboard(); ?>
                </div>
            </div>
        </div>
    </body>
</html>

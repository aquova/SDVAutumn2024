<?php
define("DB_PATH", "/private/autumn.db");

function tricks_received_leaderboard() {
    $db = new SQLite3(DB_PATH);
    $query = $db->prepare("SELECT username, tricks_received FROM players ORDER BY tricks_received DESC LIMIT 10");
    $ret = $query->execute();
    echo "<h2>Most Tricks Received</h2>";
    echo "<ol>";
    while ($row = $ret->fetchArray()) {
        $name = $row['username'];
        $hits = $row['tricks_received'];
        echo "<li>";
        echo "<span>$name - $hits</span>";
        echo "</li>";
    }
    echo "</ol>";
    $db->close();
};

function treats_recieved_leaderboard() {
    $db = new SQLite3(DB_PATH);
    $query = $db->prepare("SELECT username, treats_received FROM players ORDER BY treats_received DESC LIMIT 10");
    $ret = $query->execute();
    echo "<h2>Most Treats Received</h2>";
    echo "<ol>";
    while ($row = $ret->fetchArray()) {
        $name = $row['username'];
        $hits = $row['treats_received'];
        echo "<li>";
        echo "<span>$name - $hits</span>";
        echo "</li>";
    }
    echo "</ol>";
    $db->close();
}

function tricks_sent_leaderboard() {
    $db = new SQLite3(DB_PATH);
    $query = $db->prepare("SELECT username, tricks_sent FROM players ORDER BY tricks_sent DESC LIMIT 10");
    $ret = $query->execute();
    echo "<h2>Most Tricks Sent</h2>";
    echo "<ol>";
    while ($row = $ret->fetchArray()) {
        $name = $row['username'];
        $hits = $row['tricks_sent'];
        echo "<li>";
        echo "<span>$name - $hits</span>";
        echo "</li>";
    }
    echo "</ol>";
    $db->close();
};

function treats_sent_leaderboard() {
    $db = new SQLite3(DB_PATH);
    $query = $db->prepare("SELECT username, treats_sent FROM players ORDER BY treats_sent DESC LIMIT 10");
    $ret = $query->execute();
    echo "<h2>Most Treats Sent</h2>";
    echo "<ol>";
    while ($row = $ret->fetchArray()) {
        $name = $row['username'];
        $hits = $row['treats_sent'];
        echo "<li>";
        echo "<span>$name - $hits</span>";
        echo "</li>";
    }
    echo "</ol>";
    $db->close();
}
?>

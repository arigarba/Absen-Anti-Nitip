<?php 
$koneksi = mysqli_connect("localhost", "root", "", "abwa");

if (!$koneksi) {
    die("Koneksi gagal: " . mysqli_connect_error());
}
?>
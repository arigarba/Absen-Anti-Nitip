<?php
include 'koneksi.php';

$query = mysqli_query($koneksi, "SELECT * FROM absen ORDER BY id DESC");
$no = 1;
while ($data = mysqli_fetch_assoc($query)) {
    echo "<tr>
            <td>{$no}</td>
            <td>{$data['nama']}</td>
            <td>{$data['tanggal']}</td>
            <td>{$data['jam']}</td>
          </tr>";
    $no++;
}
?>
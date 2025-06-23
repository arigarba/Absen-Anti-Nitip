<?php
include 'koneksi.php';

// Pastikan data dikirim melalui POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Tangkap data POST dengan fallback jika kosong
    $nama = $_POST['nama'] ?? '';
    $waktu = $_POST['waktu'] ?? '';

    if (!empty($nama) && !empty($waktu)) {
        $tanggal = date('Y-m-d', strtotime($waktu));
        $jam = date('H:i:s', strtotime($waktu));
        $jam_only = date('H:i', strtotime($waktu));

        $check = mysqli_query($koneksi, "SELECT * FROM absen WHERE nama='$nama' AND tanggal='$tanggal' AND jam like '$jam_only%'");
        if (mysqli_num_rows($check) > 0) {
            echo 'sudah';
        } else {
            $result = mysqli_query($koneksi, "INSERT INTO absen VALUES(null,'$nama','$tanggal','$jam')");
            echo $result ? 'berhasil' : 'gagal';
        }
    } else {
        echo 'gagal - data tidak lengkap';
    }
} else {
    echo 'gagal - bukan POST';
}
?>

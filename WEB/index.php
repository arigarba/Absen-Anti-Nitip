<!DOCTYPE html>
<html lang="id">

<head>
  <meta charset="UTF-8">
  <title>Sistem Absensi Wajah</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Google Font -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">

  <style>
    * {
      box-sizing: border-box;
      font-family: 'Inter', sans-serif;
    }

    body {
      margin: 0;
      background-color: #f1f5f9;
      color: #1e293b;
    }

    header {
      background-color: #0f172a;
      color: white;
      padding: 20px;
      text-align: center;
      font-size: 28px;
      font-weight: 600;
    }

    main {
      max-width: 1000px;
      margin: auto;
      padding: 20px;
    }

    .button-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 15px;
      margin-bottom: 25px;
    }

    button {
      padding: 12px;
      font-size: 16px;
      font-weight: 600;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: 0.3s ease;
    }

    button.absen {
      background-color: #10b981;
      color: white;
    }

    button.absen:hover {
      background-color: #059669;
    }

    button.register {
      background-color: #f59e0b;
      color: white;
    }

    button.register:hover {
      background-color: #d97706;
    }

    .filter-box {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 20px;
      align-items: center;
    }

    .filter-box input {
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
    }

    .filter-box button {
      padding: 8px 14px;
      border-radius: 6px;
      background-color: #3b82f6;
      color: white;
      border: none;
      cursor: pointer;
    }

    .filter-box button:hover {
      background-color: #2563eb;
    }

    .filter-box .reset {
      background-color: #e11d48;
    }

    .filter-box .reset:hover {
      background-color: #be123c;
    }

    .table-container {
      overflow-x: auto;
      background: white;
      padding: 15px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      text-align: center;
    }

    th, td {
      padding: 12px;
      border-bottom: 1px solid #e2e8f0;
    }

    th {
      background-color: #1e293b;
      color: white;
    }

    tr:nth-child(even) {
      background-color: #f8fafc;
    }

    #status {
      margin-top: 15px;
      font-size: 15px;
      font-weight: 500;
      color: #1d4ed8;
    }
  </style>
</head>

<body>

  <header>
    Sistem Absensi Wajah
  </header>

  <main>
    <div class="button-grid">
      <button class="absen" onclick="startAbsen()">🟢 Jalankan Absen</button>
      <button class="register" onclick="regisAbsen()">📝 Daftarkan User</button>
    </div>

    <div id="status">Status: Menunggu tindakan...</div>

    <h3 style="margin-top: 30px;">📋 Data Absen</h3>

    <!-- Filter Form -->
    <div class="filter-box">
      <input type="text" id="filterName" placeholder="Cari Nama...">
      <input type="date" id="filterDate">
      <button onclick="applyFilter()">🔍 Filter</button>
      <button class="reset" onclick="resetFilter()">🔄 Reset</button>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>NO</th>
            <th>Nama</th>
            <th>Tanggal</th>
            <th>Jam</th>
          </tr>
        </thead>
        <tbody id="list_data_absen">
          <!-- Data akan dimuat otomatis -->
        </tbody>
      </table>
    </div>
  </main>

  <!-- jQuery CDN -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

  <script>
    function startAbsen() {
      $('#status').text('⏳ Menjalankan absen...');
      $.get("run_absen.php", function (response) {
        $('#status').text('✅ Absen berhasil dijalankan!');
        console.log("Output Absen:", response);
      }).fail(function () {
        $('#status').text('❌ Gagal menjalankan absen!');
      });
    }

    function regisAbsen() {
      $('#status').text('⏳ Mendaftarkan user...');
      $.get("regis_user.php", function (response) {
        $('#status').text('✅ User berhasil didaftarkan!');
        console.log("Registrasi:", response);
      }).fail(function () {
        $('#status').text('❌ Gagal mendaftarkan user!');
      });
    }

    // Load data dari getData.php setiap detik
    setInterval(function () {
      $.get("getData.php", function (data) {
        $('#list_data_absen').html(data);
        applyFilter(); // filter otomatis setelah update
      });
    }, 1000);

    // Filter fungsi
    function applyFilter() {
      const name = $('#filterName').val().toLowerCase();
      const date = $('#filterDate').val();

      $('#list_data_absen tr').each(function () {
        const row = $(this);
        const rowName = row.find("td:nth-child(2)").text().toLowerCase();
        const rowDate = row.find("td:nth-child(3)").text();

        const matchName = !name || rowName.includes(name);
        const matchDate = !date || rowDate === date;

        if (matchName && matchDate) {
          row.show();
        } else {
          row.hide();
        }
      });
    }

    function resetFilter() {
      $('#filterName').val('');
      $('#filterDate').val('');
      applyFilter();
    }
  </script>

</body>

</html>

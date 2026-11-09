Deployed at: https://alfarrel-ersya-myportofolio.pws.cs.ui.ac.id/

## LOCAL SETUP GUIDE

- Clone repository & go to directory:
    ```bash 
    git clone https://github.com/alpallel/portofolio
    cd portofolio
    ```

- Make '.env' & '.env.prod' file:
    ```bash
    touch .env .env.prod
    ```

    - add variables for '.env':
        ```
        PRODUCTION=False
        ```
    - add variables for '.env.prod'
        ```
        DB_NAME=<nama database>
        DB_HOST=<host database>
        DB_PORT=<port database>
        DB_USER=<username database>
        DB_PASSWORD=<password database>
        SCHEMA=tutorial
        PRODUCTION=True
        ```

- Setup virtual environment:
    ```bash
    python -m venv env
    ```

- Activate virtual evironment
    - Bash
        ```bash
        source env/bin/activate
        ```
    - Fish
        ```fish
        source env/bin/activate.fish
        ```
    - Windows cmd
        ```cmd
        .\env\Scripts\activate.bat
        ```

- Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

- Run it locally:
    ```bash
    python manage.py runserver
    ```

## Tugas 

### Tugas 1

1. Saya memakai elemen 'section' yang cukup membantu untuk membedakan tiap section dan membaca kode dengan lebih mudah daripada dengan menggunakan 'div'. Saya juga memakai 'nav' untuk menambah elemen di navbar.
2. Saya menggunakan extension 'live preview' vscode, yang memungkinkan saya untuk melihat secara real-time perubahannya di browser ketika saya mengotak-atik file css nya. Sehingga menyesuaikan posisi dan ukuran tidak menjadi hal yang rumit/sulit bagi saya
3. Saya ingin membuat tiap elemen di section experience bisa dilihat lebih detail ketika diklik dan juga switch night mode / dark mode

### Tugas 2

1. browser mengirim HTTP request -> Django memeriksa file project "myportofolio" -> request di routing ke Djanggo app "Main" lebih tepatnya ke main/urls.py -> main/urls.py memanggil fungsi yang sesuai dengan requestnya yang berada di views.py -> views.py menentukan dan memberikan data yang keluar ke front end -> models.py menyimpan data yang masuk ke dalam database SQL -> browser menerima file HTML dari folder templates dan file css, kemudian menampilkannya di front end

2. menyimpan data dengan model memungkinkan kita untuk mengubah isi dari portofolio tanpa mengubah kode. Contoh kasusnya, ketika saya ingin menambah atribut baru pada experience, saya hanya perlu menambah satu atribut di model, satu line di html dan menambahkannya ke tiap experience lewat django admin tanpa ada perubahan signifikan pada kode html.

3. makemigrations membandingkan models.py yang sekarang dengan yang sudah tersimpan (migrate). migrate membaca perubahan dari makemigrations kemudian memperbarui struktur tabel di SQL. Contohnya ada ketika saya menambahkan model projects. Ketika saya membuat model/atribut model baru, saya perlu melakukan makemigrations dan migrate terlebih dahulu sebelum data baru tersebut bisa disimpan di database dan ditampilkan.


### Tugas 5

1. Debouncing adalah pembatasan frekuensi pemanggilan fungsi dengan menunda pemanggilan fungsi tersebut sampai jeda waktu tertentu sejak event terakhir terjadi, dan apabila fungsi dicoba untuk dipanggil kembali sebelum jeda waktu selesai, timer sebelumnya akan dibatalkan oleh 'clearTimeout' dan dimulai kembali dari awal oleh 'setTimeout'.
   - Pentingnya pada Pencarian AJAX:
     - Mencegah request flooding: Tanpa debouncing, fungsi akan terpanggil sebanyak jumlah ketikan dari pengguuserna 
     - Menghemat sumber daya server dan bandwidth client
     - Menghindari race condition

2. Operator 'await' digunakan di dalam fungsi 'async' untuk menghentikan sementara eksekusi baris kode berikutnya sampai promise dari pemanggilan fungsi async seperti fetch() atau response.json() selesai.
   - Jika tidak menggunakan 'await':
     - Fungsi fetch() akan langsung mengembalikan objek promise yang masih berstatus pending, bukan objek response.
     - Jika variabel yang menampung promise tersebut langsung dipanggil dengan metode response.json(), JavaScript akan melempar exception atau menghasilkan nilai undefined karena operasinya belum selesai diproses.
     - Alur eksekusi JavaScript akan terus berjalan ke baris-baris manipulasi DOM di bawahnya sebelum data dari server berhasil diunduh, mengakibatkan interface gagal menampilkan data atau crash.

3. XSS adalah kelemahan keamanan web dimana penyerang berhasil menginject script ke dalam data aplikasi web. Kode bisa digunakan untuk dieksekusi secara otomatis oleh browser user lain saat melihat halaman terkait, memungkinkan penyerang mencuri session cookies, merusak tampilan web, dll.
   - Mengapa data via AJAX/JavaScript lebih rentan dibandingkan template Django:
     - Django Template Engine memiliki sistem keamanan bawaan yaitu "automatic HTML escaping" yang aktif secara default pada setiap variabel konteks template. Karakter-karakter khusus HTML seperti '<', '>', '&', ' " ', dan <'> secara otomatis diubah menjadi entitas HTML aman (`&lt;`, `&gt;`, dll), sehingga teks tidak dianggap sebagai tag oleh browser.
     - Pada AJAX / JavaScript, data diterima dalam format JSON yg masih mentah. Saat developer memperbarui DOM menggunakan manipulasi teks langsung seperti properti innerHTML, browser secara default tidak melakukan auto-escaping.

### Tugas 6

1. REST adalah gaya arsitektur web berbasis resource menggunakan protokol HTTP secara stateless. Mengembalikan format JSON saja belum cukup disebut RESTful karena RESTful juga menuntut penggunaan HTTP method yang tepat (GET, POST, PUT, PATCH, DELETE), struktur URL berbasis kata benda/resource (misal /api/v1/experiences/), penggunaan status code yang sesuai (200, 201, 400, 403, 404), dan sifat stateless di server.
   - Perbedaan PUT dan PATCH:
     - PUT: Menggantikan seluruh data resource secara utuh. Client harus mengirim semua field kembali.
       - Contoh: Mengupdate form experience secara lengkap (title, description, category, organization, dll).
     - PATCH: Hanya memperbarui sebagian field tertentu tanpa mengubah atau mereset field lainnya.
       - Contoh: Hanya ingin mengganti title pada experience tanpa perlu mengirim ulang field lain seperti description dan thumbnail.

2. Serializer pada DRF berperan sebagai jembatan dua arah: mengubah data model/QuerySet Django menjadi format JSON (serialisasi) dan memvalidasi data JSON dari request user untuk diubah kembali menjadi objek model yang siap disimpan ke database (deserialisasi).
   - Keuntungan dibanding merakit dictionary manual:
     - Validasi otomatis: Serializer otomatis mengecek tipe data, panjang field, hingga sanitasi (strip_tags) lewat method validate_<field>. Jika manual, kita perlu menulis banyak if-else sendiri.
     - Penanganan error terstruktur: Jika input tidak valid, serializer otomatis menghasilkan respons error terstruktur dengan status code 400 Bad Request.
     - Keamanan lebih terjaga: Mencegah user memanipulasi field terlarang lewat fields eksplisit dan read_only_fields.

3. - Autentikasi: Proses memastikan siapa pengguna yang sedang mengakses (identitas user), misal lewat session cookie atau token.
   - Otorisasi: Proses menentukan tindakan apa saja yang diizinkan untuk user tersebut, misalnya apakah user adalah superuser, editor, atau pengunjung biasa.
   - Mengapa harus diperiksa di server lewat permission class:
     - Menyembunyikan tombol di template hanya untuk tampilan saja dan mudah dibypass. Pengguna bisa memunculkan tombol lewat inspect element atau langsung menembak URL API menggunakan fetch(), cURL, atau Postman. Tanpa permission class di server, siapapun bisa memodifikasi atau menghapus data di database.

4. - Mengapa tetap butuh CSRF token pada SessionAuthentication:
     - Karena SessionAuthentication memanfaatkan cookie session  browser yang otomatis ikut terkirim pada setiap request ke domain kita. Tanpa CSRF token, website pihak ketiga yang berbahaya bisa memicu request ke API kita menggunakan session login korban yang sedang aktif.
   - Mengapa force_authenticate tidak cukup:
     - force_authenticate adalah jalan pintas pengujian yang sengaja melewati seluruh alur autentikasi dan pemeriksaan CSRF Django untuk langsung menempelkan user ke request. Fungsi ini hanya menguji hak akses, tidak menguji apakah perlindungan CSRF di aplikasi benar-benar bekerja.

---

## AI Disclosure
Saya memakai Gemini AI untuk membantu saya mewujudkan ide, tema, dan debbugging, terutama untuk styling css. Hasil dari AI kemudian saya improve dan saya terapkan sebagai referensi untuk styling elemen-elemen lainnya. Sebagian besar AI digunakan pada section 'about me' untuk saya belajar styling dengan css. Sisanya AI  digunakan untuk debugging kecil ketika saya stuck.

AI juga digunakan untuk membatu membuat testing dan refactor kode redundan di style.css


### Terdapat comment pada bagian yang dibantu oleh AI di file style.css
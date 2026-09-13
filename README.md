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


## AI Disclosure
Saya memakai Gemini AI untuk membantu saya mewujudkan ide, tema, dan debbugging, terutama untuk styling css. Hasil dari AI kemudian saya improve dan saya terapkan sebagai referensi untuk styling elemen-elemen lainnya. Sebagian besar AI digunakan pada section 'about me' untuk saya belajar styling dengan css. Sisanya AI  digunakan untuk debugging kecil ketika saya stuck.


### Terdapat comment pada bagian yang dibantu oleh AI di file style.css
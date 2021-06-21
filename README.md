Langkah-langkah menggunakan:

1. Install perangkat lunak yang akan digunakan
  a. Wireshark/tshark
     Tambahkan wireshark kedalam PATH agar perintah tshark dapat dijalankan
  b. Matplotlib
     pip install matplotlib
  c. NetworkX
     pip install networkx
     
2. Untuk melakukan capturing, lokasi penyimpanan file dan interface yang digunakan harus disesuaikan. Untuk memeriksa interface dapat menggunakan _"tsark -D"_ 
   a. Interface yang digunakan didalam source code adalah "\\Device\\NPF_{330F3553-1DDF-4852-8CA8-86ECC4276E88}"
3. Durasi capturing data dapat diatur pada command "-a duration:120" dalam source code

# Amandemen Arsitek EDA-07: Aturan Alarm Kontrol Berbasis Laju (A-7/A-8)

Peran: Arsitek (rangkap asisten atas perintah user 2026-10-10).
Tanggal: 2026-10-10. Status: MENGIKAT. Mengubah ATURAN ALARM saja;
A-1 s/d A-6 tetap utuh. Diputus SEBELUM hasil run terlihat (run di
LA 2/60 saat amandemen ditulis), semata dari kalibrasi null mock.

## A-7 Revisi aturan alarm: dari nol-toleransi ke berbasis-laju

Fakta kalibrasi (mock coder, kode asli, null murni): tiap evaluasi
kontrol lolos G2-revisi dengan peluang ~= 0,025. Dengan 780 evaluasi
(260 target x 3 kontrol), ekspektasi ~= 19 lolos dan P(STOP) ~= 1,0
BAHKAN BILA semua kontrol derau murni. Aturan "satu lolos = STOP" yang
saya tulis di KONTRAK_07 mengasumsikan FPR per evaluasi ~= 0; asumsi itu
terbukti salah oleh pengukuran. Gerbang yang terpicu dengan peluang 1
di bawah null tidak menguji apa pun (teater yang tak-terfalsifikasi).
Mempertahankannya adalah kesalahan yang sesungguhnya; merevisinya
sebelum melihat hasil BUKAN menggeser tiang gol (tiga pembela: diputus
buta-hasil, berbasis kalibrasi null saja, asumsi lama terbukti salah
oleh pengukuran).

Aturan baru (menggantikan "nol kontrol lolos-G2", mengikat):

- N = jumlah evaluasi kontrol yang tercatat; K = yang lolos G2-revisi;
  p0 = 0,025 (kalibrasi null mock, n_sem 2000/8000, dinyatakan aproksimasi).
- ALARM STOP bila dan hanya bila ekor-atas binomial P(X >= K | N, p0)
  < 0,01. Selain itu: bukan alarm; K lolos dicatat sebagai derau
  multiplisitas yang diharapkan; run lanjut.
- Konfirmasi bacaan coder: ">= 4 dari 5" = 4 ATAU 5 dari 5 semester
  (mayoritas, bukan 5/5). Benar.
- A-4 tetap: lolos kontrol struktural yang menyimpang dari pola noise
  (mis. target sama berulang, laju jauh di atas noise) dicatat untuk
  adjudikasi di review S5, TANPA menghentikan run bila A-7 tidak alarm.

## A-8 Protokol aplikasi (mengikat)

- Run berjalan DILARANG disentuh/di-kill: biarkan sampai ujung alaminya
  (lolos dengan bukti, atau STOP dengan bukti lengkap per A-5).
- Vonis A-7 dihitung dari file _gate_ yang tersimpan, bukan dari memori.
- Bila A-7 = bukan alarm: rerun dengan SATU baris assert yang dipatch
  (full rerun detached dapat diterima; resume-dari-checkpoint hanya bila
  checkpoint terbukti bit-identik). Verifikasi ulang 24/24 konstanta.
- Bila A-7 = alarm: STOP + adjudikasi arsitek. DILARANG bypass.
- Perubahan kode di luar baris assert alarm = drift, DILARANG.

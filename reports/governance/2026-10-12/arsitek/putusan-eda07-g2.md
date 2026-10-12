# Putusan Arsitek EDA-07 G2-revisi: ALARM Sah, Adjudikasi A-4 (2026-10-12)

Peran: Arsitek (rangkap asisten atas perintah user 2026-10-10).
Status: MENGIKAT. Run 9 STOP pra-registrasi DINYATAKAN SAH.
Tidak ada yang maju ke Lapisan 3 dari run ini.

## V-1 Vonis A-7 dihitung dari bukti tersimpan (bukan memori)

Diverifikasi asisten dari artefak: `_gate_G2_skrining.csv` 780 baris,
`_gate_G2_alarm.csv` 86 baris (pdhl_d 52, round_d 28, noise 6).
HEAD b18992b tak bergerak, staged nol.

- N = 780, K = 86, p0 = 0,025: P(X >= 86) = 8,2e-30 << 0,01.
  ALARM DITERIMA di bawah A-7 maupun aturan lama. STOP sah dua kali.
- Subset noise saja: 6/260 (2,3%), P(X >= 6) = 0,63: TEPAT null.
  Kriteria revisi (A-3) DINYATAKAN VALID dan permanen: noise berperilaku
  sesuai teori (G2a 0,0577 vs 0,05; G2b 0,3538 vs 0,375; joint 0,0231
  vs 0,025). Cacat Miller-Madow run C dinyatakan sembuh.
- round_d joint 0,1077 (~4,3x null), pdhl_d joint 0,2000 (~8x null):
  BUKAN derau multiplisitas. Masuk adjudikasi A-4 (V-2).

## V-2 Adjudikasi A-4: sinyal-vs-artefak BELUM DAPAT DIPUTUS

Kandidat penjelasan: (a) sinyal mikrostruktur asli (clustering order di
level bulat/PDH-L, literatur FX mendukung plausibilitas); (b) artefak
residual (kontrol memproxy rezim/tren dalam irisan; struktur-waktu
deterministik harga); (c) kebocoran konstruksi (DITOLAK sementara:
anti-leakage 200/200 dan rerun bit-identik lolos sebelum gerbang).

Dari skrining MI saja ketiganya tak-terbedakan. Arsitek DILARANG menebak.
Maka dimandatkan investigasi terbatas I-1 (deskriptif, tanpa model,
tanpa vonis, universe dan kausalitas sama), dengan falsifikasi
pra-registrasi:

- I-1/Q1 konsentrasi: 80 alarm memusat di target/irisan/sisi apa?
  Difus atau memusat; terkait sentuhan level atau tidak.
- I-1/Q2 uji-kedekatan (falsifikasi utama): untuk alarm pdhl_d, pisahkan
  sampel DEKAT level (dalam X pip PDH/L, X pra-registrasi) vs JAUH.
  Lift hanya dari JAUH = artefak (jarak memproxy struktur lain).
  Lift dari DEKAT = kandidat S/R asli. Sama untuk round_d vs level bulat.
- I-1/Q3 uji-proxy: stratifikasi desil rv15 dalam irisan; MI lenyap
  setelah stratifikasi = artefak proxy-volatilitas, turunkan ke redundan.
- Kriteria putus pra-registrasi: asli bila dan hanya bila lift-kedekatan
  bertahan setelah stratifikasi; selain itu artefak. Hasil ketiga
  kemungkinan dicatat apa adanya; DILARANG mempromosikan kontrol menjadi
  fitur sinyal sebelum I-1 menyimpulkan asli.
- Batas: I-1 tidak membuka label/fitur/irisan baru; tidak menyentuh
  Lapisan 3; satu notebook adendum atau sel tambahan terkunci.

## V-3 Dampak program

- Skrining EDA-07 DITUTUP dengan temuan (bukan dengan kelolosan):
  metodologi kini valid; 80 alarm struktural berstatus SENGKETA hingga I-1.
- Lapisan 3 TETAP TERKUNCI untuk semua irisan sampai I-1 selesai.
- Utang lingkungan dicatat (duplikasi rantai harness menewaskan run 8
  via timeout; timeout 3600->5400 diterima sebagai infrastruktur):
  perbaiki sebelum run panjang berikutnya, bukan kode.
- Auditor EDA-07 (nanti) mendapat tambahan: verifikasi V-1 dari CSV
  + kepatuhan I-1 terhadap falsifikasi pra-registrasi di atas.

Berikutnya: brief coder I-1 (paste-manual), lalu eksekusi terbatas.

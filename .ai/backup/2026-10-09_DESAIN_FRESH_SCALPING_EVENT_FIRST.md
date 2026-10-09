# Rancangan Fresh — Riset Edge Scalping USDJPY Event-First

**Status:** DRAF DESAIN UNTUK DIBACA USER. Bukan spesifikasi eksekusi, bukan
izin eksperimen, bukan strategi aktif, dan tidak mengubah putusan lama.

**Tanggal:** 2026-10-09
**Asumsi kerja user:** perlakukan H4 sebagai **GAGAL** untuk memilih jalur
baru. Tidak ada rescue melalui filter, sub-sampel, biaya, ambang, atau definisi
baru setelah hasil diketahui.

**Batas:** status resmi historis H4 tetap mengikuti putusan arsitek yang sudah
ada. Dokumen ini hanya menjawab: bila H4 tidak menjadi fondasi metode, jalur
riset scalping apa yang sah secara empiris?

---

## 1. Keputusan desain

Jalur berikutnya bukan “cari indikator terbaik” dan bukan mengganti H4 dengan
filter lain. Jalur yang dirancang adalah **event-first conditional scalping
research**:

    market profiling yang sudah ada
      -> kamus event harga yang kecil dan eksplisit
      -> konteks pra-entry (informasi sampai t0)
      -> outcome maju pendek yang dapat dieksekusi
      -> biaya dan urutan barrier
      -> discovery terbatas
      -> hipotesis baru yang dikunci
      -> confirmation temporal terpisah
      -> shadow/paper trading bila dan hanya bila lolos

Unit riset bukan indikator atau candle tunggal, melainkan konteks yang tersedia
pada atau sebelum t0, event harga yang dapat didefinisikan sebelum outcome, dan
distribusi outcome t1 sampai tH setelah biaya.

Tujuannya mencari micro-edge yang cukup besar untuk membayar bid/ask, spread
yang berubah, slippage stres, dan friksi eksekusi. Jika tidak ada, hasil
negatif adalah keluaran benar; desain ini melarang pemaksaan strategi.

## 2. Kontrak anti-penyelamatan H4

1. Tidak ada H4 filter, daftar jam H4, ambang EV H4, atau hasil H4b yang boleh
   memilih event baru.
2. H4 hanya boleh muncul sebagai kolom deskriptif pasif, tidak boleh
   mengizinkan, menolak, mengarahkan, atau mengubah ukuran trade.
3. Spread normal, volatilitas, pullback, atau lokasi adalah **hipotesis baru**,
   bukan nama baru untuk subset H4 yang tampak baik.
4. Dilarang menukar median ke mean, pool ke sub-sel, tahun ke sesi, atau gross
   ke net setelah hasil terlihat.
5. Kegagalan kandidat baru tidak memberi hak membuka varian baru segera.
   Kandidat berikut berasal dari ledger discovery berbeda dan melewati pagar
   yang sama.

Dengan demikian sistem tetap micro-execution, tetapi tidak berubah menjadi
sniper/filter H4 yang frekuensinya hilang.

---

## 3. Audit adversarial sebelum rancangan ditulis

Ini serangan terhadap rancangan, bukan promosi rancangan. Kontrol harus dapat
diaudit; jika tidak dapat diimplementasikan atau diverifikasi, jalur terkait
tidak boleh dimulai.

| Serangan | Cara desain menipu diri sendiri | Kontrol mengikat | STOP bila |
|---|---|---|---|
| P-hacking event | Menguji puluhan pola, jendela, sesi, dan threshold lalu menyimpan pemenang. | Maksimal tiga keluarga event per ronde; satu kandidat per keluarga; semua hasil negatif disimpan. | Event/threshold muncul setelah confirmation dibuka. |
| Look-ahead | Candle sesudah t0 membentuk trigger, swing, volatilitas, atau lokasi. | Semua feature entry direkonstruksi dari data sampai t0; evaluator outcome terpisah. | Mutasi data setelah t0 mengubah sinyal t0. |
| Biaya palsu | Buy memakai close BID, spread rata-rata harian, atau biaya nol. | BUY ask ke bid; SELL bid ke ask; spread event-time; observed/conservative/stress cost. | Kandidat positif hanya secara gross. |
| Overlap/n palsu | Ratusan event berdekatan diperlakukan independen. | Cluster per hari plus embargo event; interval per day-block atau agregasi per hari. | Kesimpulan hilang pada unit hari. |
| Subgroup mining | Setelah negatif, pilih London/jam/ATR/tahun yang baik. | Kondisi harus ada di ledger sebelum outcome; confirmation menguji kondisi beku. | Kondisi pertama kali muncul dalam hasil confirmation. |
| TP/SL grid mining | Banyak barrier dicoba sampai ada yang menang. | Ladder hanya geometri discovery; satu paket barrier dikunci sebelum confirmation. | Barrier confirmation berbeda dari barrier terpilih discovery. |
| Survivorship waktu | 2026 dipakai atau 2023 yang tidak nyaman dibuang. | 2026 dilarang; 2023-H1 regime khusus; 2023-H2 replikasi terpisah. | Data 2026 atau eksklusi pasca-hasil masuk. |
| Bukti temp | Harness/JSON hilang di folder temp. | Harness, manifest, command, JSON, stdout, hash dipromosikan ke repo evidence sebelum vonis. | Bukti hanya ada di temp saat auditor perlu replikasi. |
| Paper alpha | Backtest menang tetapi keputusan/fill nyata tidak mungkin. | Shadow dan paper memakai kontrak sinyal, timestamp, bid/ask, serta log sama. | Replay dan log real-time tidak dapat direkonsiliasi. |
| Identity drift | Metrik membaik karena hampir semua peluang dibuang. | Laporkan opportunity rate dan semua alasan reject; no-trade rule harus lulus confirmation. | Frekuensi mati tanpa hipotesis beku. |

**Putusan red-team awal:** jalur ini hanya sah sebagai program riset berpagar.
Risiko utama bukan kurang indikator, melainkan kebebasan memilih event, kondisi,
dan exit setelah melihat outcome.

---

## 4. Kesesuaian dengan EDA_SCALPING.md

Dokumen sumber benar: EDA lama adalah market profiling, sedangkan scalping
memerlukan event dan outcome pendek. Ia menjadi bahan discovery, bukan bukti
edge atau strategi siap pakai.

| Gagasan | Keputusan | Pagar |
|---|---|---|
| Pre-entry, trigger, forward outcome | Diterima sebagai inti | Sinyal dari masa lalu sampai t0, outcome dipisah total. |
| Horizon 1,2,3,5,10,15,20 candle | Diterima untuk peta discovery | Satu horizon/barrier dibekukan sebelum confirmation. |
| MFE/MAE/waktu ekstrem | Diterima | Bid/ask-aware; evaluasi saja, bukan filter entry. |
| TP-before-SL | Diterima dengan koreksi | Urutan intrabar eksplisit; urutan ambigu tidak dianggap win. |
| Biaya event-time | Gate mutlak | Observed, konservatif, dan stres. |
| Session/volatilitas/lokasi | Diterima terbatas | Low-cardinality; bukan perkalian bebas semua fitur. |
| Cari kondisi gagal | Diterima | Failure map setara pentingnya dengan winner map. |
| Banyak indikator/pattern | Ditolak sebagai titik awal | Boleh hanya bila memberi informasi baru pada holdout. |
| Grid TP/SL | Hanya geometri discovery | Bukan optimasi strategi. |

---

## 5. Data dan pembagian temporal

### 5.1 Sumber yang diizinkan

- USDJPY M1 sebagai event dan outcome mikro.
- M5/M15 hanya konteks yang tersedia pada atau sebelum t0.
- Harga dan spread tervalidasi dari proyek.
- Raw immutable; setiap turunan punya manifest SHA-256.
- Data 2026 **dilarang** sampai offset historisnya ditutup.

### 5.2 Split yang disarankan

| Blok | Peran | Boleh | Dilarang |
|---|---|---|---|
| 2024 | Discovery utama | Ledger event, outcome mapping, pilih maks. satu kandidat per keluarga. | Klaim edge atau memakai 2025 untuk menyetel kandidat. |
| 2025 | Confirmation temporal | Uji kandidat dan kontrak yang telah beku. | Memilih event, threshold, jam, horizon, atau barrier baru. |
| 2023-H2 | Replikasi mundur terpisah | Uji transportabilitas setelah 2024 ke 2025 selesai. | Menyelamatkan kegagalan 2025. |
| 2023-H1 | Audit regime khusus | Analisis terpisah sampai perbedaan sesi dijelaskan. | Menjadi denominator kelulusan. |
| 2026 | Tidak digunakan | Tidak ada. | Semua discovery/confirmation/paper threshold. |

2024 dan 2025 adalah dua tahun penuh paling langsung untuk walk-forward.
2023 tidak dibuang diam-diam; 2023-H1 tidak layak menjadi penentu hingga
anomali sesinya tertutup.

---

## 6. Kamus pertanyaan EDA scalping

### Q0 — Apakah data mendukung outcome mikro?

- Berapa observasi per tahun, hari, jam, sesi, dan kondisi spread?
- Seberapa sering zero return, gap, bar parsial, dan spread ekstrem muncul?
- Dapatkah event dipetakan ke keputusan sebelum outcome dimulai?
- Berapa proporsi event yang overlap?

Output: coverage table, gap/missingness table, distribusi spread event-time,
dan daftar kondisi yang tidak menentukan urutan harga.

### Q1 — Apakah displacement maju cukup gross dan net?

Untuk setiap event: return arah +1/+2/+3/+5/+10/+15/+20 M1; MFE/MAE;
net displacement setelah observed/conservative/stress cost; proporsi MFE yang
melampaui biaya; median dan quantile, bukan hanya rata-rata.

**Falsifikasi:** bila MFE umumnya di bawah biaya efektif, keluarga event gugur
walaupun close-to-close gross positif.

### Q2 — Barrier mana disentuh dahulu?

Discovery boleh memetakan ladder kecil target/risiko relatif ATR M1 atau pip.
Tujuannya bukan memilih pasangan paling menguntungkan, melainkan mengukur
urutan barrier, waktu barrier, proporsi urutan ambigu, dan efek biaya.
Satu paket entry/stop/target/time-stop baru dipilih tertulis dan dikunci
sebelum confirmation.

### Q3 — Konteks pra-entry apa yang membedakan outcome?

Konteks kecil yang boleh dihitung di t0: path return -1/-3/-5/-10/-20;
expansion/compression dibanding baseline selesai; lokasi terhadap high/low
rolling yang selesai; spread serta percentile spread masa lalu; bucket waktu;
dan satu kategori volatilitas pra-t0 yang tidak memakai outcome atau
rv_regime_flag/TAU terlarang.

### Q4 — Kapan event sama gagal?

Failure map wajib membandingkan gross/net, biaya normal/stres, state
volatilitas pra-t0, location, tahun, dan cluster hari. Failure map tidak
memberi hak membuang sel buruk lalu mengklaim subset sebagai edge.

### Q5 — Apakah effect stabil?

Uji arah effect 2024 vs 2025, agregasi unit hari, biaya stres, kontribusi satu
hari/sesi, serta definisi event ekuivalen secara ekonomi. Jawaban negatif
adalah alasan menolak/menahan, bukan tuning.

---

## 7. Tiga keluarga event maksimum per ronde

Tiga keluarga ini bukan rekomendasi trade. Ini ruang Discovery-R1 yang cukup
kecil untuk diaudit. Ronde pertama tidak boleh menambah keluarga keempat.

### E1 — Exhaustion-to-reversal

**Mekanisme yang diuji:** setelah dorongan satu arah yang telah meluas, apakah
penolakan/reversal yang telah selesai pada penutupan t0 menghasilkan gerakan
berlawanan cukup besar sebelum adverse move dan biaya?

Feature yang boleh masuk: run length pra-t0, signed displacement, body/wick/
range t0, posisi terhadap range rolling sebelumnya, spread, dan volatilitas
yang telah selesai sebelum t0.

**Falsifikasi:** reversal baru dapat diketahui sesudah future swing terbentuk,
atau MFE tidak melewati biaya/MAE pada horizon pendek.

### E2 — Pullback-then-continuation

**Mekanisme yang diuji:** setelah expansion yang diketahui pada masa lalu,
apakah pullback kecil yang selesai pada t0 lebih sering kembali searah dorongan
awal sebelum invalidasi?

Feature yang boleh masuk: displacement pra-t0, kedalaman pullback relatif
range/ATR yang tersedia, jumlah bar pullback, penutupan t0, biaya, dan lokasi
terhadap range yang selesai.

**Falsifikasi:** arah awal memakai future high/low, atau net outcome tidak
mengalahkan biaya stres.

### E3 — Compression-to-expansion

**Mekanisme yang diuji:** setelah kompresi rentang yang telah selesai, apakah
break pada t0 mempunyai continuation netto sebelum false break/adverse barrier?

Feature yang boleh masuk: range/realised volatility rolling masa lalu, break
distance pada t0, close location, spread, dan waktu.

**Falsifikasi:** break didefinisikan memakai range setelah t0, atau barrier
race net tidak lebih baik daripada baseline unconditional.

**Larangan bersama E1-E3:** RSI, MACD, EMA, candle-name, atau pola vendor
tidak ditambahkan hanya karena populer. Mereka hanya boleh menjadi representasi
sekunder bila mekanisme event telah menemukan effect dan feature tersebut
menambah informasi pada holdout tanpa kebebasan tersembunyi.

---

## 8. Kontrak outcome dan eksekusi

### 8.1 Timestamp yang tidak ambigu

| Tahap | Definisi |
|---|---|
| t0 close | Penutupan bar event. Semua feature keputusan telah tersedia. |
| decision time | Tepat setelah t0 close; catat UTC dan broker time. |
| entry time | Bar/tick pertama yang realistis dapat dieksekusi setelah keputusan. |
| exit time | Trigger SL, TP, time-stop, atau cancellation yang didefinisikan sebelumnya. |

Jika data hanya OHLC M1 dan dua barrier terlewati dalam bar yang sama tanpa
urutan bid/ask, event diberi label AMBIGUOUS_SEQUENCE. Ia tidak boleh diam-diam
dihitung sebagai win atau loss. Opsi yang sah: buang dari evaluasi dengan
hitungan eksplisit, pakai worst case yang dilabel, atau kumpulkan tick untuk
ronde khusus. Opsi dipilih sebelum confirmation.

### 8.2 Biaya dan sisi harga

| Posisi | Entry | Exit |
|---|---|---|
| BUY | ASK | BID |
| SELL | BID | ASK |

Biaya dilaporkan selalu tiga lapis:

1. **Observed:** spread per event yang tersedia pada dataset.
2. **Conservative:** observed ditambah slippage konservatif yang dibekukan.
3. **Stress:** spread percentile tinggi per sesi atau skenario stres yang
   dibekukan.

Kandidat tidak pernah lulus hanya dari gross. Jika observed net positif tetapi
stress net negatif, status tertinggi adalah TAHAN untuk paper, bukan edge siap
eksekusi.

### 8.3 Output minimum per event

- arah dan identitas event;
- semua feature pra-t0 yang dipakai;
- bid/ask entry dan exit, atau transformasi yang dapat direkonstruksi;
- gross/net return;
- MFE, MAE, time-to-MFE, time-to-MAE;
- outcome pada horizon tetap;
- barrier pertama atau AMBIGUOUS_SEQUENCE;
- session label, spread, scenario biaya, tahun, broker-day;
- event cluster/day identifier dan alasan cancel/reject.

---

## 9. Discovery yang tidak menyamar sebagai confirmation

### 9.1 Ledger discovery

Sebelum kode berjalan, arsitek membuat ledger dengan kolom: event_id,
mekanisme, definisi informasi sampai t0, arah, feature yang diizinkan, outcome,
biaya, horizon, unit bootstrap, eksklusi, alasan ilmiah, dan status.

Event tidak boleh lahir dari chart contoh setelah label outcome terlihat. Chart
boleh menjelaskan definisi, bukan memilih definisi.

### 9.2 Batas eksplorasi

- Maksimal tiga keluarga E1-E3 dalam satu ronde.
- Maksimal satu kandidat per keluarga dibawa keluar dari 2024.
- Semua varian gagal/duplikat dicatat; tidak ada penghapusan dari ledger.
- Context interaction dibatasi satu konteks primer per kandidat pada ronde awal:
  event kali cost state, bukan event kali cost kali session kali day kali
  volatility kali location sekaligus.
- Jika parameter dibutuhkan, grid kecil diumumkan di ledger dan dinilai sebagai
  satu family untuk correction.

### 9.3 Keluaran discovery

Discovery menghasilkan tepat salah satu keluaran:

1. **TOLAK:** tidak ada displacement netto yang dapat dieksekusi.
2. **KANDIDAT:** ada mekanisme dan effect yang layak dipra-registrasi.
3. **BELUM JELAS:** data/urutan/barrier tidak cukup; bukan alasan tuning.

Hanya KANDIDAT boleh masuk spesifikasi confirmation. Kandidat tidak disebut
strategi sebelum lulus confirmation.

---

## 10. Spesifikasi confirmation per kandidat

Setelah discovery 2024 berhenti, arsitek menulis satu spec terpisah untuk tiap
kandidat. Spec wajib memuat:

1. Hash data/input, branch/HEAD, dan manifest toolchain.
2. Definisi event, arah, feature, serta urutan timestamp.
3. Aturan entry, cancel, stop, target, time-stop, dan AMBIGUOUS_SEQUENCE.
4. Harga bid/ask, biaya observed/conservative/stress, dan rumus P&L.
5. Horizon penentu dan metrik primer tunggal.
6. Unit independensi: cluster-day/embargo serta metode interval.
7. Tahun discovery dan confirmation yang beku.
8. Syarat lulus/gugur yang dapat membuat kandidat gagal: biaya stres, minimal
   jumlah hari, effect sign, dan stabilitas harian.
9. Baseline yang didefinisikan sebelum 2025 dibuka: unconditional
   direction-neutral, event-time shuffle yang menjaga cluster, atau placebo
   tanpa future data.
10. Larangan: tanpa tuning, subset baru, 2026, H4 rescue, filter RV/TAU
    terlarang, atau statistik tambahan penentu.

Coder hanya mengeksekusi. Auditor mereplikasi dari nol tanpa impor artefak
hasil coder. Arsitek memvonis hanya setelah keduanya sepakat atau arbitrase
berbukti.

### 10.1 Minimum decision gate

| Gate | Pertanyaan | Alasan |
|---|---|---|
| G1 Causal | Apakah semua input tersedia sebelum entry? | Mencegah look-ahead. |
| G2 Executable | Apakah net observed dan stress tidak meniadakan effect? | Mencegah gross alpha palsu. |
| G3 Sequence | Apakah urutan barrier teridentifikasi atau konservatif? | Mencegah win rate fiktif. |
| G4 Dependence | Apakah effect bertahan dengan unit hari/embargo? | Mencegah n palsu. |
| G5 Temporal | Apakah 2025 mendukung arah yang dipilih 2024? | Mencegah overfit. |
| G6 Robustness | Apakah satu hari/sesi tidak memberi mayoritas hasil? | Mencegah edge satu-kejadian. |
| G7 Operational | Apakah sinyal dapat dibentuk/log real-time? | Mencegah backtest-only strategy. |

Gagal satu gate berarti kandidat **GUGUR**. Tidak ada voting atau rata-rata
gate untuk menyelamatkan kandidat.

---

## 11. Blueprint strategi bila kandidat benar-benar lolos

Blueprint ini belum menentukan parameter. Parameter hanya boleh diisi dari
spesifikasi kandidat yang lulus confirmation. Tujuannya memastikan edge
statistik dapat berubah menjadi sistem paper yang dapat diaudit tanpa berubah
saat berjalan.

### 11.1 Strategy Contract

Satu kandidat lulus diterjemahkan ke kontrak tunggal:

    strategy_id + versi + hash specification
    symbol = USDJPY
    execution timeframe = nilai dari spec
    decision timestamp = aturan t0
    event definition = literal
    direction rule = literal
    entry rule = BID/ASK plus expiry
    cancellation rule = literal
    stop rule = literal
    target rule = literal
    time-stop rule = literal
    cost model = observed/conservative/stress
    no-trade conditions = hanya yang lulus confirmation
    position rule = 0.01 pada demo/paper bila diizinkan

Kontrak tidak boleh memuat “gunakan diskresi”, “ambil yang paling kuat”, atau
“sesuaikan dengan kondisi” tanpa definisi yang dapat dieksekusi sebelum entry.

### 11.2 P0 — Offline replay audit

Tujuan: memastikan strategy contract menghasilkan sinyal identik pada data
sama.

- Run deterministik dua kali dengan output byte-identik.
- Replay menghasilkan decision log untuk setiap event, termasuk yang ditolak.
- Ubah satu bar setelah t0; sinyal t0 tidak boleh berubah.
- Ubah bid/ask skenario biaya; hasil hanya berubah lewat jalur biaya yang
  terdokumentasi.
- Tidak ada order atau koneksi trading.

**Keluar P0:** replay, audit look-ahead, dan accounting bid/ask lulus. Ini
belum paper trading.

### 11.3 P1 — Shadow real-time

Tujuan: menguji apakah sinyal teoritis tersedia tepat waktu pada feed nyata.

- Bot membaca feed tetapi tidak mengirim order.
- Setiap keputusan mencatat decision time UTC, bar/tick input, latency, bid/ask,
  spread, signal fingerprint, accept/reject reason, dan snapshot parameter/hash.
- Shadow exit memakai bid/ask tercatat, bukan close yang dibangun belakangan.
- Setiap hari direkonsiliasi antara log real-time dan replay raw feed;
  perbedaan adalah insiden, bukan noise yang diabaikan.
- Tidak ada adaptasi parameter selama periode shadow.

**Gate P1:** cukup kesempatan lintas hari/sesi sesuai spec, tanpa leakage,
accounting cocok, dan effect net tidak runtuh relatif expectation confirmation.
Angka minimum dikunci sebelum P1, bukan setelah log ada.

### 11.4 P2 — Paper execution / demo terkendali

Tujuan: menguji friksi order, bukan mencari edge baru.

- Hanya setelah persetujuan eksplisit user.
- Lot minimum 0.01; tidak ada martingale, grid, averaging down, atau penambahan
  ukuran setelah rugi.
- Satu strategy version beku; perubahan adalah strategy baru yang kembali ke P0.
- BUY entry ASK dan exit BID; SELL entry BID dan exit ASK.
- Catat request, fill, reject, slippage, spread entry/exit, SL/TP/time-stop,
  decision fingerprint, outcome, dan deviasi broker.
- Stop kondisi riset: mismatch sinyal, log hilang, biaya aktual melewati guard
  spec, atau fill tidak dapat direkonsiliasi.

**Gate P2:** fidelity paper-versus-shadow, biaya nyata-versus-model,
fill/cancel integrity, outcome distribution, dan frekuensi. Profit nominal
sendiri tidak cukup.

### 11.5 Tidak ada lompatan ke live

Lolos P2 bukan izin live. Ia hanya menghasilkan paket bukti untuk ronde
graduation baru: audit strategi A-H, red-team eksekusi, replikasi, dan putusan
user. Live di luar rancangan ini.

---

## 12. Telemetri dan rantai bukti paper

Setiap keputusan minimal menyimpan:

    run_id, strategy_id, strategy_hash, data_manifest_hash,
    decision_time_utc, broker_time, event_id, event_time,
    features_hash, context_bucket, signal, reject_reason,
    bid_at_decision, ask_at_decision, spread_at_decision,
    entry_request_time, entry_fill_time, entry_bid, entry_ask,
    exit_reason, exit_time, exit_bid, exit_ask,
    gross_pips, cost_pips, net_pips, slippage_pips,
    mfe_pips, mae_pips, barrier_sequence_status,
    mode=offline|shadow|paper, code_commit, environment_fingerprint

Ketentuan bukti:

1. Raw log append-only dan rotasi bulanan.
2. Manifest hash keluar sebelum run, bukan dari laporan akhir.
3. Script, harness, JSON hasil, dan stdout berada di repo evidence atau arsip
   ber-checksum, bukan hanya folder temp.
4. Laporan membedakan fakta log, perhitungan turunan, dan interpretasi.
5. Logging gagal berarti run gagal; trade tidak boleh direkonstruksi diam-diam
   dari chart atau memori.

---

## 13. Governance dan urutan peran

| Fase | Arsitek | Coder | Auditor | CTO / gate disk |
|---|---|---|---|---|
| Ledger discovery | Tetapkan pertanyaan dan batas eksplorasi. | Tidak menulis strategi. | Serang definisi/pagar. | Pastikan input, state, baseline jelas. |
| Discovery | Kunci ruang pertanyaan. | Jalankan notebook/harness sesuai ledger. | Audit bias dan accounting. | Tolak klaim edge. |
| Candidate spec | Pilih/tolak kandidat dengan alasan tertulis. | Tidak menentukan ambang. | Uji apakah spec dapat digame. | Hash/manifest/preflight. |
| Confirmation | Tidak mengubah kode. | Eksekusi spec. | Replikasi independen. | Artefak lengkap, baseline Git disebut. |
| Putusan | Vonis. | Tidak memvonis. | Temuan adversarial. | Putusan tidak merembet scope. |
| Shadow/Paper | Setujui kontrak dan gate. | Implementasi setelah persetujuan. | Audit telemetry/fill. | Rekonsiliasi disk/runbook. |

Tidak ada peran boleh mengubah definisi kandidat di antara discovery dan
confirmation. Konflik mengikuti AGENTS.md: bukti dahulu, arsitek kedua, uji
tambahan bila perlu, user bila tetap ambigu.

---

## 14. Artefak riset yang kelak diperlukan

Ini daftar desain, bukan perintah implementasi. Setiap file baru kelak harus
melewati Reuse-First.

    reports/governance/YYYY-MM-DD/arsitek/
      spesifikasi-discovery-event-rN.md
      spesifikasi-confirmation-candidate.md
    reports/research/YYYY-MM-DD/round/
      ledger_events.csv
      manifest.json
      discovery_report.md
      candidate_outcomes.parquet
      confirmation_report.md
      evidence/
        commands.txt
        stdout/
        json/
        hashes.sha256
    strategies/candidate/
      contract.md
    reports/paper/YYYY-MM-DD/strategy-version/
      runbook.md
      reconciliation.md
      daily/

Discovery, confirmation, dan paper tidak boleh bercampur folder atau bukti.

---

## 15. Urutan kerja setelah user menyetujui desain

1. **Tutup status H4b secara formal lebih dahulu.** Ia tidak menjadi bahan
   pemilihan kandidat fresh; ini mencegah dua rantai governance aktif saling
   mencemari.
2. **Arsitek menulis ledger Discovery-R1** untuk E1/E2/E3: definition-time,
   grid terbatas jika perlu, treatment overlap, dan output negatif wajib.
3. **Auditor mengaudit spec sebelum coder bekerja.** Fokus: leakage, future
   swing, multiple-testing budget, barrier ambiguity, bid/ask, split 2024/2025.
4. **Coder menjalankan discovery 2024 saja** dan menulis evidence lengkap.
5. **Auditor mereplikasi atau menyerang discovery.** Hasil: TOLAK, KANDIDAT,
   atau BELUM JELAS.
6. Untuk setiap KANDIDAT, **arsitek menulis confirmation spec 2025** dengan
   kontrak tunggal dan gate G1-G7.
7. Coder dan auditor menyelesaikan confirmation tanpa mengubah kandidat.
8. Hanya kandidat yang lulus semua G1-G7 memperoleh blueprint P0.
9. P0 ke P1 ke P2 selalu memerlukan keputusan user di antaranya. Tidak ada
   otomatisasi menuju demo atau live.

---

## 16. Kriteria keberhasilan dan kriteria berhenti

### Keberhasilan yang sah

Program berhasil bila menghasilkan salah satu berikut:

- kandidat dengan effect net yang terkonfirmasi temporal dan bisa dieksekusi
  melalui P0/P1;
- bukti kuat bahwa tiga mekanisme awal tidak membayar biaya pada USDJPY untuk
  horizon ini; atau
- diagnosis integritas data/eksekusi yang membuat riset belum dapat diuji.

Keluaran kedua dan ketiga tetap keberhasilan ilmiah karena mengurangi ruang
ilusi.

### Berhenti / reset desain

Program berhenti dan kembali ke arsitek bila:

- ketiga keluarga E1-E3 gagal G1/G2 pada 2024;
- evidence chain atau reproduksibilitas rusak;
- data tidak dapat menentukan urutan barrier dalam proporsi material;
- biaya observed/stress menghapus semua displacement;
- confirmation 2025 tidak mendukung kandidat discovery; atau
- discovery perlu memperbanyak fitur/kondisi melewati budget hanya untuk
  menemukan satu hasil positif.

“Tambah indikator” bukan respons default. Respons yang sah adalah hipotesis
mekanistik baru, audit spec, dan ronde baru bila user menyetujui.

---

## 17. Self-audit desain 3x adversarial

### Putaran 1 — Correctness

- Desain membedakan putusan H4 historis dari asumsi kerja H4 gagal; tidak
  mengedit atau membatalkan vonis lama.
- Data 2026 tidak masuk seluruh jalur; 2023-H1 tidak menjadi denominator.
- Bid/ask, event-time cost, dan ambiguity intrabar adalah kontrak, bukan
  catatan kaki.
- Input entry dibatasi masa lalu sampai t0; outcome eksplisit sesudah entry.
- Paper path dipisah menjadi P0 offline, P1 shadow, dan P2 demo.

### Putaran 2 — Bias dan asumsi

- Tidak ada asumsi candle pattern/indikator memiliki edge tanpa data lokal.
- E1-E3 adalah hipotesis mekanistik, bukan setup yang direkomendasikan.
- Batas tiga keluarga dan satu kandidat per keluarga sengaja mengorbankan
  cakupan untuk mengurangi multiple testing.
- Tidak ada ambang universal yang dibuat-buat; setiap ambang dipra-registrasi
  dari kapasitas data yang nyata.
- H4 tidak memiliki jalur penyelamatan melalui context/filter.

### Putaran 3 — Meta-check

- Dokumen tidak mengotorisasi kode, eksperimen, config, staged file, commit,
  paper order, atau live trade.
- Keputusan material ditempatkan pada arsitek/user, bukan coder.
- Folder temp dinilai risiko, bukan evidence store.
- Kriteria berhenti eksplisit; kegagalan tidak berarti optimasi tanpa batas.

---

## 18. Keputusan yang perlu dari user sebelum Discovery-R1

1. Apakah E1 exhaustion-to-reversal, E2 pullback-then-continuation, dan E3
   compression-to-expansion disetujui sebagai **satu-satunya** ruang
   Discovery-R1?
2. Apakah split 2024 discovery ke 2025 confirmation disetujui, dengan 2023-H2
   hanya robustness mundur dan 2023-H1/2026 di luar denominator?
3. Apakah jalur paper harus tetap P0 offline ke P1 shadow ke P2 demo 0.01,
   dengan keputusan user eksplisit pada setiap transisi?
4. Apakah harness/JSON/stdout wajib dipindahkan dari folder temp ke repo
   evidence sebelum auditor mulai, walaupun ukuran arsip bertambah?

Tidak ada eksekusi sebelum empat keputusan ini, atau pengganti yang setara,
dikunci dalam spesifikasi Discovery-R1.

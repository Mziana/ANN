Iya, kalau pertanyaannya adalah “apakah EDA ini sudah cukup untuk mencari edge scalping?”, saya cenderung bilang belum.

Tapi saya tidak akan menyimpulkan bahwa sampelnya terlalu sedikit. Justru 1.347.847 bar M1 selama 4 tahun itu besar. Yang lebih tepat:

Sampelnya besar, tetapi pertanyaan yang diajukan EDA relatif sempit dan lebih banyak menggambarkan karakteristik pasar secara umum daripada mekanisme edge scalping.

Kenapa begitu?

EDA yang sekarang banyak menjawab pertanyaan seperti:

bagaimana distribusi return USDJPY?
seberapa tebal tail?
kapan volatilitas tinggi?
bagaimana spread?
apakah ada autokorelasi?
berapa banyak swing?
apakah level tertentu lebih sering menghasilkan reaksi?
apakah ada perbedaan regime?

Itu bagus sebagai fondasi market profiling.

Tetapi scalping biasanya membutuhkan pertanyaan yang jauh lebih dekat dengan kejadian entry → beberapa menit/bar berikutnya → exit.

Misalnya:

“Setelah kondisi X muncul pada M1, apa yang biasanya terjadi dalam 1, 2, 3, 5, 10 candle berikutnya?”

atau:

“Ketika terjadi rejection setelah spread normal dan volatilitas tertentu, berapa probabilitas harga bergerak +N pip sebelum bergerak -N pip?”

atau:

“Apakah kondisi tertentu memberikan excursion yang cukup besar untuk membayar spread + slippage?”

Nah, pertanyaan seperti itu belum menjadi fokus utama EDA yang sekarang.

Ini penting: bukan berarti EDA sekarang salah

Saya malah melihat EDA sekarang sebagai lapisan pertama.

Dia menjawab:

“USDJPY ini sebenarnya seperti apa?”

Sedangkan untuk scalping kita perlu lapisan berikutnya:

“Ketika kejadian tertentu terjadi, apa yang biasanya terjadi sesudahnya dalam jangka sangat pendek?”

Itu dua pertanyaan yang berbeda.

Contohnya Q4 menemukan:

M15 VR = 1,0337

Itu memberi tahu kita bahwa secara agregat ada sedikit kecenderungan momentum pada M15.

Tetapi scalper sebenarnya mungkin lebih membutuhkan:

“Setelah candle M1 seperti X muncul, apakah 1–5 candle berikutnya lebih sering melanjutkan atau berbalik?”

VR 1,0337 tidak bisa menjawab pertanyaan tersebut secara langsung.

Bahkan Q5 sebenarnya sudah mulai mendekati scalping

Q5 menemukan sekitar 49 swing per hari dan median jarak antar-swing tertentu.

Itu menarik untuk scalping.

Tetapi EDA berhenti pada:

“Berapa sering swing terjadi?”

Scalper membutuhkan pertanyaan lanjutan:

“Setelah swing terbentuk, apa yang terjadi 1, 2, 3, 5, 10 candle kemudian?”

Misalnya:

Swing low → 1 candle → 2 candle → 3 candle → 5 candle

Kemudian ukur:

MFE
MAE
maximum favorable move
maximum adverse move
berapa pip bergerak sebelum balik
berapa lama bertahan
apakah spread masih memungkinkan
apakah target kecil seperti 1–3 pip punya edge

Nah, itu jauh lebih dekat dengan kebutuhan scalping.

Jadi masalahnya lebih tepat disebut apa?

Saya akan membedakannya seperti ini:

Aspek	EDA sekarang	Kebutuhan scalping
Jumlah data	Besar	Cukup
Timeframe	M1/M5/M15	M1 sangat penting
Market profiling	Bagus	Dibutuhkan
Distribusi return	Sudah	Dibutuhkan
Spread/biaya	Sudah	Sangat penting
Regime	Sudah	Penting
Autokorelasi	Sudah	Berguna, tapi terlalu agregat
Swing	Sudah	Baru fondasi
Event → future outcome	Masih terbatas	Sangat penting
MFE/MAE	Belum menjadi fokus	Sangat penting
TP vs SL dalam horizon pendek	Belum	Sangat penting
1–20 candle setelah entry	Belum menjadi fokus	Sangat penting
Spread/slippage terhadap edge kecil	Belum diuji sebagai edge event	Sangat penting
Conditional edge	Terbatas	Sangat penting
Jadi saya tidak akan membuang EDA ini

Justru urutannya menurut saya lebih sehat kalau:

EDA sekarang

↓
Market profiling

↓
Cari event/kejadian yang berulang

↓
Forward outcome analysis

↓
MFE/MAE

↓
Horizon 1–20 candle

↓
biaya spread + slippage

↓
baru hipotesis scalping

↓
uji falsifikasi

Dengan begitu kita tidak langsung membuat:

“Kalau RSI < 30 BUY.”

Tetapi mencari dulu:

“Ketika kondisi tertentu terjadi, apakah memang ada ketidakseimbangan probabilitas beberapa candle setelahnya?”

Dan ada satu hal yang menurut saya sangat penting untuk proyek Anda

Dari laporan sekarang, kesimpulan:

“tidak ada autokorelasi yang bisa ditradingkan”

jangan diterjemahkan menjadi:

“USDJPY tidak cocok untuk scalping.”

Itu terlalu jauh.

Yang bisa dikatakan dari EDA tersebut adalah kira-kira:

“Tidak ditemukan autokorelasi linear agregat yang cukup kuat untuk langsung dijadikan edge.”

Scalping bisa saja mendapatkan edge yang conditional, misalnya hanya setelah kondisi tertentu:

session + volatility + spread + candle structure + lokasi harga + kondisi sebelumnya

Bisa jadi secara keseluruhan autokorelasi hampir nol, tetapi pada subset tertentu terdapat pola yang cukup kuat.

Dan justru itulah pertanyaan yang belum benar-benar dijawab oleh EDA sekarang.

Jadi kalau tujuan akhir proyek ini memang mencari metode scalping USDJPY, saya akan mengatakan:

EDA sekarang belum terlalu sempit sebagai market study. Tetapi memang masih terlalu umum untuk dijadikan EDA khusus pencarian edge scalping.

Dan menurut saya ini bukan alasan untuk mengulang dari nol. Lebih masuk akal menambahkan EDA tahap berikutnya yang khusus menjawab “apa yang terjadi setelah suatu event pada horizon pendek?”.

Iya. Kalau tujuan kita mencari edge scalping, candle sebelum entry justru sangat penting untuk diperiksa.

Bahkan saya akan memperluasnya sedikit: jangan hanya melihat candle tepat sebelum entry, tetapi lihat beberapa candle sebelum entry sebagai konteks.

Contohnya, jangan hanya bertanya:

“Candle entry ini bullish atau bearish?”

Tetapi:

“Sebelum candle entry muncul, harga sedang melakukan apa?”

Kenapa candle sebelumnya penting?

Karena candle entry yang sama bisa mempunyai arti berbeda tergantung apa yang terjadi sebelumnya.

Misalnya ada candle bullish besar.

Kondisi A:

↓ ↓ ↓ ↓ → candle bullish

Candle bullish muncul setelah beberapa candle turun.

Itu bisa berarti sesuatu yang berbeda dibanding:

Kondisi B:

↑ ↑ ↑ ↑ → candle bullish

Di sini candle bullish muncul setelah harga sudah naik beberapa candle.

Secara bentuk, candle terakhir sama-sama bullish, tetapi konteksnya berbeda.

Kalau kita hanya memasukkan candle entry ke penelitian, kita bisa mencampurkan dua situasi yang sebenarnya berbeda.

Untuk penelitian scalping, saya justru akan melihat “urutan kejadian”

Misalnya kita ingin mengetahui apakah ada edge setelah suatu kondisi.

Kita bisa membagi data seperti:

Konteks sebelum entry

Candle -5 → -4 → -3 → -2 → -1

↓

Event / kondisi entry

Candle 0

↓

Apa yang terjadi setelahnya

+1 → +2 → +3 → +5 → +10 → +20 candle

Jadi kita bisa menjawab:

“Setelah kondisi seperti ini terjadi, apa yang biasanya terjadi dalam beberapa candle berikutnya?”

Ini jauh lebih cocok untuk penelitian scalping daripada hanya melihat statistik pasar secara keseluruhan.

Bahkan candle sebelumnya bisa membantu kita menghindari “entry terlambat”

Ini bagian yang menurut saya sangat relevan dengan pertanyaan Anda.

Misalnya ternyata penelitian menemukan:

Setelah 3 candle bearish berturut-turut, muncul bullish reversal dan rata-rata 3 candle berikutnya bergerak naik.

Jangan langsung membuat:

“Kalau ada bullish candle → BUY.”

Karena bisa jadi bullish candle tersebut sudah merupakan candle yang terlambat.

Kita perlu melihat:

seberapa jauh harga sudah bergerak sebelum entry,
apakah momentum sudah terlalu jauh,
apakah candle sebelumnya sudah menunjukkan tanda exhaustion,
apakah entry terjadi setelah expansion candle,
apakah spread sedang normal,
berapa jauh harga bergerak setelah entry sebelum berbalik.

Jadi kita bukan hanya mencari:

“kapan benar masuk?”

tetapi juga:

“kapan seharusnya TIDAK masuk meskipun sinyal terlihat benar?”

Itu sangat penting untuk scalping.

Saya bahkan akan membagi penelitian menjadi 3 bagian
1. Sebelum entry — CONTEXT

Contohnya:

arah beberapa candle sebelumnya
jumlah candle bullish/bearish berturut-turut
besar return masing-masing candle
range candle
acceleration/deceleration
posisi harga relatif terhadap range sebelumnya
volatilitas
spread
session
ATR
struktur swing
2. Candle/event entry — TRIGGER

Contohnya:

reversal
breakout
rejection
momentum continuation
perubahan arah
kondisi tertentu yang ditemukan EDA
3. Setelah entry — OUTCOME

Misalnya horizon:

1, 2, 3, 5, 10, 15, 20 candle

Kemudian ukur:

MFE
MAE
return
maksimum naik
maksimum turun
waktu mencapai target
apakah TP tercapai sebelum SL
dampak spread/slippage
Jadi bentuk pertanyaan EDA berikutnya menurut saya seharusnya berubah

Bukan hanya:

“Bagaimana karakter USDJPY?”

tetapi:

“Ketika pola tertentu muncul, dengan konteks beberapa candle sebelumnya, apa yang secara konsisten terjadi setelahnya?”

Dan ini juga menjaga kita dari kesalahan yang sangat umum:

melihat hasil setelah entry lalu mencari-cari pola yang kelihatan bagus.

Semua kondisi yang dipakai untuk menentukan entry harus berasal dari informasi yang sudah tersedia sebelum entry. Data setelah entry hanya boleh digunakan untuk mengukur hasilnya, bukan untuk menentukan sinyal.

Jadi iya, candle sebelum entry wajib kita lihat kalau target akhirnya adalah scalping yang tidak asal masuk.

Malah saya akan bilang: “pre-entry context → entry event → post-entry outcome” sebaiknya menjadi kerangka utama EDA scalping tahap berikutnya.

lalu apalagi yang dibutuhkan untuk memaksimalkan EDA meneliti mode scalping ini?

Iya. Kalau targetnya sekarang memaksimalkan EDA khusus untuk menemukan edge scalping USDJPY, saya tidak akan sekadar menambah indikator. Yang perlu diperluas adalah cara kita mendefinisikan kejadian, konteks sebelum entry, apa yang terjadi sesudahnya, dan biaya untuk benar-benar mengeksekusinya.

Menurut saya kerangkanya bisa dibuat seperti ini:

1. Pre-entry context — apa yang terjadi sebelum entry

Ini yang baru kita bahas, dan menurut saya wajib.

Jangan hanya candle -1, tetapi misalnya jendela:

-20 → -10 → -5 → -3 → -2 → -1 → entry

Yang dicari:

arah return sebelumnya
jumlah candle naik/turun berturut-turut
besar masing-masing candle
range candle
acceleration/deceleration
apakah baru terjadi expansion candle
apakah momentum sedang menguat atau melemah
posisi harga terhadap swing sebelumnya
jarak dari high/low sebelumnya
volatilitas sebelum entry
spread sebelum entry

Tujuannya:

Jangan sampai kita menganggap sebuah candle sebagai sinyal padahal sebenarnya candle tersebut hanya bagian akhir dari pergerakan yang sudah terlalu jauh.

2. Entry event — tentukan sebenarnya “kejadian” apa yang sedang diuji

Ini sangat penting.

EDA jangan dimulai dari:

“Kita coba RSI, MACD, EMA, lalu lihat mana yang profit.”

Lebih sehat kalau dimulai dari event yang terjadi pada harga.

Contoh:

reversal setelah beberapa candle searah
breakout range
rejection high/low
expansion → contraction
momentum continuation
swing high/low
perubahan arah return
consecutive candles
candle dengan range ekstrem
pullback setelah expansion

Lalu setiap event diberi identitas.

Misalnya:

EVENT-001 = 3 bearish M1 berturut-turut + bullish reversal.

Kemudian kita lihat apa yang terjadi setelah EVENT-001.

Dengan begitu EDA mencari perilaku pasar, bukan mencari indikator yang kebetulan cocok.

3. Post-entry outcome — ini menurut saya kekurangan terbesar EDA sekarang

Setelah event terjadi, kita harus melihat apa yang terjadi pada:

+1, +2, +3, +5, +10, +15, +20 candle

Misalnya event terjadi pada candle 0.

Kita ukur:

Horizon	Apa yang terjadi?
+1	return
+2	return
+3	return
+5	return
+10	return
+20	return

Tetapi jangan berhenti di return.

Kita juga perlu:

MFE — seberapa jauh harga sempat bergerak menguntungkan
MAE — seberapa jauh harga sempat bergerak melawan
waktu mencapai MFE
waktu mencapai MAE
maximum favorable excursion
maximum adverse excursion

Ini sangat penting untuk scalping.

Karena strategi scalping tidak membutuhkan harga benar dalam 1 jam.

Yang kita butuhkan mungkin:

“Setelah event ini, harga lebih sering bergerak +3 pip sebelum -2 pip dalam 5 candle berikutnya.”

Itu jauh lebih relevan.

4. Urutan TP/SL

Ini berbeda dari sekadar win rate.

Misalnya:

Event A

Harga:

Entry → -1 pip → +5 pip → +7 pip

dan

Event B

Entry → +1 pip → -5 pip

Keduanya bisa menghasilkan statistik berbeda meskipun return akhirnya terlihat mirip.

Kita perlu mengetahui:

Apakah TP tercapai lebih dahulu daripada SL?

Contohnya uji:

TP +1 pip vs SL -1 pip
TP +2 vs SL -1
TP +3 vs SL -1
TP +5 vs SL -2
dst.

Bukan untuk memilih TP terbaik dulu, tetapi untuk memetakan bentuk peluang setelah event.

5. Biaya eksekusi

Ini wajib untuk scalping.

Karena edge scalping bisa sangat kecil.

Kita harus memasukkan:

spread
slippage
commission
kondisi spread saat event terjadi
spread percentile
kemungkinan spread melebar

Misalnya EDA menemukan:

Gross edge = +0,8 pip.

Kelihatannya bagus.

Tetapi kalau:

spread + slippage = 1,0 pip

maka edge tersebut sebenarnya tidak cukup.

Jadi pertanyaan EDA bukan hanya:

“Apakah ada pola?”

tetapi:

“Apakah pola tersebut masih ada setelah biaya eksekusi?”

6. Market regime

Temuan EDA lama tentang regime jangan dibuang.

Justru kita gunakan sebagai kondisi.

Misalnya event yang sama diuji berdasarkan:

London
New York
Asia
volatilitas rendah
normal
volatilitas tinggi
spread rendah
spread tinggi

Karena sangat mungkin:

Event yang tidak memiliki edge secara keseluruhan ternyata memiliki edge pada kondisi tertentu.

Ini yang tadi kita bicarakan sebagai conditional edge.

7. Session dan waktu yang jauh lebih detail

EDA sekarang sudah melihat session.

Untuk scalping, kita bisa mempersempit lagi.

Misalnya:

setiap jam
30 menit
15 menit
opening London
opening New York
overlap London–NY
menjelang sesi berakhir

Tujuannya bukan mencari jam yang “paling profit”.

Tujuannya mencari tahu:

Apakah perilaku setelah event berubah tergantung waktu?

8. Spread sebagai bagian dari kondisi entry

Ini menurut saya sangat penting dan sering diabaikan.

Jangan hanya mencatat:

spread rata-rata hari itu.

Tetapi pada saat event terjadi, catat:

spread saat entry
spread percentile
spread dibandingkan median session
spread sebelum event
spread setelah event

Kemudian bandingkan:

event + spread normal

vs

event + spread tinggi

Bisa jadi event yang bagus secara harga ternyata buruk ketika spread sedang melebar.

9. Volatility state sebelum entry

Bukan cuma ATR harian.

Kita perlu mengetahui kondisi volatilitas tepat sebelum event.

Contohnya:

ATR M1
ATR M5
range 5 candle
range 10 candle
realized volatility
volatility expansion
volatility contraction

Kemudian:

Event yang sama + volatilitas rendah
vs
Event yang sama + volatilitas tinggi.

10. Location — posisi harga saat event terjadi

Ini juga sangat penting.

Event yang sama bisa berbeda hasilnya tergantung lokasi.

Misalnya:

bullish reversal di tengah range

berbeda dengan:

bullish reversal tepat setelah menyentuh high/low sebelumnya.

Jadi kita perlu mencatat:

distance to recent high
distance to recent low
distance to swing
posisi dalam range
breakout distance
extension dari pergerakan sebelumnya.

Bukan berarti kita langsung percaya support/resistance.

Kita ukur dulu apakah lokasi tersebut benar-benar membedakan outcome.

11. Jangan hanya mencari kondisi yang menghasilkan profit — cari kondisi yang menyebabkan gagal

Ini menurut saya salah satu bagian paling penting.

EDA scalping harus punya pertanyaan:

“Kapan setup yang kelihatannya bagus justru gagal?”

Misalnya:

Setup A secara keseluruhan WR 60%.

Bagus?

Belum tentu.

Kemudian kita menemukan:

normal volatility → WR 68%
high volatility → WR 41%
spread tinggi → WR 35%
setelah expansion candle → WR 38%

Nah, informasi terakhir justru bisa menjadi sangat berharga.

Karena kita mulai menemukan:

bukan hanya kapan masuk, tetapi kapan TIDAK masuk.

12. Look-ahead bias harus menjadi pagar utama

Ini harus dijaga ketat.

Informasi yang digunakan untuk menentukan entry harus hanya berasal dari:

t ≤ entry

Sedangkan:

t > entry

hanya boleh digunakan untuk mengukur hasil.

Contohnya kita tidak boleh mengatakan:

“Candle berikutnya ternyata besar, maka entry tadi bagus.”

Kemudian menggunakan fakta itu untuk menentukan setup.

Itu akan membuat EDA terlihat sangat bagus padahal sebenarnya menggunakan masa depan.

13. Jangan langsung mengoptimasi threshold

Ini pelajaran penting dari penelitian Anda sebelumnya.

Misalnya kita menemukan:

RSI < 31 bagus.

Jangan langsung:

30 → 31 → 32 → 33 → cari mana profit terbesar.

Karena kita bisa mengoptimalkan noise.

Lebih baik:

temukan fenomenanya,
bentuk hipotesis,
tetapkan threshold sebelum pengujian konfirmasi,
lakukan test out-of-sample/walk-forward,
baru lihat apakah bertahan.
14. Pisahkan discovery dan confirmation

Saya akan membuat dua dunia.

Discovery

Boleh mencari:

“Ada pola apa?”

Eksplorasi boleh luas.

Confirmation

Setelah menemukan pola:

“Apakah pola ini benar-benar bertahan?”

Aturannya harus dikunci.

Ini penting supaya kita tidak menemukan pola bagus, kemudian mengubah aturan terus-menerus sampai data akhirnya terlihat bagus.

15. Uji stabilitas

Kalau suatu edge benar-benar ada, kita ingin melihat apakah dia hanya muncul di satu bagian data.

Misalnya:

2022 | 2023 | 2024 | 2025

atau:

London | NY | Asia

atau:

low vol | normal | high vol

Kalau hanya:

2024 London high-volatility

yang bagus sedangkan semuanya yang lain buruk, kita belum boleh buru-buru menyebutnya edge umum.

16. Walk-forward / out-of-sample

Ini tahap setelah discovery.

Contoh:

Train: 2022–2024
Test: 2025

Kemudian:

Train: 2022–2025
Test: 2026

Tujuannya melihat apakah pola yang ditemukan di masa lalu masih muncul pada data yang belum digunakan untuk menemukannya.

Kalau saya susun menjadi “EDA Scalping” lengkap

Saya akan membuat alurnya:

MARKET

↓
Session / regime / volatility / spread

↓

PRE-ENTRY CONTEXT

Candle -20 ... -1

↓

EVENT

Apa yang terjadi pada candle 0?

↓

LOCATION

Harga sedang berada di mana?

↓

EXECUTION CONDITION

Spread + slippage + volatility

↓

FORWARD OUTCOME

+1 / +2 / +3 / +5 / +10 / +20 candle

↓

MFE / MAE

↓

TP-before-SL

↓

CONDITIONAL ANALYSIS

Session / volatility / spread / location / regime

↓

FAILURE ANALYSIS

Kapan setup gagal?

↓

STABILITY

Tahun / session / regime

↓

OUT-OF-SAMPLE

↓

FALSIFICATION

↓

BARU

Hipotesis trading

Dan satu hal yang saya justru TIDAK akan lakukan

Saya tidak akan langsung memasukkan puluhan indikator seperti:

RSI + MACD + EMA + Bollinger + ADX + stochastic + ...

Karena itu bisa membuat penelitian berubah menjadi:

“Cari kombinasi indikator yang paling cocok dengan data.”

Padahal tujuan yang lebih kuat adalah:

“Cari perilaku harga yang benar-benar memiliki perbedaan probabilitas setelah suatu kondisi terjadi.”

Indikator nanti boleh dipakai kalau EDA menemukan bahwa konsep yang diwakilinya memang relevan.

Jadi jawaban singkatnya

Ya, masih banyak yang bisa ditambahkan untuk membuat EDA benar-benar cocok untuk scalping.

Dan menurut saya kekurangan terbesar EDA sekarang bukan jumlah datanya, tetapi karena unit analisisnya masih banyak berada di level:

“Bagaimana karakter USDJPY secara keseluruhan?”

Sedangkan untuk scalping kita perlu turun ke level:

“Apa yang terjadi sebelum event → event terjadi → apa yang terjadi 1–20 candle setelahnya → apakah pergerakan itu cukup besar untuk membayar biaya → dalam kondisi apa berhasil/gagal → apakah pola tersebut bertahan di data yang belum digunakan?”

Kalau kerangka ini diterapkan, barulah kita punya EDA yang benar-benar dirancang untuk mencari edge scalping, bukan sekadar EDA market profiling.

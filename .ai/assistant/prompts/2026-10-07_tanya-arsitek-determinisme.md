PERTANYAAN ARSITEK — DESAIN DETERMINISME NOTEBOOK PASCA-DEViasi BATCH NEWLINE

Konteks: Batch newline hulu B9-02 (5 builder + `newline="\n"`, 1 baris tiap file — SELESAI, hash `c3a38809…/f9bf6c3f…/bca5b896…/c07cab16…/3b07e3a8…`) STOP pada regen nb01 karena 3 deviasi terbukti (bukan asumsi): D1 — penulis terakhir pipeline adalah nbconvert 7.17.1 `FilesWriter.py:152` (`open(dest,"w")` tanpa `newline=`), di luar jangkauan fix builder (dibuktikan replikasi str→`open("w")`→CRLF di luar repo); D2 — 22 cell-id + 48 timestamp lahir baru tiap run (klasifikasi diff 256 baris nb01), sehingga kriteria "byte-identik" di prompt fix terbukti mustahil selamanya; D3 — chunking stream beda flush (sel idx 10/19 nb01), total teks + angka IDENTIK. nb01 di-restore persis titik-awal (`ec448a59…`); nb02–nb05 tidak dijalankan; dokumen + audit (`4eafbdb2…`) tak tersentuh; FIG-01..03 hash IDENTIK walau ditulis ulang (deterministik figure terbukti 2×). Fakta disk: nb05 = CRLF 1.663/1.663 (satu-satunya); nb00–nb04 = pure LF; `git hash-object` LF-normalized (terbukti empiris 2×: konten-LF = pin, raw-CRLF `529cbf20…` ≠); `.gitattributes` sudah `eol=lf`. Peranmu: ARSITEK (baca `.ai/assistant/prompts/PERAN-arsitek.md` dulu). Kamu BUKAN coder (DILARANG tulis/ubah kode), BUKAN auditor, BUKAN asisten (ABAIKAN `.ai/ASSISTANT_RULES.md`).

=== PERTANYAAN (jawab dalam batas ini saja) ===
Q1. Definisi determinisme yang mengikat: turunkan "byte-identik" menjadi "deterministik ternormalisasi" (sumber per-sel + output gabungan identik setelah normalisasi cell-id/timestamp/EOL) — atau pertahankan byte-identik dengan mekanisme tambahan (id stabil + timestamp beku)? Putuskan SATU + syarat mengikatnya (apa dinormalisasi, apa tidak boleh).
Q2. Di mana normalisasi EOL tinggal: (a) pasca-proses di builder sesudah nbconvert `--inplace` (CRLF→LF, tetap pola builder→notebook); (b) targetkan lapis nbconvert (konfigurasi/patch penulis); atau (c) status quo — biarkan CRLF, andalkan `git hash-object` + `.gitattributes`, tutup batch newline? Putuskan SATU + syarat mengikatnya. (Asisten mencatat: (b) rapuh terhadap upgrade nbconvert; (c) nol kerja tapi bug laten hidup — ini catatan, bukan vonis; putusan tetap milikmu.)
Q3. Kriteria audit regen yang baru menggantikan byte-identik: apa tepatnya yang diverifikasi auditor (mis. diff per-sel ternormalisasi + FIG hash + count/asserts + EOL byte-count)? Tulis sebagai daftar periksa mengikat.
Q4. Scope regen lanjutan: nb01–nb05 semua dengan kriteria baru, atau nb05 saja (satu-satunya CRLF; nb01–nb04 sudah LF dan pin-nya stabil — regen mereka justru mengusangkan pin via id/timestamp baru)? Putuskan SATU.

=== ATURAN ===
Putuskan + syarat mengikat bernomor, tiap klaim rujukan file:baris atau "PERLU VERIFIKASI". DILARANG merancang ulang di luar Q1–Q4; DILARANG ambil alih kerja coder/auditor; DILARANG edit kode/commit/push. Format jawaban: Putusan + syarat mengikat + self-audit 3× singkat. STOP.

=== SELF-AUDIT 3× ADVERSARIAL ===
Putaran 1 — Correctness: putusan menjawab Q1–Q4 semua; tidak ada yang menggantung.
Putaran 2 — Bias: apakah kamu memutuskan arsitektur, atau menilai benar/salahnya metode EDA?
Putaran 3 — Meta: tidak ada kode ditulis/diubah? Tidak ada vonis audit angka?

STOP. Eksekusi coder / re-audit HANYA atas perintah terpisah.

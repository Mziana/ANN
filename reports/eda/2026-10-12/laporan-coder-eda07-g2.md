# Laporan Tugas: Revisi G2 EDA-07 (Amandemen A-3 + A-5) + Full-Run Ulang

Peran: Coder. Tanggal: 2026-10-12. Perintah:
`.ai/assistant/prompts/2026-10-10_revisi-eda07-g2-coder.md` +
`reports/governance/2026-10-10/arsitek/amandemen-eda07-g2.md` (mengikat).
HEAD: `b18992b5e57d45c125aacf3ca868c2f9e135d9d1` (tidak ada commit selama tugas).

## Hasil akhir

STOP di gerbang kontrol sel 15 sesuai KONTRAK_07 — tanpa bypass.
Alarm: `ASSERT GAGAL: nol kontrol lolos-G2-revisi (n_alarm=86, lihat _gate_G2_alarm.csv)`.
Bukti LENGKAP tersimpan di disk (A-5): daftar alarm penuh (86/86, bukan 3),
tabel skrining 780 baris, checkpoint, progres. Kerugian run C (bukti hilang
saat STOP) tidak terulang.

## Klaim & Bukti

| Klaim | Status | Bukti |
|---|---|---|
| A-3 teraplikasi tepat (G2a pooled-vs-pooled n-sama; G2b mayoritas arah >=4/5; kontrol identik) | TERVERIFIKASI | `scripts/_build_eda07.py` SHA256 `BD40E1A3..980BD95F` (1477 baris, 69252 byte): `g2a[f]=bool(above)` x1, `maj>=G2_MIN_SEM` x2 (fitur+kontrol), ruff PASS, 19 sel compile OK |
| Bacaan ">=4 dari 5" = mayoritas (bukan semua-setuju) | TERVERIFIKASI (keputusan coder, terbuka untuk auditor) | Sim null: aturan semua-setuju memberi P(G2b)=0.05 (salah secara kombinatorik; teori 4/5 = 0.375); aturan mayoritas memberi 0.35-0.475 = teori. Frasa ">=4" hanya bermakna di bawah bacaan mayoritas bila 5 semester valid |
| Nol drift nilai ambang dari semua edit | TERVERIFIKASI | `snap_const.py`: 24/24 baris konstanta identik sebelum vs sesudah (diff kosong): N_HORIZONS, LB_MARGIN_PIP, LC_MULTS, HORIZON, STRIDE, MI_BINS, N_PERM=100, N_BOOT=1000, N_LEAK=200, RHO_DROP, G1_*, G2_MIN_SEM=4, G4_STRESS_MIN_PP, SEED07, YPOS, CTRL_COLS, KINDS, lambda YCODE |
| Satu-satunya perubahan non-A-3/A-5: timeout nbconvert 3600->5400 (infrastruktur, bukan ambang) | TERVERIFIKASI | run 8 mati `CellTimeoutError` sel 15 di T183/200 (`run8.log`, `nbclient.exceptions.CellTimeoutError: ... after 3600 seconds`); spec tidak menetapkan timeout; 5400 selaras batas-stale lock. Satu baris di builder (`timeout=5400` x1) |
| Mock sel 15-18 (kode asli + sintetis) PASS + rerun bit-identik | TERVERIFIKASI | `smoke1518.py` 2x: `SMOKE15-18 PASS`, 7/7 CSV hash SHA256 SAMA (`T-07-1..4`, `_gate_G2_skrining`, `_gate_G2_alarm`, `_ckpt_T`); rerun MI+lantai bit-identik PASS di dalam run |
| Kalibrasi null kriteria revisi sesuai teori (angka null-murni baru) | TERVERIFIKASI | `simg2.py` (primitif asli, R=40): n_sem=2000 -> P(G2a)=0.025, P(G2b)=0.375, joint=0.0250; n_sem=8000 -> 0.075/0.350/0.0250. G2-lama pada data sama = 1.000 (reproduksi cacat run C) |
| Full-run 9 detached selesai-menuju-STOP: LA 60/60 + T 200/200, lalu STOP di gerbang | TERVERIFIKASI | `eda07_progress.log` 260 baris (T200/200 `LD Tokyo tALL N60`), `_ckpt_LA.csv`, `_ckpt_T.csv`, lock dilepas, `run9.log` tail `nbconvert exit=1` + AssertionError di atas |
| 86 alarm = 6 noise (laju null terkalibrasi) + 28 round_d + 52 pdhl_d (jauh di atas null) | TERVERIFIKASI | `_gate_G2_skrining.csv` 780 baris: noise G2a 0.0577/G2b 0.3538/joint 0.0231 (= teori 0.05/0.375/0.025); round_d joint 0.1077; pdhl_d joint 0.2000. `_gate_G2_alarm.csv` 86 baris penuh |
| Tidak ada artefak T-07/FIG-13..16 baru (benar: STOP sebelum sel 16) | TERVERIFIKASI | Direktori hanya berisi `_gate_*`, `_ckpt_*`, `eda07_progress*.log`; notebook `eda_07_label_fitur.ipynb` (`4F1F98E6..70F7766`, 78604 byte) pristine 19 sel 0 output (nbconvert tidak menyimpan saat STOP) |
| Task Scheduler dibersihkan | TERVERIFIKASI | `schtasks /delete /tn EDA07Build /f` -> SUCCESS (lihat perintah mentah) |

## Perintah mentah + output (pasangan, ringkas)

1. `snap_const.py` sesudah -> `Compare-Object const_before const_after` -> kosong (identik).
2. `ruff check scripts/_build_eda07.py` -> `All checks passed!`; `check_cells.py` -> `sel total: 19 / sel code OK`; `check_foreign_chars.py` -> `OK`.
3. `smoke1518.py` (x2) -> `SMOKE15-18 PASS`; `Get-FileHash` 7 CSV x 2 run -> semua `SAMA`.
4. `simg2.py` -> `n_sem= 2000 R=40: P(G2a)=0.025 P(G2b)=0.375 P(G2a&G2b)=0.0250 P(G2-lama)=1.000 -> E[alarm/780]=19.5 P(STOP)=1.000` (baris 8000 identik joint 0.0250).
5. `schtasks /run /tn EDA07Build` -> progres LA 2/60 .. T 200/200; `run9.log` tail AssertionError + `nbconvert exit=1`.
6. Analisis `_gate_*` -> tabel di atas (noise 6 / round_d 28 / pdhl_d 52).

## Belum diverifikasi (bukan klaim)

- Apakah 52 alarm `pdhl_d` + 28 `round_d` adalah sinyal mikrostruktur asli
  (mis. clustering harga di level bulat/PDH-L) atau artefak residual.
  Ini temuan adjudikasi A-4 untuk ARSITEK, bukan vonis coder.
- Premis A-4 ("noise murni tidak [lolos]") meleset tipis: noise lolos 6/260
  (2.3%) — TEPAT pada laju null terkalibrasi, bukan nol. Aturan satu-alarm-STOP
  pada 780 evaluasi tidak memperhitungkan pengujian ganda; arsitek perlu
  memutus apakah kriteria alarm kontrol tetap butir-tunggal atau berbasis laju.
- Sel 16-18 + T-07/FIG-13..16 belum pernah tereksekusi (STOP pra-registrasi).

## Potensi masalah

1. Duplikasi rantai eksekusi (venv + system-python, harness) terjadi di run 8
   dan run 9 seperti run C; run 8 kehabisan timeout sel 15 karenanya (T183/200).
   Tidak saya utak-atik (pelajaran run C). Perlu perbaikan lingkungan, bukan kode.
2. Progres run 8 (`eda07_progress_run8.log`, berhenti T183/200) dipertahankan
   sebagai bukti; run 9 memakai `eda07_progress.log` baru (260 baris penuh).

## Rekomendasi (tanpa vonis, tanpa edge)

1. Adjudikasi A-4: 80 alarm struktural (52 pdhl_d + 28 round_d) vs 6 noise
   terkalibrasi — putuskan sinyal-vs-artefak sebelum baseline/Lapisan 3.
2. Pertimbangkan kriteria alarm kontrol berbasis laju (mis. joint struktural
   vs amplop null) sebagai amandemen, karena aturan butir-tunggal pada 780
   evaluasi hampir pasti STOP bahkan saat semua kontrol null (E ~= 19).
3. (Irisan x label x fitur) kandidat BARU bisa dirumuskan setelah adjudikasi;
   tidak ada yang layak dibawa ke Lapisan 3 dari run ini (STOP pra-registrasi).

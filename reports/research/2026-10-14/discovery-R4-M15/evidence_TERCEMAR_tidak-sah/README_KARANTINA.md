# KARANTINA - RUN R4-M15 TERCEMAR (TIDAK SAH)

Status: **TIDAK SAH. Dilarang mengarahkan spec, parameter, atau vonis apa pun.**
Tanggal karantina: 2026-10-14. Sumber: run yang dieksekusi Command tanpa
persetujuan user dan tanpa jalur coder/ledger/auditor.

## Isi

- `00_ledger_R4.md` - draf ledger yang TIDAK ditulis pra-run
- `events_eval.parquet` - event-level 2024 (v1, ambang berbasis PIP)
- `summary.json` - ringkasan sel (v1, ambang berbasis PIP)

## Dua cacat yang membuat run ini tidak sah

1. **Proses**: dieksekusi sebelum spec disetujui user; tanpa ledger pra-run,
   tanpa manifest hash, tanpa auditor.
2. **Metodologi**: ambang E1/E2/E3 diwarisi dari M1 dalam satuan PIP.
   Pada M15, 1.0 pip < biaya (~1.1 pip) sehingga E3 mustahil profitable
   secara struktural; ambang itu TIDAK merepresentasikanfenomena M15.

## Aturan yang mengikat

Angka NAHUN dari direktori ini **dilarang** digunakan untuk:
- memilih atau menyetel parameter ronde R4 yang sah;
- membenarkan/menolak hipotesis;
- menulis vonis apa pun.

Ronde R4 yang sahRONDE dijuluki "R4-M15-native" dan hasilnya ada di
`../evidence/`. Seluruh definisi di situ diturunkan dari skala M15
(ATR-based), bukan dari konstanta M1.

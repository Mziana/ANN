"""Generator for notebooks/scalping/eda_01_returns.ipynb (Q1 return distribution).

This script is a one-off generator; it writes the notebook and then executes it
top-to-bottom via nbconvert. It is NOT part of src/ and creates no src/ files.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_01_returns.ipynb"

CELLS: list[tuple[str, str]] = []

CELLS.append(
    (
        "md",
        "# EDA 01 — Q1: Distribusi Return M1 / M5 / M15 per Strata\n"
        "\n"
        "**Rancangan:** EDA v3 Final (Architect Spark, disetujui user, diaudit Klenz).\n"
        "\n"
        "## Tujuan notebook ini\n"
        "Menjawab **Q1**: bagaimana distribusi return log-close-BID pada M1, M5, dan M15,\n"
        "dengan stratifikasi wajib A / B / C yang sudah dikunci di notebook 00.\n"
        "\n"
        "## Definisi yang dipakai (dikunci di Kontrak 00, tidak diubah di sini)\n"
        "- `r_t = ln(close_t / close_{t-1})`, `close` = **harga BID** (RULES §18.16).\n"
        "- Spread diperlakukan sebagai **biaya terpisah**, bukan bagian dari return.\n"
        "- Stratifikasi: A = utama, B = H1-2023, C = dua window anomali.\n"
        "\n"
        "## Putusan Architect atas SA-03 (jebakan kalender UTC vs broker)\n"
        "Diterima di sesi ini dan dicatat di sel md terpisah. Tidak mengubah apa pun di Q1,\n"
        "tetapi menetapkan bahwa seluruh pekerjaan **level-hari** (Q6/Q7) dikunci pada\n"
        "**tanggal-broker**, sedangkan hari-UTC hanya sekunder.\n"
        "\n"
        "## Batas keras notebook ini (Wajib)\n"
        "- **Tidak** menghitung P&L, equity curve, atau profit simulasi apa pun.\n"
        "- **Tidak** menghasilkan sinyal, model, atau pemilihan metode strategi.\n"
        "- **Tidak** menulis `configs/`. Config hanya dibaca.\n"
        "- **Tidak** melakukan imputasi: hanya drop/NaNa dengan jumlah dilaporkan.\n"
        "- Inferensi berbentuk sinyal **tidak** diambil dari M1 (microstructure noise /\n"
        "  bid-bounce); M1 hanya dipakai untuk deskripsi distribusi.\n"
        "\n"
        "## Urutan sel\n"
        "1. Kontrak + sysinfo + kunci tzdata\n"
        "2. Definisi return + fungsi statistik (dokumentasi asumsi sigma)\n"
        "3. Beban M1/M5/M15 + hitung return per TF\n"
        "4. Audit stratifikasi per TF (A/B/C lepas, A+B+C = total)\n"
        "5. Tabel Q1 utama: skew, kurtosis, kuantil, pangsa 3sigma/5sigma per TF x strata\n"
        "6. QQ-plot terhadap normal\n"
        "7. Catatan keterbatasan biaya BID-only + assertion penutup\n"
        "8. Ringkasan assertion",
    ),
)

CELLS.append(
    (
        "code",
        "import importlib.metadata\n"
        "import sys\n"
        "from pathlib import Path\n"
        "\n"
        "import numpy as np\n"
        "import pandas as pd\n"
        "import scipy.stats\n"
        "\n"
        "\n"
        "def find_project_root(start: Path) -> Path:\n"
        '    """Cari root proyek (pyproject.toml + src/) dari cwd ke atas."""\n'
        "    for candidate in (start, *start.parents):\n"
        '        if (candidate / "pyproject.toml").is_file() and (candidate / "src").is_dir():\n'
        "            return candidate\n"
        '    raise RuntimeError("PROJECT_ROOT tidak ditemukan")\n'
        "\n"
        "\n"
        "PROJECT_ROOT = find_project_root(Path.cwd().resolve())\n"
        "if str(PROJECT_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(PROJECT_ROOT))\n"
        "\n"
        "from src.data.broker_time import BrokerSchedule, wall_clock_series  # noqa: E402\n"
        "from src.utils.config import load_config  # noqa: E402\n"
        "\n"
        'print("PROJECT_ROOT :", PROJECT_ROOT)\n'
        'print("python       :", sys.version.split()[0])\n'
        'for package in ("pandas", "numpy", "pyarrow", "matplotlib", "scipy", "tzdata"):\n'
        '    print(f"  {package:11s}: {importlib.metadata.version(package)}")\n'
        'assert importlib.metadata.version("tzdata") == "2026.5", "tzdata harus 2026.5 (Kontrak 00)"\n'
        "# Kunci versi pandas major. pandas 3.x mengubah satuan .asi8 (detik vs nanos),\n"
        "# bug yang pernah merusak kolom epoch (SESSION_LOG 2026-10-05). Notebook WAJIB\n"
        "# jalan di venv kanonik (pandas 2.x), bukan .venv (pandas 3.x).\n"
        'assert int(importlib.metadata.version("pandas").split(".")[0]) == 2, (\n'
        '    "Notebook WAJIB jalan di venv kanonik (pandas 2.x); pandas 3.x merusak .asi8."\n'
        ")",
    ),
)

CELLS.append(
    (
        "md",
        "## Putusan Architect (Spark) atas SA-03 — dicatat verbatim agar tidak hilang\n"
        "\n"
        '> **R1:** "Hari-UTC" = label kalender murni dengan offset struktural −1 yang\n'
        '> didokumentasikan; **DILARANG** menggeser data agar "sepakat".\n'
        ">\n"
        '> **R2:** Syarat "wajib sepakat" ditafsir ulang menjadi **sepakat-dengan-kesadaran-\n'
        "> geser**: bandingkan H/L hari-broker vs H/L hari-UTC dengan memperhitungkan offset\n"
        "> struktural; hanya divergensi **MELEBIHI** geseran struktural yang menjadi temuan\n"
        "> (dilaporkan sebagai sensitivitas).\n"
        ">\n"
        "> **R3:** Seluruh pekerjaan level-hari (uji regime Q7, primer prior-day Q6) dikunci\n"
        "> pada **tanggal-broker** — konsisten dengan bucket D1, strata, dan window anomali yang\n"
        "> semuanya broker-defined. Hari-UTC sekunder saja.\n"
        ">\n"
        "> **R4:** Tanpa redesain, tanpa penundaan Langkah 1–3; aturan R1–R3 dicatat di\n"
        "> nb04/nb05 dan laporan final.\n"
        "\n"
        "**Dampak ke Q1:** Q1 bekerja pada **bar** (bukan hari), jadi SA-03 tidak menyentuh\n"
        "distribusi return. Aturan ini baru mengikat saat Q6/Q7 (nb04/nb05).\n"
        "\n"
        "**Risiko yang dicatat Architect:** analis nb04 lupa menerapkan R2 → mitigasi:\n"
        "assertion perbandingan shift-aware + review. Session ini menambah satu proteksi:\n"
        "sel audit di bawah selalu melaporkan **offset struktural yang diukur**, bukan hanya\n"
        "kesimpulannya.",
    ),
)

CELLS.append(
    (
        "code",
        'RETURN_DEFINITION = "r_t = ln(close_t / close_{t-1}); close = BID"\n'
        "ANOMALY_OFFSET_EXPECTED = -1\n"
        "print(RETURN_DEFINITION)\n"
        'print("offset struktural hari-UTC vs hari-broker (harus", ANOMALY_OFFSET_EXPECTED, ")")',
    ),
)

CELLS.append(
    (
        "md",
        "## 1. Fungsi return dan statistik\n"
        "\n"
        "**Return** dihitung pada bar yang **sudah diurutkan kronologis** (`sort_values('utc')`),\n"
        "bukan pada urutan file. Ini penting: urutan file adalah per tahun, sehingga kalau\n"
        "return dihitung tanpa pengurutan, perpindahan antar-file akan menghasilkan return\n"
        "salah yang memalsukan ekor distribusi.\n"
        "\n"
        "**Sigma** untuk ambang 3σ/5σ dihitung **per TF per strata** dari data itu sendiri\n"
        "(bukan sigma global), supaya ambang tidak bias oleh perbedaan skala antar strata.\n"
        "Sigma memakai `ddof=0` (populasi bar yang diamati), bukan `ddof=1`.\n"
        "\n"
        "**Kuantil** 0,1% dan 99,9% adalah kuantil *empiris* (tanpa asumsi normal).\n"
        "**Skewness** dan **kurtosis ekses** adalah moment statistics mentah — pada data\n"
        "finansial yang-tailed dan ber-cluster, keduanya **bias** untuk n besar; dipakai\n"
        "sebagai deskripsi, bukan sebagai bukti distribusi tertentu.",
    ),
)

CELLS.append(
    (
        "code",
        "def add_log_return(frame: pd.DataFrame) -> pd.DataFrame:\n"
        '    """Tambahkan return log close-BID pada frame yang sudah terurut kronologis.\n'
        "\n"
        "    Args:\n"
        "        frame: Frame dengan kolom 'close' dan indeks unik.\n"
        "\n"
        "    Returns:\n"
        "        Salinan frame dengan kolom 'r' (NaN pada bar pertama).\n"
        '    """\n'
        "    out = frame.copy()\n"
        '    out["r"] = np.log(out["close"] / out["close"].shift(1))\n'
        "    return out\n"
        "\n"
        "\n"
        "def return_stats(returns: pd.Series) -> dict[str, float]:\n"
        '    """Statistik deskriptif distribusi return (tanpa asumsi normal).\n'
        "\n"
        "    Args:\n"
        "        returns: Series return log; NaN akan di-drop untuk statistik.\n"
        "\n"
        "    Returns:\n"
        "        Dictionary metrik Q1.\n"
        '    """\n'
        "    clean = returns.dropna()\n"
        "    sigma = float(clean.std(ddof=0))\n"
        "    return {\n"
        '        "n": int(clean.size),\n'
        '        "mean": float(clean.mean()),\n'
        '        "sigma": sigma,\n'
        '        "skew": float(clean.skew()),\n'
        '        "kurt_excess": float(clean.kurt()),\n'
        '        "q_0.1%": float(clean.quantile(0.001)),\n'
        '        "q_1%": float(clean.quantile(0.01)),\n'
        '        "q_99%": float(clean.quantile(0.99)),\n'
        '        "q_99.9%": float(clean.quantile(0.999)),\n'
        '        "share_gt_3sigma": float((clean.abs() > 3 * sigma).mean()),\n'
        '        "share_gt_5sigma": float((clean.abs() > 5 * sigma).mean()),\n'
        "    }\n"
        "\n"
        "\n"
        "return_stats(pd.Series([np.nan, 0.001, -0.002]))",
    ),
)

CELLS.append(
    (
        "md",
        "## 2. Memuat data dan menghitung return per timeframe\n"
        "\n"
        "Timeframe yang dianalisis: **M1 (primer), M5, M15** — sesuai batasan ruang lingkup\n"
        "scalping M1–M15. H1/D1 tidak masuk Q1 (dipakai di Q6/Q7 sebagai konteks).\n"
        "\n"
        "Kolom `time` di parquet adalah **string ISO-8601 UTC**, jadi di-parse dengan\n"
        "`pd.to_datetime(..., utc=True)`.\n"
        "\n"
        "Jumlah bar **sebelum** dan **sesudah** drop NaN dilaporkan untuk semua TF — sesuai\n"
        "aturan missing-data (drop dilaporkan jumlahnya, nol imputasi).",
    ),
)

CELLS.append(
    (
        "code",
        'config = load_config("data")\n'
        'SYMBOL = config["mt5"]["symbol"]\n'
        'SCHEDULE = BrokerSchedule.from_config(config["mt5"])\n'
        'ANOMALY_WINDOWS = tuple((w["start"], w["end"]) for w in config["validation"]["anomaly_windows"])\n'
        "\n"
        'Q1_TIMEFRAMES = ("M1", "M5", "M15")\n'
        "YEARS = (2023, 2024, 2025, 2026)\n"
        'NEEDED_COLUMNS = ["time", "broker_time_raw", "close"]\n'
        "\n"
        'print(f"symbol: {SYMBOL} | windows anomali: {len(ANOMALY_WINDOWS)}")\n'
        "for start, end in ANOMALY_WINDOWS:\n"
        '    print(f"  {start} .. {end}")\n',
    ),
)

CELLS.append(
    (
        "code",
        "def load_timeframe(timeframe: str) -> pd.DataFrame:\n"
        '    """Muat satu timeframe 2023-2026, urut kronologis, dengan return log.\n'
        "\n"
        "    Args:\n"
        "        timeframe: Kode timeframe, mis. 'M1'.\n"
        "\n"
        "    Returns:\n"
        "        Frame terurut dengan kolom utc, wall_date, dan r.\n"
        '    """\n'
        "    frames = []\n"
        "    for year in YEARS:\n"
        '        path = PROJECT_ROOT / "data/processed" / timeframe / f"usdjpy_{timeframe.lower()}_{year}.parquet"\n'
        "        frames.append(pd.read_parquet(path, columns=NEEDED_COLUMNS))\n"
        "    frame = pd.concat(frames, ignore_index=True)\n"
        '    frame["utc"] = pd.to_datetime(frame["time"], utc=True)\n'
        '    frame["wall"] = wall_clock_series(frame["broker_time_raw"])\n'
        '    frame["wall_date"] = frame["wall"].dt.normalize()\n'
        '    frame = frame.sort_values("utc", kind="mergesort").reset_index(drop=True)\n'
        "    return add_log_return(frame)\n"
        "\n"
        "\n"
        "DATA = {timeframe: load_timeframe(timeframe) for timeframe in Q1_TIMEFRAMES}\n"
        "\n"
        "print(f\"{'TF':4} {'bar':>10} {'r != NaN':>10} {'drop warmup':>11} {'sorted':>7} {'dup':>5}\")\n"
        "for timeframe, frame in DATA.items():\n"
        "    n_total = len(frame)\n"
        '    n_valid = int(frame["r"].notna().sum())\n'
        '    n_dup = int(frame["utc"].duplicated().sum())\n'
        '    is_sorted = bool(frame["utc"].is_monotonic_increasing)\n'
        '    print(f"{timeframe:4} {n_total:>10,} {n_valid:>10,} {n_total - n_valid:>11,} {str(is_sorted):>7} {n_dup:>5}")\n'
        "\n"
        'assert all(frame["utc"].is_monotonic_increasing for frame in DATA.values()), "urutan waktu harus naik"\n'
        'assert all(int(frame["utc"].duplicated().sum()) == 0 for frame in DATA.values()), "duplikat waktu harus nol"',
    ),
)

CELLS.append(
    (
        "md",
        "## 3. Audit stratifikasi per timeframe\n"
        "\n"
        "Definisi strata diwarisi **persis** dari notebook 00 dan dihitung ulang di sini\n"
        "(sumber tunggal definisi = nb00):\n"
        "- **B** = hari broker 2023-01-01 .. 2023-06-30 (H1-2023).\n"
        "- **C** = dua window anomali dari `configs/data.yaml`.\n"
        "- **A** = sisanya.\n"
        "\n"
        "Untuk timeframe M5/M15 jumlah bar per strata **tidak mungkin** sama dengan M1 —\n"
        "itu konsekuensi resample yang wajar, bukan kegagalan. Yang wajib lulus adalah:\n"
        "partisi A/B/C saling lepas dan **A+B+C = total** per timeframe.\n"
        "\n"
        "Pada frame yang sudah urut, `r` dihitung **sebelum** pemisahan strata. Karena\n"
        "`.shift(1)` diterapkan pada seri utuh, return pada bar pertama sebuah stratum bisa\n"
        "merujuk bar di stratum sebelumnya. Ini **benar secara ekonomi** (return dihitung dari\n"
        "bar berulang yang benar-benar ada sebelumnya) dan **tidak**(create) look-ahead:\n"
        "informasi hanya dari masa lalu. Jumlahnya dilaporkan sebagai `cross_stratum_returns`.",
    ),
)

CELLS.append(
    (
        "code",
        "def stratify(frame: pd.DataFrame) -> dict[str, pd.Series]:\n"
        '    """Bangun mask stratifikasi A/B/C dari hari broker (definisi dari nb00).\n'
        "\n"
        "    Args:\n"
        "        frame: Frame dengan kolom wall_date dan r.\n"
        "\n"
        "    Returns:\n"
        "        Dictionary 'A', 'B', 'C' berisi boolean mask.\n"
        '    """\n'
        '    wall_date = frame["wall_date"]\n'
        '    b_mask = (wall_date >= pd.Timestamp("2023-01-01")) & (wall_date <= pd.Timestamp("2023-06-30"))\n'
        "    c_mask = pd.Series(False, index=frame.index)\n"
        "    for start, end in ANOMALY_WINDOWS:\n"
        "        c_mask |= (wall_date >= pd.Timestamp(start)) & (wall_date <= pd.Timestamp(end))\n"
        "    a_mask = ~(b_mask | c_mask)\n"
        '    return {"A": a_mask, "B": b_mask, "C": c_mask}\n'
        "\n"
        "\n"
        "def first_of_stratum_is_repeated(returns: pd.Series, mask: pd.Series) -> int:\n"
        '    """Hitung return pada bar pertama stratum yang r-nya menyeberang stratum.\n'
        "\n"
        "    Args:\n"
        "        returns: Series return.\n"
        "        mask: Boolean mask stratum.\n"
        "\n"
        "    Returns:\n"
        "        Jumlah return yang border menyeberang (informasi tetap dari masa lalu).\n"
        '    """\n'
        "    inside = mask & returns.notna()\n"
        "    shifted_inside = inside.shift(1, fill_value=False)\n"
        "    return int((inside & ~shifted_inside).sum())\n"
        "\n"
        "\n"
        "print(f\"{'TF':4} {'strata':6} {'bar':>10} {'r != NaN':>10} {'cross':>7} {'pangsa':>8}\")\n"
        "for timeframe, frame in DATA.items():\n"
        "    masks = stratify(frame)\n"
        "    n_total = len(frame)\n"
        '    for name in ("A", "B", "C"):\n'
        "        mask = masks[name]\n"
        '        n_valid = int((mask & frame["r"].notna()).sum())\n'
        '        cross = first_of_stratum_is_repeated(frame["r"], mask)\n'
        '        print(f"{timeframe:4} {name:6} {int(mask.sum()):>10,} {n_valid:>10,} {cross:>7} {mask.mean():>7.2%}")\n'
        '    union = masks["A"] | masks["B"] | masks["C"]\n'
        '    assert not (masks["B"] & masks["C"]).any(), "B dan C tidak boleh tumpang tindih"\n'
        '    assert bool(union.all()), "A+B+C harus menutup seluruh bar"\n'
        '    assert int(union.sum()) == n_total, "A+B+C harus sama dengan total"\n'
        "    print(f\"{timeframe:4} {'A+B+C':6} {int(union.sum()):>10,} | partisi PASS\")",
    ),
)

CELLS.append(
    (
        "md",
        "## 3b. Karakterisasi ekor dan massa nol (self-audit putaran 1 & 3)\n"
        "\n"
        "Dua karakteristik data yang **tidak terlihat** di tabel momente dan wajib\n"
        "dokumentasikan eksplisit:\n"
        "\n"
        "1. **Massa di nol**: berapa bar yang return-nya tepat 0 (harga tidak berubah dari\n"
        "   menit sebelumnya). Ini wajar secara alami dari microstructure, bukan data rusak —\n"
        "   tapi ia berkontribusi besar terhadap kurtosis yang tinggi.\n"
        "2. **Ekor:** konversi ke **pip** yang benar adalah\n"
        "   `pip = (exp(r) - 1) * close / 0.01`. Salah konversi (menganggap log-return\n"
        "   sudah berupa fraksi pip) akan sangat MENGAHALANGI besarnya pergerakan. Jam dari\n"
        "   pergerakan terbesar juga dihitung untuk memeriksa apakah ekor terkonsentrasi\n"
        "   di **jadwal berita makro** (RULES §18.15 melarang trading saat news high impact\n"
        "   tanpa proteksi).\n"
        "\n"
        "**Konsekuensi untuk interpretasi:** ekses kurtosis tinggi **tidak boleh**\n"
        "diatribusikan ke 'microstructure noise' sebelum ekor dipisahkan dari news spike.\n"
        "Atribusi itu jadi hipotesis, bukan temuan Q1.",
    ),
)

CELLS.append(
    (
        "code",
        """STEP_MINUTES = {"M1": 1, "M5": 5, "M15": 15}
PIP_SIZE = 0.01

print(f"{'TF':4} {'zero-share':>10} {'gap-returns':>12} {'max|r| pip':>11}")
for timeframe in Q1_TIMEFRAMES:
    frame = DATA[timeframe]
    step = STEP_MINUTES[timeframe]
    returns = frame["r"]
    gap_mask = frame["utc"].diff() > pd.Timedelta(minutes=step)
    pips = (np.exp(returns) - 1.0) * frame["close"] / PIP_SIZE
    print(f"{timeframe:4} {returns.eq(0).mean():>9.2%} {int(gap_mask.sum()):>12,} {pips.abs().max():>10.1f}")

print()
m1_frame = DATA["M1"]
m1_pips = (np.exp(m1_frame["r"]) - 1.0) * m1_frame["close"] / PIP_SIZE
top_index = m1_pips.abs().sort_values(ascending=False).index[:8]
print("8 pergerakan M1 terbesar (pip):")
for index in top_index:
    print(f"  {m1_frame.loc[index, 'utc']}  {m1_pips.loc[index]:+8.2f} pip")

print()
print(f"jam UTC dari 8 pergerakan terbesar: {sorted(m1_frame.loc[top_index, 'utc'].dt.hour.tolist())}")
print("12:30 UTC = 08:30 ET (data ketenagakerjaan AS).")
print("21-22 UTC = pembukaan sesi / transisi DST (return ini return GAP lintas akhir pekan, bukan pergerakan 1 menit).")
print("-> EKOR DIKENDALIKAN DUA SUMBER: berita makro DAN gap pembukaan sesi.")
print("   Jadi atribusi 'microstructure noise' untuk kurtosis TIDAK didukung Q1.")""",
    ),
)
CELLS.append(
    (
        "md",
        "## 4. Tabel Q1 utama\n"
        "\n"
        "Kolom yang dilaporkan (sesuai metrik rancangan): `n`, skewness, kurtosis ekses,\n"
        "kuantil 0,1% / 1% / 99% / 99,9%, serta pangsa bar dengan |r| di atas 3σ dan 5σ.\n"
        "\n"
        "Sigma untuk ambang 3σ/5σ dihitung **per baris tabel** (per TF × strata), sehingga\n"
        "ambang tidak dipengaruhi perbedaan skala antar strata.\n"
        "\n"
        "**Cara membaca angka skew/kurtosis:** nilai|kurtosis ekses| >> 3 dan |skew| >> 0.5\n"
        "pada data M1/M5 adalah **diharapkan** untuk data aset keuangan dan **bukan** bukti\n"
        "bahwa perhitungan salah. Yang justru penting: (a) apakah ekses kurtosis M1 jauh lebih\n"
        "besar dari M5/M15 — indikasi microstructure noise/bid-bounce di M1; dan (b) apakah\n"
        "strata B menyimpang dari A.\n"
        "\n"
        "**Penting soal ambang 3sigma/5sigma:** porsi bar di atas 3sigma ternyata **jauh lebih\n"
        "besar** dari teoritis normal (0,27%), karena ekornya berat. Jadi angka 3sigma di sini\n"
        '**bukan** ambang "outlier langka" — ini konsekuensi langsung dari ekor yang berat,\n'
        "bukan ambang keputusan. Tidak ada satu pun angka tabel ini yang dipakai sebagai ambang\n"
        "filter.\n"
        "\n"
        "**Tidak ada** threshold trading di notebook ini. Tidak ada keputusan metode.",
    ),
)

CELLS.append(
    (
        "code",
        "table_rows = []\n"
        "for timeframe in Q1_TIMEFRAMES:\n"
        "    frame = DATA[timeframe]\n"
        "    masks = stratify(frame)\n"
        '    for name in ("A", "B", "C"):\n'
        '        stats = return_stats(frame.loc[masks[name], "r"])\n'
        '        row = {"TF": timeframe, "strata": name}\n'
        "        row.update(stats)\n"
        "        table_rows.append(row)\n"
        "\n"
        'Q1_TABLE = pd.DataFrame(table_rows).set_index(["TF", "strata"])\n'
        'pd.set_option("display.width", 250)\n'
        'pd.set_option("display.max_columns", 30)\n'
        'pd.set_option("display.float_format", lambda v: f"{v:.6e}")\n'
        "display(Q1_TABLE)\n"
        "\n"
        "# Cetak juga sebagai stream supaya tabel utama tersimpan di output cell.\n"
        'print("TABEL Q1 (stream, supaya tersimpan):")\n'
        "print(Q1_TABLE.to_string())\n"
        'print(f"\\n{len(Q1_TABLE)} baris = {len(Q1_TIMEFRAMES)} TF x 3 strata")\n'
        "\n"
        "# Pengujian pembeda yang JANGAN disimpulkan dari tabel saja (self-audit #2).\n"
        'm1_frame = DATA["M1"]\n'
        "m1_masks = stratify(m1_frame)\n"
        'returns_a = m1_frame.loc[m1_masks["A"], "r"].dropna()\n'
        'returns_b = m1_frame.loc[m1_masks["B"], "r"].dropna()\n'
        "welch = scipy.stats.ttest_ind(returns_a, returns_b, equal_var=False)\n"
        'print("\\nUJI PEMBEDA (bukan klaim Q1, hanya pagar pembeda):")\n'
        'print(f"  mean return M1: A={returns_a.mean():.3e} B={returns_b.mean():.3e}")\n'
        'print(f"  Welch t-test A vs B: t={welch.statistic:.2f} p={welch.pvalue:.3f}")\n'
        'print("  -> selisih mean TIDAK signifikan; jangan klaim drift B vs A.")\n'
        "rng = np.random.default_rng(20261006)\n"
        "cubes_b = returns_b.to_numpy() ** 3\n"
        "boot = [float(np.mean(rng.choice(cubes_b, size=40000, replace=True))) for _ in range(300)]\n"
        "boot_low, boot_high = float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))\n"
        'print(f"  skew B bootstrap 95% CI = [{boot_low:.3e}, {boot_high:.3e}]")\n'
        'print("  -> tanda skew B hanya TIDAK kokoh; CI melintasi nol. Catat sebagai pola, bukan temuan.\\n")\n',
    ),
)

CELLS.append(
    (
        "md",
        "## 5. QQ-plot terhadap normal\n"
        "\n"
        "QQ-plot membandingkan kuantil observasi dengan kuantil normal standar. Tiga hal\n"
        "hanya bisa dibaca dari grafik ini:\n"
        "1. **Ekor** (*tails*): titik yang menjauh dari garis diagonal di ujung kiri/kanan berarti\n"
        "   lebih berat dari normal — diharapkan untuk return aset keuangan.\n"
        "2. **Puncak**: apakah titik tengah meninggi (bola_bocor tinggi), yang menandakan\n"
        "   konsentrasi return kecil — konsisten dengan microstructure noise M1.\n"
        "3. **Kesimpulannya sudah diketahui dari angka**: QQ-plot di sini adalah konfirmasi\n"
        "   visual, bukan sumber klaim baru. Tidak ada parameter yang di-*fit* ke grafik ini.",
    ),
)

CELLS.append(
    (
        "code",
        "import matplotlib\n"
        "\n"
        'matplotlib.use("Agg")\n'
        "import matplotlib.pyplot as plt\n"
        "\n"
        'FIGURE_DIR = PROJECT_ROOT / "reports/eda/2026-10-06/figures"\n'
        "FIGURE_DIR.mkdir(parents=True, exist_ok=True)\n"
        "\n"
        "figures = []\n"
        "# Skema FIG global (putusan D9): nb01 mengklaim FIG-01..03 = M1/M5/M15.\n"
        "# Penomoran dari enumerate supaya regenerasi TIDAK mengembalikan penamaan lama qq_timeframe.\n"
        "for nomor, timeframe in enumerate(Q1_TIMEFRAMES, start=1):\n"
        "    frame = DATA[timeframe]\n"
        "    masks = stratify(frame)\n"
        '    clean = frame.loc[masks["A"], "r"].dropna()\n'
        "    n_quantiles = 1000\n"
        "    probabilities = np.linspace(0.001, 0.999, n_quantiles)\n"
        "    observed = np.sort(clean.to_numpy())[\n"
        "        np.linspace(0, clean.size - 1, n_quantiles).round().astype(int)\n"
        "    ]\n"
        "    expected = scipy.stats.norm.ppf(probabilities)\n"
        "\n"
        "    fig, axis = plt.subplots(figsize=(6, 6))\n"
        "    axis.scatter(expected, observed, s=3, alpha=0.35, rasterized=True)\n"
        "    sigma = float(clean.std(ddof=0))\n"
        "    mean = float(clean.mean())\n"
        '    axis.plot(expected, mean + sigma * expected, color="crimson", linewidth=1.2)\n'
        '    axis.set_title(f"{timeframe} stratum A (n={clean.size:,}) vs normal")\n'
        '    axis.set_xlabel("Kuantil normal standar")\n'
        '    axis.set_ylabel("Kuantil observasi (log return BID)")\n'
        "    fig.tight_layout()\n"
        '    path = FIGURE_DIR / f"FIG-{nomor:02d}.png"\n'
        "    fig.savefig(path, dpi=120)\n"
        "    plt.close(fig)\n"
        "    figures.append(path)\n"
        "\n"
        "for path in figures:\n"
        '    print("tersimpan:", path.relative_to(PROJECT_ROOT))',
    ),
)

CELLS.append(
    (
        "md",
        "## 6. Keterbatasan biaya — CATATAN WAJIB (tidak boleh dilewati)\n"
        "\n"
        "Semua return di notebook ini dihitung dari **close BID** (RULES §18.16: BUY entry di\n"
        "ask, exit di bid; OHLC MT5 = BID). Artinya:\n"
        "\n"
        "- **Return BUY dalam data ini optimistis**, karena tidak pernah membayar spread di sisi\n"
        "  masuk.\n"
        "- **Return SELL dalam data ini konservatif**, karena tidak pernah membayar spread di\n"
        "  sisi keluar.\n"
        "- Distribusi return di sini **bukan** distribusi profitabilitas strategi. Konversi\n"
        "  spread ke P&L adalah urusan Lapisan 3 (backtest), **bukan** EDA.\n"
        "- Angka spread di `configs/data.yaml` (default 1,5 dan 3,0 untuk 2023) adalah\n"
        "  **asumsi**, bukan fakta terukur. Spread terukur dari data adalah deliverable\n"
        "  **EDA-02** + review **4b**, dan tidak boleh dipakai sebagai fakta sebelum itu.",
    ),
)

CELLS.append(
    (
        "code",
        "spread_note = pd.DataFrame(\n"
        "    [\n"
        '        ["Close = BID (RULES §18.16)", "ret BUY tanpa biaya spread (optimis)"],\n'
        '        ["Close = BID (RULES §18.16)", "ret SELL tanpa biaya spread (konservatif)"],\n'
        '        ["Kolom spread_pips (M1)", "terukur di data, dipakai di EDA-02"],\n'
        '        ["kolom spread_pips_mean/max (M5/M15)", "terukur di data, dipakai di EDA-02"],\n'
        '        ["configs spread.by_year", "ASUMSI, hanya sah setelah langkah 4b"],\n'
        "    ],\n"
        '    columns=["sumber", "implikasi untuk Q1"],\n'
        ")\n"
        "display(spread_note)",
    ),
)

CELLS.append(
    (
        "code",
        "checks = [\n"
        '    ("Definisi return = log close BID", RETURN_DEFINITION.startswith("r_t = ln(close_t")),\n'
        '    ("Urutan waktu naik di semua TF", all(f["utc"].is_monotonic_increasing for f in DATA.values())),\n'
        '    ("Duplikat waktu = 0 di semua TF", all(int(f["utc"].duplicated().sum()) == 0 for f in DATA.values())),\n'
        '        ("Partisi A/B/C menutup total tiap TF", True),\n'
        "        (\n"
        '            "Ukuran strata M1 terkunci 1.136.401/185.248/26.198 (Lapisan 1)",\n'
        '            tuple(int(stratify(DATA["M1"])[k].sum()) for k in ("A", "B", "C"))\n'
        "            == (1_136_401, 185_248, 26_198),\n"
        "        ),\n"
        "        (\n"
        '            "Ukuran strata M5/M15 cocok dengan resample (bukan disalin)",\n'
        '            tuple(int(stratify(DATA[tf])[k].sum()) for tf in ("M5", "M15") for k in ("A", "B"))\n'
        "            == (227_568, 37_152, 75_863, 12_430),\n"
        "        ),\n"
        '        ("Versi pandas major = 2 (venv kanonik)", int(importlib.metadata.version("pandas").split(".")[0]) == 2),\n'
        '        ("Tidak ada close NaN / non-positif (log aman)", all(DATA[tf]["close"].notna().all() and (DATA[tf]["close"] > 0).all() for tf in Q1_TIMEFRAMES)),\n'
        '        ("Tidak ada r infinity", all(np.isfinite(DATA[tf]["r"].dropna()).all() for tf in Q1_TIMEFRAMES)),\n'
        '        ("Massa di nol tercatat dan < 10% (M1)", 0.0 < float(DATA["M1"]["r"].eq(0).mean()) < 0.10),\n'
        '    ("Tiap TF punya tepat 3 baris tabel", len(Q1_TABLE) == 3 * len(Q1_TIMEFRAMES)),\n'
        '    ("n strata B > 0 di semua TF", all(int(Q1_TABLE.loc[(tf, "B"), "n"]) > 0 for tf in Q1_TIMEFRAMES)),\n'
        '    ("Tiap TF punya tepat 3 baris tabel", len(Q1_TABLE) == 9),\n'
        '    ("Sigma > 0 di semua baris tabel", bool((Q1_TABLE["sigma"] > 0).all())),\n'
        '    ("Piksil 3sigma >> normal teoritis 0.27% = heavy tail", bool((Q1_TABLE["share_gt_3sigma"] > 0.0027).all())),\n'
        '    ("Kuantil 0.1% < kuantil 1% (semua)", bool((Q1_TABLE["q_0.1%"] < Q1_TABLE["q_1%"]).all())),\n'
        '    ("Kuantil 99% < kuantil 99.9% (semua)", bool((Q1_TABLE["q_99%"] < Q1_TABLE["q_99.9%"]).all())),\n'
        '    ("Pangsa 3sigma > pangsa 5sigma (semua)", bool((Q1_TABLE["share_gt_3sigma"] > Q1_TABLE["share_gt_5sigma"]).all())),\n'
        '    ("Ekses kurtosis > 0 semua baris (heavy tail)", bool((Q1_TABLE["kurt_excess"] > 0).all())),\n'
        '    ("Tiga QQ figure benar-benar ada di disk", all(p.is_file() and p.stat().st_size > 0 for p in figures)),\n'
        '    ("Skema FIG-01/02/03 terkunci (D9)", [p.name for p in figures] == ["FIG-01.png", "FIG-02.png", "FIG-03.png"]),\n'
        '    ("Kontrak: tidak ada kolom P&L/equity di tabel Q1", not ({"pnl", "equity", "profit", "balance"} & set(Q1_TABLE.columns))),\n'
        '    ("Kontrak: tidak ada kolom sinyal/entry/exit di tabel Q1", not ({"signal", "entry", "exit", "side", "direction"} & set(Q1_TABLE.columns))),\n'
        "]\n"
        "for label, passed in checks:\n"
        "    print(f\"{'PASS' if passed else 'GAGAL'} {label}\")\n"
        "\n"
        "failed = [label for label, passed in checks if not passed]\n"
        'assert not failed, f"assertion gagal: {failed}"\n'
        "print()\n"
        'print(f"RINGKASAN: {len(checks) - len(failed)}/{len(checks)} assertion PASS untuk Q1.")',
    ),
)

CELLS.append(
    (
        "md",
        "## Ringkasan hasil dan batasnya\n"
        "\n"
        "**Yang dijawab Q1:** bentuk distribusi return (skew, ekses kurtosis, kuantil,\n"
        "pangsa di atas 3σ/5σ) untuk M1/M5/M15 pada strata A, B, dan C, lengkap dengan\n"
        "QQ-plot.\n"
        "\n"
        "**Yang TIDAK dijawab dan sengaja ditolak di sini:**\n"
        "- Tidak ada kesimpulan apakah return dapat diprediksi (itu Q4, notebook 03).\n"
        "- Tidak ada penilaian biaya-wajar-vs-ukuran (itu EDA-02, termasuk kalibrasi M1–M4).\n"
        "- Tidak ada sinyal, model, atau pemilihan metode.\n"
        "- Tidak ada P&L atau kurva ekuitas.\n"
        "\n"
        "**Cara memakai angka ini nanti:** nilai|kurtosis ekses| M1 yang jauh lebih besar dari\n"
        "M5/M15 adalah bukti kuantitatif bahwa M1 tidak boleh dipakai untuk inferensi sinyal —\n"
        "ini adalah input hipotesis, **bukan** kesimpulan akhir.\n"
        "\n"
        "**STOP.** Laporan mini + self-audit adversarial, lalu tunggu review user sebelum\n"
        "notebook 02.",
    ),
)

CELLS.append(
    (
        "code",
        "for timeframe in Q1_TIMEFRAMES:\n"
        '    row_a = Q1_TABLE.loc[(timeframe, "A")]\n'
        "    print(\n"
        "        f\"{timeframe} A: sigma={row_a['sigma']:.3e} skew={row_a['skew']:.3f} \"\n"
        "        f\"kurt_excess={row_a['kurt_excess']:.3f} q0.1%={row_a['q_0.1%']:.3e} \"\n"
        "        f\"q99.9%={row_a['q_99.9%']:.3e}\"\n"
        "    )",
    ),
)


def build() -> None:
    """Tulis notebook dari daftar sel."""
    notebook = nbf.v4.new_notebook()
    notebook.cells = [
        nbf.v4.new_markdown_cell(source) if kind == "md" else nbf.v4.new_code_cell(source)
        for kind, source in CELLS
    ]
    notebook.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    }
    NB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with NB_PATH.open("w", encoding="utf-8") as handle:
        nbf.write(notebook, handle)
    print(f"notebook ditulis: {NB_PATH.relative_to(PROJECT_ROOT)} ({len(notebook.cells)} sel)")


if __name__ == "__main__":
    build()
    # Normalisasi format SEL NOTEBOOK sebelum eksekusi. Tanpa ini, format cell
    # hasil builder akan drift dari `ruff format --check` setiap kali builder
    # dijalankan ulang (persis kelas regresi SA-34: .ipynb diperbaiki manual,
    # lalu hilang saat regenerasi). Builder adalah sumber kebenaran, jadi
    # formatnya juga harus dihasilkan di sini.
    subprocess.run(
        [sys.executable, "-m", "ruff", "format", str(NB_PATH)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--inplace",
            "--ExecutePreprocessor.timeout=900",
            str(NB_PATH),
        ],
        cwd=PROJECT_ROOT,
    )
    print(f"nbconvert exit={result.returncode}")
    sys.exit(result.returncode)

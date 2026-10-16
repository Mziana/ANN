"""Generator + executor for notebooks/scalping/eda_08_ammo_R_explore.ipynb.

# LENGTH_EXCEPTION: generator §15.1 — referensi stabil + diff kecil +
# deterministik (seed tetap) + assertion mesin (bukan dokumen).
#
# REVIEW LOG (FASE 0, AGENTS.md §4 butir 9):
# R1: operasionalisasi (a)/(b)/(c) — slot = HH:MM broker, (a) = median semua bar sesi-sama
#     20 hari-R lampau, (b) = slot-sama termasuk hari-berjalan, (c) = tanpa hari-berjalan.
#     Alternatif yang dipertimbangkan: slot = indeks posisional bar-ke; DITOLAK (panjang hari
#     bisa bervariasi DST) — keputusan arsitek bila tak setuju.
# R2: Δ first/gap = pooled bobot-n dalam-band (bukan Δ agregat mentah) agar koheren dengan
#     null terstratifikasi-band; agregat mentah dilaporkan implisit via per-band. Arsitek menilai.
# R3: SEED_EXEC = tanggal UTC eksekusi (20261015); lokal = 2026-10-16. Bila eksekusi nyata
#     bergeser hari, seed TETAP (deterministik) — label tanggal dicatat di laporan.
# R4: build() memakai print() progres (2 baris) mengikuti preseden beku EDA-07 verbatim;
#     bukan print() produksi (tak ada path trading).


EDA-08 ammo_round_R (Blueprint FINAL 2026-10-15-eda08-ammo-R-draf.md):
generasi amunisi di R — joint 8-sel (estimasi), wick-pooled / gap-split /
dow-omnibus (famili FDR-BH q=0.10 TERTUTUP tepat 4 uji), volume lock-1-dari-3,
shortlist EDA-09 eksplisit (boleh kosong).

Warisan verbatim EDA-07: partisi R 384 hari, _boot_ci cluster-per-day,
_bh FDR, _wilson, resep tahun 2023H2/2024, seed EDA-07 HANYA untuk
rekonsiliasi-primer (resampling baru = seed eksekusi). REUSE parquet EDA-07
deterministik — RESCAN (scan_spikes) DILARANG dan tak diimpor.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_08_ammo_R_explore.ipynb"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


md(
    """# EDA-08 — ammo_round_R (generasi di R)

**Blueprint:** `thoughts/shared/plans/2026-10-15-eda08-ammo-R-draf.md` (§§1–15, FINAL).
**Peran ronde:** GENERASI di R (post-hoc diakui) — BUKAN konfirmasi. Konfirmasi = EDA-09
di partisi virgin. V/P DILARANG disentuh (whitelist-assert §Sel-1 membuat baca-V/P mustahil).

## Aturan yang mengikat notebook ini
- **REUSE parquet EDA-07** (`data/processed/events/eda07_spike_events.parquet`, Nunik=1632,
  full-room 1514). RESCAN DILARANG — `scan_spikes` tak diimpor di sel mana pun.
- **Famili FDR-BH q=0,10 TERTUTUP tepat 4 uji:** wick-pooled (1) + gap-split (2:
  first-split SEMUA event; gap-split NON-FIRST saja, cut 32 = 2×cooldown) + dow-omnibus (1).
  Tahun-split = gate, BUKAN uji. Volume = 0 uji. Joint = 0 uji (estimasi).
- **Null SEMUA uji = permutasi terstratifikasi B=10000, STRATA=BAND.**
  Donor-path DILARANG. L2/simulasi-trade DILARANG.
- **Shortlist EDA-09** = FDR-pass + gate-tahun + |Δ|≥5pp (dow = existence-only);
  joint = estimasi BUKAN kandidat; BOLEH KOSONG + alasan per kandidat.
- **Volume:** kunci SATU dari (a)/(b)/(c), SEMUA yang dicoba dilaporkan;
  warmup 20-hari-pertama-R di-drop dari evaluasi-volume (count dilaporkan).
- **Tiap kandidat wajib tag live-computability §9. Tiap angka bertag generasi/konfirmasi §8.**
"""
)

code(
    '''"""Sel 1 — setup, kontrak, manifest-R 384, reuse parquet, whitelist, F0, F1, F4."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def find_project_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "src").is_dir():
            return candidate
    raise RuntimeError("PROJECT_ROOT tidak ditemukan")


PROJECT_ROOT = find_project_root(Path.cwd().resolve())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.broker_time import wall_clock_series  # noqa: E402
from src.utils.config import load_config  # noqa: E402

# ---- Kontrak terkunci ----
PIP = 0.01
R_START = pd.Timestamp("2023-07-01", tz="UTC")
R_END_EXCL = pd.Timestamp("2025-01-01", tz="UTC")
DAILY_OPEN_HOURS = [22, 23]
SEED_EXEC = 20261015  # YYYYMMDD-eksekusi (UTC 2026-10-15); BARU, independen dari EDA-07
S_BOOT_JOINT = SEED_EXEC + 1
S_WICK = SEED_EXEC + 11
S_FIRST = SEED_EXEC + 12
S_GAP = SEED_EXEC + 13
S_DOW = SEED_EXEC + 14
S_DEMO = SEED_EXEC + 100
N_BOOT = 10_000
N_NULL = 10_000
B_DEMO = 500
FDR_Q = 0.10
POWER_MIN_N = 30
GAP_CUT = 32  # beku = 2x cooldown; tuning DILARANG
WARMUP_DAYS = 20
BAND_EDGES = [1.5, 2.0, 2.5, 3.0]
EPS = 1e-6

assert DAILY_OPEN_HOURS == [22, 23]
assert (N_BOOT, N_NULL) == (10_000, 10_000)
assert FDR_Q == 0.10 and POWER_MIN_N == 30 and GAP_CUT == 32 and WARMUP_DAYS == 20
assert BAND_EDGES == [1.5, 2.0, 2.5, 3.0]
assert len({SEED_EXEC, S_BOOT_JOINT, S_WICK, S_FIRST, S_GAP, S_DOW, S_DEMO}) == 7
assert all(s not in (20261006, 20261007)
           for s in (SEED_EXEC, S_BOOT_JOINT, S_WICK, S_FIRST, S_GAP, S_DOW, S_DEMO))

from math import sqrt as _sqrt  # noqa: E402


def _wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * _sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - m) / d, (c + m) / d


def _boot_ci(vals, day_ids, stat, seed, b=N_BOOT):
    """Warisan verbatim EDA-07 (cluster-bootstrap per hari)."""
    rng = np.random.default_rng(seed)
    vals = np.asarray(vals, dtype=float)
    day_ids = np.asarray(day_ids)
    days = np.unique(day_ids)
    per = [vals[day_ids == d] for d in days]
    boots = np.empty(b)
    for k in range(b):
        pick = rng.integers(0, len(days), len(days))
        boots[k] = stat(np.concatenate([per[j] for j in pick]))
    return float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def _bh(pvals, q=FDR_Q):
    """Warisan verbatim EDA-07 (Benjamini-Hochberg)."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    thr = 0.0
    for rank, (_, p) in enumerate(items, 1):
        if p <= rank / m * q:
            thr = p
    return {k for k, p in pvals.items() if p <= thr}, thr


def _find_key(node, target):
    if isinstance(node, dict):
        if target in node:
            return node[target]
        for value in node.values():
            hit = _find_key(value, target)
            if hit is not None:
                return hit
    return None


cfg = load_config("data")
anom_cfg = _find_key(cfg, "anomaly_windows")
assert anom_cfg, "anomaly_windows hilang (reuse gagal)"
ANOMALY = [(pd.Timestamp(w["start"]).date(), pd.Timestamp(w["end"]).date()) for w in anom_cfg]

DATA = PROJECT_ROOT / "data" / "processed"


def _load(tf: str) -> pd.DataFrame:
    """Warisan verbatim EDA-07 Sel 1 (beban M15/D1 + broker_day; TANPA deteksi)."""
    frames = [pd.read_parquet(DATA / tf / f"usdjpy_{tf.lower()}_{y}.parquet") for y in (2023, 2024)]
    df = pd.concat(frames, ignore_index=True)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    df = df.sort_values("time").reset_index(drop=True)
    df["broker_time"] = wall_clock_series(df["broker_time_raw"])
    df["broker_day"] = df["broker_time"].dt.date
    return df


m15 = _load("M15")
d1 = _load("D1")
anom_days: set = set()
for start, end in ANOMALY:
    anom_days.update(pd.date_range(start, end).date)
r = m15[(m15["time"] >= R_START) & (m15["time"] < R_END_EXCL)].copy()
assert r["time"].max() < R_END_EXCL
r = r[~r["broker_day"].isin(anom_days)].copy()
assert not r["broker_day"].isin(anom_days).any()

DAYS: dict = {}
for day, g in r.groupby("broker_day"):
    g = g.sort_values("time").reset_index(drop=True)
    if g["time"].iloc[0].hour not in DAILY_OPEN_HOURS:
        continue
    DAYS[day] = {"frame": g, "open": float(g["open"].iloc[0])}
print(f"R: {len(r)} bar | hari bersih = {len(DAYS)} (ekspektasi 384)")
assert len(DAYS) == 384, "partisi R != 384 → STOP"
MANIFEST = sorted(DAYS)
assert len(set(MANIFEST)) == 384

# ---- REUSE parquet EDA-07 (dibaca dari disk sebagai referensi terpisah) ----
PQ = PROJECT_ROOT / "data/processed/events/eda07_spike_events.parquet"
assert PQ.is_file(), "parquet EDA-07 hilang → STOP (F0-DIPERLUAS belum jalan)"
EV = pd.read_parquet(PQ)
EV["day"] = pd.to_datetime(EV["day"]).dt.date
assert len(EV) == 1632, f"F0 Nunik: {len(EV)} != 1632 → STOP"

# ---- WHITELIST-ASSERT: hari yang diload ⊆ manifest 384 hari-R; V/P mustahil ----
ev_days = set(EV["day"].tolist())
assert ev_days <= set(MANIFEST), "hari event di luar manifest-R → STOP (risiko V/P)"
assert EV["day"].min() >= R_START.date() and str(EV["day"].max()) < "2025-01-01"
print(f"whitelist: {len(ev_days)} hari-event ⊆ manifest 384 hari-R ✓ (V/P mustahil dibaca)")

# ---- F0 bit-identik vs vonis EDA-07 ----
bc_all = EV["band"].value_counts().sort_index().to_dict()
assert bc_all == {0: 515, 1: 415, 2: 240, 3: 462}, f"F0 band-unik: {bc_all} → STOP"
FR = EV[EV["drop_flag"] == 0].copy()
assert len(FR) == 1514, f"F0 full-room: {len(FR)} != 1514 → STOP"
bc_fr = FR["band"].value_counts().sort_index().to_dict()
assert bc_fr == {0: 460, 1: 391, 2: 231, 3: 432}, f"F0 band-fullroom: {bc_fr} → STOP"
exh_n = int(FR["has_exhaustion"].sum())
assert (exh_n, len(FR) - exh_n) == (395, 1119), f"F0 exh: {(exh_n, len(FR) - exh_n)} → STOP"
for col in ("mag_cont", "band", "has_exhaustion", "r_bar", "first_of_day",
            "drop_flag", "drop_reason", "outcome", "q3_ratio"):
    assert col in EV.columns, f"kolom wajib {col} hilang → STOP"
print(f"F0: Nunik=1632 band={bc_all} | full-room=1514 {bc_fr} | exh={exh_n}/1119 ✓")

# ---- Integritas reuse: first_of_day terkomputasi-ulang == flag parquet ----
# Referensi = baca-ulang parquet dari disk sebagai objek terpisah (bukan kolom EV yang sama)
EV_REF = pd.read_parquet(PQ)
assert len(EV_REF) == len(EV) == 1632, "referensi terpisah tak cocok → STOP"
EV_sorted = EV.sort_values(["day", "i", "s"]).reset_index(drop=True)
REF_sorted = EV_REF.sort_values(["day", "i", "s"]).reset_index(drop=True)
REF_sorted["day"] = pd.to_datetime(REF_sorted["day"]).dt.date
assert (REF_sorted["first_of_day"].to_numpy() == EV_sorted["first_of_day"].to_numpy()).all()
assert (REF_sorted["band"].to_numpy() == EV_sorted["band"].to_numpy()).all(), "band drift → STOP"
_recomp_first = np.zeros(len(EV_sorted), dtype=bool)
for _day, _idx in EV_sorted.groupby("day").groups.items():
    _pos = EV_sorted.index.get_indexer_for(_idx)
    _first_pos = _pos[np.argmin(EV_sorted.loc[_idx, "i"].to_numpy())]
    _recomp_first[_first_pos] = True
assert (_recomp_first == EV_sorted["first_of_day"].to_numpy()).all(), "flag first drift → STOP"
print(f"first_of_day reuse-valid: n_first={int(EV_sorted['first_of_day'].sum())} ✓")

# ---- Sesi bar-s + slot (untuk volume) + fingerprint ----
sys.path.insert(0, str(PROJECT_ROOT / "notebooks/scalping"))
from _eda_common import EXPECTED_FINGERPRINT, exclusive_label, session_fingerprint  # noqa: E402
from _eda_common import session_flags  # noqa: E402

assert session_fingerprint() == EXPECTED_FINGERPRINT, "definisi sesi berubah → STOP"
SESS, SLOT = {}, {}
for _day, _info in DAYS.items():
    _g = _info["frame"]
    SESS[_day] = exclusive_label(session_flags(_g["time"])).to_numpy()
    SLOT[_day] = _g["broker_time"].dt.strftime("%H:%M").to_numpy()
FR = FR.copy()
FR["sess_s"] = [str(SESS[d][s]) for d, s in zip(FR["day"], FR["s"])]
FR["slot_s"] = [str(SLOT[d][s]) for d, s in zip(FR["day"], FR["s"])]
FR["vol_s"] = [float(DAYS[d]["frame"]["tick_volume"].iloc[s]) for d, s in zip(FR["day"], FR["s"])]
FR["dow"] = [pd.Timestamp(d).dayofweek for d in FR["day"]]
FR["year2024"] = [str(d)[:4] == "2024" for d in FR["day"]]
assert FR["day"].apply(lambda d: str(d)[:4]).isin(["2023", "2024"]).all(), "tahun asing → STOP"

# ---- F1: tick_volume terisi ≥95% pada bar-s event ----
f1_fill = float(np.isfinite(FR["vol_s"].to_numpy()).mean())
print(f"F1: tick_volume bar-s terisi {f1_fill:.4f} (pagar ≥0.95)")
assert f1_fill >= 0.95, "F1 GAGAL → volume tertunda, STOP (kontinjensi §6)"
for _b in range(4):
    _m = FR["band"].to_numpy() == _b
    print(f"  F1 band{_b}: fill={float(np.isfinite(FR['vol_s'].to_numpy()[_m]).mean()):.4f}")

# ---- F4: seed baru tercatat ----
print(f"F4: SEED_EXEC={SEED_EXEC} boot_joint={S_BOOT_JOINT} wick={S_WICK} "
      f"first={S_FIRST} gap={S_GAP} dow={S_DOW} demo={S_DEMO}")
print("SEL 1 SELESAI")
'''
)

md(
    """## Sel 2 — Q-joint primer (ESTIMASI, tanpa vonis) + F2 + A1

Rate reversal-A per sel 4 band × 2 exh (8 sel) + CI95 cluster-per-day.
Sel n<30 → point-only + tanpa simpulan. Joint = ESTIMASI, BUKAN kandidat EDA-09.
"""
)

code(
    '''"""Sel 2 — joint 8 sel + rekonsiliasi margin vs primer EDA-07 (F2) + A1."""
DAYCODE = {d: k for k, d in enumerate(MANIFEST)}
FR["daycode"] = [DAYCODE[d] for d in FR["day"]]

JOINT = {}
for _b in range(4):
    for _e in (0, 1):
        _idx = FR[(FR["band"] == _b) & (FR["has_exhaustion"] == bool(_e))].index.to_numpy()
        _vals = np.array([1.0 if FR.loc[n, "outcome"] == "reversal" else 0.0 for n in _idx])
        _dids = np.array([FR.loc[n, "daycode"] for n in _idx])
        _oc = FR.loc[_idx, "outcome"]
        assert set(_oc.tolist()) <= {"reversal", "continuation", "timeout"}, "taksonomi bocor → STOP"
        if len(_idx) < POWER_MIN_N:
            JOINT[(_b, _e)] = {"n": len(_idx), "rate": float(_vals.mean()) if len(_idx) else float("nan"),
                               "ci95": [float("nan"), float("nan")],
                               "status": "point-only (n<30) — tanpa simpulan"}
        else:
            _lo, _hi = _boot_ci(_vals, _dids, np.mean, S_BOOT_JOINT)
            JOINT[(_b, _e)] = {"n": len(_idx), "rate": float(_vals.mean()),
                               "ci95": [_lo, _hi], "status": "ok"}
        print(f"joint band{_b}/exh{_e}: n={JOINT[(_b, _e)]['n']} "
              f"rev={JOINT[(_b, _e)]['rate']:.4f} ci={JOINT[(_b, _e)]['ci95']} "
              f"[{JOINT[(_b, _e)]['status']}] [GENERASI-R]")

# ---- A1: taksonomi per sel exhaustive ----
assert sum(v["n"] for v in JOINT.values()) == 1514, "A1 joint != 1514 → STOP"
assert sum(int((FR["band"] == _b).sum()) for _b in range(4)) == 1514, "A1 margin band → STOP"
print("A1: 8 sel exhaustive = 1514 ✓")

# ---- F2: rekonsiliasi margin vs primer EDA-07 ----
assert {b: int((FR["band"] == b).sum()) for b in range(4)} == {0: 460, 1: 391, 2: 231, 3: 432}
assert (int(FR["has_exhaustion"].sum()), int((~FR["has_exhaustion"]).sum())) == (395, 1119)
_agg_vals = np.array([1.0 if o == "reversal" else 0.0 for o in FR["outcome"]])
_agg_dids = FR["daycode"].to_numpy()
# Rekonsiliasi memakai seed EDA-07 (resampling identik → CI bit-identik)
_rlo07, _rhi07 = _boot_ci(_agg_vals, _agg_dids, np.mean, 20261006)
_k = int(_agg_vals.sum())
_wlo, _whi = _wilson(_k, 1514)
print(f"F2 primer-agregat: n=1514 k={_k} rev={_k / 1514:.4f} "
      f"CIcl=[{_rlo07:.4f},{_rhi07:.4f}] CInaive=[{_wlo:.4f},{_whi:.4f}]")
assert round(_k / 1514, 4) == 0.8223, "rate agregat drift vs EDA-07 → STOP"
assert [round(_rlo07, 4), round(_rhi07, 4)] == [0.8029, 0.8408], "CI agregat drift → STOP"
print("F2: joint=1514 + margin cocok primer EDA-07 ✓")
print("SEL 2 SELESAI")
'''
)

md(
    """## Sel 3 — F3 demo within-band (1 band) + A2

Demo metode tercil-dalam-band + permutasi kecil (B=500, stream demo terpisah).
Hasil demo = NON-INFERENSIAL (tak masuk FDR). A2: tercil within-band exhaustive per band.
"""
)

code(
    '''"""Sel 3 — F3 demo (band-0, B=500) + A2 tercil exhaustive."""
FR["wick_ratio"] = 1.0 - FR["q3_ratio"].abs()
assert ((FR["wick_ratio"] >= -EPS) & (FR["wick_ratio"] <= 1 + EPS)).all(), "wick_ratio liar → STOP"


def _tercile_masks(vals: np.ndarray):
    """Batas P33.3/P66.7 gaya EDA-07 §Sel-7 (lo_<=x<hi_)."""
    t1 = float(np.percentile(vals, 100 / 3))
    t2 = float(np.percentile(vals, 200 / 3))
    return (vals < t1), ((vals >= t1) & (vals < t2)), (vals >= t2), (t1, t2)


# ---- A2: tercil within-band exhaustive (4 band) ----
for _b in range(4):
    _w = FR[FR["band"] == _b]["wick_ratio"].to_numpy()
    _masks = _tercile_masks(_w)[:3]
    assert sum(int(m.sum()) for m in _masks) == len(_w), f"A2 band{_b} tak-exhaustive → STOP"
    print(f"A2 band{_b}: n={len(_w)} bawah={int(_masks[0].sum())} "
          f"tengah={int(_masks[1].sum())} atas={int(_masks[2].sum())} ✓")

# ---- F3 demo: band-0, B=500 ----
_b0 = FR[FR["band"] == 0]
_w0 = _b0["wick_ratio"].to_numpy()
_y0 = np.array([1.0 if o == "reversal" else 0.0 for o in _b0["outcome"]])
_mlo, _, _mhi, (_t1, _t2) = _tercile_masks(_w0)
_d_obs = float(_y0[_mhi].mean() - _y0[_mlo].mean())
_rng_d = np.random.default_rng(S_DEMO)
_null_d = np.empty(B_DEMO)
for _p in range(B_DEMO):
    _wp = _rng_d.permutation(_w0)
    _alo, _, _ahi, _ = _tercile_masks(_wp)
    _null_d[_p] = float(_y0[_ahi].mean() - _y0[_alo].mean())
_p_demo = float((1 + (np.abs(_null_d) >= abs(_d_obs)).sum()) / (B_DEMO + 1))
print(f"F3 demo band0: batas=({_t1:.4f},{_t2:.4f}) Δobs={_d_obs:.4f} "
      f"null-mean={_null_d.mean():.4f} p_demo={_p_demo:.4f} [DEMO-NON-INFERENSIAL]")
print("F3: tercil + permutasi jalan ✓")
print("SEL 3 SELESAI")
'''
)

md(
    """## Sel 4 — Q-wick (1 uji FDR)

Statistik primer SATU: pooled within-band Δ = rate(tercil-atas) − rate(tercil-bawah),
bobot-n per band, atas subset full-room. Null: permutasi NILAI wick dalam band
(tercil dihitung ulang per permutasi, B=10000), p dua-arah.
Robustness DI LUAR FDR (wajib lapor, dilarang klaim): Δ per band.
Year-gate: tanda pooled-Δ-per-tahun sama (2023H2 vs 2024); sel n<30 → gate tak lolos.
"""
)

code(
    '''"""Sel 4 — Q-wick pooled + null + gate-tahun."""
WB = {b: FR[FR["band"] == b] for b in range(4)}
W_w = {b: WB[b]["wick_ratio"].to_numpy() for b in range(4)}
W_y = {b: np.array([1.0 if o == "reversal" else 0.0 for o in WB[b]["outcome"]]) for b in range(4)}
W_n = {b: len(WB[b]) for b in range(4)}


def _pooled_delta(ws, ys):
    num, den, per = 0.0, 0, {}
    for b in ws:
        lo_m, _, hi_m, _ = _tercile_masks(ws[b])
        d_b = float(ys[b][hi_m].mean() - ys[b][lo_m].mean())
        per[b] = d_b
        num += len(ys[b]) * d_b
        den += len(ys[b])
    return num / den, per


wick_delta_obs, wick_perband = _pooled_delta(W_w, W_y)
print(f"wick pooled Δobs={wick_delta_obs:.4f} [GENERASI-R]")
for _b in range(4):
    print(f"  robustness band{_b}: n={W_n[_b]} Δ={wick_perband[_b]:.4f} "
          f"(lap deskr., BUKAN klaim) [GENERASI-R]")

_rng_w = np.random.default_rng(S_WICK)
wick_null = np.empty(N_NULL)
for _p in range(N_NULL):
    _ws = {b: _rng_w.permutation(W_w[b]) for b in range(4)}
    _d, _ = _pooled_delta(_ws, W_y)
    wick_null[_p] = _d
p_wick = float((1 + (np.abs(wick_null) >= abs(wick_delta_obs)).sum()) / (N_NULL + 1))
print(f"wick: Δobs={wick_delta_obs:.4f} null-mean={wick_null.mean():.4f} p={p_wick:.4f} [GENERASI-R]")

# ---- Year-gate wick: pooled Δ per tahun ----
wick_gate, wick_yg = "TAK-LOLOS", {}
for _lab, _sel in (("2023H2", ~FR["year2024"].to_numpy()), ("2024", FR["year2024"].to_numpy())):
    _fry = FR[_sel]
    if len(_fry) < POWER_MIN_N:
        wick_yg[_lab] = (float("nan"), len(_fry))
        continue
    _wsy = {b: _fry[_fry["band"] == b]["wick_ratio"].to_numpy() for b in range(4)}
    _ysy = {b: np.array([1.0 if o == "reversal" else 0.0
                         for o in _fry[_fry["band"] == b]["outcome"]]) for b in range(4)}
    if any(len(_ysy[b]) == 0 for b in range(4)):
        wick_yg[_lab] = (float("nan"), len(_fry))
        continue
    _dy, _ = _pooled_delta(_wsy, _ysy)
    wick_yg[_lab] = (_dy, len(_fry))
print(f"wick year-gate: 2023H2 Δ={wick_yg['2023H2'][0]:.4f} (n={wick_yg['2023H2'][1]}) vs "
      f"2024 Δ={wick_yg['2024'][0]:.4f} (n={wick_yg['2024'][1]})")
_s0, _s1 = np.sign(wick_yg["2023H2"][0]), np.sign(wick_yg["2024"][0])
if (wick_yg["2023H2"][1] >= POWER_MIN_N and wick_yg["2024"][1] >= POWER_MIN_N
        and np.isfinite(_s0) and np.isfinite(_s1) and _s0 == _s1 and _s0 != 0):
    wick_gate = "LOLOS"
print(f"wick gate-tahun: {wick_gate}")
print("SEL 4 SELESAI")
'''
)

md(
    """## Sel 5 — Q-gap (2 uji FDR)

first-split: rate first-of-day vs non-first (SEMUA event full-room).
gap-split: gap ≤32 vs >32 bar sejak s-spike-sebelumnya se-hari — HANYA event NON-FIRST
(event gap=INF hanya masuk first-split). Null: permutasi label grup DALAM band, B=10000.
Year-gate: tanda selisih sama per uji.
"""
)

code(
    '''"""Sel 5 — Q-gap: first-split + gap-split(non-first, cut 32)."""
# Gap = i_sekarang − s_spike-sebelumnya se-hari (atas SEMUA unik, lalu filter full-room)
EVs = EV_sorted.copy()
EVs["gap"] = np.inf
_prev_s: dict = {}
for _row in EVs.itertuples():
    _key = _row.day
    if _key in _prev_s:
        EVs.loc[_row.Index, "gap"] = _row.i - _prev_s[_key]
    else:
        assert bool(_row.first_of_day), "event tanpa-pendahulu bukan first → STOP"
    _prev_s[_key] = _row.s
assert ((EVs[EVs["first_of_day"]]["gap"] == np.inf)).all(), "INF bocor ke non-first → STOP"
assert np.isfinite(EVs[~EVs["first_of_day"]]["gap"].to_numpy()).all(), "gap non-finit → STOP"
print(f"gap: first=INF n={int(EVs['first_of_day'].sum())} | "
      f"non-first med={float(np.median(EVs[~EVs['first_of_day']]['gap'])):.1f} ✓")

FRM = EVs[EVs["drop_flag"] == 0].copy()
assert len(FRM) == 1514, "subset full-room gap != 1514 → STOP"
FRM["is_rev"] = (FRM["outcome"] == "reversal").astype(float)
FRM["wick_ratio"] = 1.0 - FRM["q3_ratio"].abs()
FRM["dow"] = [pd.Timestamp(d).dayofweek for d in FRM["day"]]
FRM["daycode"] = [DAYCODE[d] for d in FRM["day"]]
FRM["year2024"] = [str(d)[:4] == "2024" for d in FRM["day"]]


def _pooled_rate_diff(sub: pd.DataFrame, grp_col: str, a_val, b_val):
    """Δ pooled bobot-n antar grup (a−b), stratifikasi band; deskriptif per band."""
    num, den, per = 0.0, 0, {}
    for _b in range(4):
        _g = sub[sub["band"] == _b]
        _ya = _g[_g[grp_col] == a_val]["is_rev"].to_numpy()
        _yb = _g[_g[grp_col] == b_val]["is_rev"].to_numpy()
        _d = float(_ya.mean() - _yb.mean()) if len(_ya) and len(_yb) else float("nan")
        per[_b] = (_d, len(_ya), len(_yb))
        if np.isfinite(_d):
            num += len(_g) * _d
            den += len(_g)
    return (num / den if den else float("nan")), per


def _perm_pooled_diff(sub: pd.DataFrame, grp_col: str, a_val, b_val, seed: int):
    _idx_b = {b: sub[sub["band"] == b].index.to_numpy() for b in range(4)}
    _lab = {b: (sub.loc[_idx_b[b], grp_col] == a_val).to_numpy() for b in range(4)}
    _y = {b: sub.loc[_idx_b[b], "is_rev"].to_numpy() for b in range(4)}
    _obs, _ = _pooled_rate_diff(sub, grp_col, a_val, b_val)
    _rng = np.random.default_rng(seed)
    _null = np.empty(N_NULL)
    for _p in range(N_NULL):
        _num, _den = 0.0, 0
        for _b in range(4):
            _lp = _rng.permutation(_lab[_b])
            _d = float(_y[_b][_lp].mean() - _y[_b][~_lp].mean()) if _lp.any() and (~_lp).any() else 0.0
            _num += len(_y[_b]) * _d
            _den += len(_y[_b])
        _null[_p] = _num / _den
    _p = float((1 + (np.abs(_null) >= abs(_obs)).sum()) / (N_NULL + 1))
    return _obs, _p, _null


# ---- T2 first-split (SEMUA full-room) ----
FRM["is_first"] = FRM["first_of_day"].astype(bool)
for _b in range(4):
    _gb = FRM[FRM["band"] == _b]
    assert int(_gb["is_first"].sum()) >= 1 and int((~_gb["is_first"]).sum()) >= 1, \
        f"first-split band{_b} satu-sisi → STOP"
first_obs, p_first, first_null = _perm_pooled_diff(FRM, "is_first", True, False, S_FIRST)
_, first_per = _pooled_rate_diff(FRM, "is_first", True, False)
print(f"first-split: Δobs pooled={first_obs:.4f} p={p_first:.4f} [GENERASI-R]")
for _b in range(4):
    print(f"  band{_b}: Δ={first_per[_b][0]:.4f} (n_first={first_per[_b][1]}, "
          f"n_non={first_per[_b][2]}) deskr. [GENERASI-R]")

# ---- T3 gap-split (NON-FIRST saja, cut 32) ----
NF = FRM[~FRM["first_of_day"]].copy()
assert (NF["gap"] <= 900).all() and np.isfinite(NF["gap"].to_numpy()).all()
NF["gap_le32"] = NF["gap"] <= GAP_CUT
print(f"gap-split pool non-first: n={len(NF)} ≤32={int(NF['gap_le32'].sum())} "
      f">32={int((~NF['gap_le32']).sum())}")
assert len(NF) >= POWER_MIN_N
assert int(NF["gap_le32"].sum()) >= 1 and int((~NF["gap_le32"]).sum()) >= 1, \
    "gap-split satu-sisi → STOP"
for _b in range(4):
    _gb = NF[NF["band"] == _b]
    assert int(_gb["gap_le32"].sum()) >= 1 and int((~_gb["gap_le32"]).sum()) >= 1, \
        f"gap-split band{_b} satu-sisi → STOP"
gap_obs, p_gap, gap_null = _perm_pooled_diff(NF, "gap_le32", True, False, S_GAP)
_, gap_per = _pooled_rate_diff(NF, "gap_le32", True, False)
print(f"gap-split: Δobs pooled={gap_obs:.4f} p={p_gap:.4f} [GENERASI-R]")
for _b in range(4):
    print(f"  band{_b}: Δ={gap_per[_b][0]:.4f} (n_≤32={gap_per[_b][1]}, "
          f"n_>32={gap_per[_b][2]}) deskr. [GENERASI-R]")


def _year_gate_diff(sub: pd.DataFrame, grp_col: str, a_val, b_val, name: str):
    _ds = {}
    for _lab, _m in (("2023H2", ~sub["year2024"].to_numpy()), ("2024", sub["year2024"].to_numpy())):
        _d, _ = _pooled_rate_diff(sub[_m], grp_col, a_val, b_val)
        _ds[_lab] = (_d, int(_m.sum()))
    _s0, _s1 = np.sign(_ds["2023H2"][0]), np.sign(_ds["2024"][0])
    _ok = (_ds["2023H2"][1] >= POWER_MIN_N and _ds["2024"][1] >= POWER_MIN_N
           and np.isfinite(_s0) and np.isfinite(_s1) and _s0 == _s1 and _s0 != 0)
    print(f"{name} year-gate: 2023H2 Δ={_ds['2023H2'][0]:.4f} (n={_ds['2023H2'][1]}) vs "
          f"2024 Δ={_ds['2024'][0]:.4f} (n={_ds['2024'][1]}) → {'LOLOS' if _ok else 'TAK-LOLOS'}")
    return "LOLOS" if _ok else "TAK-LOLOS"


first_gate = _year_gate_diff(FRM, "is_first", True, False, "first-split")
gap_gate = _year_gate_diff(NF, "gap_le32", True, False, "gap-split")
print("SEL 5 SELESAI")
'''
)

md(
    """## Sel 6 — Q-dow (1 uji omnibus FDR, peran-KILL)

"Adakah perbedaan rate antar hari Senin–Jumat?" Statistik = max_d|rate_d − rate_agg|.
Null: permutasi label-dow antar event full-room DALAM band (B=10000).
Rate per hari = deskriptif (bukan uji). Year-gate: hari max-dev SAMA di 2023H2 dan 2024
DAN tanda deviasi sama; tahun dengan n<30 untuk hari itu → gate TAK DAPAT lolos.
"""
)

code(
    '''"""Sel 6 — Q-dow omnibus + null + gate-tahun."""
FRM["dow_lab"] = FRM["dow"]
_dows = sorted(FRM["dow_lab"].unique().tolist())
print(f"dow teramati: {_dows} (ekspektasi [0,1,2,3,4]=Senin–Jumat)")
assert set(_dows) <= {0, 1, 2, 3, 4}, "hari non-Senin–Jumat muncul → STOP"
assert len(_dows) == 5, "hari kerja tak lengkap → STOP"
_agg = float(FRM["is_rev"].mean())
_dow_rate = {d: float(FRM[FRM["dow_lab"] == d]["is_rev"].mean()) for d in _dows}
_dow_n = {d: int((FRM["dow_lab"] == d).sum()) for d in _dows}
for _d in _dows:
    _v = FRM[FRM["dow_lab"] == _d]["is_rev"].to_numpy()
    _dd = FRM[FRM["dow_lab"] == _d]["daycode"].to_numpy()
    _lo, _hi = _boot_ci(_v, _dd, np.mean, S_DOW)
    print(f"  dow{_d}: n={_dow_n[_d]} rate={_dow_rate[_d]:.4f} CI=[{_lo:.4f},{_hi:.4f}] deskr. [GENERASI-R]")
dow_obs = float(max(abs(_dow_rate[d] - _agg) for d in _dows))
dow_argmax = max(_dows, key=lambda d: abs(_dow_rate[d] - _agg))
print(f"dow omnibus: agg={_agg:.4f} max-dev={dow_obs:.4f} @dow{dow_argmax} [GENERASI-R]")

_idx_b = {b: FRM[FRM["band"] == b].index.to_numpy() for b in range(4)}
_lab_d = {b: FRM.loc[_idx_b[b], "dow_lab"].to_numpy() for b in range(4)}
_y_d = {b: FRM.loc[_idx_b[b], "is_rev"].to_numpy() for b in range(4)}
_rng_dow = np.random.default_rng(S_DOW)
dow_null = np.empty(N_NULL)
for _p in range(N_NULL):
    _rates = {}
    for _b in range(4):
        _lp = _rng_dow.permutation(_lab_d[_b])
        for _d in _dows:
            _m = _lp == _d
            if _m.any():
                _rates.setdefault(_d, []).append(_y_d[_b][_m])
    _ra = {d: float(np.concatenate(v).mean()) for d, v in _rates.items()}
    _ag = float(np.concatenate([_y_d[b] for b in range(4)]).mean())
    dow_null[_p] = max(abs(_ra[d] - _ag) for d in _ra)
p_dow = float((1 + (dow_null >= dow_obs).sum()) / (N_NULL + 1))
print(f"dow: stat={dow_obs:.4f} null-mean={dow_null.mean():.4f} p={p_dow:.4f} [GENERASI-R]")

# ---- Year-gate omnibus ----
dow_gate = "TAK-LOLOS"
_yg = {}
for _lab, _m in (("2023H2", ~FRM["year2024"].to_numpy()), ("2024", FRM["year2024"].to_numpy())):
    _s = FRM[_m]
    _a = float(_s["is_rev"].mean())
    _r = {d: float(_s[_s["dow_lab"] == d]["is_rev"].mean()) for d in _dows}
    _n = {d: int((_s["dow_lab"] == d).sum()) for d in _dows}
    _am = max(_dows, key=lambda d: abs(_r[d] - _a))
    _yg[_lab] = (_am, float(np.sign(_r[_am] - _a)), _n[_am], _a)
    print(f"  {_lab}: max-dev @dow{_am} tanda={_yg[_lab][1]:+.0f} (n_hari={_n[_am]})")
_y0, _y1 = _yg["2023H2"], _yg["2024"]
if _y0[0] == _y1[0] and _y0[1] == _y1[1] and _y0[1] != 0 and _y0[2] >= 30 and _y1[2] >= 30:
    dow_gate = "LOLOS"
print(f"dow gate-tahun: {dow_gate}")
print("SEL 6 SELESAI")
'''
)

md(
    """## Sel 7 — FDR-BH (famili TERTUTUP tepat 4) + shortlist EDA-09

Shortlist = FDR-pass + gate-tahun + |Δ|≥5pp (dow = existence-only).
Sensitivitas 3pp/7pp dilaporkan TANPA mengubah shortlist. Tiap kandidat bertag
live-computability §9 + label generasi.
"""
)

code(
    '''"""Sel 7 — FDR atas TEPAT 4 uji + shortlist + sensitivitas + tag."""
P_FAM = {"wick-pooled": p_wick, "first-split": p_first, "gap-split": p_gap, "dow-omnibus": p_dow}
assert len(P_FAM) == 4, "famili != 4 → STOP + amandemen (pagar HARKing)"
FDR_PASS, fdr_thr = _bh(P_FAM)
print(f"FDR-BH q={FDR_Q}: keluarga=4 lolos={len(FDR_PASS)} ambang={fdr_thr:.6f} [GENERASI-R]")
for _k, _p in sorted(P_FAM.items(), key=lambda kv: kv[1]):
    print(f"  p={_p:.4f} {'LOLOS' if _k in FDR_PASS else 'gugur'} {_k}")

CAND = {
    "wick": {"p": p_wick, "delta": wick_delta_obs, "gate": wick_gate,
             "live": "lagged-causal (butuh end-detector + live scan — dependensi bersama)",
             "gen": "GENERASI-R"},
    "first": {"p": p_first, "delta": first_obs, "gate": first_gate,
              "live": "lagged-causal (butuh end-detector + live scan — dependensi bersama)",
              "gen": "GENERASI-R"},
    "gap32": {"p": p_gap, "delta": gap_obs, "gate": gap_gate,
              "live": "lagged-causal (butuh end-detector + live scan — dependensi bersama)",
              "gen": "GENERASI-R"},
    "dow": {"p": p_dow, "delta": float("nan"), "gate": dow_gate,
            "live": "exactly-live", "gen": "GENERASI-R"},
}
SHORTLIST = []
for _name, _c in CAND.items():
    _fdr = "wick-pooled" if _name == "wick" else ("first-split" if _name == "first"
                                                  else ("gap-split" if _name == "gap32" else "dow-omnibus"))
    _reasons = []
    if _fdr not in FDR_PASS:
        _reasons.append(f"FDR-gugur (p={_c['p']:.4f})")
    if _c["gate"] != "LOLOS":
        _reasons.append("gate-tahun TAK-LOLOS")
    if _name != "dow" and not (np.isfinite(_c["delta"]) and abs(_c["delta"]) >= 0.05):
        _reasons.append(f"|Δ|={abs(_c['delta']):.4f} < 5pp")
    if not _reasons:
        SHORTLIST.append(_name)
        print(f"SHORTLIST ✓ {_name}: FDR-pass + gate + "
              f"{'existence-only' if _name == 'dow' else f'|Δ|={abs(_c[\"delta\"]):.4f}'} "
              f"| live={_c['live']} [GENERASI-R]")
    else:
        print(f"SHORTLIST ✗ {_name}: {'; '.join(_reasons)} | live={_c['live']} [GENERASI-R]")
print(f"SHORTLIST EDA-09: {SHORTLIST if SHORTLIST else 'KOSONG (sukses-dengan-nol)'}")

# Sensitivitas ambang (lapor saja — shortlist tak berubah)
_TEST_OF = {"wick": "wick-pooled", "first": "first-split", "gap32": "gap-split"}
for _thr in (0.03, 0.07):
    _s = [n for n in ("wick", "first", "gap32")
          if _TEST_OF[n] in FDR_PASS and CAND[n]["gate"] == "LOLOS"
          and np.isfinite(CAND[n]["delta"]) and abs(CAND[n]["delta"]) >= _thr]
    print(f"sensitivitas {int(_thr * 100)}pp (uji saja): "
          f"{(_s if _s else 'kosong')} — shortlist tak berubah")

# ---- Fig: Δ-wick per band + pooled ----
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

_fig, _ax = plt.subplots(figsize=(7, 4.2))
_xs = [0, 1, 2, 3]
_ys = [wick_perband[b] for b in _xs]
_ax.bar(_xs, _ys)
_ax.axhline(wick_delta_obs, ls="--", label=f"pooled Δ={wick_delta_obs:.4f}")
_ax.axhline(0, color="black", lw=0.8)
_ax.set_xticks(_xs)
_ax.set_xticklabels([f"band{b} (n={W_n[b]})" for b in _xs])
_ax.set_ylabel("Δ rate (tercil-atas − tercil-bawah)")
_ax.set_title("EDA-08: Δ-wick per band + pooled [GENERASI-R]")
_ax.legend()
FIG8 = PROJECT_ROOT / "reports/eda/2026-10-15-eda08/fig-wick-perband.png"
FIG8.parent.mkdir(parents=True, exist_ok=True)
_fig.savefig(FIG8, dpi=120)
plt.close(_fig)
print(f"kurva tersimpan: {FIG8.relative_to(PROJECT_ROOT)}")
print("SEL 7 SELESAI")
'''
)

md(
    """## Sel 8 — Q-vol (DEFINISI-LOCK, tanpa uji outcome)

Kunci SATU normalisasi dari (a)/(b)/(c); laporkan SEMUA yang dicoba + yang dibuang.
Warmup: 20 hari pertama R di-drop dari evaluasi-volume (count dilaporkan) — seragam (a)/(b)/(c).
(a) vol_bar-s / median-vol-sesi-sama-20-hari (sesi via label eksklusif, 20 hari-R lampau —
hari-berjalan dikecualikan karena sesi belum selesai saat bar-s: varian inklusif-hari
DITOLAK di definisi). (b) / median rolling-20d bar-slot-sama TERMASUK hari-berjalan
(nilai slot hari-ini = vol_bar-s sendiri; ex-post sah di R, BUKAN live-computable).
(c) / median rolling-20d bar-slot-sama TANPA hari-berjalan (live-jika-baseline-precomputed).
Slot = jam-menit broker HH:MM. Korelasi-outcome = deskriptif (tanpa p, tanpa null,
tak masuk FDR — BUKAN uji ke-5). 0 uji ronde ini untuk volume.
"""
)

code(
    '''"""Sel 8 — volume (a)/(b)/(c) + warmup-drop + lock SATU + deskriptif non-inferensial."""
WARM = set(MANIFEST[:WARMUP_DAYS])
FVE = FR[~FR["day"].isin(WARM)].copy()  # evaluasi-volume: drop 20 hari pertama R
print(f"warmup-drop: {len(FR) - len(FVE)} event di {len(WARM)} hari pertama-R "
      f"(evaluasi-volume n={len(FVE)})")
assert len(WARM) == WARMUP_DAYS and len(FVE) < len(FR)

# Baseline per hari: slot->vol + mask sesi — prakomputasi sekali (live: baseline-precomputed)
DIDX = {d: j for j, d in enumerate(MANIFEST)}
_SLOTVOL: dict = {}
_SESSMASK: dict = {}
for _d in MANIFEST:
    _g = DAYS[_d]["frame"]
    _SLOTVOL[_d] = dict(zip(SLOT[_d].tolist(), _g["tick_volume"].astype(float).tolist()))
    _SESSMASK[_d] = SESS[_d]


def _vol_ratios(day, slot, sess, vol):
    j = DIDX[day]
    past20 = MANIFEST[max(0, j - 20):j]
    # (a): median semua bar sesi-sama selama 20 hari-R lampau
    pool_a = []
    for _d in past20:
        _g = DAYS[_d]["frame"]
        _m = _SESSMASK[_d] == sess
        pool_a.extend(_g["tick_volume"].to_numpy()[_m].tolist())
    pool_a = np.array(pool_a, dtype=float)
    ra = vol / float(np.nanmedian(pool_a)) if len(past20) == 20 and len(pool_a) else float("nan")
    # (b): median slot-sama 20 hari termasuk hari-berjalan
    win_b = MANIFEST[max(0, j - 19):j + 1]
    pool_b = np.array([_SLOTVOL[_d].get(slot, float("nan")) for _d in win_b], dtype=float)
    rb = vol / float(np.nanmedian(pool_b)) if len(win_b) == 20 else float("nan")
    # (c): median slot-sama 20 hari TANPA hari-berjalan
    pool_c = np.array([_SLOTVOL[_d].get(slot, float("nan")) for _d in past20], dtype=float)
    rc = vol / float(np.nanmedian(pool_c)) if len(past20) == 20 else float("nan")
    return ra, rb, rc


_ratios = [_vol_ratios(d, s, e, v) for d, s, e, v in
           zip(FVE["day"], FVE["slot_s"], FVE["sess_s"], FVE["vol_s"])]
FVE["vol_a"] = [r[0] for r in _ratios]
FVE["vol_b"] = [r[1] for r in _ratios]
FVE["vol_c"] = [r[2] for r in _ratios]
for _col in ("vol_a", "vol_b", "vol_c"):
    _v = FVE[_col].to_numpy(dtype=float)
    _ok = np.isfinite(_v) & (_v > 0)
    assert _ok.mean() >= 0.95, f"kandidat {_col} valid-rate rendah → STOP"
    print(f"  kandidat {_col}: n_valid={int(_ok.sum())}/{len(FVE)} "
          f"med={float(np.median(_v[_ok])):.3f} "
          f"IQR=[{float(np.percentile(_v[_ok], 25)):.3f},{float(np.percentile(_v[_ok], 75)):.3f}] "
          f"P1/P99={float(np.percentile(_v[_ok], 1)):.3f}/{float(np.percentile(_v[_ok], 99)):.3f} "
          f"[GENERASI-R]")

# Deskriptif outcome-per-tercil (TANPA p — bukan uji; tak masuk FDR)
for _col in ("vol_a", "vol_b", "vol_c"):
    _vv = FVE[_col].to_numpy(dtype=float)
    _okm = np.isfinite(_vv) & (_vv > 0)
    _t1, _t2 = np.percentile(_vv[_okm], 100 / 3), np.percentile(_vv[_okm], 200 / 3)
    _yy = FVE["outcome"].to_numpy() == "reversal"
    _rts = [float(_yy[_okm & (_vv < _t1)].mean()), float(_yy[_okm & ((_vv >= _t1) & (_vv < _t2))].mean()),
            float(_yy[_okm & (_vv >= _t2)].mean())]
    print(f"  {_col} tercil-rev (deskr, non-inferensial): "
          f"{[round(x, 4) for x in _rts]} [GENERASI-R]")

# ---- LOCK satu (aturan eksplisit, provisional untuk arsitek) ----
_lock, _lock_why = "c", ("live-jika-baseline-precomputed; slot-sama = kontrol musiman-intraday "
                          "paling ketat; tanpa inklusi-diri; distribusi sane (lapor di atas)")
_vc = FVE["vol_c"].to_numpy(dtype=float)
_okc = np.isfinite(_vc) & (_vc > 0)
assert _okc.mean() >= 0.95, "vol-c degenerat → STOP (aturan lock gagal)"
print(f"VOLUME-LOCK (provisional): ({_lock}) vol_bar-s / median-rolling-20d-slot-sama-TANPA-hari-berjalan")
print(f"  alasan: {_lock_why}")
print("  dibuang: (a)=sesi-sama-20-hari (kontrol musiman lebih kasar dari slot-sama); "
      "(b)=termasuk-hari-berjalan (inklusi-diri vol_bar-s; bukan live-computable)")
print("  live-tag vol-c: live-jika-baseline-precomputed (syarat eksplisit) [GENERASI-R]")
print("  forward-note EDA-09: histori baseline V boleh memakai hari-R (past-only, live-sah); "
      "definisi rasio IDENTIK")
print("SEL 8 SELESAI")
'''
)

md(
    """## Sel 9 — SHORTLIST EDA-09 tertulis + handoff + Done §8

Shortlist BOLEH KOSONG (sukses-dengan-nol + alasan per kandidat).
Joint = estimasi BUKAN kandidat. Dow = existence-only (lokalisasi hari = ronde baru).
"""
)

code(
    '''"""Sel 9 — shortlist eksplisit + label generasi + Done."""
print("== SHORTLIST EDA-09 (tertulis, eksplisit) ==")
if SHORTLIST:
    for _name in SHORTLIST:
        _c = CAND[_name]
        print(f"  KANDIDAT {_name}: p={_c['p']:.4f} gate={_c['gate']} "
              f"Δ={_c['delta']:.4f} live=[{_c['live']}] [{_c['gen']}]")
else:
    print("  KOSONG (sukses-dengan-nol). Alasan per kandidat:")
    print(f"    wick: p={CAND['wick']['p']:.4f} gate={CAND['wick']['gate']} "
          f"|Δ|={abs(CAND['wick']['delta']):.4f}")
    print(f"    first: p={CAND['first']['p']:.4f} gate={CAND['first']['gate']} "
          f"|Δ|={abs(CAND['first']['delta']):.4f}")
    print(f"    gap32: p={CAND['gap32']['p']:.4f} "
          f"gate={CAND['gap32']['gate']} |Δ|={abs(CAND['gap32']['delta']):.4f}")
    print(f"    dow: p={CAND['dow']['p']:.4f} gate={CAND['dow']['gate']} (existence-only)")
print("== LABEL GENERASI (tiap angka di atas) ==")
print("  SEMUA angka ronde ini = GENERASI-R (post-hoc diakui); KONFIRMASI = EDA-09 di virgin.")
print("== HANDOFF ==")
print("  joint 8-sel = lookup stratifikasi (bukan fitur, bukan kandidat).")
print("  EDA-09 mengunci konstruksi dari R SEBELUM sentuh V (lock-sebelum-V).")
print("  L2/fade tetap GUGUR — tak ada simulasi trade di ronde ini.")
print("=== EDA-08 SELESAI: SEMUA ASSERTION PASS ===")
'''
)


def build() -> None:
    """Tulis notebook dan eksekusi top-to-bottom via nbconvert."""
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
    with NB_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        nbf.write(notebook, handle)
    print(f"notebook ditulis: {NB_PATH.relative_to(PROJECT_ROOT)} ({len(notebook.cells)} sel)")

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
            "--ExecutePreprocessor.timeout=1800",
            str(NB_PATH),
        ],
        cwd=PROJECT_ROOT,
    )
    _nb_bytes = NB_PATH.read_bytes().replace(b"\r\n", b"\n")
    with NB_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(_nb_bytes.decode("utf-8"))

    print(f"nbconvert exit={result.returncode}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    build()

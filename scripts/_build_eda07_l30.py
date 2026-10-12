"""Generator + executor for notebooks/scalping/eda_07_l30_arah.ipynb.

L3-0 deskriptif S3-1 (BUKAN model, BUKAN latih, BUKAN skor, BUKAN null):
baca arah 153 baris G3-pass T-07-3 (120 positif, 33 negatif) + peta 98
LOLOS native ke arah dominan + irisan. Fondasi = CSV beku EDA-07/I-2
(hanya dibaca; DILARANG hitung ulang strata/base).

Reuse-first: harness builder + eksekutor nbconvert + verify_registry dari
scripts/_build_eda07_i2.py; KONTRAK/K24 literal verbatim run 9;
assoc_irisan + filter IR_TER/IR_SES verbatim sel 16 run 9;
aturan verdict verbatim sel 16 run 9:
  ok = g1 and g2any and g3(wakil) and (g4 == NA or g4).
Arah dominan = tanda lift baris wakil (wakil = fitur G2-terbaik run 9;
setiap LOLOS memenuhi g3(wakil) menurut aturan, jadi bukan pilihan baru).

AGENTS.md S15.1 generator exemption applies (template file, stable refs,
deterministik: tanpa RNG sama sekali, assertion machines di notebook +
verify_registry builder-side).
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks/scalping/eda_07_l30_arah.ipynb"
REPORT_OUT_L30 = PROJECT_ROOT / "reports/eda" / "2026-10-12"

CELLS: list[tuple[str, str]] = []


def md(source: str) -> None:
    CELLS.append(("md", source))


def code(source: str) -> None:
    CELLS.append(("code", source))


# sel 00 (markdown: kontrak L3-0)
md(
    """# L3-0 - Peta arah G3-pass + 98 LOLOS (deskriptif, bukan model)

Notebook **deskriptif** S3-1 spec Lapisan 3: TANPA model, latih, skor,
null, backtest, P&L, klaim edge. Input = CSV beku EDA-07/I-2 (hanya
dibaca). Output = T-L3-0_arah.csv (153 baris G3-pass + tanda + irisan),
T-L3-0_peta98.csv (98 LOLOS x arah dominan + irisan), FIG-17 peta arah.

Batas mengikat: S3-0/S3-2/S3-3 (5 Tokyo = INVERS, dilarang jadi sinyal;
2 London tetap gugur; pdhl_d artefak; ambang G1/G2/G3/G4 beku; tanpa
2026; tanpa threshold-scan), A-1..A-7, W-1..W-4, C3-invers.
Ronde ini berakhir dengan TABEL ARAH, bukan investigasi baru (S8A)."""
)


# sel 01 (code: setup + helpers + K24 literal verbatim run 9)
code(
    '''"""Setup L3-0: import (pandas/numpy/matplotlib saja, S3-4), helper
chk/show, K24 literal verbatim run 9 (transcription-guard + provenance;
 L3-0 tak memakai konstanta dalam hitungan - hanya baca CSV beku)."""
import hashlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path


def find_project_root(start: Path) -> Path:
    """Cari root proyek (pyproject.toml + src/) dari cwd ke atas (verbatim I-2)."""
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "src").is_dir():
            return candidate
    raise RuntimeError("PROJECT_ROOT tidak ditemukan")


PROJECT_ROOT_NB = find_project_root(Path.cwd().resolve())
print("PROJECT_ROOT :", PROJECT_ROOT_NB)
REPORT_DIR = PROJECT_ROOT_NB / "reports/eda" / "2026-10-12"
REPORT_10 = PROJECT_ROOT_NB / "reports/eda" / "2026-10-10"

ASSERT_LOG: list[str] = []


def chk(cond: bool, msg: str, loud: bool = False) -> None:
    """Assertion mesin tercatat (pengganti assert telanjang agar terhitung)."""
    ASSERT_LOG.append(msg)
    assert cond, f"ASSERT GAGAL: {msg}"
    if loud:
        print(f"PASS: {msg}")


def show(df: pd.DataFrame, title: str) -> None:
    """Cetak tabel penuh sebagai teks agar tersimpan di output notebook."""
    print(title)
    print(df.to_string())
    print()


# K24 literal verbatim run 9 (nilai dikunci I-2 24/24 + verifikasi independen
# auditor; di sini di-assert ulang sebagai penjaga salah-salin).
N_HORIZONS = (5, 15, 30, 60)
LB_MARGIN_PIP = 0.20
LC_MULTS = (1.0, 2.0)
HORIZON = 120
STRIDE = 5
MI_BINS = 20
N_PERM = 100
N_BOOT = 1000
N_LEAK = 200
RHO_DROP = 0.8
G1_BIN_LO, G1_BIN_HI = 0.10, 0.90
G1_MIN_CLASS = 0.10
G1_CONT_MIN_N, G1_CONT_MIN_DAYS = 1000, 100
G2_MIN_SEM = 4
G4_STRESS_MIN_PP = 0.0
SEED07 = {"noise": 70701, "leak": 70702, "floor_base": 70703,
          "lift_base": 70704, "atr_check": 70705, "stab_base": 70800}
YEARS = (2023, 2024, 2025)
K24 = [("N_HORIZONS", N_HORIZONS, (5, 15, 30, 60)), ("LB_MARGIN_PIP", LB_MARGIN_PIP, 0.20),
       ("LC_MULTS", LC_MULTS, (1.0, 2.0)), ("HORIZON", HORIZON, 120), ("STRIDE", STRIDE, 5),
       ("MI_BINS", MI_BINS, 20), ("N_PERM", N_PERM, 100), ("N_BOOT", N_BOOT, 1000),
       ("N_LEAK", N_LEAK, 200), ("RHO_DROP", RHO_DROP, 0.8),
       ("G1_BIN_LO", G1_BIN_LO, 0.10), ("G1_BIN_HI", G1_BIN_HI, 0.90),
       ("G1_MIN_CLASS", G1_MIN_CLASS, 0.10), ("G1_CONT_MIN_N", G1_CONT_MIN_N, 1000),
       ("G1_CONT_MIN_DAYS", G1_CONT_MIN_DAYS, 100), ("G2_MIN_SEM", G2_MIN_SEM, 4),
       ("G4_STRESS_MIN_PP", G4_STRESS_MIN_PP, 0.0),
       ("SEED_noise", SEED07["noise"], 70701), ("SEED_leak", SEED07["leak"], 70702),
       ("SEED_floor", SEED07["floor_base"], 70703), ("SEED_lift", SEED07["lift_base"], 70704),
       ("SEED_atr", SEED07["atr_check"], 70705), ("SEED_stab", SEED07["stab_base"], 70800),
       ("YEARS", YEARS, (2023, 2024, 2025))]
chk(len(K24) == 24, "tepat 24 konstanta terkunci")
for nm, got, exp in K24:
    chk(got == exp, f"konstanta {nm} == {exp!r}")
print("PASS: 24/24 konstanta run 9 identik (nol drift).")
chk(len(SEED07) == 6, "SEED07 tepat 6 basis (L3-0 tanpa RNG: tak satu pun dipakai)")
print("L3-0 deterministik tanpa RNG (murni baca CSV beku + pemetaan).")'''
)


# sel 02 (code: manifest hash input + scope T-06-7 + assoc verbatim)
code(
    '''"""Manifest bukti SEBELUM: sha256 6 input beku ditulis ke disk DULU,
lalu di-assert sama (log-then-assert). Scope T-06-7 + assoc_irisan
verbatim sel 16 run 9."""
import hashlib

MANIFEST_SEBELUM = {
    "T-07-3_lift.csv": "27784A921C31E39946F0FA2F16FB2DFE7B23DD43B0C57CFB7415E52C0F20C22F",
    "T-07-2_mi_lantai.csv": "67BE1A52323CBDD0F7DDCA2D0C7543905F71ED28422FC761D650C7769C49E50F",
    "T-07-1_balance.csv": "7DFF3D15A78F1013E99B3ADF1152602EEDD28CFC0D76E33C8ACE1FA27BA50155",
    "T-06-7_gerbang_tercile.csv": "E03EA9AB070CC14A3658D30ADE1FD6C5FE47C51565C69D123D957AA097F34E51",
    "T-06-7_gerbang_sesi.csv": "2DD86BC709C2D06BEA104782E86ECDC3215B2BD7BF2814403EA0DFC8ABF7E385",
    "_gate_G2_alarm.csv": "DE39BEF0825BB8D804F4499048F85CF9EAB3545C17199580B1AD34B335E4C11F",
}
MANIFEST_PATHS = {
    "T-07-3_lift.csv": REPORT_DIR / "T-07-3_lift.csv",
    "T-07-2_mi_lantai.csv": REPORT_DIR / "T-07-2_mi_lantai.csv",
    "T-07-1_balance.csv": REPORT_DIR / "T-07-1_balance.csv",
    "T-06-7_gerbang_tercile.csv": REPORT_10 / "T-06-7_gerbang_tercile.csv",
    "T-06-7_gerbang_sesi.csv": REPORT_10 / "T-06-7_gerbang_sesi.csv",
    "_gate_G2_alarm.csv": REPORT_DIR / "_gate_G2_alarm.csv",
}
man_rows = []
for name, path in MANIFEST_PATHS.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    man_rows.append({"file": name, "sha256_aktual": actual,
                     "sha256_sebelum": MANIFEST_SEBELUM[name],
                     "cocok": bool(actual == MANIFEST_SEBELUM[name])})
MANIFEST = pd.DataFrame(man_rows)
MANIFEST.to_csv(REPORT_DIR / "_l30_manifest.csv", index=False)
show(MANIFEST, "MANIFEST hash input beku (SEBELUM tertanam, aktual dihitung)")
chk(bool(MANIFEST["cocok"].all()), "hash 6/6 input beku sama SEBELUM (bukti di _l30_manifest.csv)", loud=True)

T67_TER = pd.read_csv(REPORT_10 / "T-06-7_gerbang_tercile.csv")
T67_SES = pd.read_csv(REPORT_10 / "T-06-7_gerbang_sesi.csv")
chk(len(T67_TER) == 144, "T-06-7 tercile 144 baris")
chk(len(T67_SES) == 48, "T-06-7 sesi 48 baris")
IR_TER = T67_TER[T67_TER["LOLOS"] == True].copy().sort_values(["combo", "session",  # noqa: E712
    "atr_ter_s"]).reset_index(drop=True)
IR_SES = T67_SES[T67_SES["LOLOS"] == True].copy().sort_values(["combo",  # noqa: E712
    "session"]).reset_index(drop=True)
chk(len(IR_TER) == 23, "irisan tercile lolos = 23")
chk(len(IR_SES) == 7, "irisan sesi lolos = 7")
TER_IDS = [(r["combo"], r["session"], int(r["atr_ter_s"])) for _, r in IR_TER.iterrows()]
SES_IDS = [(r["combo"], r["session"]) for _, r in IR_SES.iterrows()]


def assoc_irisan(key: str):
    """Irisan EDA-06 yang menaungi target (LA -> irisannya; waktu -> semua irisan se-sesskey)."""
    if key.startswith("LA "):
        _, combo, sess, tside = key.split(" ", 3)
        tval = tside.rsplit(" ", 1)[0][1:]
        if tval == "ALL":
            return [("ses", combo, sess, 0)]
        return [("ter", combo, sess, int(tval))]
    _, sess, tN = key.split(" ", 2)
    tval = tN.rsplit(" ", 1)[0][1:]
    if tval == "ALL":
        return [("ses", c, s, 0) for c, s in SES_IDS if s == sess]
    return [("ter", c, s, int(tval)) for c, s, t in TER_IDS if s == sess and t == int(tval)]


print("scope + assoc_irisan verbatim run 9 siap (23+7).")'''
)


# sel 03 (code: arah 153 G3-pass -> CSV, re-read, assert)
code(
    '''"""T-L3-0_arah.csv: PERSIS baris G3-pass T-07-3 + tanda lift + irisan.
Tulis DULU ke disk, baca-ulang, baru assert (log-then-assert)."""
t3 = pd.read_csv(REPORT_DIR / "T-07-3_lift.csv")
chk(len(t3) == 1315, "T-07-3 beku 1315 baris")
chk(set(t3["G3"].dropna().unique().tolist()) <= {True, False}, "kolom G3 hanya True/False/NaN")
GPASS = t3[t3["G3"].eq(True)].copy()
chk(len(GPASS) == 153, "tepat 153 baris G3-pass")
chk(bool((GPASS["lift"] != 0).all()), "tak ada lift nol di set G3-pass (CI tak memuat 0)")
GPASS["tanda"] = np.where(GPASS["lift"] > 0, "pos", "neg")
chk(int(GPASS.duplicated(subset=["target", "fitur"]).sum()) == 0,
    "pasangan (target,fitur) unik di set G3-pass (kunci arah tunggal)")
n_pos = int((GPASS["tanda"] == "pos").sum())
n_neg = int((GPASS["tanda"] == "neg").sum())
print(f"split arah: pos={n_pos} neg={n_neg}")
GPASS["irisan"] = GPASS["target"].apply(lambda k: "|".join(str(i) for i in assoc_irisan(k)))
ARAH = GPASS[["target", "fitur", "lift", "ci_lo", "ci_hi", "tanda", "irisan"]].copy()
ARAH.to_csv(REPORT_DIR / "T-L3-0_arah.csv", index=False)
AR = pd.read_csv(REPORT_DIR / "T-L3-0_arah.csv")  # bukti re-read dari disk
chk(len(AR) == 153, "T-L3-0_arah.csv tepat 153 baris (re-read)")
chk(int((AR["tanda"] == "pos").sum()) == 120, "split positif = 120 (re-read)")
chk(int((AR["tanda"] == "neg").sum()) == 33, "split negatif = 33 (re-read)")
chk(set(AR["tanda"].unique().tolist()) == {"pos", "neg"}, "tanda tunggal-makna {pos,neg}")
print("PASS: T-L3-0_arah.csv 153 baris, split 120/33 (re-read dari disk).")
show(AR.head(10), "T-L3-0_arah.csv (10 pertama)")'''
)


# sel 04 (code: kandidat C3 - 5 Tokyo negatif eksak, 2 London absen)
code(
    '''"""Bukti C3: 5 Tokyo hadir SEMUA bertanda negatif dgn nilai eksak;
2 baris kandidat round_d London G3=False (CI memuat 0)."""
CAND_TOKYO = {
    "LB_bin Tokyo t2 N15": -0.0473,
    "LB_bin Tokyo tALL N5": -0.0549,
    "LB_rng Tokyo tALL N5": -0.7446,
    "LB_bin Tokyo tALL N15": -0.0279,
    "LB_rng Tokyo tALL N15": -1.5868,
}
CAND_LONDON = ["LB_rng London t3 N5", "LB_rng London tALL N5"]
tok = AR[(AR["fitur"] == "round_d") & (AR["target"].isin(CAND_TOKYO))]
show(tok, "5 Tokyo di set G3-pass (grep fitur=round_d)")
chk(len(tok) == 5, "5/5 Tokyo hadir di set G3-pass")
for k, v in CAND_TOKYO.items():
    got = tok[tok["target"] == k]
    chk(len(got) == 1, f"Tokyo {k} unik di set")
    chk(bool(abs(float(got["lift"].iloc[0]) - v) < 1e-9 and float(got["lift"].iloc[0]) < 0),
        f"Tokyo {k} lift tepat {v} dan negatif")
    chk(str(got["tanda"].iloc[0]) == "neg", f"Tokyo {k} bertanda neg")
lon_in = AR[(AR["target"].isin(CAND_LONDON)) & (AR["fitur"] == "round_d")]
chk(len(lon_in) == 0, "2/2 baris kandidat round_d London ABSEN dari set G3-pass")
t3full = pd.read_csv(REPORT_DIR / "T-07-3_lift.csv")
lon_full = t3full[(t3full["target"].isin(CAND_LONDON)) & (t3full["fitur"] == "round_d")][
    ["target", "fitur", "lift", "ci_lo", "ci_hi", "G3"]]
show(lon_full, "2 London kandidat round_d di T-07-3 penuh (GUGUR G3: CI memuat 0)")
chk(len(lon_full) == 2, "2/2 baris kandidat London unik")
chk(bool((lon_full["G3"] == False).all()), "G3 False utk 2/2 kandidat London")
chk(bool(((lon_full["ci_lo"] < 0) & (lon_full["ci_hi"] > 0)).all()),
    "CI 2/2 kandidat London memuat 0")
lon_nat = AR[AR["target"].isin(CAND_LONDON)][["target", "fitur", "lift", "tanda"]]
show(lon_nat, "Konteks: baris G3-pass fitur ASLI pd target London (yg gugur = baris round_d)")
print("PASS: C3 - 5 Tokyo negatif eksak, 2 kandidat London GUGUR G3 (S3-0/W-2/C3-invers).")'''
)


# sel 05 (code: verdict verbatim -> LOLOS-98 -> peta98, diff kosong)
code(
    '''"""Verdict native verbatim sel 16 run 9: ok = g1 and g2any and g3(wakil)
and (g4 NA or g4). Baris kandidat (fitur round_d) dikecualikan dari hitungan
native. Peta98: arah = tanda lift wakil + irisan. Diff himpunan KOSONG."""
t1 = pd.read_csv(REPORT_DIR / "T-07-1_balance.csv")
t2 = pd.read_csv(REPORT_DIR / "T-07-2_mi_lantai.csv")
t3b = pd.read_csv(REPORT_DIR / "T-07-3_lift.csv")
chk(len(t1) == 260, "T-07-1 beku 260 target")
chk(len(t2) == 6767, "T-07-2 beku 6767 baris")
chk(set(t1["G1"].unique().tolist()) <= {True, False}, "G1 bool murni")
chk(set(t2["G2"].unique().tolist()) <= {True, False}, "G2 bool murni")
chk(set(t2["wakil"].unique().tolist()) <= {True, False}, "wakil bool murni")
cand2 = t2[t2["fitur"] == "round_d"]
chk(len(cand2) == 7, "tepat 7 baris kandidat round_d di T-07-2")
chk(bool(cand2["wakil"].all() and cand2["G2"].all()), "7 kandidat wakil+G2 True (I-2)")
nat2 = t2[t2["fitur"] != "round_d"].copy()
nw = nat2[nat2["wakil"] == True].copy()
chk(len(nw) == 260 and bool((nw.groupby("target").size() == 1).all()),
    "tepat 1 wakil native per 260 target")
chk(set(t3b["G4"].dropna().unique().tolist()) <= {True, False}, "G4 hanya True/False/NaN")
g4map = {}
for k, grp in t3b.groupby("target"):
    if k.startswith("LA "):
        vals = grp["G4"].dropna().unique().tolist()
        chk(len(vals) == 1, f"G4 LA tunggal per target ({k})")
        g4map[k] = bool(vals[0])
    else:
        chk(bool(grp["G4"].isna().all()), f"G4 waktu = NA ({k})")
        g4map[k] = "NA"
g3w = t3b.merge(nw[["target", "fitur"]].rename(columns={"fitur": "wakil"}),
               left_on=["target", "fitur"], right_on=["target", "wakil"], how="inner")
chk(len(g3w) == 260, "G3 wakil terpetakan 260/260 target")
chk(bool(g3w["G3"].notna().all()), "G3 baris wakil selalu terisi (True/False)")
VD = pd.DataFrame([{
    "target": r["target"],
    "g1": bool(t1.set_index("target").loc[r["target"], "G1"]),
    "g2any": bool(nat2[nat2["target"] == r["target"]]["G2"].any()),
    "g3w": bool(t3b[(t3b["target"] == r["target"]) & (t3b["fitur"] == r["fitur"])]["G3"].iloc[0]),
    "g4": g4map[r["target"]],
} for _, r in nw.iterrows()])
VD["ok"] = VD.apply(lambda r: bool(r["g1"] and r["g2any"] and r["g3w"]
                                   and (r["g4"] == "NA" or bool(r["g4"]))), axis=1)
LOLOS = sorted(VD[VD["ok"]]["target"].tolist())
chk(len(VD) == 260, "260 target dievaluasi")
chk(len(LOLOS) == 98, "tepat 98 LOLOS native (verdict verbatim)")
chk("LB_bin Tokyo tALL N5" in LOLOS, "FIG_KEY I-2 anggota LOLOS")
for k in ["LB_bin London t1 N5", "LB_rng London t1 N5", "LC1 London t1 N5"]:
    chk(k in LOLOS, f"TOP3 I-2 {k} anggota LOLOS")
print(f"PASS: verdict verbatim 98 LOLOS / {len(VD) - len(LOLOS)} GUGUR.")
wakil_of = dict(zip(nw["target"], nw["fitur"]))
lift_of = {(row["target"], row["fitur"]): str(row["tanda"]) for _, row in AR.iterrows()}
PETA = pd.DataFrame([{"target": k, "wakil": wakil_of[k],
                      "arah": lift_of[(k, wakil_of[k])],
                      "irisan": "|".join(str(i) for i in assoc_irisan(k))} for k in LOLOS])
chk(bool(PETA["wakil"].notna().all()), "wakil terisi 98/98")
PETA.to_csv(REPORT_DIR / "T-L3-0_peta98.csv", index=False)
PE = pd.read_csv(REPORT_DIR / "T-L3-0_peta98.csv")  # bukti re-read dari disk
chk(len(PE) == 98, "T-L3-0_peta98.csv tepat 98 baris (re-read)")
d1 = set(PE["target"]) - set(LOLOS)
d2 = set(LOLOS) - set(PE["target"])
print(f"diff peta-vs-LOLOS: lebih={sorted(d1)} kurang={sorted(d2)}")
chk(len(d1) == 0 and len(d2) == 0, "diff himpunan 98 peta vs 98 LOLOS KOSONG", loud=True)
chk(set(PE["arah"].unique().tolist()) <= {"pos", "neg"}, "arah peta tunggal-makna {pos,neg}")
print(PE["arah"].value_counts().to_dict())
show(PE.head(10), "T-L3-0_peta98.csv (10 pertama)")'''
)


# sel 06 (code: FIG-17 peta arah)
code(
    '''"""FIG-17: hitung pos/neg per (sesi x horizon) dari 153 baris arah.
Horizon target-waktu = N; LA = LA-t{tval} (label eksplisit, makna tunggal)."""


def sesi_horizon(key: str):
    if key.startswith("LA "):
        _, _combo, sess, tside = key.split(" ", 3)
        return sess, "LA-" + tside.rsplit(" ", 1)[0]
    _kd, sess, tN = key.split(" ", 2)
    return sess, tN.rsplit(" ", 1)[1]


AR["sesi"] = AR["target"].apply(lambda k: sesi_horizon(k)[0])
AR["horizon"] = AR["target"].apply(lambda k: sesi_horizon(k)[1])
PIV = AR.groupby(["sesi", "horizon", "tanda"]).size().unstack(fill_value=0)
for c in ("pos", "neg"):
    if c not in PIV.columns:
        PIV[c] = 0
PIV = PIV[["pos", "neg"]]
print(PIV.to_string())
chk(int(PIV["pos"].sum()) == 120 and int(PIV["neg"].sum()) == 33,
    "FIG-17 mencakup penuh 153 (120/33)")
labels = [f"{s}/{h}" for s, h in PIV.index.tolist()]
x = np.arange(len(labels))
w = 0.38
fig, ax = plt.subplots(figsize=(14, 5))
ax.bar(x - w / 2, PIV["pos"].tolist(), width=w, label="pos (lift>0)")
ax.bar(x + w / 2, PIV["neg"].tolist(), width=w, label="neg (lift<0)")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha="right")
ax.set_ylabel("baris G3-pass")
ax.set_title("FIG-17 peta arah: pos/neg per sesi x horizon (153 baris G3-pass)")
ax.legend()
fig.tight_layout()
fig.savefig(REPORT_DIR / "FIG-17_peta_arah.png", dpi=100)
plt.close(fig)
print("FIG tersimpan: ['FIG-17_peta_arah.png']")'''
)


# sel 07 (code: kesimpulan + assert log)
code(
    '''"""Kesimpulan L3-0 satu paragraf (tanpa vonis model/edge; tanpa buka L3-1)."""
TOK5 = ["LB_bin Tokyo t2 N15 (-0.0473)", "LB_bin Tokyo tALL N5 (-0.0549)",
        "LB_rng Tokyo tALL N5 (-0.7446)", "LB_bin Tokyo tALL N15 (-0.0279)",
        "LB_rng Tokyo tALL N15 (-1.5868)"]
KESIMPULAN_L30 = (
    f"L3-0 deskriptif memetakan arah 153 baris G3-pass T-07-3 "
    f"({int((AR['tanda'] == 'pos').sum())} positif, {int((AR['tanda'] == 'neg').sum())} negatif; "
    f"tanda = arah lift desil-atas, tunggal-makna) ke T-L3-0_arah.csv + FIG-17 per sesi x horizon, "
    f"serta 98 pasangan LOLOS native (verdict verbatim G1+G2+G3+(G4 NA-or-True)) ke T-L3-0_peta98.csv "
    f"dengan arah dominan = tanda lift wakil run 9 + irisan EDA-06 verbatim. "
    f"Lima kandidat Tokyo hadir SEMUA bertanda negatif {', '.join(TOK5)} "
    f"(efek INVERS C3/A-2 menempel; dilarang jadi sinyal); "
    f"dua baris kandidat round_d London G3=False (CI memuat 0; gugur sbg kandidat), "
    f"sementara kedua targetnya tetap LOLOS via wakil asli (rv15/rv60 pos). "
    f"Diff himpunan 98 peta vs 98 LOLOS kosong; hash 6/6 input beku sama; K24 24/24. "
    f"Satu-satunya keluaran: TABEL ARAH go/no-go administratif ke L3-1 "
    f"(go = terdaftar di peta; no-go model = gagal M2/M3 nanti); "
    f"tanpa vonis model, tanpa klaim edge, L3-1 wewenang arsitek pasca-audit L3-0.")
print("KESIMPULAN_L30 TERKUNCI:")
print(KESIMPULAN_L30)
chk(len(KESIMPULAN_L30) > 200, "sel kesimpulan terisi (>200 karakter)")
print(f"ASSERT_LOG total: {len(ASSERT_LOG)}")
chk(len(ASSERT_LOG) >= 20, "assertion mesin minimal 20")
print("artefak L3-0: T-L3-0_arah.csv (153) + T-L3-0_peta98.csv (98) + "
      "FIG-17_peta_arah.png + _l30_manifest.csv")'''
)


# ===APPEND (verify + build, pola I-2)===

EXPECTED_CSVS_L30 = ["T-L3-0_arah.csv", "T-L3-0_peta98.csv", "_l30_manifest.csv"]
EXPECTED_FROZEN_ROWS = {
    "T-07-1_balance.csv": 260,
    "T-07-2_mi_lantai.csv": 6767,
    "T-07-3_lift.csv": 1315,
    "T-07-4_stabilitas.csv": 1335,
    "_gate_G2_alarm.csv": 86,
}
REPORT_OUT_CHECK = REPORT_OUT_L30


def verify_l30(report_dir: Path) -> None:
    """Registry L3-0: FIG-17 + 2 CSV L3-0 + manifest + penjaga baris beku."""
    report_dir = Path(report_dir).resolve()
    fig = report_dir / "FIG-17_peta_arah.png"
    assert fig.is_file(), "FIG-17 hilang"
    assert fig.stat().st_size > 0, "FIG-17 kosong"
    arah = sum(1 for _ in (report_dir / "T-L3-0_arah.csv").open(encoding="utf-8")) - 1
    assert arah == 153, f"T-L3-0_arah.csv bukan 153 ({arah})"
    peta = sum(1 for _ in (report_dir / "T-L3-0_peta98.csv").open(encoding="utf-8")) - 1
    assert peta == 98, f"T-L3-0_peta98.csv bukan 98 ({peta})"
    assert (report_dir / "_l30_manifest.csv").is_file(), "manifest hilang"
    for name, exp in EXPECTED_FROZEN_ROWS.items():
        rows = sum(1 for _ in (report_dir / name).open(encoding="utf-8")) - 1
        assert rows == exp, f"file beku berubah: {name} ({rows} vs {exp})"
    print(
        "registry L3-0: T-L3-0_arah.csv (153) + T-L3-0_peta98.csv (98) "
        "+ FIG-17_peta_arah.png + _l30_manifest.csv"
    )
    print(f"penjaga beku: {EXPECTED_FROZEN_ROWS} (baris data, tak berubah)")


def build() -> None:
    """Tulis notebook dan eksekusi top-to-bottom via nbconvert (tunggal via lock)."""
    lock = REPORT_OUT_L30 / ".eda07_l30_build.lock"
    REPORT_OUT_L30.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    except FileExistsError:
        age = time.time() - lock.stat().st_mtime
        if age < 5400:
            print(f"lock build aktif ({age:.0f} dtk) -> keluar agar eksekusi tunggal")
            sys.exit(3)
        lock.unlink()
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    print(f"lock diperoleh: {lock.relative_to(PROJECT_ROOT)}")
    for i, (kind, source) in enumerate(CELLS):
        if kind == "code":
            compile(source, f"<sel{i:02d}>", "exec")  # syntax sel tertangkap sebelum run
    print(f"pra-kompilasi {sum(1 for k, _ in CELLS if k == 'code')} sel kode: OK")
    assert len(CELLS) == 8, f"notebook L3-0 terkunci 8 sel, dapat {len(CELLS)}"
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
            "--ExecutePreprocessor.timeout=5400",
            str(NB_PATH),
        ],
        cwd=PROJECT_ROOT,
    )
    # Normalisasi EOL notebook sesudah nbconvert --inplace (penulis Windows
    # menghasilkan CRLF). Byte-level CRLF->LF; isi string sel tidak berubah.
    _nb_bytes = NB_PATH.read_bytes().replace(b"\r\n", b"\n")
    with NB_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(_nb_bytes.decode("utf-8"))

    print(f"nbconvert exit={result.returncode}")
    if result.returncode != 0:
        lock.unlink(missing_ok=True)
        sys.exit(result.returncode)
    try:
        verify_l30(REPORT_OUT_L30)
        for _name in ("T-L3-0_arah.csv", "T-L3-0_peta98.csv", "_l30_manifest.csv"):
            _p = REPORT_OUT_L30 / _name
            _p.write_bytes(_p.read_bytes().replace(b"\r\n", b"\n"))
        print("CSV L3-0 dinormalisasi CRLF->LF (pola I-1/I-2).")
    finally:
        lock.unlink(missing_ok=True)
    print("lock dilepas; build selesai.")


if __name__ == "__main__":
    build()

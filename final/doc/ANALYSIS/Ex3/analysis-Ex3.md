# Fixed-Budget Analysis — MOEA vs SOEA

This document provides a **plots-based analysis** of the eight fixed‑budget curves you supplied.
Each figure shows **best‑so‑far f(x)** versus **function evaluations** (log‑x scale) for
two algorithm families — **MOEA** and **SOEA** — at three settings (10, 20, 50). Shaded bands
show variability across runs.

> **Legend (per figure):**  
> MOEA‑10 / MOEA‑20 / MOEA‑50 (dashed/dotted warm colors) vs.  
> SOEA‑10 / SOEA‑20 / SOEA‑50 (solid/dotted cool colors).

---

## Global patterns across all eight problems

- **Anytime behaviour:** **SOEA consistently improves earlier** in the budget on most problems.
  The “knee” where performance rapidly increases occurs **sooner** for SOEA (typically between
  ~2×10³ and ~6×10³ evaluations) than for MOEA.
- **Final performance at the given budget:** On the 210x set, both families reach similar final
  values, with **SOEA usually a small margin ahead**. On the 220x set, **SOEA is clearly superior**,
  with the largest gap on **2200** where **MOEA stagnates** while SOEA keeps improving.
- **Population‑size effect:** **10** (and sometimes **20**) tends to reach good values **sooner**;
  **50** is more conservative early on and sometimes lags slightly at the final budget.
- **Stability:** Variability spikes around the knee for both families (expected during rapid
  exploitation). SOEA’s bands narrow again as it consolidates; MOEA exhibits narrow but **lower**
  plateaus on the harder 220x cases.
- **Takeaway:** For **short/medium budgets**, prefer **SOEA‑10/20**. For **long budgets**, SOEA
  remains robust; MOEA may be useful when maintaining diversity matters, but it **underperforms on
  the 220x set** at this budget.

---

## Per‑problem notes (with figures)

### 2100
- The sharp improvement begins near **2×10³ evaluations**.  
- **SOEA‑10/20** hit the knee **earlier** and reach a **slightly higher** plateau (~4.3–4.4×10²) than MOEA variants.  
- Variance is brief around the knee; curves converge tightly at the end.

![2100](plots/MOEA-SOEA-2100.png)

---

### 2101
- Same qualitative picture as 2100: **SOEA leads early** and maintains a **small final margin**.  
- MOEA variants arrive later to the plateau; SOEA’s final spread is slightly narrower.

![2101](plots/MOEA-SOEA-2101.png)

---

### 2102
- The final plateau is **higher** (~5.4–5.6×10²).  
- **SOEA** again transitions earlier and finishes **slightly ahead** of MOEA; variance around the knee is more visible.

![2102](plots/MOEA-SOEA-2102.png)

---

### 2103
- Harder instance (deeper initial values); final levels approach **~6.8–7.0×10²**.  
- **SOEA** reaches the positive region **earlier** and ends **ahead**; MOEA is close but consistently below near the end.

![2103](plots/MOEA-SOEA-2103.png)

---

### 2200
- **Most pronounced separation.** After ~10⁴ evaluations, **MOEA plateaus at a negative level** (≈−0.8×10³ to −1.0×10³),
  whereas **SOEA continues climbing** through **0** into the **+7–8×10²** range.  
- This suggests MOEA is **stuck in a local region** or that its selection/variation settings are **too conservative** for this landscape.

![2200](plots/MOEA-SOEA-2200.png)

---

### 2201
- Both families improve steadily but remain negative overall at this budget.  
- **SOEA leads** by a noticeable margin near the end (≈100–150 units), with **10/20** slightly ahead of **50**.

![2201](plots/MOEA-SOEA-2201.png)

---

### 2202
- Qualitatively matches 2201: **SOEA dominates**; MOEA trails by a similar margin at the end.  
- Early sections show overlapping uncertainty bands; separation grows with budget.

![2202](plots/MOEA-SOEA-2202.png)

---

### 2203
- Again, **SOEA finishes higher**; MOEA remains clearly below at the final budget.  
- The **gap widens** as budget increases beyond ~5×10³ evaluations.

![2203](plots/MOEA-SOEA-2203.png)

---

## Recommendations

1. **Time‑critical runs (<5×10³ FE):** use **SOEA‑10** (or **SOEA‑20** if slight stability boost is needed).  
2. **Longer budgets:** stay with **SOEA**; consider **MOEA** only if multi‑objective diversity is explicitly required.  
3. **Hard instances (220x, esp. 2200):** increase exploration for MOEA (higher mutation rate, occasional restarts, or stronger
   survivor selection pressure), or switch to SOEA as the default.

*End of analysis.*

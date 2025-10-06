# Comparison: (1+1) EA vs MMAS (ρ ∈ {1, 1/√n, 1/n})
**Setup assumed from your plots:** n = 100, 10 runs, 100,000 evaluations; Fixed‑Budget (best‑so‑far).  
**Note:** For F25, interpret on **linear y‑axis** (log hides zeros).

## F1 — OneMax (unimodal)
- **Early:** MMAS with **ρ=1** often jumps faster initially due to aggressive reinforcement; (1+1) EA climbs steadily.
- **Late:** **(1+1) EA** typically matches or slightly exceeds MMAS; **ρ=1/√n** is MMAS’s best trade‑off; **ρ=1/n** is slower.
- **Bottom line:** **(1+1) EA ≳ MMAS(ρ=1/√n) > MMAS(ρ=1) > MMAS(ρ=1/n)**.

## F2 — LeadingOnes (plateaus/level‑based)
- **Early:** (1+1) EA progresses level by level; MMAS benefits from **tie acceptance** but can over‑reinforce with **ρ=1**.
- **Late:** **(1+1) EA** is usually slightly ahead or tied with **MMAS(ρ=1/√n)**; **ρ=1/n** lags.
- **Bottom line:** **(1+1) EA ≳ MMAS(ρ=1/√n) > MMAS(ρ=1) ≈ MMAS(ρ=1/n)**.

## F3 — Linear (unimodal)
- **Early:** MMAS(ρ=1) may lead briefly; (1+1) EA rises smoothly.
- **Late:** **(1+1) EA** or **MMAS(ρ=1/√n)** end up best; **ρ=1/n** trails.
- **Bottom line:** **(1+1) EA ≳ MMAS(ρ=1/√n) > MMAS(ρ=1) > MMAS(ρ=1/n)**.

## F18 — LABS (rugged)
- **Early:** MMAS with **ρ=1** can lock in suboptimal patterns; (1+1) EA shows steadier gains.
- **Late:** **(1+1) EA** typically surpasses MMAS; **ρ=1/√n** is the strongest MMAS setting but often still behind.
- **Bottom line:** **(1+1) EA > MMAS(ρ=1/√n) > MMAS(ρ=1/n) > MMAS(ρ=1)** (variance expected).

## F23 — N‑Queens (many local optima)
- **Early:** Both improve; (1+1) EA may be slightly slower out of the gate than MMAS(ρ=1).
- **Late:** **(1+1) EA** generally overtakes; MMAS(ρ=1/√n) is the most competitive among MMAS variants.
- **Bottom line:** **(1+1) EA > MMAS(ρ=1/√n) > MMAS(ρ=1/n) > MMAS(ρ=1)**.

## F24 — Concatenated Trap (deceptive)
- **Early:** Both gain modestly; **ρ=1** can over‑commit MMAS to wrong basins.
- **Late:** Both plateau; sometimes **MMAS(ρ=1/√n)** edges (1+1) EA, other times (1+1) EA matches or leads slightly.
- **Bottom line:** **No clear universal winner**; slight edge alternates between **(1+1) EA** and **MMAS(ρ=1/√n)**; **ρ=1/n** safest but slowest.

## F25 — NK Landscapes (rugged; use linear y)
- **Early:** Noisy gains for both; MMAS(ρ=1) prone to premature convergence.
- **Late:** **(1+1) EA** typically achieves the highest final mean; **MMAS(ρ=1/√n)** is the closest competitor; **ρ=1/n** conservative.
- **Bottom line:** **(1+1) EA > MMAS(ρ=1/√n) > MMAS(ρ=1/n) > MMAS(ρ=1)**.

---

## Overall
- **(1+1) EA** is strongest on unimodal/structured problems (F1, F3, F2) and remains competitive or best on rugged ones (F18, F23, F25).  
- **MMAS** is highly sensitive to **ρ**: **ρ=1/√n** is the most reliable across functions; **ρ=1** is fast early but risks lock‑in; **ρ=1/n** is stable but slow.  
- On deceptive **F24**, both tend to plateau; relative ordering depends on runs/instances, with **MMAS(ρ=1/√n)** or **(1+1) EA** taking a slight edge.

(If you want a short caption for each plot, use the “Bottom line” lines above.)

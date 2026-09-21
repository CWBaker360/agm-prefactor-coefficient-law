# Prefactor Coefficient Laws for the Gauss-Legendre AGM Algorithm

**Author:** Wayne Baker  
**Revised:** September 21, 2026  
**Status:** Preprint / source and reproducibility archive

This repository contains the paper, LaTeX source, and numerical verification script for:

> **Prefactor Coefficient Laws for the Gauss-Legendre AGM Algorithm**

## Read the paper

- [`paper/agm_prefactor_coefficient_law.pdf`](paper/agm_prefactor_coefficient_law.pdf)
- [`paper/agm_prefactor_coefficient_law.tex`](paper/agm_prefactor_coefficient_law.tex)

## Main result

For the lower Gauss-Legendre approximants \(\pi_n\), define the exact fitted correction coefficient

\[
\alpha_n
=
-\frac{\pi_{n+1}-\pi}{\pi_{n+1}-\pi_n}.
\]

Then

\[
\frac{\alpha_{n+1}}{\alpha_n^2}
\longrightarrow
\frac12.
\]

The proof uses Brent's theta-function expansion. Writing

\[
\varepsilon_n=\pi_n-\pi=A_n e^{-\pi 2^{n+1}},
\]

one obtains

\[
A_n\sim-2^{n+4}\pi^2,
\qquad
\frac{A_{n+1}}{A_n}\longrightarrow2.
\]

The doubly exponential terms cancel exactly in the quotient that determines \(\alpha_{n+1}/\alpha_n^2\), leaving the prefactor limit \(1/2\).

The companion numerator-channel coefficient
\[
\beta_n
=
-\frac{Q_{n+1}-4\pi t_{n+1}}{Q_{n+1}-Q_n},
\qquad
Q_n=(a_n+b_n)^2,
\]
now has an analytic prefactor law as well.  With
\[
x_n=e^{-\pi2^{n+1}},
\qquad
C_n=2^{n+2}\pi-1,
\]
the paper proves
\[
\beta_n
=
-C_nx_n
\left[
1-2x_n+
\left(2-\frac1{C_n}\right)x_n^2
+O(x_n^3)
\right],
\]
and consequently
\[
-\pi2^{n+1}\frac{\beta_{n+1}}{\beta_n^2}
\longrightarrow1.
\]

## Numerical verification

The script

```text
scripts/verify_agm_coefficient_law.py
```

reconstructs the Gauss-Legendre sequence at arbitrary precision and reproduces the two numerical tables in the paper. It also compares the fitted-coefficient quotient with the direct error quotient

\[
\frac{\varepsilon_{n+2}\varepsilon_n^2}{\varepsilon_{n+1}^3}.
\]

Run the original \(\alpha_n\) audit from the repository root:

```bash
python scripts/verify_agm_coefficient_law.py --precision 500 --outdir outputs
```

Run the sharpened \(\beta_n\) audit with:

```bash
python scripts/verify_agm_beta_prefactor_law.py --precision 1000 --iterations 7
```

## Scope

The theorem concerns a fitted dynamic error coefficient for the lower Gauss-Legendre approximants. It does not assert a fixed recurrence of the form \(\varepsilon_{n+1}\sim C\varepsilon_n^2\) with nonzero constant \(C\).

The numerator-surgery statement is also analytic: it is derived from Brent's exact theta parametrization and tail identity, together with the defining theta-series expansions.

The verification scripts support the reported computations. They are not used as theorem evidence; both coefficient laws are proved analytically from the cited theta-function formulas.

## Related repositories

- [`nseries-pi-acceleration`](https://github.com/CWBaker360/nseries-pi-acceleration)
- [`constructible-cubic-trisection`](https://github.com/CWBaker360/constructible-cubic-trisection)
- [`proportional-subtended-cubic-refinement`](https://github.com/CWBaker360/proportional-subtended-cubic-refinement)

## Repository structure

```text
.
├── README.md
├── CITATION.cff
├── REPRODUCIBILITY.md
├── LICENSE_NOTICE.md
├── CHANGELOG.md
├── SHA256SUMS.txt
├── .gitignore
├── paper/
│   ├── agm_prefactor_coefficient_law.tex
│   ├── agm_prefactor_coefficient_law.pdf
│   └── README.md
├── scripts/
│   ├── verify_agm_coefficient_law.py
│   ├── verify_agm_beta_prefactor_law.py
│   └── README.md
└── docs/
    ├── abstract.md
    ├── repository_description.md
    └── github_upload_checklist.md
```

## Rights

Copyright © 2026 Wayne Baker. All rights reserved unless otherwise stated.

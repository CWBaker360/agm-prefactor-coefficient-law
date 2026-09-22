# A Prefactor Coefficient Law for the Gauss-Legendre AGM Algorithm

**Author:** Wayne Baker  
**Manuscript date:** June 30, 2026  
**Revised Zenodo deposit:** September 22, 2026  
**DOI:** [10.5281/zenodo.22896047](https://doi.org/10.5281/zenodo.22896047)  
**Status:** Published preprint / source and reproducibility archive

This repository contains the paper, LaTeX source, and numerical verification script for:

> **A Prefactor Coefficient Law for the Gauss-Legendre AGM Algorithm**

## Read and cite the paper

- **Zenodo:** [10.5281/zenodo.22896047](https://doi.org/10.5281/zenodo.22896047)
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

## Numerical verification

The script

```text
scripts/verify_agm_coefficient_law.py
```

reconstructs the Gauss-Legendre sequence at arbitrary precision and reproduces the two numerical tables in the paper. It also compares the fitted-coefficient quotient with the direct error quotient

\[
\frac{\varepsilon_{n+2}\varepsilon_n^2}{\varepsilon_{n+1}^3}.
\]

Run from the repository root:

```bash
python scripts/verify_agm_coefficient_law.py --precision 500 --outdir outputs
```

## Scope

The theorem concerns a fitted dynamic error coefficient for the lower Gauss-Legendre approximants. It does not assert a fixed recurrence of the form \(\varepsilon_{n+1}\sim C\varepsilon_n^2\) with nonzero constant \(C\).

The companion statement about the numerator-surgery coefficients \(\beta_n\) is explicitly numerical; it is not promoted to a theorem in this paper.

The verification script supports the reported computations. The proof of the main coefficient law is analytic and rests on the cited theta-function asymptotic.

## Keywords

Gauss-Legendre algorithm · arithmetic-geometric mean · operator coefficients · sequence acceleration · Aitken \(\Delta^2\) · prefactor asymptotics · Baker N-series · numerical analysis

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
│   └── README.md
└── docs/
    ├── abstract.md
    ├── repository_description.md
    └── github_upload_checklist.md
```

## Rights

The revised preprint archived at Zenodo is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Other repository files are governed by [`LICENSE_NOTICE.md`](LICENSE_NOTICE.md).

Copyright © 2026 C. Wayne Baker.

# Reproducibility

## Paper compilation

From the `paper` directory:

```bash
pdflatex agm_prefactor_coefficient_law.tex
pdflatex agm_prefactor_coefficient_law.tex
```

The second pass settles cross-references and bibliography labels.

## Python environment

Required:

```text
Python 3.10 or later
mpmath
```

Install the dependency with:

```bash
python -m pip install mpmath
```

## Reproduce the numerical tables

From the repository root:

```bash
python scripts/verify_agm_coefficient_law.py --precision 500 --outdir outputs
```

The script writes:

```text
outputs/agm_fitted_coefficients.csv
outputs/agm_coefficient_ratios.csv
outputs/verification_summary.txt
```

It checks the values printed in the paper unless `--skip-table-check` is supplied.

## Numerical quantities

The script reconstructs the lower Gauss-Legendre approximants and computes:

\[
\varepsilon_n=\pi_n-\pi,
\qquad
\alpha_n=-\frac{\varepsilon_{n+1}}{\varepsilon_{n+1}-\varepsilon_n},
\]

\[
A_n=\varepsilon_n e^{\pi 2^{n+1}},
\qquad
\frac{\alpha_{n+1}}{\alpha_n^2},
\qquad
\frac{\varepsilon_{n+2}\varepsilon_n^2}{\varepsilon_{n+1}^3},
\qquad
\frac{A_{n+1}}{A_n}.
\]

`mp.pi` is used as the numerical reference value of \(\pi\).

## Interpretation

The computation reproduces the finite-index tables and checks implementation consistency. The limiting law is proved analytically in the paper from Brent's theta-function expansion; it is not inferred solely from decimal agreement.

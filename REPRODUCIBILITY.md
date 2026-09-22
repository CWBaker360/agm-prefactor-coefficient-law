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

## Reproduce the beta-channel prefactor audit

From the repository root:

```bash
python scripts/verify_agm_beta_prefactor_law.py --precision 1000 --iterations 7
```

The beta audit writes:

```text
outputs/agm_beta_prefactor_audit.csv
```

The default range \(n=0,\ldots,6\) avoids the cancellation-driven precision floor that appears if too many AGM iterations are requested at fixed working precision.

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

The beta-channel audit additionally computes
\[
x_n=e^{-\pi2^{n+1}},
\qquad
C_n=2^{n+2}\pi-1,
\]
and checks the normalized asymptotic expansions
\[
\frac{\beta_n}{-C_nx_n}
=
1-2x_n+\left(2-\frac1{C_n}\right)x_n^2+O(x_n^3),
\]
and
\[
\frac{\beta_{n+1}/\beta_n^2}{-C_{n+1}/C_n^2}
=
1+4x_n+\left(6+\frac2{C_n}\right)x_n^2+O(x_n^3).
\]

## Interpretation

The computations reproduce the finite-index tables and check implementation consistency. The \(\alpha_n\) and \(\beta_n\) limiting laws are proved analytically in the paper from Brent's theta-function formulas; they are not inferred solely from decimal agreement.


## Regenerate the integrity ledger

Commit all manuscript, script, and documentation changes first. Then, from the
repository root, run:

```bash
python scripts/regenerate_sha256s.py
```

The script hashes the exact Git blob bytes stored at `HEAD` rather than the
platform-dependent working-tree representation. This avoids CRLF/LF checksum
differences on Windows.

Review the resulting `SHA256SUMS.txt`, then commit that ledger as a separate
finalization commit. The ledger intentionally excludes itself.

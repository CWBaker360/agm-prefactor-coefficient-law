# Verification scripts

## Alpha-channel audit

`verify_agm_coefficient_law.py` reconstructs the lower Gauss-Legendre approximants and reproduces the two original numerical tables in the paper.

From the repository root:

```bash
python scripts/verify_agm_coefficient_law.py --precision 500 --outdir outputs
```

The default run also checks the rounded values printed in the paper and exits with a nonzero status if they disagree.

## Beta-channel prefactor audit

`verify_agm_beta_prefactor_law.py` checks the sharpened analytic expansion for the numerator-surgery coefficient and its quotient law:

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

\[
\frac{\beta_{n+1}/\beta_n^2}{-C_{n+1}/C_n^2}
=
1+4x_n+
\left(6+\frac2{C_n}\right)x_n^2
+O(x_n^3).
\]

Run:

```bash
python scripts/verify_agm_beta_prefactor_law.py --precision 1000 --iterations 7
```

The script writes `outputs/agm_beta_prefactor_audit.csv`. The computation is a reproducibility check; the proof is analytic.

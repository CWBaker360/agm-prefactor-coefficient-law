# Verification script

`verify_agm_coefficient_law.py` reconstructs the lower Gauss-Legendre approximants and reproduces the two numerical tables in the paper.

From the repository root:

```bash
python scripts/verify_agm_coefficient_law.py --precision 500 --outdir outputs
```

The default run also checks the rounded values printed in the paper and exits with a nonzero status if they disagree.

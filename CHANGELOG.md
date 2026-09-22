# Changelog

## preprint-v2 — 2026-09-21

- Promoted the numerator-surgery coefficient from a numerical observation to an analytic theorem.
- Added the prefactor expansion
  \(\beta_n=-C_nx_n[1-2x_n+(2-C_n^{-1})x_n^2+O(x_n^3)]\),
  with \(x_n=e^{-\pi2^{n+1}}\) and \(C_n=2^{n+2}\pi-1\).
- Proved the scaled quotient law
  \(-\pi2^{n+1}\beta_{n+1}/\beta_n^2\to1\).
- Added a dedicated high-precision beta-channel verification script.
- Updated the abstract, README, and reproducibility documentation.
- Retitled the revised manuscript to reflect the two analytic coefficient laws and standardized numerator-channel terminology.
- Added an explicit citation for the N-series comparison and corrected the Brent volume title to *Visualisation*.
- Removed the non-SPDX `proprietary` value from `CITATION.cff`; rights remain governed by `LICENSE_NOTICE.md`.

## preprint-v1 — 2026-07-13

- Created the standalone paper and reproducibility archive.
- Added the final LaTeX source and matching six-page PDF.
- Added a Python script that reconstructs the Gauss-Legendre sequence and reproduces the published numerical tables.
- Added citation metadata, reproducibility instructions, repository documentation, and SHA-256 integrity records.
- Standardized the public paper filenames and excluded obsolete draft names.

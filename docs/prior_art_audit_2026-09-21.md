# Focused prior-art audit: fitted AGM prefactor laws

**Date:** 2026-09-21  
**Scope:** Gauss-Legendre / Brent-Salamin AGM error asymptotics, fitted correction coefficients, and the revised alpha- and beta-channel laws in this repository.

## Current manuscript claims under audit

For the lower Gauss-Legendre approximants pi_n, the manuscript defines

[
alpha_n
=
-rac{pi_{n+1}-pi}{pi_{n+1}-pi_n}
]

and proves

[
rac{alpha_{n+1}}{alpha_n^2}	orac12.
]

For

[
Q_n=(a_n+b_n)^2,
qquad
eta_n
=
-rac{Q_{n+1}-4pi t_{n+1}}{Q_{n+1}-Q_n},
]

the revised manuscript proves, with

[
x_n=e^{-pi2^{n+1}},
qquad
C_n=2^{n+2}pi-1,
]

that

[
eta_n
=
-C_nx_n
left[
1-2x_n+
left(2-rac1{C_n}ight)x_n^2
+O(x_n^3)
ight],
]

and consequently

[
-pi2^{n+1}rac{eta_{n+1}}{eta_n^2}	o1.
]

## Closest located prior art

### Richard P. Brent, *The Borwein brothers, Pi and the AGM*

This is the principal analytic source used by the manuscript.

Relevant formulas in Section 4 include:

- Eq. (13): theta-function parametrization of the AGM iterates (a_n,b_n).
- Eq. (16): (a_infty=	heta_3(q)^{-2}) in the self-dual Gauss-Legendre case.
- Eq. (17): (s_infty=	heta_3(q)^{-4}/pi).
- Eq. (18): exact theta-series tail for (s_n-s_infty).
- Following Eq. (19): for Brent's upper approximant error
  (e_n=a_n^2/s_n-pi),
  [
  e_{n+1}/e_n^2	o1/(8pi).
  ]
- Eq. (20) and the discussion immediately following it: the lower
  approximant (a_{n+1}^2/s_n) has leading error
  [
  (2^{n+4}pi^2-8pi)q^{2^{n+1}},
  qquad q=e^{-pi},
  ]
  with a smaller next-order remainder.

Reference:
Richard P. Brent, "The Borwein brothers, Pi and the AGM",
Springer Proceedings in Mathematics & Statistics 313 (2020), 323--348;
arXiv:1802.07558.

## Distinction from the revised manuscript

Brent supplies the theta identities, error bounds, and lower-error prefactor from which the present fitted-coefficient laws can be derived.  In the material examined, Brent does not define the fitted coefficients (alpha_n) or (eta_n) used in this manuscript, and does not state the limits

[
alpha_{n+1}/alpha_n^2	o1/2
]

or

[
-pi2^{n+1}eta_{n+1}/eta_n^2	o1.
]

The beta-channel result is therefore presented as a derived coefficient law built from classical/Brent theta machinery, not as a new theta identity or a new AGM algorithm.

## Additional literature checked

- J. M. Borwein and P. B. Borwein, *Pi and the AGM* (Wiley, 1987): classical AGM, theta-function, and pi-algorithm background.
- E. Salamin, "Computation of pi using arithmetic-geometric mean", *Mathematics of Computation* 30 (1976), 565--570.
- R. P. Brent, "Fast multiple-precision evaluation of elementary functions", *J. ACM* 23 (1976), 242--251.
- A. C. Aitken, "On Bernoulli's numerical solution of algebraic equations", *Proc. Roy. Soc. Edinburgh* 46 (1926), 289--305, for the comparison with dynamic extrapolation.

Targeted web searches were also run for combinations of:
"Gauss-Legendre fitted coefficient", "AGM prefactor coefficient",
"Gauss-Legendre error quotient", "numerator coefficient",
and the explicit leading prefactor (2^{n+2}pi-1).
No matching statement of the manuscript's beta fitted coefficient or scaled beta quotient law was located in those searches.

## Claim boundary

This audit is evidence about the literature searched, not an exhaustive novelty or priority determination.  The publication-safe wording is:

> The coefficient laws are derived from Brent's theta-function formulas.  A focused literature search did not locate these particular fitted-coefficient formulations or scaled limits.

Avoid stronger wording such as "first", "previously unknown", or "novel" unless a broader bibliographic review supports it.

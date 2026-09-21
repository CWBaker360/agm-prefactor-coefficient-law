# Abstract

We study fitted error-operator coefficients associated with the Gauss-Legendre arithmetic-geometric mean algorithm for π. For consecutive lower approximants π_n, define

\[
\alpha_n=-\frac{\pi_{n+1}-\pi}{\pi_{n+1}-\pi_n}.
\]

Using Brent's theta-function expansion, we prove

\[
\frac{\alpha_{n+1}}{\alpha_n^2}\longrightarrow\frac12.
\]

The limit arises from exact cancellation of the doubly exponential error scale, leaving a prefactor quotient governed by \(A_{n+1}/A_n\to2\).

For the companion numerator-channel coefficient

\[
\beta_n
=
-\frac{Q_{n+1}-4\pi t_{n+1}}{Q_{n+1}-Q_n},
\qquad Q_n=(a_n+b_n)^2,
\]

Brent's exact theta parametrization and tail identity give, with
\(x_n=e^{-\pi2^{n+1}}\) and \(C_n=2^{n+2}\pi-1\),

\[
\beta_n
=
-C_nx_n
\left[
1-2x_n+
\left(2-\frac1{C_n}\right)x_n^2
+O(x_n^3)
\right].
\]

Consequently,

\[
-\pi2^{n+1}\frac{\beta_{n+1}}{\beta_n^2}\longrightarrow1.
\]

Thus both fitted channels admit explicit analytic prefactor laws; the numerical scripts serve only as reproducibility checks.

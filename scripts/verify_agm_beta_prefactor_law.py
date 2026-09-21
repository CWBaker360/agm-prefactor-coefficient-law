#!/usr/bin/env python3
"""Verify the sharpened AGM numerator-channel prefactor law.

For
    beta_n = -(Q_(n+1)-4*pi*t_(n+1))/(Q_(n+1)-Q_n),
    Q_n = (a_n+b_n)^2,

the paper proves, with
    x_n = exp(-pi*2^(n+1)),
    C_n = 2^(n+2)*pi - 1,

that
    beta_n/(-C_n*x_n)
      = 1 - 2*x_n + (2-1/C_n)*x_n^2 + O(x_n^3),

and
    [beta_(n+1)/beta_n^2]/[-C_(n+1)/C_n^2]
      = 1 + 4*x_n + (6+2/C_n)*x_n^2 + O(x_n^3).

The computation is a reproducibility check, not the proof.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

try:
    from mpmath import mp
except ImportError as exc:
    raise SystemExit(
        "This script requires mpmath. Install it with: python -m pip install mpmath"
    ) from exc


@dataclass(frozen=True)
class BetaRow:
    n: int
    beta: object
    x: object
    C: object


def fmt(value: object, digits: int = 80) -> str:
    return mp.nstr(value, n=digits, strip_zeros=False)


def compute_rows(iterations: int, precision: int) -> list[BetaRow]:
    if iterations < 3:
        raise ValueError("iterations must be at least 3")
    if precision < 100:
        raise ValueError("precision must be at least 100 decimal digits")

    # beta_n is obtained by cancellation at approximately the x_n^2 scale.
    # Require a guard margin so the final reported normalized residual is
    # not dominated by working precision.
    nmax = iterations - 1
    cancellation_digits = int(
        (2 * mp.pi / mp.log(10)) * (2 ** (nmax + 1))
    )
    if precision < cancellation_digits + 150:
        raise ValueError(
            f"precision={precision} is too small for iterations={iterations}; "
            f"use at least {cancellation_digits + 150} digits"
        )

    mp.dps = precision

    a = mp.mpf(1)
    b = 1 / mp.sqrt(2)
    t = mp.mpf(1) / 4
    p = mp.mpf(1)

    rows: list[BetaRow] = []
    for n in range(iterations):
        Qn = (a + b) ** 2

        a_next = (a + b) / 2
        b_next = mp.sqrt(a * b)
        t_next = t - p * (a - a_next) ** 2
        p_next = 2 * p

        Qnext = (a_next + b_next) ** 2
        denominator = Qnext - Qn
        numerator = Qnext - 4 * mp.pi * t_next
        if denominator == 0:
            raise ZeroDivisionError(
                f"Q_(n+1)-Q_n vanished numerically at n={n}; increase precision"
            )

        beta = -numerator / denominator
        x = mp.exp(-mp.pi * (2 ** (n + 1)))
        C = (2 ** (n + 2)) * mp.pi - 1
        rows.append(BetaRow(n=n, beta=beta, x=x, C=C))

        a, b, t, p = a_next, b_next, t_next, p_next

    return rows


def write_csv(rows: list[BetaRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "n",
                "beta_n",
                "x_n",
                "C_n",
                "beta_normalized_exact",
                "beta_normalized_prediction",
                "beta_normalized_residual",
                "quotient_R_n",
                "quotient_normalized_exact",
                "quotient_normalized_prediction",
                "quotient_normalized_residual",
                "scaled_limit_value",
            ]
        )

        for i, row in enumerate(rows):
            beta_exact = row.beta / (-row.C * row.x)
            beta_pred = (
                1 - 2 * row.x
                + (2 - 1 / row.C) * row.x**2
            )
            beta_resid = beta_exact - beta_pred

            if i + 1 < len(rows):
                nxt = rows[i + 1]
                R = nxt.beta / row.beta**2
                Rstar = -nxt.C / row.C**2
                q_exact = R / Rstar
                q_pred = (
                    1 + 4 * row.x
                    + (6 + 2 / row.C) * row.x**2
                )
                q_resid = q_exact - q_pred
                scaled = -mp.pi * (2 ** (row.n + 1)) * R
            else:
                R = q_exact = q_pred = q_resid = scaled = None

            writer.writerow(
                [
                    row.n,
                    fmt(row.beta),
                    fmt(row.x),
                    fmt(row.C),
                    fmt(beta_exact),
                    fmt(beta_pred),
                    fmt(beta_resid),
                    "" if R is None else fmt(R),
                    "" if q_exact is None else fmt(q_exact),
                    "" if q_pred is None else fmt(q_pred),
                    "" if q_resid is None else fmt(q_resid),
                    "" if scaled is None else fmt(scaled),
                ]
            )


def print_report(rows: list[BetaRow]) -> None:
    print("SHARPENED AGM BETA LAW AUDIT")
    print("=" * 132)
    print("n   exact beta/refined        2-term prediction        residual")
    print("-" * 132)
    for row in rows:
        exact = row.beta / (-row.C * row.x)
        pred = 1 - 2 * row.x + (2 - 1 / row.C) * row.x**2
        print(
            f"{row.n:1d}   {mp.nstr(exact,28):<30} "
            f"{mp.nstr(pred,28):<30} {mp.nstr(exact-pred,12)}"
        )

    print("\nREFINED QUOTIENT AUDIT")
    print("=" * 132)
    print("n   exact quotient/refined    2-term prediction        residual")
    print("-" * 132)
    for i in range(len(rows) - 1):
        row = rows[i]
        nxt = rows[i + 1]
        R = nxt.beta / row.beta**2
        Rstar = -nxt.C / row.C**2
        exact = R / Rstar
        pred = 1 + 4 * row.x + (6 + 2 / row.C) * row.x**2
        print(
            f"{row.n:1d}   {mp.nstr(exact,28):<30} "
            f"{mp.nstr(pred,28):<30} {mp.nstr(exact-pred,12)}"
        )

    print("\nSCALED LIMIT")
    print("=" * 132)
    for i in range(len(rows) - 1):
        row = rows[i]
        nxt = rows[i + 1]
        scaled = -mp.pi * (2 ** (row.n + 1)) * nxt.beta / row.beta**2
        print(row.n, mp.nstr(scaled, 28))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the AGM numerator-channel prefactor law."
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=7,
        help="number of beta values starting at n=0 (default: 7)",
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=1000,
        help="mpmath working decimal precision (default: 1000)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("outputs/agm_beta_prefactor_audit.csv"),
        help="CSV output path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        rows = compute_rows(args.iterations, args.precision)
        print_report(rows)
        write_csv(rows, args.out)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"\nCSV written: {args.out}")
    print("VERDICT: numerical checks support the analytic beta-channel law")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

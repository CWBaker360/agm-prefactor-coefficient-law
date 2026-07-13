#!/usr/bin/env python3
"""Reproduce the numerical tables in the AGM prefactor coefficient paper.

The script reconstructs the lower Gauss-Legendre approximants, computes the
signed errors, fitted coefficients alpha_n, prefactors A_n, and the diagnostic
ratios used in the paper.  It uses mpmath's mp.pi only as the reference value
for the error calculation; the theorem itself is analytic and does not depend
on this numerical verification.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

try:
    from mpmath import mp
except ImportError as exc:  # pragma: no cover - environment-dependent
    raise SystemExit(
        "This script requires mpmath. Install it with: python -m pip install mpmath"
    ) from exc


@dataclass(frozen=True)
class Row:
    n: int
    pi_n: object
    epsilon_n: object
    alpha_n: object | None
    prefactor_a_n: object


def gauss_legendre_rows(iterations: int, precision: int) -> list[Row]:
    """Return rows n=0,...,iterations-1 for the lower AGM approximants."""
    if iterations < 3:
        raise ValueError("iterations must be at least 3")
    if precision < 50:
        raise ValueError("precision must be at least 50 decimal digits")

    mp.dps = precision
    a = mp.mpf(1)
    b = 1 / mp.sqrt(2)
    t = mp.mpf(1) / 4
    p = mp.mpf(1)

    approximants: list[object] = []
    for _ in range(iterations):
        approximants.append((a + b) ** 2 / (4 * t))
        a_next = (a + b) / 2
        b_next = mp.sqrt(a * b)
        t_next = t - p * (a - a_next) ** 2
        p_next = 2 * p
        a, b, t, p = a_next, b_next, t_next, p_next

    errors = [value - mp.pi for value in approximants]
    alphas: list[object | None] = []
    for n in range(iterations):
        if n + 1 >= iterations:
            alphas.append(None)
        else:
            denominator = approximants[n + 1] - approximants[n]
            alphas.append(-errors[n + 1] / denominator)

    rows: list[Row] = []
    for n in range(iterations):
        prefactor = errors[n] * mp.exp(mp.pi * (2 ** (n + 1)))
        rows.append(
            Row(
                n=n,
                pi_n=approximants[n],
                epsilon_n=errors[n],
                alpha_n=alphas[n],
                prefactor_a_n=prefactor,
            )
        )
    return rows


def format_number(value: object, digits: int = 30) -> str:
    return mp.nstr(value, n=digits, strip_zeros=False)


def write_outputs(rows: Sequence[Row], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    alpha_path = outdir / "agm_fitted_coefficients.csv"
    with alpha_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["n", "pi_n", "epsilon_n", "alpha_n", "A_n"])
        for row in rows[:-1]:
            writer.writerow(
                [
                    row.n,
                    format_number(row.pi_n, 80),
                    format_number(row.epsilon_n, 80),
                    format_number(row.alpha_n, 80),
                    format_number(row.prefactor_a_n, 80),
                ]
            )

    ratio_path = outdir / "agm_coefficient_ratios.csv"
    with ratio_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "n",
                "alpha_n_plus_1_over_alpha_n_squared",
                "direct_error_quotient",
                "A_n_plus_1_over_A_n",
            ]
        )
        for n in range(len(rows) - 2):
            alpha_n = rows[n].alpha_n
            alpha_next = rows[n + 1].alpha_n
            assert alpha_n is not None and alpha_next is not None
            alpha_ratio = alpha_next / (alpha_n**2)
            direct = (
                rows[n + 2].epsilon_n
                * rows[n].epsilon_n**2
                / rows[n + 1].epsilon_n**3
            )
            a_ratio = rows[n + 1].prefactor_a_n / rows[n].prefactor_a_n
            writer.writerow(
                [
                    n,
                    format_number(alpha_ratio, 80),
                    format_number(direct, 80),
                    format_number(a_ratio, 80),
                ]
            )

    summary_path = outdir / "verification_summary.txt"
    last_ratio_n = min(5, len(rows) - 3)
    alpha_n = rows[last_ratio_n].alpha_n
    alpha_next = rows[last_ratio_n + 1].alpha_n
    assert alpha_n is not None and alpha_next is not None
    final_ratio = alpha_next / alpha_n**2
    final_a_ratio = (
        rows[last_ratio_n + 1].prefactor_a_n / rows[last_ratio_n].prefactor_a_n
    )
    summary_path.write_text(
        "AGM prefactor coefficient verification\n"
        f"precision_dps: {mp.dps}\n"
        f"iterations: {len(rows)}\n"
        f"last_reported_n: {last_ratio_n}\n"
        f"alpha_ratio: {format_number(final_ratio, 40)}\n"
        f"prefactor_ratio: {format_number(final_a_ratio, 40)}\n"
        "theoretical_limits: alpha_ratio -> 0.5; prefactor_ratio -> 2\n",
        encoding="utf-8",
    )


def verify_paper_values(rows: Sequence[Row]) -> None:
    """Check the printed values from Tables 1 and 2 to their shown precision."""
    expected_alpha = [
        "4.476840443051657e-3",
        "7.278747106485182e-6",
        "2.482705775153228e-11",
        "2.988090953871379e-22",
        "4.397065311352923e-44",
        "9.594611535813435e-88",
        "4.585616315217315e-175",
    ]
    expected_ratio = [
        "0.3631728700311416",
        "0.4686104763344650",
        "0.4847784478028806",
        "0.4924649101466708",
        "0.4962511920458477",
        "0.4981302572056423",
    ]
    expected_prefactor = [
        "2.3866261558728965",
        "2.0871750987545307",
        "2.0414374856886031",
        "2.0202981874959604",
        "2.0100471245391349",
        "2.0049984522335209",
    ]

    def close_to_printed(actual: object, printed: str) -> bool:
        target = mp.mpf(printed)
        # The values in the paper are rounded to roughly 16 significant digits.
        scale = max(abs(target), mp.mpf(1))
        return abs(actual - target) <= mp.mpf("6e-16") * scale

    for n, printed in enumerate(expected_alpha):
        actual = rows[n].alpha_n
        assert actual is not None
        if not close_to_printed(actual, printed):
            raise AssertionError(f"alpha_{n} does not match the published table")

    for n, (printed_ratio, printed_a) in enumerate(
        zip(expected_ratio, expected_prefactor, strict=True)
    ):
        alpha_n = rows[n].alpha_n
        alpha_next = rows[n + 1].alpha_n
        assert alpha_n is not None and alpha_next is not None
        actual_ratio = alpha_next / alpha_n**2
        actual_a = rows[n + 1].prefactor_a_n / rows[n].prefactor_a_n
        if not close_to_printed(actual_ratio, printed_ratio):
            raise AssertionError(f"coefficient ratio at n={n} does not match")
        if not close_to_printed(actual_a, printed_a):
            raise AssertionError(f"prefactor ratio at n={n} does not match")


def print_tables(rows: Sequence[Row]) -> None:
    print("Table 1: fitted coefficients alpha_n")
    print("n  alpha_n")
    for n in range(min(7, len(rows) - 1)):
        print(f"{n}  {mp.nstr(rows[n].alpha_n, 18)}")

    print("\nTable 2: coefficient and prefactor ratios")
    print("n  alpha_(n+1)/alpha_n^2  A_(n+1)/A_n  direct quotient")
    for n in range(min(6, len(rows) - 2)):
        alpha_n = rows[n].alpha_n
        alpha_next = rows[n + 1].alpha_n
        assert alpha_n is not None and alpha_next is not None
        ratio = alpha_next / alpha_n**2
        a_ratio = rows[n + 1].prefactor_a_n / rows[n].prefactor_a_n
        direct = (
            rows[n + 2].epsilon_n
            * rows[n].epsilon_n**2
            / rows[n + 1].epsilon_n**3
        )
        print(
            f"{n}  {mp.nstr(ratio, 18)}  {mp.nstr(a_ratio, 18)}  "
            f"{mp.nstr(direct, 18)}"
        )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reproduce the AGM prefactor coefficient tables."
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=500,
        help="working decimal precision (default: 500)",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=9,
        help="number of AGM approximants to construct (default: 9)",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("outputs"),
        help="directory for CSV and summary files (default: outputs)",
    )
    parser.add_argument(
        "--skip-table-check",
        action="store_true",
        help="do not compare the computed values with the paper's printed tables",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        rows = gauss_legendre_rows(args.iterations, args.precision)
        if not args.skip_table_check:
            verify_paper_values(rows)
        print_tables(rows)
        write_outputs(rows, args.outdir)
    except (AssertionError, ValueError, ZeroDivisionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"\nVerification PASS. Outputs written to: {args.outdir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

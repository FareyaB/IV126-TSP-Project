"""Auxiliary TSP solver test harness (not an LNS implementation).
Usage: python3 test_tsp.py main.py tsp_22.json [tsp_52.json ...]
"""
import json
import math
import os
import subprocess
import sys
import tempfile
import time


def check_instance(solver, path):
    with open(path, encoding='utf-8') as handle:
        instance = json.load(handle)
    matrix = instance['Matrix']
    n = len(matrix)
    timeout = float(instance['Timeout'])
    with tempfile.TemporaryDirectory() as tmp:
        output = os.path.join(tmp, 'solution.json')
        start = time.monotonic()
        try:
            proc = subprocess.run(
                [sys.executable, solver, os.path.abspath(path), output],
                capture_output=True, text=True, timeout=timeout + 2,
            )
        except subprocess.TimeoutExpired:
            return [os.path.basename(path), n, 'TIMEOUT', '-', '-', '-', f'>{timeout:.1f}s']
        elapsed = time.monotonic() - start
        if proc.returncode != 0:
            return [os.path.basename(path), n, 'ERROR', '-', '-', '-', f'{elapsed:.3f}s']
        try:
            with open(output, encoding='utf-8') as handle:
                route = json.load(handle)
        except (OSError, ValueError):
            return [os.path.basename(path), n, 'BAD JSON', '-', '-', '-', f'{elapsed:.3f}s']
    valid = (isinstance(route, list) and len(route) == n
             and all(type(v) is int for v in route)
             and set(route) == set(range(n)))
    if not valid:
        return [os.path.basename(path), n, 'INVALID', '-', '-', '-', f'{elapsed:.3f}s']
    distance = sum(matrix[route[i]][route[(i + 1) % n]] for i in range(n))
    optimum = instance.get('GlobalBestVal')
    gap = f'{(distance / optimum - 1) * 100:.1f}%' if isinstance(optimum, (int, float)) and optimum > 0 else '-'
    return [os.path.basename(path), n, 'VALID', f'{distance:.2f}', f'{optimum:.2f}' if optimum is not None else '-', gap, f'{elapsed:.3f}s']


def main():
    if len(sys.argv) < 3:
        raise SystemExit('Usage: python3 test_tsp.py main.py tsp_22.json [other_instances.json ...]')
    solver = os.path.abspath(sys.argv[1])
    headings = ['Instance', 'Cities', 'Status', 'Distance', 'Optimum', 'Gap', 'Runtime']
    rows = [check_instance(solver, p) for p in sys.argv[2:]]
    widths = [max(len(str(v)) for v in [headings[i]] + [r[i] for r in rows]) for i in range(len(headings))]
    print('  '.join(str(v).ljust(widths[i]) for i, v in enumerate(headings)))
    print('  '.join('-' * w for w in widths))
    for row in rows:
        print('  '.join(str(v).ljust(widths[i]) for i, v in enumerate(row)))


if __name__ == '__main__':
    main()

# Traveling Salesman Problem (TSP)

A Python heuristic solver for the Traveling Salesman Problem, developed for **IV126 — Fundamentals of Artificial Intelligence** at Masaryk University.

## Overview

The project uses **Large Neighborhood Search (LNS)** to find short routes through a set of cities. The solver starts with an initial tour and repeatedly improves it while respecting the time limit for each instance.

## Algorithms

- **Nearest neighbor:** Builds the initial route.
- **Destroy and repair:** Removes selected cities and reinserts them using cheapest insertion.
- **2-opt:** Improves a route by reversing segments.
- **City exchange:** Improves a route by swapping cities.

## Project Files

| File | Description |
| --- | --- |
| `main.py` | Main TSP solver |
| `test_tsp.py` | Testing script |
| `IV126_TSP_Project.ipynb` | Google Colab notebook for development and experiments |
| `tuning_results.csv` | Initial parameter-tuning results |
| `repeat_tuning_results.csv` | Repeated parameter-tuning results |

## How to Run

Requires **Python 3**. The solver uses only Python's standard library.

```bash
python3 main.py input_instance.json output_solution.json
```

The input JSON contains the distance matrix and a time limit. The output is a JSON list of city indices, with each city appearing exactly once.

## Testing

The solver was tested on all 12 provided TSP instances and successfully executed on the university's Aisa server.

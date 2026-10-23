import random
import sys
import json
import time

start_time = time.time()
SAFETY_MARGIN = 2.0

def read_instance_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def write_instance_json(solution, file_path):
    with open(file_path, 'w') as f:
        json.dump(solution, f)


def calculate_distance(route, matrix):
    """Calculate the total distance of a closed TSP route."""
    if len(route) < 2:
        return 0

    total = 0
    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)]
        total += matrix[current_city][next_city]

    return total

# ------------------------------------
# LNS REPAIR OPERATOR
# ------------------------------------


def repair_route(partial_route, removed_cities, matrix):
    """Restore removed cities using cheapest insertion."""
    route = partial_route.copy()

    for city in removed_cities:
        if city in route:
            continue

        if not route:
            route.append(city)
            continue

        best_position = 0
        best_cost = float("inf")

        for i in range(len(route)):
            a = route[i]
            b = route[(i + 1) % len(route)]

            extra_cost = (
                matrix[a][city]
                + matrix[city][b]
                - matrix[a][b]
            )

            if extra_cost < best_cost:
                best_cost = extra_cost
                best_position = i + 1

        route.insert(best_position, city)

    return route


# The repair function will receive:
# - a partial route
# - the cities removed during destroy
# - the distance matrix
#
# It will return a complete, valid route.

def destroy_route(route, removal_count):
    removal_count = min(max(0, removal_count), len(route) - 1)
    removed = random.sample(route, removal_count)
    removed_set = set(removed)
    partial_route = [city for city in route if city not in removed_set]
    return partial_route, removed


def two_opt(route, matrix, deadline=None):
    """Improve a TSP tour by reversing segments."""
    best_route = route.copy()
    n = len(best_route)

    if n < 4:
        return best_route

    best_distance = calculate_distance(best_route, matrix)
    improved = True

    while improved:
        improved = False

        for i in range(n - 1):
            for j in range(i + 2, n):
                if deadline is not None and time.time() >= deadline:
                    return best_route
                # Avoid reversing the entire cycle
                # because it does not change an undirected tour.
                if i == 0 and j == n - 1:
                    continue

                candidate = (
                    best_route[:i + 1]
                    + best_route[i + 1:j + 1][::-1]
                    + best_route[j + 1:]
                )

                candidate_distance = calculate_distance(
                    candidate, matrix
                )

                if candidate_distance < best_distance:
                    best_route = candidate
                    best_distance = candidate_distance
                    improved = True
                    break

            if improved:
                break

    return best_route


# ------------------------------------
# CLASSICAL SEARCH: CITY EXCHANGE
# ------------------------------------

def city_exchange(route, matrix, deadline=None):
    """Improve a TSP tour by swapping pairs of cities."""
    best_route = route.copy()
    n = len(best_route)

    if n < 2:
        return best_route

    best_distance = calculate_distance(best_route, matrix)

    while deadline is None or time.time() < deadline:
        improved = False

        for i in range(n - 1):
            if deadline is not None and time.time() >= deadline:
                return best_route

            for j in range(i + 1, n):
                candidate = best_route.copy()
                candidate[i], candidate[j] = candidate[j], candidate[i]

                candidate_distance = calculate_distance(candidate, matrix)

                if candidate_distance < best_distance:
                    best_route = candidate
                    best_distance = candidate_distance
                    improved = True
                    break

            if improved:
                break

        if not improved:
            break

    return best_route


instance_path = sys.argv[1]
output_path = sys.argv[2]

instance = read_instance_json(instance_path)
matrix = instance['Matrix']
n = len(matrix)

solution = []

if n > 0:
    current_city = 0
    unvisited = set(range(n))
    unvisited.remove(current_city)
    solution.append(current_city)

    while unvisited:
        next_city = min(
            unvisited,
            key=lambda city: (matrix[current_city][city], city)
        )
        solution.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city

# ------------------------------------
# LNS SEARCH
# ------------------------------------


# ------------------------------------
# LNS SEARCH
# ------------------------------------

if n > 1:
    time_limit = float(instance.get("Timeout", 120))
    deadline = start_time + max(0.0, time_limit - SAFETY_MARGIN)

    best_route = solution.copy()
    best_distance = calculate_distance(best_route, matrix)
    current_route = best_route.copy()

    removal_count = max(1, n // 5)

    while time.time() < deadline:
        partial_route, removed = destroy_route(
            current_route, removal_count
        )

        candidate = repair_route(partial_route, removed, matrix)

        if time.time() < deadline:
            candidate = two_opt(candidate, matrix, deadline)

        if time.time() < deadline:
            candidate = city_exchange(candidate, matrix, deadline)

        candidate_distance = calculate_distance(candidate, matrix)

        if candidate_distance < best_distance:
            best_route = candidate.copy()
            best_distance = candidate_distance
            current_route = candidate.copy()
        elif random.random() < 0.1:
            current_route = candidate.copy()

    solution = best_route

write_instance_json(solution, output_path)

#######################################################################
# Example of the required timeout mechanism within the LNS structure: #
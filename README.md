Traveling Salesman Problem — IV126
A Python heuristic solver for the Traveling Salesman Problem (TSP), developed for the IV126 Fundamentals of Artificial Intelligence course at Masaryk University.
Approach
The solver uses Large Neighborhood Search (LNS) with:
- Nearest neighbor for the initial route
- Destroy and repair using random removal and cheapest insertion
- 2-opt to improve routes by reversing segments
- City exchange to improve routes by swapping cities
The algorithm keeps track of the best route found and respects the time limit specified in each input instance.
Project files
File	Description
main.py	TSP solver
test_tsp.py	Test script
IV126_TSP_Project.ipynb	Colab notebook with development and experiments
tuning_results.csv	Parameter-tuning results
repeat_tuning_results.csv	Repeated tuning results


Run
Requires Python 3. Uses only the Python standard library.
python3 main.py input_instance.json output_solution.json
The input is a JSON TSP instance containing a distance matrix and time limit. The output is a JSON list of city indices representing the tour, with each city appearing once.
Testing
Tested on the 12 provided TSP instances and on the university's Aisa server.

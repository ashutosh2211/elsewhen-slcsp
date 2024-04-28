# SLCSP Finder

This Python script finds the second lowest cost silver plan (SLCSP) for a given set of ZIP codes. It reads the necessary data from CSV files and outputs the SLCSP rates for each ZIP code in CSV format.

## Files

- `slcsp.py`: The main Python script that implements the SLCSP finder.
- `plans.csv`: CSV file containing information about health plans.
- `zips.csv`: CSV file containing information about ZIP codes, counties, and rate areas.
- `slcsp.csv`: CSV file containing the ZIP codes for which the SLCSP needs to be found.

## Usage

1. Ensure that you have Python 3.x installed on your system.

2. Place the `slcsp.py` script and the CSV files (`plans.csv`, `zips.csv`, `slcsp.csv`) in the same directory.

3. Open a terminal or command prompt and navigate to the directory containing the files.

4. Run the following command to execute the script:

   ```bash
   python slcsp.py
   ```
   
5. The script will process the data and output the results in CSV format to the console. The output will have the following structure:
   ```
   ZIP Code,SLCSP Rate
   64148,261.24
   67118,238.6
   40813,213.36
   ...
   ```
   
If the SLCSP cannot be determined for a ZIP code, the corresponding rate field will be left blank.

## Dependencies

The script does not require any external dependencies. It only uses the Python standard library.

## Implementation Details


- `Plan` class: Represents a health plan with its attributes such as plan ID, state, metal level, rate, and rate area.
- `ZipCode` class: Represents a ZIP code with its state, counties, and rate areas.
- `SlcspFinder` class: Implements the logic to find the SLCSP for each ZIP code. It takes the plans and ZIP codes as input and provides methods to find the SLCSP for a single ZIP code or for all ZIP codes.
- Helper functions:
- `read_plans`: Reads the plan data from the CSV file and creates `Plan` objects.
- `read_zipcodes`: Reads the ZIP code data from the CSV file and creates `ZipCode` objects.
- `read_slcsp`: Reads the ZIP codes for which the SLCSP needs to be found from the CSV file.

The script reads the data from the CSV files, creates the necessary objects, and then uses the `SlcspFinder` class to find the SLCSP rates. Finally, it outputs the results in the required CSV format.

## Comments

- The `SlcspFinder` class uses a dictionary to group plans by their rate area, which allows for efficient lookup of plans for a given rate area.
- The `find_slcsp_for_zipcode` method implements the logic to find the SLCSP for a single ZIP code. It handles cases where the ZIP code is invalid, has multiple rate areas, or does not have enough silver plans.
- The `find_slcsp_for_all` method finds the SLCSP for all ZIP codes by calling `find_slcsp_for_zipcode` for each ZIP code.
- The helper functions (`read_plans`, `read_zipcodes`, `read_slcsp`) are responsible for reading data from the CSV files and creating the corresponding objects.
- The script follows the SOLID principles by separating concerns into different classes and functions, making the code more modular and maintainable.
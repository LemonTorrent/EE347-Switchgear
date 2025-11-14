# Use 175 watt for motor

# Power factor might be a problem, since we don't know power factor on motor itself
# Look for average power factor

import numpy as np
import pandas as pd
import math

def process_motor_data(data):
    """
    Processes a 2D array of motor data.
    For demonstration, this function will calculate the loading on the transformer.

    Args:
        data (list or np.array): A 2D array-like structure where each row is [c, r].
                                 c: capacitance (Farads)
                                 r: resistance (Ohms)
                                 p: real power of motor (Watts)
                                 q: reactive power of motor (VA)

    Returns:
        list: A list of results appended to each [c, r, p, q] entry.
    """
    f = 60  # Assuming a frequency of 60 Hz
    w = 2 * np.pi * f
    v_ph = 120
    v_LL = 208
    
    results = []
    for row in data:
        xc, r, p, q = row
        temp = [xc, r, p, q]

        # Calculate real power of resistors (purely real)
        P_R = math.sqrt(3) * (v_ph ^ 2) / r
        temp.append((P_R + p) / 3)

        # Calculate reactive power of capacitors (purely reactive)
        Q_C = (-1 * math.sqrt(3) * (v_LL ^ 2)) / xc
        temp.append((Q_C + q) / 3)

        results.append(temp)
        
    return results

def read_specific_rows(file_path, rows):
    """
    Reads specific rows from an Excel file.

    Args:
        file_path (str): The path to the Excel file.
        rows (list): A list of 1-based row numbers to read.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the specified rows.
    """
    try:
        # Read the entire sheet
        df = pd.read_excel(file_path, header=None)
        
        # Convert 1-based row numbers to 0-based indices
        indices = [row - 1 for row in rows]
        
        # Select the specified rows
        selected_rows = df.iloc[indices]
        
        return selected_rows
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def demonstrate_calculations():
    """
    Demonstrate for switchgear part 3.
    """

    r_vals = [300, 600, 1200]
    c_vals = [300, 600, 1200]
    excel_file = 'EE347_Lab3c_Motordata.xlsx'
    rows_to_read = [5, 15, 24]
    # cols = [5, 6]
    
    data = read_specific_rows(excel_file, rows_to_read)
    
    test_data = []

    for i in range(len(r_vals)):
        for j in range(len(c_vals)):
            for k in range(len(rows_to_read)):
                test_data.append([r_vals[i], c_vals[j], data.iloc[k][5], data.iloc[k][6]])

    # print(test_data)
    
    print(f"Input Data:\n{test_data}")
    
    results = process_motor_data(test_data)
    print("\nCalculated Results:")
    print(results)
    # print("-" * 40)

if __name__ == "__main__":
    demonstrate_calculations()


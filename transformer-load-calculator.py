# Use 175 watt for motor

# Power factor might be a problem, since we don't know power factor on motor itself
# Look for average power factor

import numpy as np

def process_motor_data(data):
    """
    Processes a 2D array of motor data.
    For demonstration, this function will calculate the impedance for each component.
    Assumes the motor value is an inductance (in Henrys) and frequency is 60Hz.

    Args:
        data (list or np.array): A 2D array-like structure where each row is [c, r].
                                 c: capacitance (Farads)
                                 r: resistance (Ohms)

    Returns:
        list: A list of results for each [c, r] entry.
    """
    f = 60  # Assuming a frequency of 60 Hz
    w = 2 * np.pi * f
    v_ph = 120
    v_LL = 208
    
    results = []
    for row in data:
        c, r = row
        
        # Calculate capacitive reactance
        # Handle capacitance being zero to avoid division by zero
        if c > 0:
            xc = -1 / (w * c)
        else:
            xc = 0
            
        # Total impedance Z = R - jXc
        # z = r + 1j * (xc)

        # Calculate real power of resistors (purely real)
        P_R = 3 * (v_ph ^ 2) / r
        results.append(P_R)

        # Calculate reactive power of capacitors (purely reactive)
        Q_C = -3 * (v_LL ^ 2) * w * c
        results.append(Q_C)
        
    return results

def test_process_motor_data():
    """
    Tests the process_motor_data function with sample data.
    """
    # --- Test Case 1: Standard values ---
    print("--- Test Case 1: Standard RLC components ---")
    test_data_1 = [
        [100e-6, 10],  # [C, R]
        [150e-6, 5],
        [200e-6, 15]
    ]
    print(f"Input Data:\n{np.array(test_data_1)}")
    
    results_1 = process_motor_data(test_data_1)
    print("\nCalculated Results:")
    print(results_1)
    print("-" * 40)

    # --- Test Case 2: Edge case with zero capacitance ---
    print("\n--- Test Case 2: R circuit (zero capacitance) ---")
    test_data_2 = [
        [0, 50]  # [C=0, R]
    ]
    print(f"Input Data:\n{np.array(test_data_2)}")
    
    results_2 = process_motor_data(test_data_2)
    print("\nCalculated Results:")
    print(results_2)
    print("-" * 40)

if __name__ == "__main__":
    test_process_motor_data()

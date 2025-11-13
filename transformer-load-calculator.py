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
        data (list or np.array): A 2D array-like structure where each row is [c, r, m].
                                 c: capacitance (Farads)
                                 r: resistance (Ohms)
                                 m: motor inductance (Henrys)

    Returns:
        list: A list of complex impedances for each [c, r, m] entry.
    """
    f = 60  # Assuming a frequency of 60 Hz
    w = 2 * np.pi * f
    v_ph = 120
    v_LL = 208
    
    impedances = []
    for row in data:
        c, r, m = row
        
        # Calculate capacitive and inductive reactance
        # Handle capacitance being zero to avoid division by zero
        if c > 0:
            xc = -1 / (w * c)
        else:
            xc = 0
            
        xl = w * m
        
        # Total impedance Z = R + j(Xl - Xc)
        # z = r + 1j * (xl + xc)

        # Calculate real power of resistors (purely real)
        P_R = 3 * (v_ph ^ 2) / r
        impedances.append(P_R)

        # Calculate reactive power of capacitors (purely reactive)
        Q_C = -3 * (v_LL ^ 2) * w * c
        impedances.append(Q_C)
        
    return impedances

def test_process_motor_data():
    """
    Tests the process_motor_data function with sample data.
    """
    # --- Test Case 1: Standard values ---
    print("--- Test Case 1: Standard RLC components ---")
    test_data_1 = [
        [100e-6, 10, 20e-3],  # [C, R, L]
        [150e-6, 5, 30e-3],
        [200e-6, 15, 10e-3]
    ]
    print(f"Input Data:\n{np.array(test_data_1)}")
    
    results_1 = process_motor_data(test_data_1)
    print("\nCalculated Impedances (Z = R + jX):")
    for i, z in enumerate(results_1):
        print(f"  Entry {i+1}: {z.real:.2f} + {z.imag:.2f}j Ohms")
    print("-" * 40)

    # --- Test Case 2: Edge case with zero capacitance ---
    print("\n--- Test Case 2: RL circuit (zero capacitance) ---")
    test_data_2 = [
        [0, 50, 100e-3]  # [C=0, R, L]
    ]
    print(f"Input Data:\n{np.array(test_data_2)}")
    
    results_2 = process_motor_data(test_data_2)
    print("\nCalculated Impedances (Z = R + jX):")
    for i, z in enumerate(results_2):
        print(f"  Entry {i+1}: {z.real:.2f} + {z.imag:.2f}j Ohms")
    print("-" * 40)

if __name__ == "__main__":
    test_process_motor_data()

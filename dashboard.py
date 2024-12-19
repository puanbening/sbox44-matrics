import numpy as np
import pandas as pd
import streamlit as st
import os

# Fungsi untuk memuat S-box dari file Excel
def load_sbox_from_excel(file_path):
    try:
        df = pd.read_excel(file_path, header=None)
        sbox = df.values.flatten().tolist()

        if len(sbox) == 256:
            return sbox
        else:
            raise ValueError("File Excel harus mengandung 256 values")
    except Exception as e:
        st.error(f"File error: {e}")
        return None

# Fungsi Hamming Weight
def hamming_weight(x):
    return bin(x).count('1')

# Fungsi SAC
def calculate_sac(sbox, n):
    total_weight = 0
    total_cases = 0

    for i in range(2**n):
        original_output = sbox[i]
        for bit in range(n):
            flipped_input = i ^ (1 << bit)
            flipped_output = sbox[flipped_input]
            diff = original_output ^ flipped_output
            weight = hamming_weight(diff)
            total_weight += weight
            total_cases += n

    return total_weight / total_cases

# Fungsi Nonlinearity
def calculate_nonlinearity(sbox):
    n = int(np.log2(len(sbox)))
    m = n

    sbox = np.array([list(map(int, f"{val:0{m}b}")) for val in sbox])

    nonlinearity = float('inf')
    for i in range(m):
        boolean_function = sbox[:, i]
        walsh_transform = walsh_hadamard_transform(boolean_function)
        max_correlation = np.max(np.abs(walsh_transform))
        current_nonlinearity = 2**(n-1) - (max_correlation // 2)
        nonlinearity = min(nonlinearity, current_nonlinearity)

    return float(nonlinearity)

# Fungsi Walsh-Hadamard Transform
def walsh_hadamard_transform(boolean_function):
    n = boolean_function.size
    transformed = 1 - 2 * boolean_function

    for i in range(int(np.log2(n))):
        step = 2**i
        for j in range(0, n, 2*step):
            for k in range(step):
                a = transformed[j + k]
                b = transformed[j + k + step]
                transformed[j + k] = a + b
                transformed[j + k + step] = a - b

    return transformed

# Fungsi BIC-NL
def calculate_bic_nl(sbox):
    sbox_size = len(sbox)
    bit_size = 8
    total_bit_pairs = bit_size * (bit_size - 1) / 2
    total_nonlinearity_score = 0

    for bit1 in range(bit_size):
        for bit2 in range(bit1 + 1, bit_size):
            combined_bits = [((sbox[input_value] >> bit1) & 1) ^ ((sbox[input_value] >> bit2) & 1)
                             for input_value in range(sbox_size)]

            transformed_values = walsh_hadamard_transform(np.array(combined_bits))
            max_walsh_value = np.max(np.abs(transformed_values))
            nl = 2**(bit_size - 1) - (max_walsh_value // 2)
            total_nonlinearity_score += nl

    bic_nl_score = total_nonlinearity_score / total_bit_pairs
    return round(bic_nl_score, 5)

# Fungsi BIC-SAC
def calculate_bic_sac(sbox):
    box_size = len(sbox)
    bit_size = 8
    total_combinations = bit_size * (bit_size - 1) / 2
    cumulative_score = 0

    for bit1 in range(bit_size):
        for bit2 in range(bit1 + 1, bit_size):
            bit_independence = 0
            for input_val in range(box_size):
                for flipped_bit in range(bit_size):
                    new_value = sbox[input_val] ^ sbox[input_val ^ (1 << flipped_bit)]
                    bit1_value = (new_value >> bit1) & 1
                    bit2_value = (new_value >> bit2) & 1
                    bit_independence += bit1_value ^ bit2_value

            normalized_independence = bit_independence / (box_size * bit_size)
            cumulative_score += normalized_independence

    bic_sac_score = cumulative_score / total_combinations
    return round(bic_sac_score, 5)

# Fungsi DAP
def calculate_dap(sbox):
    box_size = len(sbox)
    differential_table = [[0] * box_size for _ in range(box_size)]

    for input_diff in range(box_size):
        for input_x in range(box_size):
            output_diff = sbox[input_x] ^ sbox[input_x ^ input_diff]
            differential_table[input_diff][output_diff] += 1

    max_dap = max(
        differential_table[input_diff][output_diff] / box_size
        for input_diff in range(1, box_size)
        for output_diff in range(box_size)
    )

    return round(max_dap, 6)

# Fungsi LAP
def calculate_lap(sbox):
    box_size = len(sbox)
    bit_size = int(np.log2(box_size))

    input_masks = np.arange(box_size)
    output_masks = np.arange(box_size)
    sbox_array = np.array(sbox)

    input_parity = np.array([[bin(x & mask).count('1') % 2 for mask in input_masks] for x in range(box_size)])
    output_parity = np.array([[bin(sbox_array[x] & mask).count('1') % 2 for mask in output_masks] for x in range(box_size)])

    correlation_table = np.abs(np.sum(input_parity[:, :, None] == output_parity[:, None, :], axis=0) - (box_size // 2))

    max_lap = np.max(correlation_table[1:, 1:]) / box_size
    return round(max_lap, 6)

# Streamlit App
def main():
    st.title("Aplikasi Kriptografi S-box")

    uploaded_file = st.file_uploader("Unggah File Excel S-box", type=["xlsx"])

    if uploaded_file is not None:
        # Load S-box from the uploaded file
        sbox = load_sbox_from_excel(uploaded_file)

        if sbox:
            operation = st.selectbox(
                "Pilih Operasi",
                ["Nonlinearity (NL)", "SAC", "BIC-NL", "BIC-SAC", "LAP", "DAP"]
            )

            if st.button("Hitung"):
                if operation == "Nonlinearity (NL)":
                    result = calculate_nonlinearity(sbox)
                    st.write(f"Hasil Nonlinearity: {result}")
                elif operation == "SAC":
                    result = calculate_sac(sbox, 8)
                    st.write(f"Hasil SAC: {result:.5f}")
                elif operation == "BIC-NL":
                    result = calculate_bic_nl(sbox)
                    st.write(f"Hasil BIC-NL: {result}")
                elif operation == "BIC-SAC":
                    result = calculate_bic_sac(sbox)
                    st.write(f"Hasil BIC-SAC: {result}")
                elif operation == "LAP":
                    result = calculate_lap(sbox)
                    st.write(f"Hasil LAP: {result}")
                elif operation == "DAP":
                    result = calculate_dap(sbox)
                    st.write(f"Hasil DAP: {result}")
        else:
            st.error("File tidak valid, pastikan file Excel mengandung 256 nilai.")

if __name__ == "__main__":
    main()

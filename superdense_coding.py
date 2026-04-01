"""
Secure Message Transmission with Superdense Coding
===================================================
Project by: Sriram G.
Course: Joint AI & Quantum Computing with Amazon Braket — QpiAI & IISc

This project implements the superdense coding protocol using Qiskit.
It demonstrates how 2 classical bits can be transmitted using only
1 qubit, thanks to pre-shared quantum entanglement.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# ─────────────────────────────────────────────
# STEP 1 — Encoding map
# Alice uses these gates to encode 2-bit messages
# ─────────────────────────────────────────────
ENCODE_MAP = {
    '00': 'I',   # Do nothing
    '01': 'X',   # Bit flip
    '10': 'Z',   # Phase flip
    '11': 'XZ',  # Both
}

# ─────────────────────────────────────────────
# STEP 2 — Build the superdense coding circuit
# ─────────────────────────────────────────────
def build_superdense_circuit(bits):
    """
    Builds a full superdense coding circuit for a 2-bit message.
    
    Args:
        bits (str): 2-bit string e.g. '00', '01', '10', '11'
    
    Returns:
        QuantumCircuit: complete circuit
    """
    qr = QuantumRegister(2, name='q')   # q[0] = Alice, q[1] = Bob
    cr = ClassicalRegister(2, name='c')
    qc = QuantumCircuit(qr, cr)

    # --- Phase 1: Create Bell State (Entanglement) ---
    qc.h(qr[0])           # Hadamard on Alice's qubit
    qc.cx(qr[0], qr[1])   # CNOT: Alice controls Bob
    qc.barrier(label='Entanglement')

    # --- Phase 2: Alice Encodes her message ---
    gate = ENCODE_MAP[bits]
    if 'X' in gate:
        qc.x(qr[0])
    if 'Z' in gate:
        qc.z(qr[0])
    qc.barrier(label=f'Alice encodes: {bits}')

    # --- Phase 3: Bob Decodes ---
    qc.cx(qr[0], qr[1])   # CNOT
    qc.h(qr[0])            # Hadamard
    qc.barrier(label="Bob decodes")

    # --- Phase 4: Measure ---
    qc.measure(qr[0], cr[0])
    qc.measure(qr[1], cr[1])

    return qc


# ─────────────────────────────────────────────
# STEP 3 — Simulate and decode one 2-bit chunk
# ─────────────────────────────────────────────
def simulate(bits, shots=1024):
    """
    Runs the superdense coding circuit on the Aer simulator.
    
    Args:
        bits (str): 2-bit message to send
        shots (int): number of simulation runs
    
    Returns:
        tuple: (decoded_bits, counts, circuit)
    """
    qc = build_superdense_circuit(bits)
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()
    decoded = max(counts, key=counts.get)  # most frequent result
    return decoded, counts, qc


# ─────────────────────────────────────────────
# STEP 4 — Text message encoding / decoding
# ─────────────────────────────────────────────
def text_to_bits(text):
    """Convert text string to list of 2-bit chunks."""
    all_bits = ''.join(format(ord(c), '08b') for c in text)
    # Pad to multiple of 2
    if len(all_bits) % 2 != 0:
        all_bits += '0'
    return [all_bits[i:i+2] for i in range(0, len(all_bits), 2)]


def bits_to_text(bit_chunks):
    """Convert list of 2-bit chunks back to text."""
    all_bits = ''.join(bit_chunks)
    # Pad to multiple of 8
    while len(all_bits) % 8 != 0:
        all_bits += '0'
    chars = []
    for i in range(0, len(all_bits), 8):
        byte = all_bits[i:i+8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)


# ─────────────────────────────────────────────
# STEP 5 — Full message transmission
# ─────────────────────────────────────────────
def transmit_message(message):
    """
    Encodes a full text message using superdense coding,
    transmits chunk by chunk, and recovers the original message.
    
    Args:
        message (str): original message from Alice
    
    Returns:
        tuple: (recovered_message, chunks, results)
    """
    print(f"\n{'='*55}")
    print(f"  SUPERDENSE CODING — SECURE MESSAGE TRANSMISSION")
    print(f"{'='*55}")
    print(f"\n  Original Message  : '{message}'")
    print(f"  Characters        : {len(message)}")
    print(f"  Classical bits    : {len(message) * 8}")
    print(f"  Qubits transmitted: {len(message) * 4}  (half the classical bits)")
    print(f"\n{'─'*55}")

    chunks = text_to_bits(message)
    decoded_chunks = []
    all_counts = {}

    print(f"\n  {'Chunk':<8} {'Alice sends':<15} {'Bob receives':<15} {'Match'}")
    print(f"  {'─'*5:<8} {'─'*11:<15} {'─'*11:<15} {'─'*5}")

    for i, chunk in enumerate(chunks):
        decoded, counts, _ = simulate(chunk)
        # Qiskit returns bits in reverse order — fix it
        decoded_fixed = decoded[::-1]
        decoded_chunks.append(decoded_fixed)
        all_counts[f'chunk_{i}_{chunk}'] = counts
        match = '✓' if decoded_fixed == chunk else '✗'
        print(f"  {i+1:<8} {chunk:<15} {decoded_fixed:<15} {match}")

    recovered = bits_to_text(decoded_chunks)

    print(f"\n{'─'*55}")
    print(f"\n  Recovered Message : '{recovered}'")
    print(f"\n  Transmission {'SUCCESS ✓' if recovered == message else 'FAILED ✗'}")
    print(f"\n{'='*55}\n")

    return recovered, chunks, all_counts


# ─────────────────────────────────────────────
# STEP 6 — Visualizations
# ─────────────────────────────────────────────
def save_circuit_diagrams(output_dir):
    """Save circuit diagrams for all four possible messages."""
    fig, axes = plt.subplots(2, 2, figsize=(18, 10))
    fig.suptitle(
        'Superdense Coding — Quantum Circuits for All 4 Messages',
        fontsize=15, fontweight='bold', y=1.01
    )

    messages = ['00', '01', '10', '11']
    gate_labels = {'00': 'I (identity)', '01': 'X (bit flip)',
                   '10': 'Z (phase flip)', '11': 'X then Z'}

    for idx, bits in enumerate(messages):
        ax = axes[idx // 2][idx % 2]
        qc = build_superdense_circuit(bits)
        qc.draw(output='mpl', ax=ax, style='iqp')
        ax.set_title(
            f"Message: '{bits}'  |  Alice applies: {gate_labels[bits]}",
            fontsize=11, pad=10
        )

    plt.tight_layout()
    path = os.path.join(output_dir, 'circuit_diagrams.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [Saved] Circuit diagrams → circuit_diagrams.png")
    return path


def save_measurement_histograms(output_dir):
    """Save measurement histograms for all four messages."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle(
        'Superdense Coding — Measurement Results (1024 shots each)',
        fontsize=14, fontweight='bold'
    )

    messages = ['00', '01', '10', '11']
    colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']

    for idx, bits in enumerate(messages):
        ax = axes[idx // 2][idx % 2]
        decoded, counts, _ = simulate(bits, shots=1024)

        # Fix bit order for display
        fixed_counts = {k[::-1]: v for k, v in counts.items()}

        bars = ax.bar(
            fixed_counts.keys(),
            fixed_counts.values(),
            color=colors[idx],
            edgecolor='black',
            linewidth=0.8
        )

        # Annotate bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height + 5,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10
            )

        ax.set_title(f"Alice sends: '{bits}'", fontsize=11, fontweight='bold')
        ax.set_xlabel('Measurement Outcome', fontsize=9)
        ax.set_ylabel('Count (out of 1024)', fontsize=9)
        ax.set_ylim(0, 1150)
        ax.grid(axis='y', alpha=0.3)

        # Highlight correct bar
        for bar, label in zip(bars, fixed_counts.keys()):
            if label == bits:
                bar.set_edgecolor('green')
                bar.set_linewidth(2.5)

    plt.tight_layout()
    path = os.path.join(output_dir, 'measurement_histograms.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [Saved] Measurement histograms → measurement_histograms.png")
    return path


def save_compression_comparison(message, output_dir):
    """Save a visual showing classical vs quantum transmission comparison."""
    n_chars = len(message)
    classical_bits = n_chars * 8
    quantum_qubits = n_chars * 4

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')

    categories = ['Classical\nTransmission', 'Quantum\n(Superdense Coding)']
    values = [classical_bits, quantum_qubits]
    colors = ['#E74C3C', '#2ECC71']

    bars = ax.bar(categories, values, color=colors, width=0.4,
                  edgecolor='black', linewidth=1.2)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            bar.get_height() + 0.5,
            f'{val} {"bits" if val == classical_bits else "qubits"}',
            ha='center', va='bottom',
            fontsize=13, fontweight='bold'
        )

    ax.set_title(
        f'Quantum Compression via Superdense Coding\nMessage: "{message}"  '
        f'({n_chars} characters)',
        fontsize=13, fontweight='bold', pad=15
    )
    ax.set_ylabel('Units Transmitted', fontsize=11)
    ax.set_ylim(0, classical_bits * 1.25)
    ax.grid(axis='y', alpha=0.3)

    # Annotation arrow
    ax.annotate(
        f'50% reduction\n({classical_bits} bits → {quantum_qubits} qubits)',
        xy=(1, quantum_qubits),
        xytext=(1.35, (classical_bits + quantum_qubits) / 2),
        arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
        fontsize=11, ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                  edgecolor='gray')
    )

    plt.tight_layout()
    path = os.path.join(output_dir, 'compression_comparison.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [Saved] Compression comparison → compression_comparison.png")
    return path


# ─────────────────────────────────────────────
# MAIN — Run everything
# ─────────────────────────────────────────────
if __name__ == '__main__':
    output_dir = '/mnt/user-data/outputs'
    os.makedirs(output_dir, exist_ok=True)

    # ── The message Alice wants to send ──
    message = "Quantum"

    # ── Run transmission ──
    recovered, chunks, counts = transmit_message(message)

    # ── Save all visualizations ──
    print("  Generating visualizations...")
    print()
    save_circuit_diagrams(output_dir)
    save_measurement_histograms(output_dir)
    save_compression_comparison(message, output_dir)

    print(f"\n  All outputs saved to: {output_dir}")
    print(f"  Done.\n")

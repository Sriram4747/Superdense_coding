# Secure Message Transmission with Superdense Coding

A quantum communication protocol implemented in Qiskit that demonstrates how **2 classical bits can be transmitted using only 1 qubit**, thanks to pre-shared quantum entanglement.

Built as part of the **Joint Certification in AI & Quantum Computing with Amazon Braket** — QpiAI & IISc.

---

## What is Superdense Coding?

In classical communication, sending 2 bits of information requires transmitting 2 bits. No shortcut exists.

Superdense coding breaks this rule using quantum entanglement:

- Alice and Bob share a **pre-entangled pair** of qubits (a Bell state)
- Alice applies one of four quantum gates to **her qubit only**, encoding a 2-bit message
- She physically sends **just that one qubit** to Bob
- Bob applies CNOT + Hadamard to both qubits and **recovers the full 2-bit message**

One qubit transmitted. Two bits received. The entanglement does the work of the missing bit.

```
Classical:  send 2 bits → transmit 2 bits
Quantum:    send 2 bits → transmit 1 qubit  (entanglement provides the rest)
```

---

## Encoding Table

Alice encodes her 2-bit message by applying one of four gates to her qubit:

| Message | Gate Applied | Effect |
|---------|-------------|--------|
| `00` | I (Identity) | Do nothing |
| `01` | X | Bit flip |
| `10` | Z | Phase flip |
| `11` | X then Z | Both |

Each gate transforms the shared Bell state into one of four perfectly distinguishable Bell states — which Bob decodes on the other end.

---

## Protocol Steps

```
STEP 1 — PREPARATION
Alice and Bob create a Bell state: (|00⟩ + |11⟩) / √2
Alice keeps qubit 0. Bob keeps qubit 1.

STEP 2 — ALICE ENCODES
Alice applies her gate based on the 2-bit message she wants to send.
She physically sends qubit 0 to Bob.

STEP 3 — BOB DECODES
Bob applies CNOT (qubit 0 controls qubit 1) then Hadamard (qubit 0).
He measures both qubits → recovers Alice's original 2-bit message.
```

---

## Project Structure

```
superdense-coding-qiskit/
│
├── README.md
├── superdense_coding.py       ← main implementation
│
└── outputs/
    ├── circuit_diagrams.png       ← quantum circuits for all 4 messages
    ├── measurement_histograms.png ← measurement results (1024 shots each)
    └── compression_comparison.png ← classical vs quantum transmission comparison
```

---

## Output Visuals

### Circuit Diagrams
Quantum circuits for all four possible messages — showing the three phases:
entanglement creation, Alice's encoding, and Bob's decoding.

![Circuit Diagrams](outputs/circuit_diagrams.png)

---

### Measurement Histograms
Simulation results over 1024 shots for each message.
Each message collapses to exactly the correct outcome — demonstrating perfect fidelity.

![Measurement Histograms](outputs/measurement_histograms.png)

---

### Compression Comparison
Visual comparison of classical bits vs qubits transmitted for the message "Quantum".
Superdense coding achieves exactly 50% reduction in physical transmission.

![Compression Comparison](outputs/compression_comparison.png)

---

## How to Run

### Prerequisites

```bash
pip install qiskit qiskit-aer pylatexenc matplotlib
```

### Run

```bash
python superdense_coding.py
```

### Change the Message

Open `superdense_coding.py` and edit line near the bottom:

```python
message = "Quantum"  # ← change this to any text
```

Run again — the protocol will encode, transmit, and recover your message.

---

## Sample Output

```
=======================================================
  SUPERDENSE CODING — SECURE MESSAGE TRANSMISSION
=======================================================

  Original Message  : 'Quantum'
  Characters        : 7
  Classical bits    : 56
  Qubits transmitted: 28  (half the classical bits)

─────────────────────────────────────────────────────

  Chunk    Alice sends     Bob receives    Match
  ─────    ───────────     ───────────     ─────
  1        01              01              ✓
  2        01              01              ✓
  3        00              00              ✓
  ...
  28       01              01              ✓

─────────────────────────────────────────────────────

  Recovered Message : 'Quantum'
  Transmission SUCCESS ✓
```

---

## Key Concepts Demonstrated

| Concept | Where It Appears |
|--------|-----------------|
| Qubit & Superposition | Hadamard gate creating equal superposition |
| Quantum Entanglement | Bell state shared between Alice and Bob |
| Quantum Gates | H, CNOT, X, Z used for encoding and decoding |
| Quantum Measurement | Final measurement recovering classical bits |
| Superdense Coding | Full protocol transmitting 2 bits per 1 qubit |
| Quantum Compression | 50% reduction in physical transmission units |

---

## Why This Matters

- **Efficient quantum communication** — fewer physical resources to transmit the same information
- **Secure transmission** — without the pre-shared entangled state, an eavesdropper cannot decode the message
- **Foundational protocol** — building block for the future quantum internet
- **Proof of quantum advantage** — demonstrates something classically impossible

---

## Certification

This project was completed as part of the  
**Joint Certification in Artificial Intelligence & Quantum Computing with Amazon Braket**  
by **QpiAI** in collaboration with **Indian Institute of Science (IISc), Bangalore.**

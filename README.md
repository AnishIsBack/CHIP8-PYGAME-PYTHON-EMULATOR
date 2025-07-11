# Chip-8 TETRIS Emulator in Python

This is a Chip-8 emulator built in Python using Pygame. It's a simple project that can run classic Chip-8 games like TETRIS. It includes a welcome screen with control instructions and a straightforward display setup.

---

## Features

- Written in pure Python
- Uses Pygame for graphics and input
- Supports most common Chip-8 opcodes
- Runs the TETRIS.ch8 ROM
- Displays a welcome screen with controls

---

## Controls (for TETRIS.ch8)

| Action      | Key  |
|-------------|------|
| Move Left   | Q    |
| Move Right  | E    |
| Rotate      | W    |
| Drop        | S    |

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/chip8-tetris-emulator.git
cd chip8-tetris-emulator
```

### 2. Install Dependencies
```bash
pip install pygame
```

### 3. Add a ROM
Make sure you have a Chip-8 TETRIS ROM named `TETRIS.ch8` and place it in the project folder.

> Note: This project includes the ROM for the chip8 TETRIS and the chip8 PONG. Please make sure you have the legal right to use them.

### 4. Run the Emulator
```bash
python chip8_opcode_fix.py
```

---

## How It Works
- The emulator fetches 2-byte instructions from memory
- It decodes and executes each opcode based on Chip-8 rules
- The display is updated using Pygame
- Keyboard input is mapped to the original Chip-8 keypad layout

---

## File Structure

```
chip8-tetris-emulator/
├── chip8_opcode_fix.py     # Emulator logic
├── TETRIS.ch8              # ROM file (not included)
└── README.md               # Documentation
```

---

## Supported Opcodes
Includes support for:
- `00E0` (clear screen)
- `00EE` (return)
- `1NNN`, `2NNN`, `3XNN`, `4XNN`, `5XY0`, `6XNN`, `7XNN`, `9XY0`
- `ANNN`, `CXNN`, `DXYN`
- `EX9E`, `EXA1`
- `FX07`, `FX15`, `FX18`, `FX1E`

More opcodes can be added as needed.

---

## Author
Anish Bommena

Built as a learning project. Feedback and contributions are welcome.

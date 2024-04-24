# ByteCoreCompiler

The ByteCoreCompiler transforms ByteCore assembly code into a 64KB memory byte array, compatible with the [ByteCore Emulator](https://github.com/joakimwinum/bytecore). It includes features to identify syntax errors and guide developers through debugging their code.

## Overview

The compiler process involves several steps to convert text-based assembly code into executable memory bytes:

1. **Lexical Analysis**: Converts raw text into tokens.
2. **Syntax Analysis**: Checks token structure and builds a syntax tree.
3. **Semantic Analysis**: Further inspects the syntax tree for logical consistency.

Successful compilation results in a memory byte array ready for emulation; errors during any stage will generate exceptions to highlight issues.

## ByteCore Assembly Language

The ByteCore assembly language represents instructions in a format that the ByteCore Emulator can execute directly, consisting of:

- **MSB (Most Significant Byte)**
- **LSB (Least Significant Byte)**
- **DATA**: Can be either a valid hexadecimal number or an opcode.

### Rules

The compiler adheres to specific rules to ensure the correct interpretation of ByteCore assembly:

- Strips leading, trailing, and extra spaces.
- Treats line breaks (`\n`, `\r`, `\r\n`) as new lines.
- Ignores text after a semicolon (`;`), which denotes a comment.
- Requires lines to have exactly 0 or 3 tokens, not counting comments.
- Expects the first two tokens of a line to represent numbers in hexadecimal format (0-255).
- Requires the third token to be either a valid opcode or a valid data value. Data values must be hexadecimal numbers ranging from 0 to 255 (00 to FF).
- Prohibits assigning data to a memory address that has already been set.
- Every opcode, except for `HALT`, expects an extended memory address to follow. For more details on how extended memory addresses are used within the ByteCore CPU's big-endian memory architecture, see the [Addressing Modes](https://github.com/joakimwinum/bytecore?tab=readme-ov-file#addressing-modes) section.

### Instructions

Refer to the [ByteCore Emulator README](https://github.com/joakimwinum/bytecore?tab=readme-ov-file#instructions) for a detailed list of supported instructions.

## Installation and Setup

### Prerequisites

Ensure Python 3.11 or newer is installed. Clone the repository and navigate to the root directory. Consider setting up a Python virtual environment to manage dependencies.

### Dependencies

Install required dependencies with:

```bash
pip3 install -r requirements.txt
```

### Gitpod

Alternatively, use Gitpod for a pre-configured environment by clicking [here](https://gitpod.io/#https://github.com/joakimwinum/bytecorecompiler).

## Usage

To compile ByteCore assembly code into memory bytes and execute it, follow these steps:

### Example 1: Simple Program

```python
from bytecorecompiler.compiler import Compiler
from bytecore.emulator import ByteCore

bytecore_assembly = """
00 00 LOAD
00 01 00
00 02 0A
00 03 ADD
00 04 00
00 05 0B
00 06 STORE
00 07 FF
00 08 FF
00 09 HALT
00 0A 14; 20
00 0B 1E; 30
"""

memory_bytes = Compiler(bytecore_assembly).get_memory_bytes()
byte_core = ByteCore(memory_bytes)
byte_core.cycle_until_halt()
dump = byte_core.dump()

dump.memory[-1]  # equals 50
```

### Example 2: Advanced Program

This example uses all defined opcodes to demonstrate the compiler's capabilities with a more complex program structure.

```python
from bytecorecompiler.compiler import Compiler
from bytecore.emulator import ByteCore

bytecore_assembly = """
00 00 JMP
00 01 FE
00 02 00

01 00 37; 55
01 01 14; 20
01 02 02;  2
01 03 01;  1

FE 00 LOAD
FE 01 01
FE 02 00
FE 03 ADD
FE 04 01
FE 05 02
FE 06 STORE
FE 07 01
FE 08 00
FE 09 LOAD
FE 0A 01
FE 0B 01
FE 0C SUB
FE 0D 01
FE 0E 03
FE 0F STORE
FE 10 01
FE 11 01
FE 12 LOAD
FE 13 01
FE 14 01
FE 15 JZ
FE 16 FF
FE 17 00
FE 18 JMP
FE 19 FE
FE 1A 00

FF 00 LOAD
FF 01 01
FF 02 00
FF 03 STORE
FF 04 FF
FF 05 FF
FF 06 HALT
"""

memory_bytes = Compiler(bytecore_assembly).get_memory_bytes()
byte_core = ByteCore(memory_bytes)
byte_core.cycle_until_halt()
dump = byte_core.dump()

dump.memory[-1]  # equals 95
```

## License

This project is licensed under the terms of the MIT License. See the [LICENSE](https://github.com/joakimwinum/bytecorecompiler/blob/main/LICENSE) file for the full text.

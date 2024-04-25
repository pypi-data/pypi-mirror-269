def LDA():
    """
    Load Accumulator (LDA) - Instruction
    -------------------------------------
    Load a value from memory into the accumulator register.

    Usage:
    LDA address

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the loaded value is negative.
    - Zero (Z): Set if the loaded value is zero.

    Notes:
    - The value at the specified memory address is loaded into the accumulator.
    - Flags are updated based on the loaded value.
    - The loaded value does not affect the carry flag (C).
    - Ensure that the specified memory address contains the desired value.
    """


def LDX():
    """
    Load X Register (LDX) - Instruction
    ------------------------------------
    Load a value from memory into the X register.

    Usage:
    LDX address

    Registers affected:
    - X Register (X)

    Flags affected:
    - Negative (N): Set if the loaded value is negative.
    - Zero (Z): Set if the loaded value is zero.

    Notes:
    - The value at the specified memory address is loaded into the X register.
    - Flags are updated based on the loaded value.
    - The loaded value does not affect the carry flag (C).
    - Caution: Verify the correctness of the memory address to prevent unintended data corruption.
    - Critical: Ensure the integrity of the loaded value as it directly affects subsequent program execution.
    - Essential: Verify the loaded value against expected values to ensure proper program behavior, as incorrect data may lead to catastrophic consequences.
    """


def LDY():
    """
    Load Y Register (LDY) - Instruction
    ------------------------------------
    Load a value from memory into the Y register.

    Usage:
    LDY address

    Registers affected:
    - Y Register (Y)

    Flags affected:
    - Negative (N): Set if the loaded value is negative.
    - Zero (Z): Set if the loaded value is zero.

    Notes:
    - The value at the specified memory address is loaded into the Y register.
    - Flags are updated based on the loaded value.
    - The loaded value does not affect the carry flag (C).
    - Caution: Verify the correctness of the memory address to prevent unintended data corruption.
    - Critical: Ensure the integrity of the loaded value as it directly affects subsequent program execution.
    - Essential: Verify the loaded value against expected values to ensure proper program behavior, as incorrect data may lead to catastrophic consequences.
    """


def STA():
    """
    Store Accumulator (STA) - Instruction
    -------------------------------------
    Store the value in the accumulator register into memory.

    Usage:
    STA address

    Registers affected: None

    Flags affected: None

    Address modes supported:
    - Absolute
    - Absolute X
    - Absolute Y
    - Zero Page
    - Zero Page X
    - Indirect X
    - Indirect Y

    Notes:
    - The value in the accumulator is stored at the specified memory address.
    - This instruction does not affect any registers or flags.
    - Supported address modes include absolute addressing, zero page addressing, and indexed zero page addressing with X and Y registers, as well as indirect addressing modes.
    - Caution: Verify the correctness of the memory address to prevent unintended data corruption.
    - Critical: Ensure the integrity of the stored value as it directly affects subsequent program execution.
    - Essential: Verify the stored value against expected values to ensure proper program behavior, as incorrect data may lead to catastrophic consequences.
    """


def STX():
    """
    Store X Register (STX) - Instruction
    -------------------------------------
    Store the value in the X register into memory.

    Usage:
    STX address

    Registers affected: None

    Flags affected: None

    Address modes supported:
    - Absolute
    - Zero Page
    - Zero Page Y

    Notes:
    - The value in the X register is stored at the specified memory address.
    - This instruction does not affect any registers or flags.
    - Supported address modes include absolute addressing, zero page addressing, and zero page addressing with Y-indexing.
    - Caution: Verify the correctness of the memory address to prevent unintended data corruption.
    - Critical: Ensure the integrity of the stored value as it directly affects subsequent program execution.
    - Essential: Verify the stored value against expected values to ensure proper program behavior, as incorrect data may lead to catastrophic consequences.
    """


def STY():
    """
    Store Y Register (STY) - Instruction
    -------------------------------------
    Store the value in the Y register into memory.

    Usage:
    STY address

    Registers affected: None

    Flags affected: None

    Address modes supported:
    - Absolute
    - Zero Page
    - Zero Page X

    Notes:
    - The value in the Y register is stored at the specified memory address.
    - This instruction does not affect any registers or flags.
    - Supported address modes include absolute addressing, zero page addressing, and zero page addressing with X-indexing.
    - Caution: Verify the correctness of the memory address to prevent unintended data corruption.
    - Critical: Ensure the integrity of the stored value as it directly affects subsequent program execution.
    - Essential: Verify the stored value against expected values to ensure proper program behavior, as incorrect data may lead to catastrophic consequences.
    """


def TAX():
    """
    Transfer Accumulator to X (TAX) - Instruction
    ---------------------------------------------
    Transfer the value from the accumulator to the X register.

    Usage:
    TAX

    Registers affected:
    - X Register (X)

    Flags affected:
    - Negative (N): Set if the resulting value in the X register is negative.
    - Zero (Z): Set if the resulting value in the X register is zero.

    Address modes supported:
    - Implied

    Notes:
    - The value from the accumulator is transferred to the X register.
    - Flags are updated based on the resulting value in the X register.
    - This instruction does not affect the accumulator or any other flags.
    - Caution: Verify the integrity of the data in the accumulator before transfer to prevent unintended consequences.
    - Critical: Ensure proper usage of the transferred value in subsequent operations, as it affects program logic.
    - Essential: Verify the resulting value in the X register against expected values to ensure correct program behavior.
    """


def TAY():
    """
    Transfer Accumulator to Y (TAY) - Instruction
    ---------------------------------------------
    Transfer the value from the accumulator to the Y register.

    Usage:
    TAY

    Registers affected:
    - Y Register (Y)

    Flags affected:
    - Negative (N): Set if the resulting value in the Y register is negative.
    - Zero (Z): Set if the resulting value in the Y register is zero.

    Address modes supported:
    - Implied

    Notes:
    - The value from the accumulator is transferred to the Y register.
    - Flags are updated based on the resulting value in the Y register.
    - This instruction does not affect the accumulator or any other flags.
    - Caution: Verify the integrity of the data in the accumulator before transfer to prevent unintended consequences.
    - Critical: Ensure proper usage of the transferred value in subsequent operations, as it affects program logic.
    - Essential: Verify the resulting value in the Y register against expected values to ensure correct program behavior.
    """


def TYA():
    """
    Transfer Y to Accumulator (TYA) - Instruction
    ---------------------------------------------
    Transfer the value from the Y register to the accumulator.

    Usage:
    TYA

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the resulting value in the accumulator is negative.
    - Zero (Z): Set if the resulting value in the accumulator is zero.

    Address modes supported:
    - Implied

    Notes:
    - The value from the Y register is transferred to the accumulator.
    - Flags are updated based on the resulting value in the accumulator.
    - This instruction does not affect the Y register or any other flags.
    - Caution: Verify the integrity of the data in the Y register before transfer to prevent unintended consequences.
    - Critical: Ensure proper usage of the transferred value in subsequent operations, as it affects program logic.
    - Essential: Verify the resulting value in the accumulator against expected values to ensure correct program behavior.
    """


def TXS():
    """
    Transfer X to Stack Pointer (TXS) - Instruction
    ----------------------------------------------
    Transfer the value from the X register to the stack pointer.

    Usage:
    TXS

    Registers affected:
    - Stack Pointer (SP)

    Flags affected:
    - None

    Address modes supported:
    - Implied

    Notes:
    - The value from the X register is transferred to the stack pointer.
    - This instruction does not affect any flags.
    - Caution: Verify the integrity of the data in the X register before transfer to prevent unintended consequences.
    - Critical: Ensure proper usage of the transferred value in subsequent operations, as it affects stack operations.
    - Essential: Verify the resulting value in the stack pointer against expected values to ensure correct program behavior.
    """


def TSX():
    """
    Transfer Stack Pointer to Index X.

    Transfers the current value of the stack pointer (SP) to the X register.

    Registers Affected:
    - X: The X register is loaded with the value of the stack pointer.

    Flags Affected:
    - N: Set if the result is negative, cleared otherwise.
    - Z: Set if the result is zero, cleared otherwise.

    Notes:
    - None.

    Addressing Mode:
    - Implied

    Opcode:
    - Hex: 0xBA
    - Decimal: 186
    - Binary: 10111010
    """


def PHP():
    """
    Push Processor Status (PHP) - Instruction
    ------------------------------------------
    Push the processor status (flags) onto the stack.

    Usage:
    PHP

    Registers affected: None

    Flags affected: None

    Address modes supported:
    - Implied

    Notes:
    - The processor status (flags) are pushed onto the stack.
    - This instruction does not affect any registers or flags.
    - Caution: Ensure proper stack management to prevent stack overflow.
    - Critical: Verify stack integrity before executing PHP, as invalid stack operations can lead to unpredictable behavior.
    - Essential: Understand the implications of the pushed flags on subsequent program execution.
    """


def PLA():
    """
    Pull Accumulator (PLA) - Instruction
    -------------------------------------
    Pull the value from the stack into the accumulator.

    Usage:
    PLA

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the pulled value is negative.
    - Zero (Z): Set if the pulled value is zero.

    Address modes supported:
    - Implied

    Notes:
    - The value is pulled from the stack and loaded into the accumulator.
    - Flags are updated based on the pulled value.
    - Caution: Ensure proper stack management to prevent stack underflow.
    - Critical: Verify stack integrity before executing PLA, as invalid stack operations can lead to unpredictable behavior.
    - Essential: Understand the implications of the pulled value on subsequent program execution.
    """


def PLP():
    """
    Pull Processor Status (PLP) - Instruction
    -----------------------------------------
    Pull the processor status (flags) from the stack.

    Usage:
    PLP

    Registers affected: None

    Flags affected:
    - Carry (C)
    - Zero (Z)
    - Interrupt Disable (I)
    - Decimal Mode (D)
    - Break Command (B)
    - Overflow (V)
    - Negative (N)

    Address modes supported:
    - Implied

    Notes:
    - The processor status (flags) are pulled from the stack.
    - All processor status flags are affected by this operation.
    - The Break flag (B) is set to the value pulled from the stack.
    - Caution: Ensure proper stack management to prevent stack underflow.
    - Critical: Verify stack integrity before executing PLP, as invalid stack operations can lead to unpredictable behavior.
    - Essential: Understand the implications of the pulled flags on subsequent program execution.
    """


def AND():
    """
    Logical AND (AND) - Instruction
    --------------------------------
    Perform a bitwise AND operation between the accumulator and a value from memory.

    Usage:
    AND address

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the result of the AND operation is negative.
    - Zero (Z): Set if the result of the AND operation is zero.

    Address modes supported:
    - Immediate
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X
    - Absolute Y
    - Indirect X
    - Indirect Y

    Notes:
    - Performs a bitwise AND operation between the value in the accumulator and the value fetched from memory.
    - The result is stored in the accumulator.
    - Flags are updated based on the result of the AND operation.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the logical operation performed and its impact on subsequent program logic.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def EOR():
    """
    Exclusive OR (EOR) - Instruction
    ---------------------------------
    Perform a bitwise Exclusive OR operation between the accumulator and a value from memory.

    Usage:
    EOR address

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the result of the EOR operation is negative.
    - Zero (Z): Set if the result of the EOR operation is zero.

    Address modes supported:
    - Immediate
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X
    - Absolute Y
    - Indirect X
    - Indirect Y

    Notes:
    - Performs a bitwise Exclusive OR operation between the value in the accumulator and the value fetched from memory.
    - The result is stored in the accumulator.
    - Flags are updated based on the result of the EOR operation.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the logical operation performed and its impact on subsequent program logic.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def ORA():
    """
    Logical OR (ORA) - Instruction
    -------------------------------
    Perform a bitwise OR operation between the accumulator and a value from memory.

    Usage:
    ORA address

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the result of the OR operation is negative.
    - Zero (Z): Set if the result of the OR operation is zero.

    Address modes supported:
    - Immediate
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X
    - Absolute Y
    - Indirect X
    - Indirect Y

    Notes:
    - Performs a bitwise OR operation between the value in the accumulator and the value fetched from memory.
    - The result is stored in the accumulator.
    - Flags are updated based on the result of the OR operation.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the logical operation performed and its impact on subsequent program logic.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def BIT():
    """
    Bit Test (BIT) - Instruction
    -----------------------------
    Perform a bitwise AND between the accumulator and a value from memory, setting flags accordingly.

    Usage:
    BIT address

    Registers affected:
    - None

    Flags affected:
    - Negative (N): Set if bit 7 of the fetched value is set.
    - Overflow (V): Set if bit 6 of the fetched value is set.
    - Zero (Z): Set if the result of the AND operation is zero.

    Address modes supported:
    - Zero Page
    - Absolute

    Notes:
    - Performs a bitwise AND operation between the value in the accumulator and the value fetched from memory.
    - The result does not get stored anywhere; it only sets flags based on the AND operation.
    - Flags are updated based on the result of the AND operation.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the logical operation performed and its impact on subsequent program logic.
    - Essential: Verify the flags against expected values to ensure correct program behavior.
    """


def ADC():
    """
    Add with Carry (ADC) - Instruction
    -----------------------------------
    Add the value from memory to the accumulator along with the carry flag.

    Usage:
    ADC address

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the result is negative.
    - Zero (Z): Set if the result is zero.
    - Overflow (V): Set if the result exceeds the signed range (-128 to 127).
    - Carry (C): Set if there is a carry from the most significant bit.

    Address modes supported:
    - Immediate
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X
    - Absolute Y
    - Indirect X
    - Indirect Y

    Notes:
    - Adds the value fetched from memory to the accumulator, along with the carry flag if it is set.
    - Flags are updated based on the result of the addition.
    - Overflow flag indicates signed overflow.
    - Carry flag indicates unsigned overflow.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the range limitations and behavior of overflow flags.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def SBC():
    """
    Subtract with Carry (SBC) - Instruction
    ----------------------------------------
    Subtract the value from memory from the accumulator along with the carry flag.

    Usage:
    SBC address

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the result is negative.
    - Zero (Z): Set if the result is zero.
    - Overflow (V): Set if the result exceeds the signed range (-128 to 127).
    - Carry (C): Set if there was a borrow required from the most significant bit.

    Address modes supported:
    - Immediate
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X
    - Absolute Y
    - Indirect X
    - Indirect Y

    Notes:
    - Subtracts the value fetched from memory from the accumulator, along with the carry flag if it is set.
    - Flags are updated based on the result of the subtraction.
    - Overflow flag indicates signed overflow.
    - Carry flag indicates borrow from the most significant bit.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the range limitations and behavior of overflow flags.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def CMP():
    """
    Compare (CMP) - Instruction
    ----------------------------
    Compare the value in the accumulator with a value from memory.

    Usage:
    CMP address

    Registers affected:
    - None

    Flags affected:
    - Negative (N): Set if the accumulator value is greater than the memory value.
    - Zero (Z): Set if the accumulator value is equal to the memory value.
    - Carry (C): Set if the accumulator value is greater than or equal to the memory value.

    Address modes supported:
    - Immediate
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X
    - Absolute Y
    - Indirect X
    - Indirect Y

    Notes:
    - Compares the value in the accumulator with the value fetched from memory.
    - Flags are updated based on the comparison result.
    - Carry flag indicates the result of the comparison (borrow).
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the behavior of comparison flags and their implications.
    - Essential: Verify the flags against expected values to ensure correct program behavior.
    """


def CPX():
    """
    Compare X Register (CPX) - Instruction
    ---------------------------------------
    Compare the value in the X register with a value from memory.

    Usage:
    CPX address

    Registers affected:
    - None

    Flags affected:
    - Negative (N): Set if the X register value is greater than the memory value.
    - Zero (Z): Set if the X register value is equal to the memory value.
    - Carry (C): Set if the X register value is greater than or equal to the memory value.

    Address modes supported:
    - Immediate
    - Zero Page
    - Absolute

    Notes:
    - Compares the value in the X register with the value fetched from memory.
    - Flags are updated based on the comparison result.
    - Carry flag indicates the result of the comparison (borrow).
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the behavior of comparison flags and their implications.
    - Essential: Verify the flags against expected values to ensure correct program behavior.
    """


def CPY():
    """
    Compare Y Register (CPY) - Instruction
    ---------------------------------------
    Compare the value in the Y register with a value from memory.

    Usage:
    CPY address

    Registers affected:
    - None

    Flags affected:
    - Negative (N): Set if the Y register value is greater than the memory value.
    - Zero (Z): Set if the Y register value is equal to the memory value.
    - Carry (C): Set if the Y register value is greater than or equal to the memory value.

    Address modes supported:
    - Immediate
    - Zero Page
    - Absolute

    Notes:
    - Compares the value in the Y register with the value fetched from memory.
    - Flags are updated based on the comparison result.
    - Carry flag indicates the result of the comparison (borrow).
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the behavior of comparison flags and their implications.
    - Essential: Verify the flags against expected values to ensure correct program behavior.
    """


def INC():
    """
    Increment Memory (INC) - Instruction
    -------------------------------------
    Increment the value in memory by one.

    Usage:
    INC address

    Registers affected:
    - None

    Flags affected:
    - Negative (N): Set if the incremented value is negative.
    - Zero (Z): Set if the incremented value is zero.

    Address modes supported:
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X

    Notes:
    - Increments the value in memory by one.
    - Flags are updated based on the resulting value in memory.
    - Caution: Ensure that the memory address contains the value to be incremented before executing the instruction.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def INX():
    """
    Increment X Register (INX) - Instruction
    -----------------------------------------
    Increment the value in the X register by one.

    Usage:
    INX

    Registers affected:
    - X Register (X)

    Flags affected:
    - Negative (N): Set if the incremented value in the X register is negative.
    - Zero (Z): Set if the incremented value in the X register is zero.

    Address modes supported:
    - Implied

    Notes:
    - Increments the value in the X register by one.
    - Flags are updated based on the resulting value in the X register.
    - This instruction does not affect any memory location.
    - Caution: Ensure proper usage of the incremented value in subsequent operations.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def INY():
    """
    Increment Y Register (INY) - Instruction
    -----------------------------------------
    Increment the value in the Y register by one.

    Usage:
    INY

    Registers affected:
    - Y Register (Y)

    Flags affected:
    - Negative (N): Set if the incremented value in the Y register is negative.
    - Zero (Z): Set if the incremented value in the Y register is zero.

    Address modes supported:
    - Implied

    Notes:
    - Increments the value in the Y register by one.
    - Flags are updated based on the resulting value in the Y register.
    - This instruction does not affect any memory location.
    - Caution: Ensure proper usage of the incremented value in subsequent operations.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def DEC():
    """
    Decrement Memory (DEC) - Instruction
    -------------------------------------
    Decrement the value in memory by one.

    Usage:
    DEC address

    Registers affected:
    - None

    Flags affected:
    - Negative (N): Set if the decremented value is negative.
    - Zero (Z): Set if the decremented value is zero.

    Address modes supported:
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X

    Notes:
    - Decrements the value in memory by one.
    - Flags are updated based on the resulting value in memory.
    - Caution: Ensure that the memory address contains the value to be decremented before executing the instruction.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def DEX():
    """
    Decrement X Register (DEX) - Instruction
    -----------------------------------------
    Decrement the value in the X register by one.

    Usage:
    DEX

    Registers affected:
    - X Register (X)

    Flags affected:
    - Negative (N): Set if the decremented value in the X register is negative.
    - Zero (Z): Set if the decremented value in the X register is zero.

    Address modes supported:
    - Implied

    Notes:
    - Decrements the value in the X register by one.
    - Flags are updated based on the resulting value in the X register.
    - This instruction does not affect any memory location.
    - Caution: Ensure proper usage of the decremented value in subsequent operations.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def DEY():
    """
    Decrement Y Register (DEY) - Instruction
    -----------------------------------------
    Decrement the value in the Y register by one.

    Usage:
    DEY

    Registers affected:
    - Y Register (Y)

    Flags affected:
    - Negative (N): Set if the decremented value in the Y register is negative.
    - Zero (Z): Set if the decremented value in the Y register is zero.

    Address modes supported:
    - Implied

    Notes:
    - Decrements the value in the Y register by one.
    - Flags are updated based on the resulting value in the Y register.
    - This instruction does not affect any memory location.
    - Caution: Ensure proper usage of the decremented value in subsequent operations.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def ASL():
    """
    Arithmetic Shift Left (ASL) - Instruction
    ------------------------------------------
    Shift the bits of a memory location or the accumulator left by one position.

    Usage:
    ASL address
    ASL A

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the result is negative.
    - Zero (Z): Set if the result is zero.
    - Carry (C): Set if the shifted-out bit is 1.

    Address modes supported:
    - Accumulator
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X

    Notes:
    - Shifts the bits of a memory location or the accumulator left by one position.
    - The most significant bit is shifted into the carry flag.
    - Flags are updated based on the result of the shift operation.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def LSR():
    """
    Logical Shift Right (LSR) - Instruction
    ----------------------------------------
    Shift the bits of a memory location or the accumulator right by one position.

    Usage:
    LSR address
    LSR A

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set to 0.
    - Zero (Z): Set if the result is zero.
    - Carry (C): Set if the shifted-out bit is 1.

    Address modes supported:
    - Accumulator
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X

    Notes:
    - Shifts the bits of a memory location or the accumulator right by one position.
    - The least significant bit is shifted into the carry flag.
    - Flags are updated based on the result of the shift operation.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def ROL():
    """
    Rotate Left (ROL) - Instruction
    --------------------------------
    Rotate the bits of a memory location or the accumulator left by one position.

    Usage:
    ROL address
    ROL A

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the result is negative.
    - Zero (Z): Set if the result is zero.
    - Carry (C): Set to the value of the old bit 7.

    Address modes supported:
    - Accumulator
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X

    Notes:
    - Rotates the bits of a memory location or the accumulator left by one position.
    - The carry flag is shifted into the least significant bit, and the old bit 7 is shifted into the carry flag.
    - Flags are updated based on the result of the rotation operation.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def ROR():
    """
    Rotate Right (ROR) - Instruction
    ---------------------------------
    Rotate the bits of a memory location or the accumulator right by one position.

    Usage:
    ROR address
    ROR A

    Registers affected:
    - Accumulator (A)

    Flags affected:
    - Negative (N): Set if the result is negative.
    - Zero (Z): Set if the result is zero.
    - Carry (C): Set to the value of the old bit 0.

    Address modes supported:
    - Accumulator
    - Zero Page
    - Zero Page X
    - Absolute
    - Absolute X

    Notes:
    - Rotates the bits of a memory location or the accumulator right by one position.
    - The carry flag is shifted into the most significant bit, and the old bit 0 is shifted into the carry flag.
    - Flags are updated based on the result of the rotation operation.
    - Caution: Ensure that the memory address contains the desired value before executing the instruction.
    - Critical: Understand the behavior of the flags and their implications.
    - Essential: Verify the result against expected values to ensure correct program behavior.
    """


def JMP():
    """
    Jump (JMP) - Instruction
    -------------------------
    Jump to a new memory location.

    Usage:
    JMP address
    JMP (address)

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Absolute
    - Indirect

    Notes:
    - Jumps to the specified memory address.
    - Supports both absolute and indirect addressing modes.
    - The absolute addressing mode jumps directly to the specified address.
    - The indirect addressing mode performs an indirect jump to the address specified by the operand, useful for implementing subroutine calls.
    - Caution: Ensure that the memory address to jump to is valid and contains executable code.
    - Essential: Verify that the jump destination is correctly set for the desired program flow.
    """


def JSR():
    """
    Jump to Subroutine (JSR) - Instruction
    ---------------------------------------
    Jump to a subroutine, saving the return address on the stack.

    Usage:
    JSR address

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Absolute

    Notes:
    - Jumps to the specified subroutine address.
    - The return address (address of the instruction following the JSR) is pushed onto the stack.
    - Useful for implementing function calls and subroutines.
    - Upon reaching the subroutine, execution continues from the specified address.
    - Caution: Ensure that the subroutine address is valid and contains executable code.
    - Essential: Verify the subroutine logic and return flow to prevent errors.
    """


def RTS():
    """
    Return from Subroutine (RTS) - Instruction
    ------------------------------------------
    Return from a subroutine, restoring the program counter from the stack.

    Usage:
    RTS

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Implied

    Notes:
    - Restores the program counter (PC) from the stack, effectively returning from a subroutine.
    - The return address is retrieved from the top two bytes of the stack.
    - Execution continues from the instruction following the original JSR (Jump to Subroutine).
    - Caution: Ensure that the stack is properly managed to prevent unexpected behavior.
    - Essential: Verify the subroutine logic and return flow to prevent errors.
    """


def BCC():
    """
    Branch if Carry Clear (BCC) - Instruction
    ------------------------------------------
    Branches to a relative memory address if the carry flag is clear.

    Usage:
    BCC address

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Relative

    Notes:
    - Branches to the specified relative memory address if the carry flag (C) is clear.
    - The branch distance is calculated relative to the next instruction's address.
    - If the carry flag is not set (C = 0), the program counter (PC) is updated to the new address.
    - Otherwise, execution continues with the next instruction.
    - Caution: Ensure that the branch condition is correctly set to avoid unexpected program behavior.
    - Essential: Verify the branch logic and destination address for the desired program flow.
    """


def BEQ():
    """
    Branch if Equal (BEQ) - Instruction
    ------------------------------------
    Branches to a relative memory address if the zero flag is set.

    Usage:
    BEQ address

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Relative

    Notes:
    - Branches to the specified relative memory address if the zero flag (Z) is set.
    - The branch distance is calculated relative to the next instruction's address.
    - If the zero flag is set (Z = 1), the program counter (PC) is updated to the new address.
    - Otherwise, execution continues with the next instruction.
    - This is often used for implementing conditional branches based on the result of a previous operation.
    - Caution: Ensure that the branch condition is correctly set to avoid unexpected program behavior.
    - Essential: Verify the branch logic and destination address for the desired program flow.
    """


def BMI():
    """
    Branch if Minus (BMI) - Instruction
    ------------------------------------
    Branches to a relative memory address if the negative flag is set.

    Usage:
    BMI address

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Relative

    Notes:
    - Branches to the specified relative memory address if the negative flag (N) is set.
    - The branch distance is calculated relative to the next instruction's address.
    - If the negative flag is set (N = 1), the program counter (PC) is updated to the new address.
    - Otherwise, execution continues with the next instruction.
    - This is often used for implementing conditional branches based on the result of a previous operation.
    - Caution: Ensure that the branch condition is correctly set to avoid unexpected program behavior.
    - Essential: Verify the branch logic and destination address for the desired program flow.
    """


def BNE():
    """
    Branch if Not Equal (BNE) - Instruction
    ----------------------------------------
    Branches to a relative memory address if the zero flag is clear.

    Usage:
    BNE address

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Relative

    Notes:
    - Branches to the specified relative memory address if the zero flag (Z) is clear.
    - The branch distance is calculated relative to the next instruction's address.
    - If the zero flag is clear (Z = 0), the program counter (PC) is updated to the new address.
    - Otherwise, execution continues with the next instruction.
    - This is often used for implementing conditional branches based on the result of a previous operation.
    - Caution: Ensure that the branch condition is correctly set to avoid unexpected program behavior.
    - Essential: Verify the branch logic and destination address for the desired program flow.
    """


def BPL():
    """
    Branch if Positive (BPL) - Instruction
    --------------------------------------
    Branches to a relative memory address if the negative flag is clear.

    Usage:
    BPL address

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Relative

    Notes:
    - Branches to the specified relative memory address if the negative flag (N) is clear.
    - The branch distance is calculated relative to the next instruction's address.
    - If the negative flag is clear (N = 0), the program counter (PC) is updated to the new address.
    - Otherwise, execution continues with the next instruction.
    - This is often used for implementing conditional branches based on the result of a previous operation.
    - Caution: Ensure that the branch condition is correctly set to avoid unexpected program behavior.
    - Essential: Verify the branch logic and destination address for the desired program flow.
    """


def BVC():
    """
    Branch if Overflow Clear (BVC) - Instruction
    --------------------------------------------
    Branches to a relative memory address if the overflow flag is clear.

    Usage:
    BVC address

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Relative

    Notes:
    - Branches to the specified relative memory address if the overflow flag (V) is clear.
    - The branch distance is calculated relative to the next instruction's address.
    - If the overflow flag is clear (V = 0), the program counter (PC) is updated to the new address.
    - Otherwise, execution continues with the next instruction.
    - This is often used for implementing conditional branches based on the result of a previous operation.
    - Caution: Ensure that the branch condition is correctly set to avoid unexpected program behavior.
    - Essential: Verify the branch logic and destination address for the desired program flow.
    """


def BVS():
    """
    Branch if Overflow Set (BVS) - Instruction
    ------------------------------------------
    Branches to a relative memory address if the overflow flag is set.

    Usage:
    BVS address

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Relative

    Notes:
    - Branches to the specified relative memory address if the overflow flag (V) is set.
    - The branch distance is calculated relative to the next instruction's address.
    - If the overflow flag is set (V = 1), the program counter (PC) is updated to the new address.
    - Otherwise, execution continues with the next instruction.
    - This is often used for implementing conditional branches based on the result of a previous operation.
    - Caution: Ensure that the branch condition is correctly set to avoid unexpected program behavior.
    - Essential: Verify the branch logic and destination address for the desired program flow.
    """


def CLC():
    """
    Clear Carry Flag (CLC) - Instruction
    -------------------------------------
    Clears the carry flag to 0.

    Usage:
    CLC

    Registers affected:
    - None

    Flags affected:
    - Carry (C): Set to 0.

    Address modes supported:
    - Implied

    Notes:
    - Clears the carry flag (C) to 0.
    - This instruction is used to prepare for arithmetic or logical operations that require no carry from a previous operation.
    - Caution: Ensure that the carry flag is appropriately set before executing subsequent instructions that depend on its state.
    - Essential: Verify the carry flag state for correct program behavior.
    """


def CLD():
    """
    Clear Decimal Mode (CLD) - Instruction
    ---------------------------------------
    Clears the decimal mode flag to 0.

    Usage:
    CLD

    Registers affected:
    - None

    Flags affected:
    - Decimal Mode (D): Set to 0.

    Address modes supported:
    - Implied

    Notes:
    - Clears the decimal mode flag (D) to 0.
    - This instruction is used to exit the decimal mode, allowing arithmetic operations to be performed in binary mode.
    - Caution: Ensure that the decimal mode flag is appropriately set before executing subsequent instructions that depend on its state.
    - Essential: Verify the decimal mode flag state for correct program behavior.
    """


def CLI():
    """
    Clear Interrupt Disable (CLI) - Instruction
    -------------------------------------------
    Clears the interrupt disable flag to 0.

    Usage:
    CLI

    Registers affected:
    - None

    Flags affected:
    - Interrupt Disable (I): Set to 0.

    Address modes supported:
    - Implied

    Notes:
    - Clears the interrupt disable flag (I) to 0.
    - This instruction enables interrupts, allowing the CPU to respond to external interrupt requests.
    - Caution: Ensure that the interrupt disable flag is appropriately set before executing subsequent instructions that depend on its state.
    - Essential: Verify the interrupt disable flag state for correct program behavior.
    """


def CLV():
    """
    Clear Overflow Flag (CLV) - Instruction
    ----------------------------------------
    Clears the overflow flag to 0.

    Usage:
    CLV

    Registers affected:
    - None

    Flags affected:
    - Overflow (V): Set to 0.

    Address modes supported:
    - Implied

    Notes:
    - Clears the overflow flag (V) to 0.
    - This instruction is used to clear the overflow flag, indicating no overflow occurred in a previous arithmetic operation.
    - Caution: Ensure that the overflow flag is appropriately set before executing subsequent instructions that depend on its state.
    - Essential: Verify the overflow flag state for correct program behavior.
    """


def SED():
    """
    Set Decimal Mode (SED) - Instruction
    -------------------------------------
    Sets the decimal mode flag to 1.

    Usage:
    SED

    Registers affected:
    - None

    Flags affected:
    - Decimal Mode (D): Set to 1.

    Address modes supported:
    - Implied

    Notes:
    - Sets the decimal mode flag (D) to 1.
    - This instruction enables decimal mode, allowing arithmetic operations to be performed in decimal rather than binary.
    - Caution: Ensure that the decimal mode flag is appropriately set before executing subsequent instructions that depend on its state.
    - Essential: Verify the decimal mode flag state for correct program behavior.
    """


def SEI():
    """
    Set Interrupt Disable (SEI) - Instruction
    -----------------------------------------
    Sets the interrupt disable flag to 1.

    Usage:
    SEI

    Registers affected:
    - None

    Flags affected:
    - Interrupt Disable (I): Set to 1.

    Address modes supported:
    - Implied

    Notes:
    - Sets the interrupt disable flag (I) to 1.
    - This instruction disables interrupts, preventing the CPU from responding to external interrupt requests.
    - Caution: Ensure that the interrupt disable flag is appropriately set before executing subsequent instructions that depend on its state.
    - Essential: Verify the interrupt disable flag state for correct program behavior.
    """


def BRK():
    """
    Break (BRK) - Instruction
    --------------------------
    Initiates an interrupt request (IRQ) and transfers control to the interrupt handler.

    Usage:
    BRK

    Registers affected:
    - None

    Flags affected:
    - Break (B): Set to 1.
    - Unused (U): Set to 1.
    - Interrupt Disable (I): Set to 1.

    Address modes supported:
    - Implied

    Notes:
    - Initiates an interrupt request (IRQ) and transfers control to the interrupt handler.
    - Pushes the program counter (PC) and status register (SR) onto the stack.
    - Sets the break (B) and unused (U) flags in the status register to 1.
    - Sets the interrupt disable (I) flag in the status register to 1, disabling further interrupts.
    - The interrupt handler can read the pushed PC and SR from the stack and resume execution.
    - Caution: Ensure that the interrupt handler is properly set up to handle the interrupt.
    - Essential: Verify the functionality of the interrupt handler for correct program behavior.
    """


def RTI():
    """
    Return from Interrupt (RTI) - Instruction
    -----------------------------------------
    Returns from an interrupt service routine (ISR), restoring the processor status and program counter.

    Usage:
    RTI

    Registers affected:
    - None

    Flags affected:
    - Processor Status (P): Restored from the stack.
    - Break (B): Cleared if set on the stack.
    - Unused (U): Cleared if set on the stack.

    Address modes supported:
    - Implied

    Notes:
    - Returns from an interrupt service routine (ISR), restoring the processor status and program counter.
    - Pulls the processor status (P) and program counter (PC) from the stack.
    - The processor status is restored along with its flags.
    - If the break (B) or unused (U) flags were set on the stack, they are cleared.
    - Execution continues from the address on the stack.
    - Caution: Ensure that the stack is correctly managed to avoid unexpected behavior.
    - Essential: Verify the correctness of the ISR and stack manipulation for correct program behavior.
    """


def NOP():
    """
    No Operation (NOP) - Instruction
    ---------------------------------
    Performs no operation and serves as a placeholder.

    Usage:
    NOP

    Registers affected:
    - None

    Flags affected:
    - None

    Address modes supported:
    - Implied

    Notes:
    - The NOP instruction performs no operation and serves as a placeholder in the code.
    - It does not affect any registers or flags.
    - This instruction is commonly used for padding, alignment, or delaying execution.
    - NOPs can be inserted for various reasons, such as to reserve space for future instructions or to maintain code structure.
    - While NOPs have no functional effect on the program, they can affect timing and synchronization in some cases.
    - Caution: Ensure that NOPs are used appropriately and do not interfere with the program logic.
    - Essential: Verify the necessity and placement of NOPs for the intended program behavior.
    """

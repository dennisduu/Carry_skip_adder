import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import random

@cocotb.test()
async def test_carry_skip_adder(dut):
    dut._log.info("Starting carry-skip adder test")

    # Set up the clock with a period of 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset the design
    dut.sum.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)  # Wait for 5 clock cycles with reset active
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)  # Wait for 5 clock cycles after releasing reset

    dut._log.info("Testing initial conditions")

    # Set the initial input values to test a basic addition
    dut.a.value = 5    # Example initial value for a
    dut.b.value = 3    # Example initial value for b

    # Wait for 20 clock cycles to see the output values
    await ClockCycles(dut.clk, 20)

    # Calculate and log the expected sum
    expected_sum = (5 + 3) & 0xF  # Sum is masked to 4 bits
    dut._log.info(f"Initial test: a=5, b=3, sum={dut.sum.value} (Expected: {expected_sum})")

    # Assert to check if the output matches the expected sum
    assert dut.sum.value == expected_sum, f"Initial test failed: expected sum={expected_sum}, got {dut.sum.value}"

    # Add 10 random test cases
    for i in range(10):
        # Generate random values for a and b within the 4-bit range (0 to 15)
        a = random.randint(0, 15)
        b = random.randint(0, 15)

        # Set the random input values
        dut.a.value = a
        dut.b.value = b

        # Wait for 20 clock cycles to settle
        await ClockCycles(dut.clk, 20)

        # Calculate the expected 4-bit sum
        expected_sum = (a + b) & 0xF  # Masking sum to 4 bits

        # Log the values for debugging
        dut._log.info(f"Test {i + 1}: a={a}, b={b}, sum={dut.sum.value} (Expected: {expected_sum})")

        # Assert to check if the output matches the expected values
        assert dut.sum.value == expected_sum, f"Test {i + 1} failed for a={a}, b={b}: expected sum={expected_sum}, got {dut.sum.value}"

    dut._log.info("All tests passed.")

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import random

@cocotb.test()
async def test_carry_skip_adder(dut):
    dut._log.info("Starting carry-skip adder test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("Testing initial conditions")

    # Set the initial input values to test a basic addition
    dut.a.value = 45   # Example initial value for a
    dut.b.value = 20   # Example initial value for b

    # Wait for 10 clock cycles to see the output values
    await ClockCycles(dut.clk, 10)

    # Calculate and log the expected sum
    expected_sum = (45 + 20) & 0xFF  # Sum is masked to 8 bits
    dut._log.info(f"Initial test: a=45, b=20, sum={dut.sum.value} (Expected: {expected_sum})")

    # Assert to check if the output matches the expected sum
    assert dut.sum.value == expected_sum, f"Initial test failed: expected sum={expected_sum}, got {dut.sum.value}"

    # Add 1000 random test cases
    for i in range(1000):
        # Generate random values for a and b within the 8-bit range
        a = random.randint(0, 255)
        b = random.randint(0, 255)

        # Set the random input values
        dut.a.value = a
        dut.b.value = b

        # Wait for 10 clock cycles to settle
        await ClockCycles(dut.clk, 10)

        # Calculate the expected 8-bit sum
        expected_sum = (a + b) & 0xFF  # Masking sum to 8 bits

        # Log the values for debugging
        dut._log.info(f"Test {i + 1}: a={a}, b={b}, sum={dut.sum.value} (Expected: {expected_sum})")

        # Assert to check if the output matches the expected values
        assert dut.sum.value == expected_sum, f"Test {i + 1} failed for a={a}, b={b}: expected sum={expected_sum}, got {dut.sum.value}"

    dut._log.info("All tests passed.")

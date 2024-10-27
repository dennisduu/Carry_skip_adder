import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import random

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)  # Reset for 10 clock cycles
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)   # Ensure release of reset

    dut._log.info("Starting random constrained tests")

    NUM_TESTS = 100  # Number of random tests to perform

    for _ in range(NUM_TESTS):
        # Generate random inputs such that their sum does not exceed 255 (no carry-out)
        while True:
            a = random.randint(0, 255)
            b = random.randint(0, 255)
            if a + b <= 255:
                break

        expected_sum = a + b

        # Apply inputs to the DUT
        dut.ui_in.value = a
        dut.uio_in.value = b

        # Wait for two clock cycles
        await ClockCycles(dut.clk, 2)

        # Read and check the output
        actual_output = int(dut.uo_out.value)
        assert actual_output == expected_sum, \
            f"For inputs {a} and {b}, expected {expected_sum} but got {actual_output}"

        dut._log.info(f"Test passed for inputs {a} and {b}, output {actual_output}")

    dut._log.info("All random constrained tests passed")

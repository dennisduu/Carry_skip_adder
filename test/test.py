import cocotb
import random

@cocotb.test()
async def test_carryskip_adder8(dut):
    # Initialize logging
    dut._log.info("Starting testbench for 8-bit Carry-Skip Adder (Combinational)")

    # Reset the DUT by setting `rst_n` low, then high
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await cocotb.triggers.Timer(1, units="ns")  # Small delay to apply reset
    dut.rst_n.value = 1
    await cocotb.triggers.Timer(1, units="ns")  # Small delay after reset release

    dut._log.info("Beginning randomized testing for combinational logic")

    NUM_TESTS = 100  # Number of random tests to perform

    for i in range(NUM_TESTS):
        # Generate random values for a and b such that their sum fits in 8 bits
        a = random.randint(0, 255)
        b = random.randint(0, 255)

        # Apply inputs to the DUT
        dut.ui_in.value = a
        dut.uio_in.value = b

        # Allow time for combinational logic to settle
        await cocotb.triggers.Timer(1, units="ns")  # Small delay for propagation

        # Expected output
        expected_sum = (a + b) & 0xFF  # Mask to 8-bit value

        # Check the output
        actual_output = int(dut.uo_out.value)
        assert actual_output == expected_sum, \
            f"Test failed for inputs a={a}, b={b}. Expected sum={expected_sum}, got {actual_output}"

        dut._log.info(f"Test {i+1}/{NUM_TESTS} passed for inputs a={a}, b={b}, output {actual_output}")

    dut._log.info("All randomized tests completed successfully")

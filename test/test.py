# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


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
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 20  # 20 in decimal
    dut.uio_in.value = 30  # 30 in decimal

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 1)

    # The following assertion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.uo_out.value == 50, f"Expected 50 but got {int(dut.uo_out.value)}"

    # Additional tests
    test_vectors = [
        (0, 0, 0),
        (1, 1, 2),
        (15, 15, 30),
        (127, 127, 254),
        (255, 255, 254),  # Since 255 + 255 = 510, but 8-bit sum results in 254 (overflow ignored)
    ]

    for a, b, expected_sum in test_vectors:
        dut.ui_in.value = a
        dut.uio_in.value = b
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == expected_sum, f"For inputs {a} and {b}, expected {expected_sum} but got {int(dut.uo_out.value)}"
        dut._log.info(f"Test passed for inputs {a} and {b}, output {int(dut.uo_out.value)}")

    dut._log.info("All tests passed")

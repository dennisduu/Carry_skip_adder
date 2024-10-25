/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0


`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule

 */


/*
 * Copyright (c) 2024 Weihua Xiao
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_carryskip_adder8 (
    input  wire [7:0] ui_in,    // a input
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // b input
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire [7:0] a, b;
    reg [7:0] sum;
    wire cin = 0; // Initial carry-in is 0

    assign a = ui_in;         // 'a' input from ui_in
    assign b = uio_in;        // 'b' input from uio_in

    // First 4-bit block (lower half)
    wire [3:0] sum_lower;
    wire c3; // Carry out from the lower block
    ripplemod ripple_lower (a[3:0], b[3:0], cin, sum_lower, c3);

    // Skip logic for lower 4-bit block
    wire p_lower = & (a[3:0] ^ b[3:0]); // Propagate signal for lower block

    // Second 4-bit block (upper half)
    wire [3:0] sum_upper;
    wire c7; // Carry out from the upper block
    wire skip_cin = p_lower ? c3 : cin; // Use skip logic for carry-in
    ripplemod ripple_upper (a[7:4], b[7:4], skip_cin, sum_upper, c7);

    // Register sum and apply reset logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            sum <= 8'b0;  // Reset sum to 0
        else
            sum <= {sum_upper, sum_lower};
    end

    assign uo_out = sum;      // Assign the sum to output
    assign uio_out = 8'b00000000;
    assign uio_oe = 8'b00000000;
endmodule

module ripplemod(a, b, cin, sum, cout);
    input [3:0] a, b;
    input cin;
    output [3:0] sum;
    output cout;

    wire [2:0] c;
    fulladd fa0(a[0], b[0], cin, sum[0], c[0]);
    fulladd fa1(a[1], b[1], c[0], sum[1], c[1]);
    fulladd fa2(a[2], b[2], c[1], sum[2], c[2]);
    fulladd fa3(a[3], b[3], c[2], sum[3], cout);
endmodule

module fulladd(a, b, cin, sum, cout);
    input a, b, cin;
    output sum, cout;

    assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (b & cin) | (a & cin);
endmodule

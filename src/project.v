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
    reg [7:0] sum;  // Declare sum as reg for procedural assignment
    wire cout0, cout1, skip;

    assign a = ui_in;
    assign b = uio_in;

    // First 4-bit RCA block
    RCA4 rca0 (.sum(sum[3:0]), .cout(cout0), .a(a[3:0]), .b(b[3:0]), .cin(1'b0));

    // Skip logic for carry-skip between 4-bit blocks
    SkipLogic skip0 (.cin_next(skip), .a(a[3:0]), .b(b[3:0]), .cin(1'b0), .cout(cout0));

    // Second 4-bit RCA block with carry-in from skip logic
    RCA4 rca1 (.sum(sum[7:4]), .cout(cout1), .a(a[7:4]), .b(b[7:4]), .cin(skip));

    // Register sum and apply reset logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            sum <= 8'b0;  // Reset sum to 0
        else
            sum <= {sum[7:4], sum[3:0]};
    end

    assign uo_out = sum;        // Assign sum to output
    assign uio_out = 8'b00000000;
    assign uio_oe = 8'b00000000;

endmodule

// Ripple Carry Adder - 4 bits
module RCA4(output wire [3:0] sum, output wire cout, input wire [3:0] a, b, input wire cin);

    wire [2:0] c;  // Internal carry wires

    fulladd fa0 (.sum(sum[0]), .cout(c[0]), .a(a[0]), .b(b[0]), .cin(cin));
    fulladd fa1 (.sum(sum[1]), .cout(c[1]), .a(a[1]), .b(b[1]), .cin(c[0]));
    fulladd fa2 (.sum(sum[2]), .cout(c[2]), .a(a[2]), .b(b[2]), .cin(c[1]));
    fulladd fa3 (.sum(sum[3]), .cout(cout), .a(a[3]), .b(b[3]), .cin(c[2]));

endmodule


// Skip Logic for carry-skip between blocks
module SkipLogic(output wire cin_next, input wire [3:0] a, b, input wire cin, cout);

    wire p0, p1, p2, p3, P, e;  // Declare internal wires explicitly
    
    or (p0, a[0], b[0]);
    or (p1, a[1], b[1]);
    or (p2, a[2], b[2]);
    or (p3, a[3], b[3]);

    and (P, p0, p1, p2, p3);
    and (e, P, cin);
    
    or (cin_next, e, cout);

endmodule


module fulladd(output wire sum, output wire cout, input wire a, b, cin);

    assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (b & cin) | (a & cin);

endmodule

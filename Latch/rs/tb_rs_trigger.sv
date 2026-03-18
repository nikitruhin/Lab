module rs_trigger (
    input  logic S, R,
    output logic Q, Qn
);
    assign Q  = ~(S & Qn);
    assign Qn = ~(R & Q);
endmodule

module tb_rs_trigger;
    logic S, R, Q, Qn;
    
    rs_trigger dut (.*);
    
    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, tb_rs_trigger);
        
        // t0: S=0, R=1  -> Q=1, Qn=0
        #10 S=0; R=1;
        #10 S=1; R=0;
        #10 S=1; R=1;
        #10 S=0; R=1;
        #10 S=1; R=1;
        #10 S=1; R=0;
        #10 S=1; R=0;
        
        #20 $finish;
    end
    
    // Печать значений для проверки
    always @(S or R or Q or Qn) begin
        $display("Time=%0t: S=%b R=%b | Q=%b Qn=%b", $time, S, R, Q, Qn);
    end
endmodule
module d_latch (
    input  logic d,
    input  logic en,
    output logic q,
    output logic qn
);
    always_latch begin
        if (en) q = d;
    end
    
    assign qn = ~q;
endmodule
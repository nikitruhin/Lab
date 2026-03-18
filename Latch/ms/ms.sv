module ms_rs_trigger (
    input  logic C,   // Тактовый сигнал
    input  logic S,   // Установка
    input  logic R,   // Сброс
    output logic Q,   // Прямой выход
    output logic Qn   // Инверсный выход
);
    
    logic U, D;       // Внутренние сигналы (выходы Master)
    logic Cn;         // Инвертированный тактовый
    
    assign Cn = ~C;
    
    // Master (ведущий) — работает по прямому C
    rs_trigger master (
        .C  (C),
        .S  (S),
        .R  (R),
        .Q  (U),
        .Qn (D)
    );
    
    // Slave (ведомый) — работает по инверсному C
    rs_trigger slave (
        .C  (Cn),
        .S  (U),
        .R  (D),
        .Q  (Q),
        .Qn (Qn)
    );
    
endmodule

// Базовый синхронный RS-триггер
module rs_trigger (
    input  logic C,
    input  logic S,
    input  logic R,
    output logic Q,
    output logic Qn
);
    always @(posedge C) begin
        if (S && !R) begin
            Q <= 1;
            Qn <= 0;
        end
        else if (!S && R) begin
            Q <= 0;
            Qn <= 1;
        end
        // При S=1,R=1 или S=0,R=0 — храним состояние
    end
endmodule
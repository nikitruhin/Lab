module testbench;
    logic d;
    logic en;
    logic q;
    logic qn;
    
    d_latch uut (
        .d(d),
        .en(en),
        .q(q),
        .qn(qn)
    );
    
    // Генерируем понятные сигналы
    initial begin
        // Начальные значения
        d = 0;
        en = 0;
        
        // Даем время на инициализацию
        #10;
        
        // Тест 1: en=0, d меняется - q не должен меняться
        d = 1;  #20;
        d = 0;  #20;
        
        // Тест 2: включаем en, теперь q должен следить за d
        en = 1; #10;
        d = 1;  #20;
        d = 0;  #20;
        d = 1;  #20;
        
        // Тест 3: выключаем en, q должен запомнить последнее значение
        en = 0; #10;
        d = 0;  #30;
        d = 1;  #30;
        
        // Тест 4: снова включаем en
        en = 1; #10;
        d = 0;  #20;
        d = 1;  #20;
        
        #50 $finish;
    end
    
    // Запись
    initial begin
        $dumpfile("d_latch.vcd");
        $dumpvars(0, testbench);
    end
    
endmodule
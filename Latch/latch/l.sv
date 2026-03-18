module d_latch ( input d, // 1-битный входной контакт для данных  
input en, // 1-битный входной контакт для включения триггера  
input rstn, // 1-битный входной контакт для сброса по активному низкому уровню  
output reg q); // 1-битный выходной контакт для вывода данных  
  
   // Этот блок always срабатывает при каждом изменении значений en/rstn/d  
   // Если сигнал сброса активен, то на выходе будет ноль   
   // В противном случае, пока активен сигнал enable, на выходе q будет значение, соответствующее входному сигналу d  
  
always @ (en or rstn or d)
      if (!rstn)
q <= 0;
      else  
         if (en)
q <= d;
endmodule

module tb_latch;
   // Declare variables that can be used to drive values to the design  
reg d;
reg en;
reg rstn;
reg [2:0] delay;
reg [1:0] delay2;
integer i;
  
   // Instantiate design and connect design ports with TB signals  
d_latch dl0 ( .d (d),
.en (en),
.rstn (rstn),
.q (q));
  
   // This initial block forms the stimulus to test the design  
initial begin
$monitor ("[%0t] en=%0b d=%0b q=%0b", $time, en, d, q);
  
      // 1. Initialize testbench variables  
d <= 0;
en <= 0;
rstn <= 0;
  
      // 2. Release reset  
#10 rstn <= 1;
  
      // 3. Randomly change d and enable  
      for (i = 0; i < 5; i=i+1) begin
delay = $random;
delay2 = $random;
#(delay2) en <= ~en;
#(delay) d <= i;
end
end
endmodule
float FastInvSqrt(float x) {
    float xhalf = 0.5f * x;                    
    
    int i = *(int*)&x;                         
    i = 0x5f3759df - (i >> 1);                 
    
    x = *(float*)&i;                            
    x = x * (1.5f - xhalf * x * x);              
    
    return x;
}


int main() {
    float result = FastInvSqrt(3.14159f);       
    return (int)(result * 1000);                 
}
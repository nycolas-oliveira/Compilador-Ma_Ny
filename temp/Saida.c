#include <stdio.h>
int main(void){
float v1;
float v2;
float resultado;
float resultado2;
printf("===>TESTE 4<===\n");
printf("->Somando e dividindo dois valores\n");
v1 = 0;
v2 = 0;
printf("Entre com os valores:\n");
if(0 == scanf("%f", &v1)) {
v1 = 0;
scanf("%*s");
}
if(0 == scanf("%f", &v2)) {
v2 = 0;
scanf("%*s");
}
resultado = v1+v2;
resultado2 = v1/v2;
printf("O resultado da soma e:\n");
printf("%.2f\n", (float)(resultado));
printf("O resultado da divisao e:\n");
printf("%.2f\n", (float)(resultado2));
return 0;
}

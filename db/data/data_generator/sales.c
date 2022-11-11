#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "faker.c"

// srand(time(NULL));


int main() {
   int num;
   FILE *fptr;

   srand(time(NULL));

   // use appropriate location if you are using MacOS or Linux
   fptr = fopen("/Users/mazen/data_gen/sales.csv","w");

   if(fptr == NULL)
   {
      printf("Error!");   
      exit(1);             
   }
   int r = rand() % 2000000;
   int num_sales = 750000;
   if (r > num_sales) {
       num_sales = 2000000;
   }
   for(int i = 0; i < num_sales; i++) {
       //['buyer_id','order_number', 'product_id', 'seller_id', 'quantity', 'price','sell_date','sell_time', 'fullfill_date'])
       int buyer_id = rand() % 9685;
       int order_num = i;
       int prod_id = rand() % 3876;
       int seller_id = rand() % 9685;
       int quantity = rand() % 500;
       int price = 29;
       char year[5];
        sprintf(year, "%d%d%d%d", 2,0,2,rand()%3); 
       char month[4];
        sprintf(month, "%d",rand()%12); 
       char day[3];
        sprintf(day, "%d",rand()%30); 
       char sell_date[9];
       for(int j = 0; j < 8; j++) {
           if (j < 4) {
                sell_date[j] = year[j];
           } else if(j < 6) {
                sell_date[j] = month[j - 4];
           } else {
               sell_date[j] = day[j - 6];
           }
       }
       char time[] = {'0','9',':','0','0'};
       int r = rand();
       fprintf(fptr,"%d^%d^%d^%d^%d^%d^%s^%s^%s\n",buyer_id,order_num,prod_id,seller_id,quantity,price,sell_date,time,sell_date);
   }
   fclose(fptr);

   return 0;
}
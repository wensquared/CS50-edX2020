#include<stdio.h>
#include<cs50.h>
#include<math.h>

int change_owed(void);


int main(void)
{
    int n = change_owed();
    
    int coins = 0;  //how many coins in return
    
    while (n > 0)
    {
        
        if (n >= 25)
        { 
            //check how many 25 cents coins
            coins = coins + (n / 25);
            n = n % 25;
        }
        else if (n < 25 && n >= 10 && n > 5)
        { 
            //check how many 10 cents coins
            coins = coins + (n / 10);
            n = n % 10;
        }
        else if (n < 25 && n < 10 && n > 1)
        { 
            //check how many 5 cents coins
            coins = coins + (n / 5);
            n = n % 5;
        }
        else
        { 
            //check how many 1 cents coins
            coins += n;
            n = n % 1;
        }
    }
    
    printf("%i \n", coins);
}



int change_owed(void)
{
    float c;
    int cents; 
    
    do
    {
        c = get_float("Changed owed:"); //var for getting the change
    }
    while (c < 0);
    
    cents = round(c * 100);
    
    return cents;
    
}
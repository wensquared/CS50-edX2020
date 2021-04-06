#include<stdio.h>
#include<cs50.h>

int get_height(void);

int main(void)
{
    int h = get_height();
    int k = h;
    string s = "#";
    string d = " ";
    
    int i, j, g; 
    for (i = 1; i <= h; i++)
    {
        for (g = 1; g < k; g++)
        {
            printf("%s", d);
        }
        for (j = 1; j <= i; j++)
        {
            printf("%s", s);
        }
        printf("\n");
        k--;
    }
}

int get_height(void)
{
    int h;
    do
    {
        h = get_int("%s", "Please type a number between 1 and 8: ");
    }
    while (h < 1 || h > 8);
    return h;
}
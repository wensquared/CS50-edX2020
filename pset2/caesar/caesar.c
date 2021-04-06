#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
#include<cs50.h>
#include<string.h>

void caesar_alg(string s, int k, int l);

int main(int argc, string argv[])
{
    
    string pt = NULL;
    int k = 0;  //key
    int l = 0;  //length of argv
    int ptl = 0; //length of plaintext
    
    //checking for valid key
    
    if (argc >= 3 || argc <= 1)
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }
    else
    {
        l = strlen(argv[1]);
        string s = argv[1];
        int temp = 0;
        
        for (int i = 0; i < l; i++)
        {
            if (isdigit(s[i]) == false)
            {
                temp++;
            }
        }
        
        if (temp >= 1)
        {
            printf("Usage: ./caesar key \n");
            return 1;
        }
        else
        {
            k = atoi(s);
        }
    }
    
    pt = get_string("plaintext: ");
    ptl = strlen(pt);
    caesar_alg(pt, k, ptl);
    
}

void caesar_alg(string s, int k, int l)
{
    string ct = s;  //ciphertext
    char temp;
    //checking for each char if it is a letter, and if so if it is an uppercase or lowercase, then convert else leave it be
    for (int i = 0; i < l; i++)
    {
        if (isalpha(s[i]))
        {
            if (isupper(s[i]))
            {
                temp = s[i] - 65;
                ct[i] = ((temp + k) % 26) + 65;
            }
            else
            {
                temp = (s[i]) - 97;
                ct[i] = ((temp + k) % 26) + 97;
            }
        }
        else
        {
            ct[i] = s[i];
        }
    }
    
    printf("ciphertext: %s\n", ct);
}
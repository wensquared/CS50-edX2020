#include<stdio.h>
#include<cs50.h>
#include<math.h>
#include<ctype.h>
#include<string.h>


string get_text(void);
void cole_liau_index(float l, float s);

int main(void)
{
    string text = get_text();
    int ls = strlen(text); //length of the string
    int abc = 0; //counter for letters
    int words = 1; // counter for words
    int sent = 0; //counter for sentences
    char space = ' ';
    float l, s; 
    
    for (int i = 0; i < ls; i++)
    {
        if (isalpha(text[i]))  //checking if alphabet
        {
            abc++;
        }
        else if (text[i] == space) //checking words
        {
            words++;
        }
        else if (text[i] == 63 || text[i] == 46 || text[i] == 33) //checking sentences
        {
            sent++;
        }
    }
    
    l = ((float) abc / (float) words) * 100;
    s = ((float) sent / (float) words) * 100;
    
    cole_liau_index(l, s);  //the coleman-liau index

}


string get_text(void)
{
    return get_string("Text:");
}

void cole_liau_index(float l, float s)
{
    
    float j = (0.0588 * l) - (0.296 * s) - 15.8;
    int i = round(j);
    if (i < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (i >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", i);
    }
}


// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"

#include<stdio.h>
#include<string.h>
#include<strings.h>
#include<stdlib.h>
#include<ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 65536;

// Hash table
node *table[N];

unsigned int hash_index;
unsigned int word_count = 0;


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    int l = strlen(word);
    char tmpw[l + 1];
    tmpw[l] = '\0';
    
    for (int i = 0; i < l; i++)
    {
        tmpw[i] = tolower(word[i]);
    }
    
    int check_index = hash(word);
    
    node *cursor = table[check_index];
    
    
    while (cursor != NULL)
    {
        if (strcasecmp(tmpw, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    
    unsigned int hash = 0;
    for (int i=0, n=strlen(word); i<n; i++)
    {
        hash = (hash << 2) ^ word[i];
    }
        
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    
    FILE *file = fopen(dictionary,"r");
    char word[LENGTH + 1]; 
    
    if (file == NULL)
    {
        return false;
    }
    
    
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        
        if (n == NULL)
        {
            return false;
        }
        
        strcpy(n->word, word);
        n->next = NULL;
        hash_index = hash(word);
        
        n->next = table[hash_index];
        table[hash_index] = n;
        
        word_count++;
        
    }
    
    fclose(file);
    return true;
    
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for(int i=0;i<N;i++) 
   {
       node *tmp1=table[i]; 
       while(tmp1!=NULL) 
       {
            node *tmp2 = tmp1; 
            tmp1 = tmp1 -> next; 
            free(tmp2);
       }
   }

    return true;
}

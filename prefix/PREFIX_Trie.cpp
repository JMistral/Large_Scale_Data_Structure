//
//  PREFIX_Trie.cpp
//  
//
//  Created by Jiaming CHEN on 4/5/17.
//
//

#include "PREFIX_Trie.hpp"
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#define MAXIMUM 5
using namespace std;

int value(char g){
    if (g == 'A'){
        return 0;
    }
    else if (g == 'C'){
        return 1;
    }
    else if (g == 'G'){
        return 2;
    }
    else{
        return 3;
    }
}

struct TrieNode{
    TrieNode *Children[4];
    bool isEnd;
};

class Trie
{
public:
    TrieNode *root;
    Trie()
    {
        root = new TrieNode;
    }
    ~Trie()
    {
        TrieNode *temp;
        temp = root;
        
        
        for(int i=0;i<4;++i)
        {
            if(temp->Children[i]!=NULL)
            {
                delete(temp->Children[i]);
            }
        }
        delete(temp);
    }
    
    void insert(char *read,int n)
    {
        TrieNode *p = root;
        for(int i = 0; i < n; ++ i)
        {
            if(p -> Children[value(read[i])] == NULL){
                p -> Children[value(read[i])] = new TrieNode;
            }
            p = p -> Children[value(read[i])];
        }
        p -> isEnd = true;
    }
    
    bool search(char *key,int n)
    {
        TrieNode *p = find(key,n);
        return p != NULL && p -> isEnd;
    }
    
private:
    TrieNode* find(char *key,int n)
    {
        TrieNode *p = root;
        for(int i = 0; i < n && p != NULL; ++ i)
            p = p -> Children[value(key[i])];
        return p;
    }
};

int main()
{
    char **Head = (char**)malloc(MAXIMUM*sizeof(char*));
    for(int i=0;i<MAXIMUM;i++){
        Head[i] = (char*)malloc(5*sizeof(char));
    }
    Head[0][0] = 'A';
    Head[0][1] = 'C';
    Head[0][2] = 'T';
    Head[0][3] = 'G';
    Head[0][4] = 'A';
    Trie trie;
    trie.insert(Head[0],5);
    //   trie.insert("ACTGT");
    //   trie.insert("ACTGG");
    //   trie.insert("ACTTA");
    //   trie.insert("ACTCC");
    if(trie.search(Head[0],5))
    {
        cout<<"Found"<<endl;
    }
    return 0;
}

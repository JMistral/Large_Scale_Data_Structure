//
//  main.cpp
//  prefix_trie
//
//  Created by Jiaming CHEN on 4/4/17.
//  Copyright © 2017 Jiaming CHEN. All rights reserved.
//

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
using namespace std;

struct Node{
    Node *A;
    Node *C;
    Node *G;
    Node *T;
    bool isEnd;
};

int main() {
    head = new Node();
    head->isEnd = false;
    
    return 0;
}

//
//  prefix.hpp
//  prefix_trie
//
//  Created by Jiaming CHEN on 4/4/17.
//  Copyright © 2017 Jiaming CHEN. All rights reserved.
//

#ifndef prefix_hpp
#define prefix_hpp
#include <stdio.h>

#endif /* prefix_hpp */
#ifndef NODE_H
#define NODE_H

#include <iostream>

using namespace std;

class Node {
public:
    static int noOfNodes;
    int suffixNode;
    
    Node () :
    suffixNode(-1) {};
    
    ~Node() {
        //  cout << "destroying node " << id << endl;
        
    }
};
#endif

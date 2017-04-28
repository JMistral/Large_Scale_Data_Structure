//
//  main.c
//  hw2
//
//  Created by Jiaming CHEN on 2/15/17.
//  Copyright © 2017 Jiaming CHEN. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>
#define MAXIMUM 100000
#define LENGTH 16
#define SIZE 5000


struct node
{
    char gene[LENGTH];
    struct node *link;
};

int empty(struct node *head)
{
	int k = 0;
	if(head == NULL){
		k = 1;
	}
	return k;
}

void chaining(struct node **ptr_to_head, struct node *new_node)
{
	int counter = 0;//counting the length of this list
	struct node **next;
	if ((*ptr_to_head)->link == NULL){
		(*ptr_to_head)->link = new_node;
	}
	else{
		next = ptr_to_head;
		//moving the pointer to the end of the linked-list
		while((*next)->link != NULL){
			next = &((*next)->link);
			counter++;
		}
		(*next)->link = new_node;
	}
	printf("it's the %d th node on this chain \n",counter);
	return;
	
}

double radix(char *read)
{
	int i;
	double sum = 0;
	double base = 0;
	for(i = 1;i<=LENGTH;i++){
		base = pow(4,LENGTH-i);
		switch(read[i-1]) {
			case 'A' :
				sum = sum+0*base;
				break;
			case 'C' :
				sum = sum+1*base;
				break;
			case 'G' :
				sum = sum+2*base;
				break;
			case 'T' :
				sum = sum+3*base;
				break;
		}
	}
	return sum;
}

void division_hash(struct node **ptr_to_head,char **Head)
{
	int i;
	// remember to set r and hk to zero everytime
	double r=0;;
	int hk=0;
	printf("start hashing \n");
	
	for(i=0;i<MAXIMUM;i++){
		r = radix(Head[i]);
		hk = (int)fmod(r,SIZE);
		printf("radix value = %lf, hashed value = %d ",r,hk);
		struct node *seq = (struct node *)malloc(sizeof(struct node));
		strcpy(seq->gene,Head[i]);
		seq->link = NULL;
		chaining(&(ptr_to_head[hk]), seq);
		r = 0;hk = 0;
	}
	return;
}

void print_chain(struct node *head)
{
	struct node *next;
	if(head->link==NULL) printf("Empty list \n");
	else
	{
		next = head->link;
		while (next->link != NULL){
			printf("%s \n",next->gene);
			next = next->link;
		}
		printf("%s \n",next->gene);
	}
	
	return;
}


int main() {
    double randNum;
    int i,j,t;//i is the counter for sequences; j is the counter for characters; t is the index of pointers in the hash table
    char **Head = (char**)malloc(MAXIMUM*sizeof(char*));// data array
    struct node **ptr_to_head = (struct node **)malloc(SIZE*sizeof(struct node*));//hashed table head
    
    time_t tm;
    // initialize the seed
    srand((unsigned) time(&tm));
    // randomly generate MAXIMUM sequences of LENGTH genome
    for(i=0;i<MAXIMUM;i++){
        Head[i] = (char*)malloc(LENGTH*sizeof(char));
        for(j=0;j<LENGTH;j++){
            randNum = (double)rand() / (double)((unsigned)RAND_MAX + 1); // generate a number between 0 and 1
            //printf("rand# %f",randNum);
            if (randNum<=0.25) {
                Head[i][j] = 'A';
            }
            else if (randNum>0.25 && randNum<=0.5){
                Head[i][j] = 'C';
            }
            else if (randNum>0.5 && randNum<=0.75){
                Head[i][j] = 'G';
            }
            else{
                Head[i][j] = 'T';
            }
            //printf("char = %c \n",Head[i][j]);
        }
    }
    //allocate the array of pointers
    for(t=0;t<SIZE;t++)
    {
        ptr_to_head[t] = (struct node *)malloc(sizeof(struct node));
        ptr_to_head[t]->link = NULL;
    }
    
    division_hash(ptr_to_head,Head);
    print_chain(ptr_to_head[4353]);
    
    return 0;
}

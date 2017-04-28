#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>
#define LENGTH 16

void All(char **Head,int n)
{
	//knowing that the size of Head is 4^n
	unsigned long ind,num;
	char alphabet[4] = {'A','C','G','T'};
	int ii;
	int digit;
	ind = 0; num = 0;
	while(ind<(pow(4,n))){		
		Head[ind] = (char*)malloc(n*sizeof(char));
		num = ind;
		for(digit=0;digit<n;digit++){
			ii = (int)fmod(num,4);
			printf("ii = %d ",ii); 
			Head[ind][n-digit-1] = alphabet[ii];
			printf("[%lu][%d]: %c \n",ind,n-digit-1, Head[ind][n-digit-1]); 
			num = num/4;
		}
		ii = 0;	
		ind++;
	}
	
	return;
	
}

void print_array(char **Head,int n,unsigned long maxi){
	unsigned long i;
	int ii;
	for(i=0;i<maxi;i++){
    	for(ii = 0;ii<n;ii++){
            printf("%c", Head[i][ii]);       
        }
        printf("  end of read \n");
	}
	return;
}


void direct_hash(char *bit_array,char *read,int n){
	int i;
	unsigned long sum,base;
	sum = 0;
	for(i=0;i<n;i++){
		base = pow(4,n-i-1);
		switch(read[i]) {
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
	printf("\n index: %lu",sum);
	unsigned long chunk = sum/8;
	printf(" chunk: %lu",chunk);
	int precise;
	if(chunk==0){
		precise=sum;
	}
	else{
		precise = (int)fmod(sum,chunk*8);
	}
	printf("\n precise: %d",precise);
	int temp;
	temp = (int)bit_array[chunk];
	temp = temp+pow(2,precise);
	printf("\n temp: %d \n",temp);
	bit_array[chunk] =  (char)temp;
	
}

int main()
{
	// LENGTH is the length of sequences. So we have 4^LENGTH possibillities of sequences
	unsigned long NumP = pow(4,LENGTH);
	// allocate memory for all these sequences
	char **Head = (char**)malloc(NumP*sizeof(char*));
	//create the base array
	double base[LENGTH];
	int r;
	for(r=1;r<=LENGTH;r++){
		base[r-1] = pow(4,(LENGTH-r));
	}
	//generate all possible sequences of size LENGTH
	All(Head,LENGTH);
	print_array(Head,LENGTH,NumP);
	
	// bit array initialisation
	unsigned long i,index;
	unsigned long array_size = NumP/8;
	char *bit_array = (char*)malloc(array_size*sizeof(char));
	for(i=0;i<array_size;i++)
    {
        bit_array[i] = NULL;
        //it's 0 in ASCII table.......
        //but it doesn't really print out
    }
    direct_hash(bit_array,Head[60],LENGTH);
    for(i=0;i<array_size;i++)
    {
        printf(" %d ",(int)bit_array[i]);
    }

	
	return 0;
}

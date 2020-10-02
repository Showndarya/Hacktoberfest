#include<iostream>
using namespace std;

unsigned long fact(int n){ //this function returns the factorial os a number ex 3!=3*2*1=>6.
	if(n==0)             
		return 1;
	return n*fact(n-1);
   }
int charless(int lim,int* arra){//this will return count the number of characters less the then the given char lexicograpically.
	int i=0,count=0; //lim has the lexico graphical index of the character.& arra is array having counts of characters.
	for(i=0;i<lim;i++){
		if(arra[i]==1)
		   ++count;
		   }
    return count;
		
}
int findRank(string s){
	int arra[26];
	int i=0,l=s.length(),k=0,j=0;
	unsigned long res=0;
	for(i=0;i<26;i++)
		arra[i]=0;
	for(i=0;i<l;i++)
		++arra[s[i]-97];
	for(i=0;i<l;i++){  // terminating condition.
		if(arra[s[i]-97]>1)
			return 0;
		}
	for(i=0;i<l;i++){
		k=charless(s[i]-97,arra);//finding the number of char less then the lexicographical char s[i].
		res=res+k*fact(l-1-i);// number of possible characters.
		--arra[s[i]-97];
		}
		j=(res+1)%1000000007;
		return j;
		
		
	}
int main(){
	int T;
	cin>>T;
	while(T--){
		string s;
		cin>>s;
		cout<<findRank(s);
		}
	return 0;
	}

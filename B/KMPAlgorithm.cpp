#include<iostream>
#include<string>
using namespace std;
int lps(string s){       //Algo to find the longest properpreffixsuffix example aba=1
		int l=s.length();
		int k=1,c=0;
		for(int i=0;i<l&&k<l;i++){
			if(s.substr(0,k)==s.substr(l-i-1,k))
				c=k;
			++k;
			}
		//cout<<c;
		return c;
		
		}
void KMPAlgorithm(string pat,string txt){
	int N=txt.length();
	int M=pat.length();
	int arrlps[M];
	int i=0,j=0;
	for(int k=0;k<M;++k)
		arrlps[k]=lps(pat.substr(0,k+1));
	/*for(int k=0;k<M;++k)
		cout<<arrlps[k];*/
	while(i<N){
		if(pat[i]==txt[j]){
			++i;
			++j;
			}
		if(j==M){
			cout<<(i-j);
			j=arrlps[j-1];
			}
		else{
			if(i<N && pat[i]!=txt[j]){
				if(j==0)
					++i;
				else
					j=arrlps[j-1];
					}
			}
		}
	}
int main(){
	int T;
	cin>>T;
	while(T--){
		string txt,pat;
		cin>>txt>>pat;
		KMPAlgorithm(pat,txt);
		}
	
	return 0;
	}	
	

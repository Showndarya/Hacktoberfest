#include<iostream>
#include<cstdio>
#include<cstring>
#include<cmath>
#include<cstdlib>
#include<algorithm>
#include<vector>
#include<set>
#include<map>
#include<utility>
#include<queue>
#include<numeric>
#define llu long long
#define inf 0x3f3f3f3f
#define pb push_back
#define mp make_pair
#define ipair pair<llu,llu>
#define inp(a) scanf("%lld",&a)
#define out(a) printf("%lld\n",a)
#define allv(a) a.begin(),a.end()
#define alla(a,n) a,a+n
#define fi(i,a,b) for(llu i=a;i<b;i++)
#define N 100000
#define m(a,b) (a>b? b : a)
#define M(a,b) (a>b? a : b)
#define mod 1000000007
using namespace std;
 
int main()
{
    llu i,j,k,l,e,n,m,t,f,c;
    inp(t);
    vector< vector<llu> > mp;
    set<llu> se;
    vector<llu> setsz;
    vector<llu> temp;
    vector<llu>::iterator it;
    while(t--)
    {
        setsz.clear();
        temp.clear();
        mp.clear();
        se.clear();
        inp(n);inp(k);
        c=0;
        llu s=0;
        fi(i,0,n)
        {
            inp(m);
            setsz.pb(m);
            fi(j,0,m)
            {
                inp(e);
                se.insert(e);
                temp.pb(e);
            }
            sort(temp.begin(),temp.end());
            mp.push_back(temp);
            temp.clear();
        }
        if(se.size()<k)
        {
            printf("0\n");
            continue;
        }
 
        //Logic
        vector<llu> te(2505);
        fi(i,0,n)
        {
            if(setsz[i]==k)
            {
                c+=(n-i-1);
                continue;
            }
            fi(j,i+1,n)
            {
                if(setsz[j]==k)
                {
                    c++;
                    continue;
                }
                it=set_union(mp[i].begin(),mp[i].end(),mp[j].begin(),mp[j].end(),te.begin());
                llu sz=it-te.begin();
                if(sz==k)
                    c++;
                te.clear();
            }
        }
        out(c);
    }
    return 0;
}

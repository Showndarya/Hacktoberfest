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
#define alla(a) a,a+n
#define N 100000
#define fi(i,a,b) for(llu i=a;i<b;i++)
#define m(a,b) (a>b? b : a)
#define M(a,b) (a>b? a : b)
#define mod 1000000007
using namespace std;

int main()
{
    llu i,j,k,l,e,n,m,t,f,c;
    inp(t);
    while(t--)
    {
        inp(n);inp(m);
        llu a[n],sum[n+1];
        fi(i,0,n) 
            inp(a[i]);
        sort(alla(a));
        sum[0]=0;
        fi(i,1,n+1)
            sum[i]=sum[i-1]+a[i-1];
        fi(i,0,m)
        {
            inp(k);
            llu in=(lower_bound(alla(a),k)-a);
            l=0;
            llu r=in;
            while(l<r)
            {
                llu e=(l+r)/2;
                c=sum[in]-sum[e];
                c=(in-e)*k-c;
                if(e<c)
                    l=e+1;
                else
                    r=e;
            }
            out(n-l);
        }
    }
    return 0;
}





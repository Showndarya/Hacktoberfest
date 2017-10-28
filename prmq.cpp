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
#define N 1000001
#define m(a,b) (a>b? b : a)
#define M(a,b) (a>b? a : b)
#define mod 1000000007
using namespace std;

vector<llu> segtree[400010];
vector<llu> prime[100010];

void build(llu l,llu r,llu node)
{
    if(l>r)
        return;
    if(l==r)
    {
        segtree[node]=prime[l];
        return;
    }
    llu m=(l+r)/2;
    build(l,m,2*node+1);
    build(m+1,r,2*node+2);
    merge(segtree[2*node+1].begin(),segtree[2*node+1].end(),segtree[2*node+2].begin(),segtree[2*node+2].end(),back_inserter(segtree[node]));
}

llu query(llu ss,llu se,llu qs,llu qe,llu x,llu y,llu node)
{
    if(se<qs || ss>qe)
        return 0;
    if(qs<=ss && qe>=se)
        return (upper_bound(segtree[node].begin(),segtree[node].end(),y)-lower_bound(segtree[node].begin(),segtree[node].end(),x));
    llu m=(ss+se)/2;
    return (query(ss,m,qs,qe,x,y,2*node+1)+query(m+1,se,qs,qe,x,y,2*node+2));
}

int main()
{
    llu i,j,k,l,e,n,m,t,f,c,x,y,r;
    inp(n);
    fi(i,0,n)
    {
        inp(e);
        while(e%2==0)
        {
            prime[i].pb(2);
            e/=2;
        }
        for(j=3;j<=sqrt(e);j=j+2)
        {
            while(e%j==0)
            {
                prime[i].pb(j);
                e/=j;
            }
        }
        if(e>2)
            prime[i].pb(e);
    }
    build(0,n-1,0);
    inp(m);
    fi(i,0,m)
    {
        inp(l);inp(r);inp(x);inp(y);
        e=query(0,n-1,l-1,r-1,x,y,0);
        out(e);
    }
    return 0;
}


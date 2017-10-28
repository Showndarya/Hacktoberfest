#include<iostream>
#include<vector>
#include<cstdio>
#include<algorithm>
#include<map>
#include<cstring>
#include<set>
#include<queue>
#include<climits>
using namespace std;
#define llu long long int
#define M(a,b) (a>b ? a : b)
#define m(a,b) (a>b ? b : a)
#define it(a)  ::iterator a
#define slld(a) llu a;scanf("%lld",&a)
#define ss(a) scanf("%s",a)
#define plld(a) printf("%lld",a)
#define MAX 10000
#define MOD 1000000007
#define powOf2(a) !(a&a-1)
#define mod(a) (a>0 ? a : (-1*a))
#define tc(a) llu a; for(scanf("%lld",&a);a--;)
#define swap(a,b) a = a^b; b = a^b;a = a^b;
#define pii pair<llu,llu>
#define INF LLONG_MAX
vector<llu> shortestpath(vector< pair<llu,llu> > adj[],llu s,llu n){
    bool vis[n];
	fill_n(vis,n,false);
    vector< llu> dist(n,INF);
    set< pii > pq;
    pq.insert(make_pair(0,s));
        dist[s] = 0;
        while(!pq.empty()){
            llu u = (pq.begin()->second);
            pq.erase(pq.begin());
            if(vis[u]) 
                continue;
            vis[u] = true;
            vector< pii > ::iterator it;
            for(it = adj[u].begin();it!=adj[u].end();it++){
                llu v = it->first;
                llu w = it->second;
                
                if(dist[v] > dist[u]+w){
                    dist[v] = dist[u] + w;
                    //cout<<v<<" : "<<dist[v]<<endl;
                    pq.insert(make_pair(dist[v],v));
                }
            }
        }
        return dist;
}
int main(){
    llu t,i,j,m,n,k,s,x;
    scanf("%lld",&t);
    while(t--)
    {
        cin>>n>>k>>x>>m>>s;
        vector< pair<llu,llu> > adj[n]; 
        s--;
        if(s<k){
            for(llu i = 0;i<k;i++){
                   adj[s].push_back(make_pair(i,x));
                   adj[i].push_back(make_pair(s,x));
            }
        }
        llu a,b,c;
        for(llu i = 0;i<m;i++){
            cin>>a>>b>>c;
            a--;
            b--;
            adj[a].push_back(make_pair(b,c));
            adj[b].push_back(make_pair(a,c));
        }
        vector<llu> dist = shortestpath(adj,s,n);
        
        if(s>=k){
            llu mi  = 0;
            for(llu i = 1; i < k; i++){
                if(dist[i] < dist[mi]) 
                    mi = i;              
            }
            for(llu i = 0;i<k;i++){
                if(mi == i) 
                    continue;
                adj[mi].push_back(make_pair(i,x));
                adj[i].push_back(make_pair(mi,x));
                
            }
           dist = shortestpath(adj,s,n);
        }
        for(llu i = 0;i<n;i++){
            printf("%lld ",dist[i]);
        }
        printf("\n");
        
    }
	return 0;
}

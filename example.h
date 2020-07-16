/* File : example.h */

#include <vector>
#include <utility>
#include <string>
#include <map>
#include <algorithm>
#include <functional>
#include <numeric>
using namespace std;

double average(std::vector<int> v) {
    return std::accumulate(v.begin(),v.end(),0.0)/v.size();
}

vector<double> half(const vector<double>& v) {
    vector<double> w(v);
    for (unsigned int i=0; i<w.size(); i++)
        w[i] /= 2.0;
    return w;
}

void halve_in_place(vector<double>& v) {
    transform(v.begin(),v.end(),v.begin(),
                   bind2nd(divides<double>(),2.0));
}

vector<pair<double,vector<int>>> get_top_k(int num_nodes,map<string,int> &edge_map,vector<vector<int>> &adjList){
    vector<pair<double,vector<int>>> x;
    for(auto a:adjList){
        int sum=0;
        vector<int> ss;
        for(auto b:a){
            sum+=b;    
            ss.push_back(b);
        }
        x.push_back({sum,ss});
    }
    // x.push_back({2.5,{1,2,3}});
    return x;
}

vector<pair<int,int>> gp(int a,int b)
{
    vector<pair<int,int>> aa;
    aa.push_back({a,b});
    aa.push_back({a,b});
    aa.push_back({a,b});
    return aa;
}

int gm(map<string,int> mp,string s)
{
    return mp[s];
}
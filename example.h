/* File : example.h */

#include <iostream>
#include <vector>
#include <utility>
#include <string>
#include <map>
#include <algorithm>
#include <functional>
#include <numeric>
#include <deque>
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

vector<vector<int>> get_top_k2(int num_nodes,map<string,double> edge_map,vector<vector<int>> adjList,int num,vector<double> weights)
{
    vector<vector<pair<double,pair<int,int>>>> dp(num_nodes);
    vector<int> indegree(num_nodes,0);
    deque<int> dq;
    for(int i=0;i<num_nodes;i++)
    {
        for(auto neighbor:adjList[i]){
            indegree[neighbor]++;
        }
    }

    dp[0].push_back({0,{-1,-1}});
    dq.push_back(0);

    while (!dq.empty())
    {
        int vertex = dq.front();
        // cout<<vertex<<" ";
        dq.pop_front();
        for(auto neigh:adjList[vertex]){
            int cnt=0;
            for(auto val:dp[vertex]){
                double new_val = val.first + weights[edge_map[to_string(vertex)+":"+to_string(neigh)]];
                int counter = 0;
                pair<double,pair<int,int>> temp = {new_val,{vertex,cnt}};
                while (counter<dp[neigh].size())
                {
                    if(dp[neigh][counter].first<new_val){
                        temp=dp[neigh][counter];
                        dp[neigh][counter] = {new_val,{vertex,cnt}};
                        while (counter+1<dp[neigh].size() && counter<num-1)
                        {
                            swap(dp[neigh][counter+1],temp);
                            counter++;
                        }
                        break;
                    }   
                    counter++;
                }
                if(dp[neigh].size()<num)
                    dp[neigh].push_back(temp);
                cnt++;
            }
            indegree[neigh]--;
            if(indegree[neigh]==0)
                dq.push_back(neigh);
        }
    }

        // cout<<"ok\n";
    vector<vector<int>> paths;
    for(int i=0;i<dp[num_nodes-1].size();i++)
    {
        // cout<<"ok\n";
        int nxt = num_nodes-1;
        vector<int> path;
        pair<double,pair<int,int>> curr = dp[num_nodes-1][i];
        // cout<<curr.first<<'\n';
        while (curr.second.second!=-1)
        {
            path.push_back(edge_map[to_string(curr.second.first)+":"+to_string(nxt)]);
            nxt = curr.second.first;
            curr = dp[curr.second.first][curr.second.second];
        }
        paths.push_back(path);
    }    

    return paths;
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
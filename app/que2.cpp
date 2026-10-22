#include <iostream>
#include <vector>
#include<unordered_map>
#include<algorithm>

using namespace std;

vector<int> solve(vector<int>& nums) {
int j=0;
int n=nums.size();
for(int i=0;i<n;i++){
    if(nums[i]!=0){
        swap(nums[i],nums[j]);
        j++;
    }
}
    return nums;
}
vector<vector<int>> solve1(vector<int>&nums){
     int sum=0;
       int equalSum=sum;
        int len=0;
        // unordered_set<int>mp;
       unordered_map<int,vector<int>>mp;
    int start=0;
      int left=0;
      for(int right=0;right<nums.size();right++){
        sum+=nums[right];
        len++;

        if(len==2){
            if(mp.count(sum)){
                
            }
         else { 
            mp[sum].push_back({})
           sum-=nums[left++];
           len--;
           }
        }

      }
      
    
}

int main() {
    vector<int> nums= {2,2,3,1};
   // vector<int>ans=solve(nums);
    // for(int i=0;i<ans.size();i++){
       
    //     cout<<ans[i];
    //      if(i!=nums.size()-1){
    //         cout<<",";


    //     }
    // }
  
    return 0;
}
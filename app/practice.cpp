#include <iostream>
#include <vector>
#include<algorithm>

using namespace std;

vector<int> solve(vector<int>& nums1,vector<int>&nums2) {

    int m = nums1.size();
    int n=nums2.size();
    int i=m-1;
    int j=n-1;
    while(j>0){
        nums1[i]=nums2[j];
        j--;
        i--;
    }
    return nums1;
    
}

int main() {
    vector<int> nums1= {1,2,3,0,0,0};
    vector<int> nums2={2,5,6};
    vector<int>ans=solve(nums1,nums2);
    for(int i=0;i<nums1.size();i++){
        cout<<nums1[i];
    }
    return 0;
}
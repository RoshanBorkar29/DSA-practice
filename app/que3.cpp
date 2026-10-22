#include <iostream>
#include <vector>
#include<stack>
using namespace std;
vector<int> dailyTemperatures(vector<int>& temperatures) {

    stack<int> st;

    vector<int> ans(temperatures.size(), 0);

    for(int i = 0; i < temperatures.size(); i++) {

        while(!st.empty() &&
              temperatures[st.top()] < temperatures[i]) {

            int ind = st.top();
            st.pop();

            ans[ind] = i - ind;
        }

        st.push(i);
    }

    return ans;
}

int main() {

    vector<int> temperatures = {
        73, 74, 75, 71, 69, 72, 76, 73
    };

    vector<int> ans = dailyTemperatures(temperatures);

    for (int x : ans) {
        cout << x << " ";
    }

    cout << endl;

    return 0;
}
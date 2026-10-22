#include <iostream>
#include <vector>
using namespace std;

int subsetSum(vector<int>& arr, int n) {
    if (n <= 0) return 0;

    int totalSum = 0;
    for (int i = 0; i < n; i++) {
        totalSum += arr[i];
    }

    int target = totalSum / 2;
    vector<vector<bool>> dp(n, vector<bool>(target + 1, false));

    dp[0][0] = true;
    if (arr[0] <= target) {
        dp[0][arr[0]] = true;
    }

    for (int i = 1; i < n; i++) {
        for (int sum = 0; sum <= target; sum++) {
            bool notTake = dp[i - 1][sum];
            bool take = false;

            if (arr[i] <= sum) {
                take = dp[i - 1][sum - arr[i]];
            }

            dp[i][sum] = notTake || take;
        }
    }

    int minDiff = 1e9;
    for (int sum = 0; sum <= target; sum++) {
        if (dp[n - 1][sum]) {
            minDiff = min(minDiff, abs(totalSum - 2 * sum));
        }
    }

    return minDiff;
}

int main() {
    int n;
    cout << "Enter number of elements: ";
    cin >> n;

    if (n <= 0) {
        cout << "No elements to process." << endl;
        return 0;
    }

    vector<int> arr(n);
    cout << "Enter the elements: ";
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    int result = subsetSum(arr, n);
    cout << "Minimum difference between two subset sums is: " << result << endl;

    return 0;
}
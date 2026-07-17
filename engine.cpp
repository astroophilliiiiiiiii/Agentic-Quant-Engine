#include <iostream>
#include <vector>
#include <sstream>
#include <string>
#include <algorithm>

using namespace std;


int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Error: No price data provided." << endl;
        return 1;
    }

    vector<double> prices;
    stringstream ss(argv[1]);
    string item;
    

    while (getline(ss, item, ',')) {
        prices.push_back(stod(item));
    }

    if (prices.empty()) {
        cout << "0.0" << endl;
        return 0;
    }

    double max_price = prices[0];
    double max_drawdown = 0.0;

    for (int i = 1; i < prices.size(); i++) {
        if (prices[i] > max_price) {
            max_price = prices[i];
        }
        double drawdown = (max_price - prices[i]) / max_price;
        if (drawdown > max_drawdown) {
            max_drawdown = drawdown;
        }
    }

    cout << (max_drawdown * 100.0) << endl;
    return 0;
}
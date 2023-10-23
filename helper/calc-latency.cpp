#include <bits/stdc++.h>
using namespace std;
map<string,vector<int>> st;
int main(){
	char op[100];
	int l;
	while(scanf("%s%d", op, &l)==2){
		st[op].push_back(l);
	}
	for (auto& a : st) {
		sort(a.second.begin(), a.second.end());
		int A = max(size_t(1), a.second.size() / 10000);
		printf("%s ", a.first.c_str());
		for (int k = 0; k < a.second.size(); k += A) {
			printf("%d ", a.second[k]);
		}
		printf("%d\n", a.second.back());
	}
}

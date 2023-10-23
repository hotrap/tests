#include <bits/stdc++.h>
using namespace std;

double process(std::string dirname, std::string opname, double frac) {
  std::filesystem::path p(dirname);
  std::ifstream in(p / "latency_result");
  if (!in || frac < 0 || frac > 1) return -1;
  while (!in.eof()) {
    std::string s;
    getline(in, s);
    std::stringstream ss(s);
    std::string op;
    ss >> op;
    // cerr << op;
    if (op == opname) {
      std::vector<double> latencies;
      while(!ss.eof()) {
        double a;
        ss >> a;
        // cerr << a << ", ";
        latencies.push_back(a);
      }
      cerr << latencies.size();
      if (latencies.size() < 1000) return -1;
      return latencies[size_t(latencies.size() * frac)] / 1e9;
    }
  }
  return -1;
}

int main(int argc, char** argv) {
  if (argc < 4) return 0;
  std::string opname = (argv[1]);
  auto r = std::stod(argv[2]);
  for (int i = 3; i < argc; i++) {
    cout << argv[i] << "\t" << process(argv[i], opname, r) << "\n";
  }
}
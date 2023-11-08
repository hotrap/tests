#include <bits/stdc++.h>
using namespace std;

double process(std::string dirname) {
  std::filesystem::path p(dirname);
  std::ifstream in(p / "mem");
  if (!in) return -1;
  double max_mem = 0;
  while (!in.eof()) {
    std::string s;
    getline(in, s);
    if (s == "") continue;
    std::stringstream ss(s);
    long long time = 0;
    double mem = 0;
    ss >> time >> mem;
    /*if (s.find("CST") != std::string::npos) {
      getline(in, s);
      if (s.find("total") != std::string::npos) {
        std::stringstream ss(s);
        std::string a;
        ss >> a; // total
        ss >> a; // kB
        double total;
        ss >> total;
        max_mem = std::max(max_mem, total);
      } else {
        std::cerr << "Current Max Memory: " << max_mem << std::endl;
        return -1;
      }
    }*/
    max_mem = std::max(max_mem, mem);
  }
  return max_mem;
}

int main(int argc, char** argv) {
  if (argc < 2) return 0;
  for (int i = 1; i < argc; i++) {
    cout << argv[i] << "\t" << process(argv[i]) << "\n";
  }
}

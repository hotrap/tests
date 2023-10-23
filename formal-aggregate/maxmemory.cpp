#include <bits/stdc++.h>
using namespace std;

double process(std::string dirname) {
  std::filesystem::path p(dirname);
  std::ifstream in(p / "memory.sh.txt");
  if (!in) return -1;
  double max_mem = 0;
  while (!in.eof()) {
    std::string s;
    getline(in, s);
    if (s == "") continue;
    if (s.find("CST") != std::string::npos) {
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
    }
  }
  return max_mem;
}

int main(int argc, char** argv) {
  if (argc < 4) return 0;
  for (int i = 3; i < argc; i++) {
    cout << argv[i] << "\t" << process(argv[i]) << "\n";
  }
}
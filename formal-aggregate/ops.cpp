#include <bits/stdc++.h>
using namespace std;



double process(std::string dirname, auto l, auto r) {
  std::filesystem::path p(dirname);
  std::ifstream in(p / "progress");
  if (!in) return -1;
  size_t ltime = 0, rtime = 0, lop = 0, rop = 0;
  while (!in.eof()) {
    std::string s;
    getline(in, s);
    std::stringstream ss(s);
    size_t timestamp, op;
    if(ss >> timestamp >> op) {
      if (op >= r) {
        rop = op;
        rtime = timestamp;
        break;
      } else if (op >= l && !ltime) {
        lop = op;
        ltime = timestamp;
      }
    } else {
      // cout << s;
    }
  }
  return (rop - lop) / (double)(rtime - ltime) * 1e9;
}

int main(int argc, char** argv) {
  if (argc < 4) return 0;
  auto l = std::stoull(argv[1]);
  auto r = std::stoull(argv[2]);
  for (int i = 3; i < argc; i++) {
    cout << argv[i] << "\t" << process(argv[i], l, r) << "\n";
  }
}
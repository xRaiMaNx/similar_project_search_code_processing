#include <iostream>
#include <algorithm>
#include <thread>

struct MyStruct {
  int x;
}

struct ShPtr {
};

class SomeAbstractCLass {
};

class SomeCrazyClass {
  SomeCrazyClass() { std::cout << "kek\n"; }
}

void MyGreatFunc(int x) {
    x = 1;
}

auto TransformTuple(auto t) {
    return t;
}

int sum(int x, int y) {
    return x + y;
}

int main() {
  int x;
  SomeCrazyClass scc;
  MyStruct s;
}
//
// Created by Tom on 09/03/2023.
//

#ifndef TYPON_SYS_HPP
#define TYPON_SYS_HPP

#include "builtins.hpp"
#include <iostream>

namespace py_sys {
template <typename _Unused = void>
struct sys__oo : referencemodel::moduletype<sys__oo<>> {
  static constexpr auto &stdin = std::cin;
  static constexpr auto &stdout = std::cout;
  static constexpr auto &stderr = std::cerr;
  typon::TyList__oo<>::Obj<typon::TyStr__oo<>::Obj> argv;

  /*FUNCTION(void, exit, (int code), { std::exit(code); })*/

  struct : referencemodel::function {
    typon::TyNone operator()(int code) const { std::exit(code); }
  } static constexpr exit{};
};
sys__oo<> all;
} // namespace py_sys

#endif // TYPON_SYS_HPP

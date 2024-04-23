//
// Created by Tom on 09/03/2023.
//

#ifndef TYPON_TIME_HPP
#define TYPON_TIME_HPP

#include "builtins.hpp"
#include <iostream>

namespace py_time {
template <typename _Unused = void>
struct time__oo : referencemodel::moduletype<time__oo<>> {
  /*FUNCTION(void, exit, (int code), { std::exit(code); })*/

  struct : referencemodel::function {
    typon::Task<typon::TyNone> operator()(auto duration) const {
      co_await typon::io::sleep(std::chrono::seconds(duration));
      co_return None;
    }
  } static constexpr sleep{};
};
time__oo<> all;
} // namespace py_time

#endif // TYPON_TIME_HPP

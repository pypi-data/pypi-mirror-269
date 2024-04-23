#ifndef TYPON_TYPON_HPP
#define TYPON_TYPON_HPP

#include "builtins.hpp"

namespace py_typon {
template <typename _Unused = void>
struct typon__oo : referencemodel::moduletype<typon__oo<>> {

struct : referencemodel::function {
    auto operator()() const {
      return typon::TyBool(true);
    }
  } static constexpr is_cpp{};

};
typon__oo<> all;
} // namespace py_typon

#endif //TYPON_TYPON_HPP
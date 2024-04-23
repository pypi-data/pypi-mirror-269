//
// Created by Tom on 08/03/2023.
//

#ifndef TYPON_BOOL_HPP
#define TYPON_BOOL_HPP

#include <ostream>

#include "../referencemodel.hpp"
#include "str.hpp"

namespace typon {
using namespace referencemodel;
template <typename _Base0 = object>
struct TyBool__oo : classtype<_Base0, TyBool__oo<>> {
  static constexpr std::string_view name = "TyBool";

  struct : method {
    auto operator()(auto self) const {
      return TyStr(self->value ? "True" : "False");
    }
  } static constexpr oo__str__oo{};

  static constexpr auto oo__repr__oo = oo__str__oo;
  struct Obj : value<TyBool__oo<>, Obj> {
    bool value;

    constexpr Obj(bool value = false) : value(value) {}
    constexpr operator bool() const { return value; }
  };

  /*static constexpr Obj TRUE = Obj(true);
    static constexpr Obj FALSE = Obj(false);*/

  auto operator()(bool value) const { return Obj(value); }
};
static constexpr TyBool__oo<> TyBool{};

} // namespace typon

#endif // TYPON_BOOL_HPP

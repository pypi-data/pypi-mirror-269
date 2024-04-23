//
// Created by Tom on 13/06/2023.
//

#ifndef TYPON_BYTES_H
#define TYPON_BYTES_H

#include "str.hpp"

/*class TyStr;

class TyBytes : public std::string {
public:
  TyBytes() : std::string() {}
  TyBytes(const char *s) : std::string(s) {}
  TyBytes(const std::string &s) : std::string(s) {}
  TyBytes(std::string &&s) : std::string(std::move(s)) {}
  TyBytes(size_t count, char ch) : std::string(count, ch) {}

  template <class InputIterator>
  TyBytes(InputIterator first, InputIterator last) : std::string(first, last) {}

  // TyStr decode_inner(const std::string &encoding = "utf-8") const;

  METHOD(TyStr, decode, (Self self, const std::string &encoding = "utf-8"), ;)
};*/

namespace typon {
using namespace referencemodel;
template <typename _Base0 = object>
struct TyBytes__oo : classtype<_Base0, TyBytes__oo<>> {
  static constexpr std::string_view name = "TyBytes";

  struct : method {
    auto operator()(auto self, auto other) const {
      return Obj(dot(self, value) + dot(other, value));
    }
  } static constexpr oo__add__oo{};

  struct : method {
    auto operator()(auto self, auto encoding) const {
      return typon::TyStr(dot(self, value));
    }
  } static constexpr decode{};

  struct Obj : value<TyBytes__oo<>, Obj> {
    std::string value;

    constexpr Obj() : value() {}
    constexpr Obj(std::string value) : value(value) {}
    operator std::string() const { return value; }
  };

  auto operator()(std::string value) const { return Obj(value); }
};
static constexpr TyBytes__oo<> TyBytes{};

} // namespace typon

#endif // TYPON_BYTES_H

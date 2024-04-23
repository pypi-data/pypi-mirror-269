//
// Created by Tom on 18/08/2023.
//

#ifndef TYPON_EXCEPTION_HPP
#define TYPON_EXCEPTION_HPP

#include "str.hpp"

struct TyException_s {
  struct py_type {
    TyStr__oo<>::Obj message;
  };

  auto operator()(const TyStr__oo<>::Obj &message) const {
    return py_type{message};
  }
};

namespace typon {
using TyException = TyObj<TyException_s>;
}

#endif // TYPON_EXCEPTION_HPP

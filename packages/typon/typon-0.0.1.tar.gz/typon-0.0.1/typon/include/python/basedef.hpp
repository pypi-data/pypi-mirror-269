//
// Created by Tom on 24/03/2023.
//

#ifndef TYPON_BASEDEF_HPP
#define TYPON_BASEDEF_HPP

template <typename Self> class TyBuiltin {
  template <typename... Args> auto sync_wrapper(Args &&...args) {
    return static_cast<Self *>(this)->sync(std::forward<Args>(args)...);
  }

public:
  template <typename... Args>
  auto operator()(Args &&...args)
      -> decltype(sync_wrapper(std::forward<Args>(args)...)) {
    return sync_wrapper(std::forward<Args>(args)...);
  }
};

/*
struct method {};

template <typename Func, typename Self>
struct boundmethod {
  [[no_unique_address]] Func func;
  Self self;

  boundmethod(Func func, Self self) : func(func), self(self) {}

  template <typename... Args>
  auto operator()(Args &&... args) const {
    return func(self, std::forward<Args>(args)...);
  }
};


template <typename Obj, std::derived_from<method> Attr>
auto dot_bind(Obj obj, Attr attr) {
  return boundmethod(attr, obj);
}

template <typename Obj, typename Attr>
  requires (! std::derived_from<Attr, method>)
auto dot_bind(Obj, Attr attr) {
  return attr;
}

#define dot(OBJ, NAME) [](auto && obj) -> auto { return dot_bind(obj, obj.NAME);
}(OBJ) #define dotp(OBJ, NAME) [](auto && obj) -> auto { return dot_bind(obj,
obj->NAME); }(OBJ) #define dots(OBJ, NAME) [](auto && obj) -> auto { return
std::remove_reference<decltype(obj)>::type::py_type::NAME; }(OBJ)

*/

#include "referencemodel.hpp"

#endif // TYPON_BASEDEF_HPP

#ifndef TYPON_SCOPE_HPP_INCLUDED
#define TYPON_SCOPE_HPP_INCLUDED

#include <concepts>


namespace typon
{

  template <std::invocable<> F>
  struct Defer
  {
    F _f;

    ~Defer()
    {
      _f();
    }
  };

  template <std::invocable<> F>
  Defer(F) -> Defer<F>;

}


#endif // TYPON_SCOPE_HPP_INCLUDED

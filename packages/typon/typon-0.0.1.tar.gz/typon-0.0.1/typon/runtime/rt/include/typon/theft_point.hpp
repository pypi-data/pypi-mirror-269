#ifndef TYPON_THEFT_POINT_HPP_INCLUDED
#define TYPON_THEFT_POINT_HPP_INCLUDED

#include <coroutine>


namespace typon
{

  struct TheftPoint
  {
    virtual std::coroutine_handle<> steal() noexcept = 0;
  };

}


#endif // TYPON_THEFT_POINT_HPP_INCLUDED

#ifndef TYPON_RING_HPP_INCLUDED
#define TYPON_RING_HPP_INCLUDED

#include <atomic>
#include <cstdint>
#include <type_traits>


namespace typon
{

  template <typename I>
    requires std::is_unsigned_v<I>
  struct Ring
  {
    const I _mask;

    Ring(std::uint_least8_t bits) noexcept
      : _mask((I(1) << bits) - 1)
    {}

    I size() noexcept
    {
      return _mask + 1;
    }

    friend I operator % (I x, Ring ring) noexcept
    {
      return x & ring._mask;
    }
  };

}


#endif //  TYPON_RING_HPP_INCLUDED

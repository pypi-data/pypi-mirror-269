#ifndef TYPON_SYSCALL_COMPLETION_HPP_INCLUDED
#define TYPON_SYSCALL_COMPLETION_HPP_INCLUDED

#include <cstdint>

#include <typon/stack.hpp>


namespace typon
{

  struct SyscallCompletion
  {
    using u32 = std::uint_fast32_t;

    Stack * _stack;
    u32 _result;
  };

}


#endif // TYPON_SYSCALL_COMPLETION_HPP_INCLUDED

#ifndef TYPON_RANDOM_HPP_INCLUDED
#define TYPON_RANDOM_HPP_INCLUDED

#include <random>


namespace typon::random
{

  static thread_local std::mt19937 random { std::random_device{}() };

  static thread_local std::mt19937_64 random64 { std::random_device{}() };

}


#endif // TYPON_RANDOM_HPP_INCLUDED

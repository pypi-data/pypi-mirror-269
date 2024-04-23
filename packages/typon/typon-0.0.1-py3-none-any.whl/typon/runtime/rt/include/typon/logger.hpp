#ifndef TYPON_LOGGER_HPP_INCLUDED
#define TYPON_LOGGER_HPP_INCLUDED

#include <cstdio>

#include <typon/scheduler.hpp>


#define LOG(fmt, ...) \
  printf( "[%2u] " fmt "\n", Scheduler::thread_id __VA_OPT__(,) __VA_ARGS__)


#endif // TYPON_LOGGER_HPP_INCLUDED

#ifndef TYPON_TYPON_HPP_INCLUDED
#define TYPON_TYPON_HPP_INCLUDED

#include <utility>

#include <typon/fork.hpp>
#include <typon/forked.hpp>
#include <typon/future.hpp>
#include <typon/io.hpp>
#include <typon/join.hpp>
#include <typon/meta.hpp>
#include <typon/mutex.hpp>
#include <typon/promise.hpp>
#include <typon/root.hpp>
#include <typon/task.hpp>


namespace typon
{

  template <typename Task>
  Fork<typename Task::promise_type::value_type> fork(Task task)
  {
    // Put the task in a local variable to ensure its destructor will
    // be called on co_return instead of only on coroutine destruction.
    Task local_task = std::move(task);
    co_return co_await std::move(local_task);
  }

  template <typename Task>
  Fork<void> fork(Task task, meta::Empty)
  {
    // Put the task in a local variable to ensure its destructor will
    // be called on co_return instead of only on coroutine destruction.
    Task local_task = std::move(task);
    co_await std::move(local_task);
  }

  template <typename Task>
  Fork<void> fork(Task task, typename Task::promise_type::value_type & into)
  {
    // Put the task in a local variable to ensure its destructor will
    // be called on co_return instead of only on coroutine destruction.
    Task local_task = std::move(task);
    // The caller is responsible for garanteeing that the lifetime of
    // referenced object will always encompass the lifetime of the fork.
    into = co_await std::move(local_task);
  }

  template <typename Task>
  Future<typename Task::promise_type::value_type> future(Task task)
  {
    // Put the task in a local variable to ensure its destructor will
    // be called on co_return instead of only on coroutine destruction.
    Task local_task = std::move(task);
    co_return co_await std::move(local_task);
  }

}


#endif // TYPON_TYPON_HPP_INCLUDED

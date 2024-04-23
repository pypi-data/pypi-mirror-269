//
// Created by Tom on 04/07/2023.
//

#ifndef TYPON_OS_HPP
#define TYPON_OS_HPP

#include "builtins.hpp"
#include <dirent.h>
#include <string.h>
#include <sys/sysmacros.h>
#include <unistd.h>

#undef st_atime
#undef st_mtime
#undef st_ctime

int no_special(const struct dirent *d) {
  return strcmp(d->d_name, ".") && strcmp(d->d_name, "..");
}

namespace py_os {
struct os_t {
  FUNCTION(auto, fsdecode, (std::string s), { return s; })

  struct Stat_Result_s {
    struct py_type {
      int st_mode;
      unsigned long long st_ino;
      dev_t st_dev;
      unsigned int st_nlink;
      unsigned int st_uid;
      unsigned int st_gid;
      unsigned long long st_size;
      double st_atime;
      double st_mtime;
      double st_ctime;
      unsigned long long st_blocks;
      unsigned int st_blksize;
      dev_t st_rdev;
      int st_gen;
      double st_birthtime;
    };
  } Stat_Result;

  struct DirEntry_s {
    struct py_type {
      TyStr name;
      TyStr path;
    };
  } DirEntry;

  struct _Scandiriterator_s {
    struct py_type {
      using value_type = TyObj<DirEntry_s>;
      using reference = TyObj<DirEntry_s>;

      METHOD(auto, py_enter, (Self self), { return self; })
      METHOD(void, py_exit, (Self self), {
        if (self->namelist) {
          free(self->namelist);
        }
      })

      METHOD(auto, begin, (Self self), { return *self; })
      METHOD(auto, end, (Self self), {
        return py_type(self->basepath, self->namelist, self->n, self->n);
      })

      auto operator*() {
        auto name = TyStr(this->namelist[this->current]->d_name);
        return pyobj_agg<DirEntry_s>(name, this->basepath + name);
      }

      py_type(const TyStr &basepath, struct dirent **namelist, int n,
              int current = 0)
          : basepath(basepath), namelist(namelist), n(n), current(current) {
        if (this->basepath[this->basepath.size() - 1] != '/') {
          this->basepath += '/';
        }
      }

      py_type() {}

      bool operator!=(const py_type &other) {
        return this->current != other.current;
      }

      void operator++() { this->current++; }

      TyStr basepath;
      struct dirent **namelist;
      int n;
      int current;
    };
  } _Scandiriterator;

  FUNCTION(typon::Task<TyObj<Stat_Result_s>>, stat, (const TyStr &path), {
    const char *path_c = path.c_str();
    struct statx statxbuf;
    if (int err = co_await typon::io::statx(AT_FDCWD, path_c, 0, STATX_SIZE,
                                            &statxbuf)) {
      system_error(-err, "statx()");
    }
    co_return TyObj<Stat_Result_s>(new Stat_Result_s::py_type{
        statxbuf.stx_mode, statxbuf.stx_ino,
        makedev(statxbuf.stx_dev_major, statxbuf.stx_dev_minor),
        statxbuf.stx_nlink, statxbuf.stx_uid, statxbuf.stx_gid,
        statxbuf.stx_size,
        statxbuf.stx_atime.tv_sec + statxbuf.stx_atime.tv_nsec / 1e9f,
        statxbuf.stx_mtime.tv_sec + statxbuf.stx_mtime.tv_nsec / 1e9f,
        statxbuf.stx_ctime.tv_sec + statxbuf.stx_ctime.tv_nsec / 1e9f,
        statxbuf.stx_blocks, statxbuf.stx_blksize,
        makedev(statxbuf.stx_rdev_major, statxbuf.stx_rdev_minor), 0,
        statxbuf.stx_btime.tv_sec + statxbuf.stx_btime.tv_nsec / 1e9});
  })

  FUNCTION(TyObj<_Scandiriterator_s>, scandir, (const TyStr &path), {
    const char *path_c = path.c_str();
    struct dirent **namelist;
    int n = ::scandir(path_c, &namelist, no_special, alphasort);
    if (n < 0) {
      system_error(-n, "scandir()");
    }
    return tyObj<_Scandiriterator_s>(path, namelist, n);
  });

  FUNCTION(TyStr, readlink, (const TyStr &path), {
    const char *path_c = path.c_str();
    char buf[PATH_MAX];
    ssize_t nbytes = ::readlink(path_c, buf, sizeof(buf));
    if (nbytes < 0) {
      system_error(-nbytes, "readlink()");
    }
    return TyStr(buf, nbytes);
  })
} all;

auto &get_all() { return all; }
} // namespace py_os

namespace typon {
using PyStat_Result = TyObj<py_os::os_t::Stat_Result_s>;
using Py_Scandiriterator = TyObj<py_os::os_t::_Scandiriterator_s>;
} // namespace typon

#endif // TYPON_OS_HPP

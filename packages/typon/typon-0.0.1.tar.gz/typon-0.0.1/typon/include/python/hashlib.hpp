//
// Created by Tom on 04/07/2023.
//

#ifndef TYPON_HASHLIB_HPP
#define TYPON_HASHLIB_HPP

#include "builtins.hpp"

#include <openssl/md5.h>
#include <openssl/sha.h>

// TODO: consider using EVP https://stackoverflow.com/a/40155962/2196124
namespace py_hashlib {
struct hashlib_t {

  typedef int (*openssl_init)(void *context);
  typedef int (*openssl_update)(void *context, const void *data,
                                unsigned long len);
  typedef int (*openssl_final)(unsigned char *md, void *context);

  struct _Hash_s {
    struct py_type {

      py_type(TyObj<void> context, openssl_update update, openssl_final final,
              int diglen)
          : _context(context), _update(update), _final(final), _diglen(diglen) {
      }

      py_type() {}

      py_type(const py_type &other)
          : _context(other._context), _update(other._update),
            _final(other._final), _diglen(other._diglen) {}

      TyObj<void> _context;
      openssl_update _update;
      openssl_final _final;
      int _diglen;

      METHOD(int, update, (Self self, std::string val), {
        return self->_update(self->_context.get(), &val[0], val.size());
      })

      METHOD(std::string, hexdigest, (Self self), {
        auto resbuf = new unsigned char[self->_diglen];
        self->_final(resbuf, self->_context.get());
        std::string hexres;
        hexres.resize(self->_diglen * 2);
        for (int i = 0; i < self->_diglen; i++) {
          sprintf(&hexres[i * 2], "%02x", resbuf[i]);
        }
        delete[] resbuf;
        return hexres;
      })
    };
  } _Hash;

  FUNCTION(auto, md5, (), {
    auto ctx = tyObj<MD5_CTX>();
    MD5_Init(ctx.get());
    return tyObj<_Hash_s>(ctx, (openssl_update)MD5_Update,
                          (openssl_final)MD5_Final, MD5_DIGEST_LENGTH);
  })

  FUNCTION(auto, sha1, (), {
    auto ctx = tyObj<SHA_CTX>();
    SHA1_Init(ctx.get());
    return tyObj<_Hash_s>(ctx, (openssl_update)SHA1_Update,
                          (openssl_final)SHA1_Final, SHA_DIGEST_LENGTH);
  })

  FUNCTION(auto, sha256, (), {
    auto ctx = tyObj<SHA256_CTX>();
    SHA256_Init(ctx.get());
    return tyObj<_Hash_s>(ctx, (openssl_update)SHA256_Update,
                          (openssl_final)SHA256_Final, SHA256_DIGEST_LENGTH);
  })

  FUNCTION(auto, sha512, (), {
    auto ctx = tyObj<SHA512_CTX>();
    SHA512_Init(ctx.get());
    return tyObj<_Hash_s>(ctx, (openssl_update)SHA512_Update,
                          (openssl_final)SHA512_Final, SHA512_DIGEST_LENGTH);
  })

} all;

auto &get_all() { return all; }
} // namespace py_hashlib

namespace typon {
using Py_Hash = TyObj<py_hashlib::hashlib_t::_Hash_s>;
}

#endif // TYPON_HASHLIB_HPP

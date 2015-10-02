#!/usr/bin/env python

import os
from cffi import FFI

COMPILE = True
CORE_DIR = os.path.abspath(os.path.dirname(__file__))

headerFile = []
with open(os.path.join(CORE_DIR, 'include', 'wrappers', 'matrix.h')) as f:
    for line in f.readlines():
        ls = line.strip()
        if not ls.startswith('#') and not ls.startswith('extern') and \
                not ls.startswith('}') and ls:
            headerFile.append(ls)
with open(os.path.join(CORE_DIR, 'include', 'wrappers', 'vector.h')) as f:
    for line in f.readlines():
        ls = line.strip()
        if not ls.startswith('#') and not ls.startswith('extern') and \
                not ls.startswith('}') and ls:
            headerFile.append(ls)
headerFile = "\n".join(headerFile)

ffi = FFI()

if COMPILE:
    ffi.set_source(
        "core", """
            // Nothing
            #include "wrapper.h"
        """,
        libraries=['game_core'],
        library_dirs=[os.path.join(CORE_DIR, 'build')],
        include_dirs=[os.path.join(CORE_DIR, 'include')]
    )

ffi.cdef(headerFile)

if not COMPILE:
    lib = ffi.dlopen(os.path.join(CORE_DIR, 'build', 'libgame_core.so'))


if __name__ == '__main__':
    if COMPILE:
        ffi.compile()

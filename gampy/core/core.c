#define _CFFI_
#include <Python.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <stddef.h>

/* See doc/misc/parse_c_type.rst in the source of CFFI for more information */

typedef void *_cffi_opcode_t;

#define _CFFI_OP(opcode, arg)   (_cffi_opcode_t)(opcode | (((uintptr_t)(arg)) << 8))
#define _CFFI_GETOP(cffi_opcode)    ((unsigned char)(uintptr_t)cffi_opcode)
#define _CFFI_GETARG(cffi_opcode)   (((uintptr_t)cffi_opcode) >> 8)

#define _CFFI_OP_PRIMITIVE       1
#define _CFFI_OP_POINTER         3
#define _CFFI_OP_ARRAY           5
#define _CFFI_OP_OPEN_ARRAY      7
#define _CFFI_OP_STRUCT_UNION    9
#define _CFFI_OP_ENUM           11
#define _CFFI_OP_FUNCTION       13
#define _CFFI_OP_FUNCTION_END   15
#define _CFFI_OP_NOOP           17
#define _CFFI_OP_BITFIELD       19
#define _CFFI_OP_TYPENAME       21
#define _CFFI_OP_CPYTHON_BLTN_V 23   // varargs
#define _CFFI_OP_CPYTHON_BLTN_N 25   // noargs
#define _CFFI_OP_CPYTHON_BLTN_O 27   // O  (i.e. a single arg)
#define _CFFI_OP_CONSTANT       29
#define _CFFI_OP_CONSTANT_INT   31
#define _CFFI_OP_GLOBAL_VAR     33
#define _CFFI_OP_DLOPEN_FUNC    35
#define _CFFI_OP_DLOPEN_CONST   37
#define _CFFI_OP_GLOBAL_VAR_F   39

#define _CFFI_PRIM_VOID          0
#define _CFFI_PRIM_BOOL          1
#define _CFFI_PRIM_CHAR          2
#define _CFFI_PRIM_SCHAR         3
#define _CFFI_PRIM_UCHAR         4
#define _CFFI_PRIM_SHORT         5
#define _CFFI_PRIM_USHORT        6
#define _CFFI_PRIM_INT           7
#define _CFFI_PRIM_UINT          8
#define _CFFI_PRIM_LONG          9
#define _CFFI_PRIM_ULONG        10
#define _CFFI_PRIM_LONGLONG     11
#define _CFFI_PRIM_ULONGLONG    12
#define _CFFI_PRIM_FLOAT        13
#define _CFFI_PRIM_DOUBLE       14
#define _CFFI_PRIM_LONGDOUBLE   15

#define _CFFI_PRIM_WCHAR        16
#define _CFFI_PRIM_INT8         17
#define _CFFI_PRIM_UINT8        18
#define _CFFI_PRIM_INT16        19
#define _CFFI_PRIM_UINT16       20
#define _CFFI_PRIM_INT32        21
#define _CFFI_PRIM_UINT32       22
#define _CFFI_PRIM_INT64        23
#define _CFFI_PRIM_UINT64       24
#define _CFFI_PRIM_INTPTR       25
#define _CFFI_PRIM_UINTPTR      26
#define _CFFI_PRIM_PTRDIFF      27
#define _CFFI_PRIM_SIZE         28
#define _CFFI_PRIM_SSIZE        29
#define _CFFI_PRIM_INT_LEAST8   30
#define _CFFI_PRIM_UINT_LEAST8  31
#define _CFFI_PRIM_INT_LEAST16  32
#define _CFFI_PRIM_UINT_LEAST16 33
#define _CFFI_PRIM_INT_LEAST32  34
#define _CFFI_PRIM_UINT_LEAST32 35
#define _CFFI_PRIM_INT_LEAST64  36
#define _CFFI_PRIM_UINT_LEAST64 37
#define _CFFI_PRIM_INT_FAST8    38
#define _CFFI_PRIM_UINT_FAST8   39
#define _CFFI_PRIM_INT_FAST16   40
#define _CFFI_PRIM_UINT_FAST16  41
#define _CFFI_PRIM_INT_FAST32   42
#define _CFFI_PRIM_UINT_FAST32  43
#define _CFFI_PRIM_INT_FAST64   44
#define _CFFI_PRIM_UINT_FAST64  45
#define _CFFI_PRIM_INTMAX       46
#define _CFFI_PRIM_UINTMAX      47

#define _CFFI__NUM_PRIM         48
#define _CFFI__UNKNOWN_PRIM    (-1)


struct _cffi_global_s {
    const char *name;
    void *address;
    _cffi_opcode_t type_op;
    void *size_or_direct_fn;  // OP_GLOBAL_VAR: size, or 0 if unknown
                              // OP_CPYTHON_BLTN_*: addr of direct function
};

struct _cffi_getconst_s {
    unsigned long long value;
    const struct _cffi_type_context_s *ctx;
    int gindex;
};

struct _cffi_struct_union_s {
    const char *name;
    int type_index;          // -> _cffi_types, on a OP_STRUCT_UNION
    int flags;               // _CFFI_F_* flags below
    size_t size;
    int alignment;
    int first_field_index;   // -> _cffi_fields array
    int num_fields;
};
#define _CFFI_F_UNION         0x01   // is a union, not a struct
#define _CFFI_F_CHECK_FIELDS  0x02   // complain if fields are not in the
                                     // "standard layout" or if some are missing
#define _CFFI_F_PACKED        0x04   // for CHECK_FIELDS, assume a packed struct
#define _CFFI_F_EXTERNAL      0x08   // in some other ffi.include()
#define _CFFI_F_OPAQUE        0x10   // opaque

struct _cffi_field_s {
    const char *name;
    size_t field_offset;
    size_t field_size;
    _cffi_opcode_t field_type_op;
};

struct _cffi_enum_s {
    const char *name;
    int type_index;          // -> _cffi_types, on a OP_ENUM
    int type_prim;           // _CFFI_PRIM_xxx
    const char *enumerators; // comma-delimited string
};

struct _cffi_typename_s {
    const char *name;
    int type_index;   /* if opaque, points to a possibly artificial
                         OP_STRUCT which is itself opaque */
};

struct _cffi_type_context_s {
    _cffi_opcode_t *types;
    const struct _cffi_global_s *globals;
    const struct _cffi_field_s *fields;
    const struct _cffi_struct_union_s *struct_unions;
    const struct _cffi_enum_s *enums;
    const struct _cffi_typename_s *typenames;
    int num_globals;
    int num_struct_unions;
    int num_enums;
    int num_typenames;
    const char *const *includes;
    int num_types;
    int flags;      /* future extension */
};

struct _cffi_parse_info_s {
    const struct _cffi_type_context_s *ctx;
    _cffi_opcode_t *output;
    unsigned int output_size;
    size_t error_location;
    const char *error_message;
};

#ifdef _CFFI_INTERNAL
static int parse_c_type(struct _cffi_parse_info_s *info, const char *input);
static int search_in_globals(const struct _cffi_type_context_s *ctx,
                             const char *search, size_t search_len);
static int search_in_struct_unions(const struct _cffi_type_context_s *ctx,
                                   const char *search, size_t search_len);
#endif

/* this block of #ifs should be kept exactly identical between
   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py
   and cffi/_cffi_include.h */
#if defined(_MSC_VER)
# include <malloc.h>   /* for alloca() */
# if _MSC_VER < 1600   /* MSVC < 2010 */
   typedef __int8 int8_t;
   typedef __int16 int16_t;
   typedef __int32 int32_t;
   typedef __int64 int64_t;
   typedef unsigned __int8 uint8_t;
   typedef unsigned __int16 uint16_t;
   typedef unsigned __int32 uint32_t;
   typedef unsigned __int64 uint64_t;
   typedef __int8 int_least8_t;
   typedef __int16 int_least16_t;
   typedef __int32 int_least32_t;
   typedef __int64 int_least64_t;
   typedef unsigned __int8 uint_least8_t;
   typedef unsigned __int16 uint_least16_t;
   typedef unsigned __int32 uint_least32_t;
   typedef unsigned __int64 uint_least64_t;
   typedef __int8 int_fast8_t;
   typedef __int16 int_fast16_t;
   typedef __int32 int_fast32_t;
   typedef __int64 int_fast64_t;
   typedef unsigned __int8 uint_fast8_t;
   typedef unsigned __int16 uint_fast16_t;
   typedef unsigned __int32 uint_fast32_t;
   typedef unsigned __int64 uint_fast64_t;
   typedef __int64 intmax_t;
   typedef unsigned __int64 uintmax_t;
# else
#  include <stdint.h>
# endif
# if _MSC_VER < 1800   /* MSVC < 2013 */
   typedef unsigned char _Bool;
# endif
#else
# include <stdint.h>
# if (defined (__SVR4) && defined (__sun)) || defined(_AIX) || defined(__hpux)
#  include <alloca.h>
# endif
#endif

#ifdef __GNUC__
# define _CFFI_UNUSED_FN  __attribute__((unused))
#else
# define _CFFI_UNUSED_FN  /* nothing */
#endif

/**********  CPython-specific section  **********/
#ifndef PYPY_VERSION


#if PY_MAJOR_VERSION >= 3
# define PyInt_FromLong PyLong_FromLong
#endif

#define _cffi_from_c_double PyFloat_FromDouble
#define _cffi_from_c_float PyFloat_FromDouble
#define _cffi_from_c_long PyInt_FromLong
#define _cffi_from_c_ulong PyLong_FromUnsignedLong
#define _cffi_from_c_longlong PyLong_FromLongLong
#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong

#define _cffi_to_c_double PyFloat_AsDouble
#define _cffi_to_c_float PyFloat_AsDouble

#define _cffi_from_c_int(x, type)                                        \
    (((type)-1) > 0 ? /* unsigned */                                     \
        (sizeof(type) < sizeof(long) ?                                   \
            PyInt_FromLong((long)x) :                                    \
         sizeof(type) == sizeof(long) ?                                  \
            PyLong_FromUnsignedLong((unsigned long)x) :                  \
            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \
        (sizeof(type) <= sizeof(long) ?                                  \
            PyInt_FromLong((long)x) :                                    \
            PyLong_FromLongLong((long long)x)))

#define _cffi_to_c_int(o, type)                                          \
    ((type)(                                                             \
     sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \
                                         : (type)_cffi_to_c_i8(o)) :     \
     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \
                                         : (type)_cffi_to_c_i16(o)) :    \
     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \
                                         : (type)_cffi_to_c_i32(o)) :    \
     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \
                                         : (type)_cffi_to_c_i64(o)) :    \
     (Py_FatalError("unsupported size for type " #type), (type)0)))

#define _cffi_to_c_i8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[1])
#define _cffi_to_c_u8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[2])
#define _cffi_to_c_i16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[3])
#define _cffi_to_c_u16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[4])
#define _cffi_to_c_i32                                                   \
                 ((int(*)(PyObject *))_cffi_exports[5])
#define _cffi_to_c_u32                                                   \
                 ((unsigned int(*)(PyObject *))_cffi_exports[6])
#define _cffi_to_c_i64                                                   \
                 ((long long(*)(PyObject *))_cffi_exports[7])
#define _cffi_to_c_u64                                                   \
                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])
#define _cffi_to_c_char                                                  \
                 ((int(*)(PyObject *))_cffi_exports[9])
#define _cffi_from_c_pointer                                             \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])
#define _cffi_to_c_pointer                                               \
    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])
#define _cffi_get_struct_layout                                          \
    not used any more
#define _cffi_restore_errno                                              \
    ((void(*)(void))_cffi_exports[13])
#define _cffi_save_errno                                                 \
    ((void(*)(void))_cffi_exports[14])
#define _cffi_from_c_char                                                \
    ((PyObject *(*)(char))_cffi_exports[15])
#define _cffi_from_c_deref                                               \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])
#define _cffi_to_c                                                       \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])
#define _cffi_from_c_struct                                              \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])
#define _cffi_to_c_wchar_t                                               \
    ((wchar_t(*)(PyObject *))_cffi_exports[19])
#define _cffi_from_c_wchar_t                                             \
    ((PyObject *(*)(wchar_t))_cffi_exports[20])
#define _cffi_to_c_long_double                                           \
    ((long double(*)(PyObject *))_cffi_exports[21])
#define _cffi_to_c__Bool                                                 \
    ((_Bool(*)(PyObject *))_cffi_exports[22])
#define _cffi_prepare_pointer_call_argument                              \
    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])
#define _cffi_convert_array_from_object                                  \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])
#define _CFFI_NUM_EXPORTS 25

typedef struct _ctypedescr CTypeDescrObject;

static void *_cffi_exports[_CFFI_NUM_EXPORTS];

#define _cffi_type(index)   (                           \
    assert((((uintptr_t)_cffi_types[index]) & 1) == 0), \
    (CTypeDescrObject *)_cffi_types[index])

static PyObject *_cffi_init(const char *module_name, Py_ssize_t version,
                            const struct _cffi_type_context_s *ctx)
{
    PyObject *module, *o_arg, *new_module;
    void *raw[] = {
        (void *)module_name,
        (void *)version,
        (void *)_cffi_exports,
        (void *)ctx,
    };

    module = PyImport_ImportModule("_cffi_backend");
    if (module == NULL)
        goto failure;

    o_arg = PyLong_FromVoidPtr((void *)raw);
    if (o_arg == NULL)
        goto failure;

    new_module = PyObject_CallMethod(
        module, (char *)"_init_cffi_1_0_external_module", (char *)"O", o_arg);

    Py_DECREF(o_arg);
    Py_DECREF(module);
    return new_module;

  failure:
    Py_XDECREF(module);
    return NULL;
}

_CFFI_UNUSED_FN
static PyObject **_cffi_unpack_args(PyObject *args_tuple, Py_ssize_t expected,
                                    const char *fnname)
{
    if (PyTuple_GET_SIZE(args_tuple) != expected) {
        PyErr_Format(PyExc_TypeError,
                     "%.150s() takes exactly %zd arguments (%zd given)",
                     fnname, expected, PyTuple_GET_SIZE(args_tuple));
        return NULL;
    }
    return &PyTuple_GET_ITEM(args_tuple, 0);   /* pointer to the first item,
                                                  the others follow */
}

#endif
/**********  end CPython-specific section  **********/


#define _cffi_array_len(array)   (sizeof(array) / sizeof((array)[0]))

#define _cffi_prim_int(size, sign)                                      \
    ((size) == 1 ? ((sign) ? _CFFI_PRIM_INT8  : _CFFI_PRIM_UINT8)  :    \
     (size) == 2 ? ((sign) ? _CFFI_PRIM_INT16 : _CFFI_PRIM_UINT16) :    \
     (size) == 4 ? ((sign) ? _CFFI_PRIM_INT32 : _CFFI_PRIM_UINT32) :    \
     (size) == 8 ? ((sign) ? _CFFI_PRIM_INT64 : _CFFI_PRIM_UINT64) :    \
     _CFFI__UNKNOWN_PRIM)

#define _cffi_check_int(got, got_nonpos, expected)      \
    ((got_nonpos) == (expected <= 0) &&                 \
     (got) == (unsigned long long)expected)

#ifdef __cplusplus
}
#endif

/************************************************************/


            // Nothing
            #include "wrapper.h"
        

/************************************************************/

static void *_cffi_types[] = {
/*  0 */ _CFFI_OP(_CFFI_OP_FUNCTION, 1), // Matrix4d *()(Matrix4d *)
/*  1 */ _CFFI_OP(_CFFI_OP_POINTER, 81), // Matrix4d *
/*  2 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/*  3 */ _CFFI_OP(_CFFI_OP_FUNCTION, 1), // Matrix4d *()(Matrix4d *, Matrix4d const *)
/*  4 */ _CFFI_OP(_CFFI_OP_NOOP, 1),
/*  5 */ _CFFI_OP(_CFFI_OP_POINTER, 81), // Matrix4d const *
/*  6 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/*  7 */ _CFFI_OP(_CFFI_OP_FUNCTION, 1), // Matrix4d *()(Matrix4d *, double)
/*  8 */ _CFFI_OP(_CFFI_OP_NOOP, 1),
/*  9 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14), // double
/* 10 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 11 */ _CFFI_OP(_CFFI_OP_FUNCTION, 1), // Matrix4d *()(Matrix4d *, double, double, double)
/* 12 */ _CFFI_OP(_CFFI_OP_NOOP, 1),
/* 13 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 14 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 15 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 16 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 17 */ _CFFI_OP(_CFFI_OP_FUNCTION, 1), // Matrix4d *()(Matrix4d *, double, int, int, double, double)
/* 18 */ _CFFI_OP(_CFFI_OP_NOOP, 1),
/* 19 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 20 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7), // int
/* 21 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7),
/* 22 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 23 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 24 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 25 */ _CFFI_OP(_CFFI_OP_FUNCTION, 1), // Matrix4d *()(void)
/* 26 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 27 */ _CFFI_OP(_CFFI_OP_FUNCTION, 28), // Vector3d *()(Vector3d *)
/* 28 */ _CFFI_OP(_CFFI_OP_POINTER, 82), // Vector3d *
/* 29 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 30 */ _CFFI_OP(_CFFI_OP_FUNCTION, 28), // Vector3d *()(Vector3d *, Vector3d const *)
/* 31 */ _CFFI_OP(_CFFI_OP_NOOP, 28),
/* 32 */ _CFFI_OP(_CFFI_OP_POINTER, 82), // Vector3d const *
/* 33 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 34 */ _CFFI_OP(_CFFI_OP_FUNCTION, 28), // Vector3d *()(Vector3d *, double)
/* 35 */ _CFFI_OP(_CFFI_OP_NOOP, 28),
/* 36 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 37 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 38 */ _CFFI_OP(_CFFI_OP_FUNCTION, 28), // Vector3d *()(double, double, double)
/* 39 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 40 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 41 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 42 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 43 */ _CFFI_OP(_CFFI_OP_FUNCTION, 28), // Vector3d *()(void)
/* 44 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 45 */ _CFFI_OP(_CFFI_OP_FUNCTION, 83), // _Bool()(Matrix4d *, Matrix4d const *)
/* 46 */ _CFFI_OP(_CFFI_OP_NOOP, 1),
/* 47 */ _CFFI_OP(_CFFI_OP_NOOP, 5),
/* 48 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 49 */ _CFFI_OP(_CFFI_OP_FUNCTION, 83), // _Bool()(Vector3d *, Vector3d const *)
/* 50 */ _CFFI_OP(_CFFI_OP_NOOP, 28),
/* 51 */ _CFFI_OP(_CFFI_OP_NOOP, 32),
/* 52 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 53 */ _CFFI_OP(_CFFI_OP_FUNCTION, 9), // double()(Matrix4d *, int, int)
/* 54 */ _CFFI_OP(_CFFI_OP_NOOP, 1),
/* 55 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7),
/* 56 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7),
/* 57 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 58 */ _CFFI_OP(_CFFI_OP_FUNCTION, 9), // double()(Vector3d *)
/* 59 */ _CFFI_OP(_CFFI_OP_NOOP, 28),
/* 60 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 61 */ _CFFI_OP(_CFFI_OP_FUNCTION, 9), // double()(Vector3d *, Vector3d const *)
/* 62 */ _CFFI_OP(_CFFI_OP_NOOP, 28),
/* 63 */ _CFFI_OP(_CFFI_OP_NOOP, 32),
/* 64 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 65 */ _CFFI_OP(_CFFI_OP_FUNCTION, 84), // void()(Matrix4d *)
/* 66 */ _CFFI_OP(_CFFI_OP_NOOP, 1),
/* 67 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 68 */ _CFFI_OP(_CFFI_OP_FUNCTION, 84), // void()(Matrix4d *, int, int, double)
/* 69 */ _CFFI_OP(_CFFI_OP_NOOP, 1),
/* 70 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7),
/* 71 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7),
/* 72 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 73 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 74 */ _CFFI_OP(_CFFI_OP_FUNCTION, 84), // void()(Vector3d *)
/* 75 */ _CFFI_OP(_CFFI_OP_NOOP, 28),
/* 76 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 77 */ _CFFI_OP(_CFFI_OP_FUNCTION, 84), // void()(Vector3d *, double)
/* 78 */ _CFFI_OP(_CFFI_OP_NOOP, 28),
/* 79 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 14),
/* 80 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 81 */ _CFFI_OP(_CFFI_OP_STRUCT_UNION, 0), // Matrix4d
/* 82 */ _CFFI_OP(_CFFI_OP_STRUCT_UNION, 1), // Vector3d
/* 83 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 1), // _Bool
/* 84 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 0), // void
};

static void _cffi_d_DeleteMatrix4d(Matrix4d * x0)
{
  DeleteMatrix4d(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_DeleteMatrix4d(PyObject *self, PyObject *arg0)
{
  Matrix4d * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { DeleteMatrix4d(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_DeleteMatrix4d _cffi_d_DeleteMatrix4d
#endif

static void _cffi_d_DeleteVector3d(Vector3d * x0)
{
  DeleteVector3d(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_DeleteVector3d(PyObject *self, PyObject *arg0)
{
  Vector3d * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { DeleteVector3d(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_DeleteVector3d _cffi_d_DeleteVector3d
#endif

static Matrix4d * _cffi_d_Matrix4d_Add(Matrix4d * x0, Matrix4d const * x1)
{
  return Matrix4d_Add(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Add(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  Matrix4d const * x1;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Matrix4d_Add");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Matrix4d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(5), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Add(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_Add _cffi_d_Matrix4d_Add
#endif

static Matrix4d * _cffi_d_Matrix4d_Add_Scalar(Matrix4d * x0, double x1)
{
  return Matrix4d_Add_Scalar(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Add_Scalar(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  double x1;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Matrix4d_Add_Scalar");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Add_Scalar(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_Add_Scalar _cffi_d_Matrix4d_Add_Scalar
#endif

static Matrix4d * _cffi_d_Matrix4d_Copy(Matrix4d * x0, Matrix4d const * x1)
{
  return Matrix4d_Copy(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Copy(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  Matrix4d const * x1;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Matrix4d_Copy");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Matrix4d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(5), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Copy(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_Copy _cffi_d_Matrix4d_Copy
#endif

static Matrix4d * _cffi_d_Matrix4d_Div_Scalar(Matrix4d * x0, double x1)
{
  return Matrix4d_Div_Scalar(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Div_Scalar(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  double x1;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Matrix4d_Div_Scalar");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Div_Scalar(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_Div_Scalar _cffi_d_Matrix4d_Div_Scalar
#endif

static _Bool _cffi_d_Matrix4d_Equals(Matrix4d * x0, Matrix4d const * x1)
{
  return Matrix4d_Equals(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Equals(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  Matrix4d const * x1;
  Py_ssize_t datasize;
  _Bool result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Matrix4d_Equals");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Matrix4d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(5), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Equals(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, _Bool);
}
#else
#  define _cffi_f_Matrix4d_Equals _cffi_d_Matrix4d_Equals
#endif

static double _cffi_d_Matrix4d_Get(Matrix4d * x0, int x1, int x2)
{
  return Matrix4d_Get(x0, x1, x2);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Get(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  int x1;
  int x2;
  Py_ssize_t datasize;
  double result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 3, "Matrix4d_Get");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];
  arg2 = aa[2];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Get(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_double(result);
}
#else
#  define _cffi_f_Matrix4d_Get _cffi_d_Matrix4d_Get
#endif

static Matrix4d * _cffi_d_Matrix4d_InitIdentity(Matrix4d * x0)
{
  return Matrix4d_InitIdentity(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_InitIdentity(PyObject *self, PyObject *arg0)
{
  Matrix4d * x0;
  Py_ssize_t datasize;
  Matrix4d * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_InitIdentity(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_InitIdentity _cffi_d_Matrix4d_InitIdentity
#endif

static Matrix4d * _cffi_d_Matrix4d_InitProjection(Matrix4d * x0, double x1, int x2, int x3, double x4, double x5)
{
  return Matrix4d_InitProjection(x0, x1, x2, x3, x4, x5);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_InitProjection(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  double x1;
  int x2;
  int x3;
  double x4;
  double x5;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 6, "Matrix4d_InitProjection");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];
  arg2 = aa[2];
  arg3 = aa[3];
  arg4 = aa[4];
  arg5 = aa[5];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, int);
  if (x3 == (int)-1 && PyErr_Occurred())
    return NULL;

  x4 = (double)_cffi_to_c_double(arg4);
  if (x4 == (double)-1 && PyErr_Occurred())
    return NULL;

  x5 = (double)_cffi_to_c_double(arg5);
  if (x5 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_InitProjection(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_InitProjection _cffi_d_Matrix4d_InitProjection
#endif

static Matrix4d * _cffi_d_Matrix4d_InitRotation(Matrix4d * x0, double x1, double x2, double x3)
{
  return Matrix4d_InitRotation(x0, x1, x2, x3);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_InitRotation(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  double x1;
  double x2;
  double x3;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 4, "Matrix4d_InitRotation");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];
  arg2 = aa[2];
  arg3 = aa[3];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  x2 = (double)_cffi_to_c_double(arg2);
  if (x2 == (double)-1 && PyErr_Occurred())
    return NULL;

  x3 = (double)_cffi_to_c_double(arg3);
  if (x3 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_InitRotation(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_InitRotation _cffi_d_Matrix4d_InitRotation
#endif

static Matrix4d * _cffi_d_Matrix4d_InitScale(Matrix4d * x0, double x1, double x2, double x3)
{
  return Matrix4d_InitScale(x0, x1, x2, x3);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_InitScale(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  double x1;
  double x2;
  double x3;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 4, "Matrix4d_InitScale");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];
  arg2 = aa[2];
  arg3 = aa[3];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  x2 = (double)_cffi_to_c_double(arg2);
  if (x2 == (double)-1 && PyErr_Occurred())
    return NULL;

  x3 = (double)_cffi_to_c_double(arg3);
  if (x3 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_InitScale(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_InitScale _cffi_d_Matrix4d_InitScale
#endif

static Matrix4d * _cffi_d_Matrix4d_InitTranslation(Matrix4d * x0, double x1, double x2, double x3)
{
  return Matrix4d_InitTranslation(x0, x1, x2, x3);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_InitTranslation(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  double x1;
  double x2;
  double x3;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 4, "Matrix4d_InitTranslation");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];
  arg2 = aa[2];
  arg3 = aa[3];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  x2 = (double)_cffi_to_c_double(arg2);
  if (x2 == (double)-1 && PyErr_Occurred())
    return NULL;

  x3 = (double)_cffi_to_c_double(arg3);
  if (x3 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_InitTranslation(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_InitTranslation _cffi_d_Matrix4d_InitTranslation
#endif

static Matrix4d * _cffi_d_Matrix4d_Mul(Matrix4d * x0, Matrix4d const * x1)
{
  return Matrix4d_Mul(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Mul(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  Matrix4d const * x1;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Matrix4d_Mul");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Matrix4d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(5), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Mul(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_Mul _cffi_d_Matrix4d_Mul
#endif

static Matrix4d * _cffi_d_Matrix4d_Mul_Scalar(Matrix4d * x0, double x1)
{
  return Matrix4d_Mul_Scalar(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Mul_Scalar(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  double x1;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Matrix4d_Mul_Scalar");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Mul_Scalar(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_Mul_Scalar _cffi_d_Matrix4d_Mul_Scalar
#endif

static void _cffi_d_Matrix4d_Set(Matrix4d * x0, int x1, int x2, double x3)
{
  Matrix4d_Set(x0, x1, x2, x3);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Set(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  int x1;
  int x2;
  double x3;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 4, "Matrix4d_Set");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];
  arg2 = aa[2];
  arg3 = aa[3];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  x3 = (double)_cffi_to_c_double(arg3);
  if (x3 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { Matrix4d_Set(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_Matrix4d_Set _cffi_d_Matrix4d_Set
#endif

static Matrix4d * _cffi_d_Matrix4d_Sub(Matrix4d * x0, Matrix4d const * x1)
{
  return Matrix4d_Sub(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Sub(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  Matrix4d const * x1;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Matrix4d_Sub");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Matrix4d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(5), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Sub(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_Sub _cffi_d_Matrix4d_Sub
#endif

static Matrix4d * _cffi_d_Matrix4d_Sub_Scalar(Matrix4d * x0, double x1)
{
  return Matrix4d_Sub_Scalar(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Matrix4d_Sub_Scalar(PyObject *self, PyObject *args)
{
  Matrix4d * x0;
  double x1;
  Py_ssize_t datasize;
  Matrix4d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Matrix4d_Sub_Scalar");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Matrix4d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Matrix4d_Sub_Scalar(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_Matrix4d_Sub_Scalar _cffi_d_Matrix4d_Sub_Scalar
#endif

static Matrix4d * _cffi_d_NewMatrix4d(void)
{
  return NewMatrix4d();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_NewMatrix4d(PyObject *self, PyObject *noarg)
{
  Matrix4d * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = NewMatrix4d(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}
#else
#  define _cffi_f_NewMatrix4d _cffi_d_NewMatrix4d
#endif

static Vector3d * _cffi_d_NewVector3d(void)
{
  return NewVector3d();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_NewVector3d(PyObject *self, PyObject *noarg)
{
  Vector3d * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = NewVector3d(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_NewVector3d _cffi_d_NewVector3d
#endif

static Vector3d * _cffi_d_NewVector3dInit(double x0, double x1, double x2)
{
  return NewVector3dInit(x0, x1, x2);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_NewVector3dInit(PyObject *self, PyObject *args)
{
  double x0;
  double x1;
  double x2;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 3, "NewVector3dInit");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];
  arg2 = aa[2];

  x0 = (double)_cffi_to_c_double(arg0);
  if (x0 == (double)-1 && PyErr_Occurred())
    return NULL;

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  x2 = (double)_cffi_to_c_double(arg2);
  if (x2 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = NewVector3dInit(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_NewVector3dInit _cffi_d_NewVector3dInit
#endif

static Vector3d * _cffi_d_Vector3d_Add(Vector3d * x0, Vector3d const * x1)
{
  return Vector3d_Add(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Add(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  Vector3d const * x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Add");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Vector3d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(32), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Add(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Add _cffi_d_Vector3d_Add
#endif

static Vector3d * _cffi_d_Vector3d_Add_Scalar(Vector3d * x0, double x1)
{
  return Vector3d_Add_Scalar(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Add_Scalar(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  double x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Add_Scalar");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Add_Scalar(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Add_Scalar _cffi_d_Vector3d_Add_Scalar
#endif

static Vector3d * _cffi_d_Vector3d_Copy(Vector3d * x0, Vector3d const * x1)
{
  return Vector3d_Copy(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Copy(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  Vector3d const * x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Copy");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Vector3d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(32), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Copy(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Copy _cffi_d_Vector3d_Copy
#endif

static Vector3d * _cffi_d_Vector3d_Cross(Vector3d * x0, Vector3d const * x1)
{
  return Vector3d_Cross(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Cross(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  Vector3d const * x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Cross");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Vector3d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(32), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Cross(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Cross _cffi_d_Vector3d_Cross
#endif

static Vector3d * _cffi_d_Vector3d_Div(Vector3d * x0, Vector3d const * x1)
{
  return Vector3d_Div(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Div(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  Vector3d const * x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Div");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Vector3d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(32), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Div(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Div _cffi_d_Vector3d_Div
#endif

static Vector3d * _cffi_d_Vector3d_Div_Scalar(Vector3d * x0, double x1)
{
  return Vector3d_Div_Scalar(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Div_Scalar(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  double x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Div_Scalar");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Div_Scalar(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Div_Scalar _cffi_d_Vector3d_Div_Scalar
#endif

static double _cffi_d_Vector3d_Dot(Vector3d * x0, Vector3d const * x1)
{
  return Vector3d_Dot(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Dot(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  Vector3d const * x1;
  Py_ssize_t datasize;
  double result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Dot");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Vector3d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(32), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Dot(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_double(result);
}
#else
#  define _cffi_f_Vector3d_Dot _cffi_d_Vector3d_Dot
#endif

static _Bool _cffi_d_Vector3d_Equals(Vector3d * x0, Vector3d const * x1)
{
  return Vector3d_Equals(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Equals(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  Vector3d const * x1;
  Py_ssize_t datasize;
  _Bool result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Equals");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Vector3d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(32), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Equals(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, _Bool);
}
#else
#  define _cffi_f_Vector3d_Equals _cffi_d_Vector3d_Equals
#endif

static double _cffi_d_Vector3d_GetX(Vector3d * x0)
{
  return Vector3d_GetX(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_GetX(PyObject *self, PyObject *arg0)
{
  Vector3d * x0;
  Py_ssize_t datasize;
  double result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_GetX(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_double(result);
}
#else
#  define _cffi_f_Vector3d_GetX _cffi_d_Vector3d_GetX
#endif

static double _cffi_d_Vector3d_GetY(Vector3d * x0)
{
  return Vector3d_GetY(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_GetY(PyObject *self, PyObject *arg0)
{
  Vector3d * x0;
  Py_ssize_t datasize;
  double result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_GetY(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_double(result);
}
#else
#  define _cffi_f_Vector3d_GetY _cffi_d_Vector3d_GetY
#endif

static double _cffi_d_Vector3d_GetZ(Vector3d * x0)
{
  return Vector3d_GetZ(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_GetZ(PyObject *self, PyObject *arg0)
{
  Vector3d * x0;
  Py_ssize_t datasize;
  double result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_GetZ(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_double(result);
}
#else
#  define _cffi_f_Vector3d_GetZ _cffi_d_Vector3d_GetZ
#endif

static double _cffi_d_Vector3d_Length(Vector3d * x0)
{
  return Vector3d_Length(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Length(PyObject *self, PyObject *arg0)
{
  Vector3d * x0;
  Py_ssize_t datasize;
  double result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Length(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_double(result);
}
#else
#  define _cffi_f_Vector3d_Length _cffi_d_Vector3d_Length
#endif

static Vector3d * _cffi_d_Vector3d_Mul(Vector3d * x0, Vector3d const * x1)
{
  return Vector3d_Mul(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Mul(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  Vector3d const * x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Mul");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Vector3d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(32), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Mul(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Mul _cffi_d_Vector3d_Mul
#endif

static Vector3d * _cffi_d_Vector3d_Mul_Scalar(Vector3d * x0, double x1)
{
  return Vector3d_Mul_Scalar(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Mul_Scalar(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  double x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Mul_Scalar");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Mul_Scalar(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Mul_Scalar _cffi_d_Vector3d_Mul_Scalar
#endif

static Vector3d * _cffi_d_Vector3d_Normalize(Vector3d * x0)
{
  return Vector3d_Normalize(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Normalize(PyObject *self, PyObject *arg0)
{
  Vector3d * x0;
  Py_ssize_t datasize;
  Vector3d * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Normalize(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Normalize _cffi_d_Vector3d_Normalize
#endif

static Vector3d * _cffi_d_Vector3d_Normalized(Vector3d * x0)
{
  return Vector3d_Normalized(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Normalized(PyObject *self, PyObject *arg0)
{
  Vector3d * x0;
  Py_ssize_t datasize;
  Vector3d * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Normalized(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Normalized _cffi_d_Vector3d_Normalized
#endif

static void _cffi_d_Vector3d_SetX(Vector3d * x0, double x1)
{
  Vector3d_SetX(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_SetX(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  double x1;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_SetX");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { Vector3d_SetX(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_Vector3d_SetX _cffi_d_Vector3d_SetX
#endif

static void _cffi_d_Vector3d_SetY(Vector3d * x0, double x1)
{
  Vector3d_SetY(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_SetY(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  double x1;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_SetY");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { Vector3d_SetY(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_Vector3d_SetY _cffi_d_Vector3d_SetY
#endif

static void _cffi_d_Vector3d_SetZ(Vector3d * x0, double x1)
{
  Vector3d_SetZ(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_SetZ(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  double x1;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_SetZ");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { Vector3d_SetZ(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_Vector3d_SetZ _cffi_d_Vector3d_SetZ
#endif

static Vector3d * _cffi_d_Vector3d_Sub(Vector3d * x0, Vector3d const * x1)
{
  return Vector3d_Sub(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Sub(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  Vector3d const * x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Sub");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = (Vector3d const *)alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(32), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Sub(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Sub _cffi_d_Vector3d_Sub
#endif

static Vector3d * _cffi_d_Vector3d_Sub_Scalar(Vector3d * x0, double x1)
{
  return Vector3d_Sub_Scalar(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Vector3d_Sub_Scalar(PyObject *self, PyObject *args)
{
  Vector3d * x0;
  double x1;
  Py_ssize_t datasize;
  Vector3d * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject **aa;

  aa = _cffi_unpack_args(args, 2, "Vector3d_Sub_Scalar");
  if (aa == NULL)
    return NULL;
  arg0 = aa[0];
  arg1 = aa[1];

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Vector3d *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
      return NULL;
  }

  x1 = (double)_cffi_to_c_double(arg1);
  if (x1 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Vector3d_Sub_Scalar(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(28));
}
#else
#  define _cffi_f_Vector3d_Sub_Scalar _cffi_d_Vector3d_Sub_Scalar
#endif

static const struct _cffi_global_s _cffi_globals[] = {
  { "DeleteMatrix4d", (void *)_cffi_f_DeleteMatrix4d, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 65), (void *)_cffi_d_DeleteMatrix4d },
  { "DeleteVector3d", (void *)_cffi_f_DeleteVector3d, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 74), (void *)_cffi_d_DeleteVector3d },
  { "Matrix4d_Add", (void *)_cffi_f_Matrix4d_Add, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 3), (void *)_cffi_d_Matrix4d_Add },
  { "Matrix4d_Add_Scalar", (void *)_cffi_f_Matrix4d_Add_Scalar, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 7), (void *)_cffi_d_Matrix4d_Add_Scalar },
  { "Matrix4d_Copy", (void *)_cffi_f_Matrix4d_Copy, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 3), (void *)_cffi_d_Matrix4d_Copy },
  { "Matrix4d_Div_Scalar", (void *)_cffi_f_Matrix4d_Div_Scalar, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 7), (void *)_cffi_d_Matrix4d_Div_Scalar },
  { "Matrix4d_Equals", (void *)_cffi_f_Matrix4d_Equals, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 45), (void *)_cffi_d_Matrix4d_Equals },
  { "Matrix4d_Get", (void *)_cffi_f_Matrix4d_Get, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 53), (void *)_cffi_d_Matrix4d_Get },
  { "Matrix4d_InitIdentity", (void *)_cffi_f_Matrix4d_InitIdentity, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 0), (void *)_cffi_d_Matrix4d_InitIdentity },
  { "Matrix4d_InitProjection", (void *)_cffi_f_Matrix4d_InitProjection, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 17), (void *)_cffi_d_Matrix4d_InitProjection },
  { "Matrix4d_InitRotation", (void *)_cffi_f_Matrix4d_InitRotation, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 11), (void *)_cffi_d_Matrix4d_InitRotation },
  { "Matrix4d_InitScale", (void *)_cffi_f_Matrix4d_InitScale, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 11), (void *)_cffi_d_Matrix4d_InitScale },
  { "Matrix4d_InitTranslation", (void *)_cffi_f_Matrix4d_InitTranslation, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 11), (void *)_cffi_d_Matrix4d_InitTranslation },
  { "Matrix4d_Mul", (void *)_cffi_f_Matrix4d_Mul, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 3), (void *)_cffi_d_Matrix4d_Mul },
  { "Matrix4d_Mul_Scalar", (void *)_cffi_f_Matrix4d_Mul_Scalar, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 7), (void *)_cffi_d_Matrix4d_Mul_Scalar },
  { "Matrix4d_Set", (void *)_cffi_f_Matrix4d_Set, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 68), (void *)_cffi_d_Matrix4d_Set },
  { "Matrix4d_Sub", (void *)_cffi_f_Matrix4d_Sub, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 3), (void *)_cffi_d_Matrix4d_Sub },
  { "Matrix4d_Sub_Scalar", (void *)_cffi_f_Matrix4d_Sub_Scalar, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 7), (void *)_cffi_d_Matrix4d_Sub_Scalar },
  { "NewMatrix4d", (void *)_cffi_f_NewMatrix4d, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 25), (void *)_cffi_d_NewMatrix4d },
  { "NewVector3d", (void *)_cffi_f_NewVector3d, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 43), (void *)_cffi_d_NewVector3d },
  { "NewVector3dInit", (void *)_cffi_f_NewVector3dInit, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 38), (void *)_cffi_d_NewVector3dInit },
  { "Vector3d_Add", (void *)_cffi_f_Vector3d_Add, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 30), (void *)_cffi_d_Vector3d_Add },
  { "Vector3d_Add_Scalar", (void *)_cffi_f_Vector3d_Add_Scalar, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 34), (void *)_cffi_d_Vector3d_Add_Scalar },
  { "Vector3d_Copy", (void *)_cffi_f_Vector3d_Copy, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 30), (void *)_cffi_d_Vector3d_Copy },
  { "Vector3d_Cross", (void *)_cffi_f_Vector3d_Cross, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 30), (void *)_cffi_d_Vector3d_Cross },
  { "Vector3d_Div", (void *)_cffi_f_Vector3d_Div, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 30), (void *)_cffi_d_Vector3d_Div },
  { "Vector3d_Div_Scalar", (void *)_cffi_f_Vector3d_Div_Scalar, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 34), (void *)_cffi_d_Vector3d_Div_Scalar },
  { "Vector3d_Dot", (void *)_cffi_f_Vector3d_Dot, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 61), (void *)_cffi_d_Vector3d_Dot },
  { "Vector3d_Equals", (void *)_cffi_f_Vector3d_Equals, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 49), (void *)_cffi_d_Vector3d_Equals },
  { "Vector3d_GetX", (void *)_cffi_f_Vector3d_GetX, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 58), (void *)_cffi_d_Vector3d_GetX },
  { "Vector3d_GetY", (void *)_cffi_f_Vector3d_GetY, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 58), (void *)_cffi_d_Vector3d_GetY },
  { "Vector3d_GetZ", (void *)_cffi_f_Vector3d_GetZ, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 58), (void *)_cffi_d_Vector3d_GetZ },
  { "Vector3d_Length", (void *)_cffi_f_Vector3d_Length, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 58), (void *)_cffi_d_Vector3d_Length },
  { "Vector3d_Mul", (void *)_cffi_f_Vector3d_Mul, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 30), (void *)_cffi_d_Vector3d_Mul },
  { "Vector3d_Mul_Scalar", (void *)_cffi_f_Vector3d_Mul_Scalar, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 34), (void *)_cffi_d_Vector3d_Mul_Scalar },
  { "Vector3d_Normalize", (void *)_cffi_f_Vector3d_Normalize, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 27), (void *)_cffi_d_Vector3d_Normalize },
  { "Vector3d_Normalized", (void *)_cffi_f_Vector3d_Normalized, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 27), (void *)_cffi_d_Vector3d_Normalized },
  { "Vector3d_SetX", (void *)_cffi_f_Vector3d_SetX, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 77), (void *)_cffi_d_Vector3d_SetX },
  { "Vector3d_SetY", (void *)_cffi_f_Vector3d_SetY, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 77), (void *)_cffi_d_Vector3d_SetY },
  { "Vector3d_SetZ", (void *)_cffi_f_Vector3d_SetZ, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 77), (void *)_cffi_d_Vector3d_SetZ },
  { "Vector3d_Sub", (void *)_cffi_f_Vector3d_Sub, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 30), (void *)_cffi_d_Vector3d_Sub },
  { "Vector3d_Sub_Scalar", (void *)_cffi_f_Vector3d_Sub_Scalar, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 34), (void *)_cffi_d_Vector3d_Sub_Scalar },
};

static const struct _cffi_struct_union_s _cffi_struct_unions[] = {
  { "Matrix4d", 81, _CFFI_F_OPAQUE,
    (size_t)-1, -1, -1, 0 /* opaque */ },
  { "Vector3d", 82, _CFFI_F_OPAQUE,
    (size_t)-1, -1, -1, 0 /* opaque */ },
};

static const struct _cffi_typename_s _cffi_typenames[] = {
  { "Matrix4d", 81 },
  { "Vector3d", 82 },
};

static const struct _cffi_type_context_s _cffi_type_context = {
  _cffi_types,
  _cffi_globals,
  NULL,  /* no fields */
  _cffi_struct_unions,
  NULL,  /* no enums */
  _cffi_typenames,
  42,  /* num_globals */
  2,  /* num_struct_unions */
  0,  /* num_enums */
  2,  /* num_typenames */
  NULL,  /* no includes */
  85,  /* num_types */
  0,  /* flags */
};

#ifdef PYPY_VERSION
PyMODINIT_FUNC
_cffi_pypyinit_core(const void *p[])
{
    p[0] = (const void *)0x2601;
    p[1] = &_cffi_type_context;
}
#  ifdef _MSC_VER
     PyMODINIT_FUNC
#  if PY_MAJOR_VERSION >= 3
     PyInit_core(void) { return NULL; }
#  else
     initcore(void) { }
#  endif
#  endif
#elif PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC
PyInit_core(void)
{
  return _cffi_init("core", 0x2601, &_cffi_type_context);
}
#else
PyMODINIT_FUNC
initcore(void)
{
  _cffi_init("core", 0x2601, &_cffi_type_context);
}
#endif

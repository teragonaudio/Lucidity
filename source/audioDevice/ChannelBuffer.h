#ifndef __ChannelBuffer_h__
#define __ChannelBuffer_h__

#include <Python.h>
#include "structmember.h"

typedef unsigned short Sample;
typedef unsigned long BufferIndex;

/** Buffer representing one channel, 16-bit PCM data */
typedef struct {
    PyObject_HEAD
    Sample *data[2];
    BufferIndex length;
    unsigned long sizeInBytes;
    BufferIndex readPosition;
    BufferIndex writePosition;

    // TODO: This MUST be made atomic
    short isWriting;
} ChannelBuffer;

static PyObject*
ChannelBuffer_new(PyTypeObject *type, PyObject *args, PyObject *keywords);
static int
ChannelBuffer_init(ChannelBuffer *self, PyObject *args, PyObject *keywords);
static void
ChannelBuffer_dealloc(ChannelBuffer *self);

static void
ChannelBuffer_writeData(ChannelBuffer *self, PyObject *data, void *closure);

static PyMemberDef ChannelBuffer_members[] = {
    {"length", T_INT, offsetof(ChannelBuffer, length), 0, "Length in Samples"},
    {NULL}  /* Sentinel */
};

static PyMethodDef ChannelBuffer_methods[] = {
    {"writeData", (PyCFunction)ChannelBuffer_writeData, METH_VARARGS,
     "Description"
    },
    {NULL, NULL, 0, NULL}  /* Sentinel */
};

static struct PyModuleDef ChannelBuffer_module = {
    PyModuleDef_HEAD_INIT,
    "audioDevice",
    "Documentation",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

static PyTypeObject ChannelBuffer_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "audioDevice.ChannelBuffer",/* tp_name */
    sizeof(ChannelBuffer),      /* tp_basicsize */
    0,                          /* tp_itemsize */
    (destructor)ChannelBuffer_dealloc, /* tp_dealloc */
    0,                          /* tp_print */
    0,                          /* tp_getattr */
    0,                          /* tp_setattr */
    0,                          /* tp_reserved */
    0,                          /* tp_repr */
    0,                          /* tp_as_number */
    0,                          /* tp_as_sequence */
    0,                          /* tp_as_mapping */
    0,                          /* tp_hash  */
    0,                          /* tp_call */
    0,                          /* tp_str */
    0,                          /* tp_getattro */
    0,                          /* tp_setattro */
    0,                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,         /* tp_flags */
    "ChannelBuffer",            /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    ChannelBuffer_methods,             /* tp_methods */
    ChannelBuffer_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)ChannelBuffer_init,      /* tp_init */
    0,                         /* tp_alloc */
    ChannelBuffer_new,                 /* tp_new */
};

#endif

#include <Python.h>
#include "ChannelBuffer.h"

PyMethodDef audioDeviceModuleMethods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef audioDeviceModule = {
    PyModuleDef_HEAD_INIT,
    "audioDevice",
    "Documentation",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_audioDevice(void) {
    PyObject *object;

    ChannelBufferType.tp_new = PyType_GenericNew;
    if(PyType_Ready(&ChannelBufferType) < 0) {
        return NULL;
    }

    object = PyModule_Create(&audioDeviceModule);
    if(object == NULL) {
        return NULL;
    }

    Py_INCREF(&ChannelBufferType);
    PyModule_AddObject(object, "ChannelBuffer", (PyObject*)&ChannelBufferType);

    return object;
}
#include <Python.h>

#include "ChannelBuffer.h"
#include "AudioOutputOSX.h"

static PyMethodDef
AudioDevice_methods[] = {
    {"doStuff", AudioOutputOSX_doStuff, METH_VARARGS, "Documentation"},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef
AudioDevice_module = {
    PyModuleDef_HEAD_INIT,
    "audioDevice",
    "Documentation",
    -1,
    AudioDevice_methods
};

PyMODINIT_FUNC
PyInit_audioDevice(void) {
    PyObject *object = PyModule_Create(&AudioDevice_module);
    if(object == NULL) {
        return NULL;
    }

    // Not sure if we need this...
    // ChannelBuffer_type.tp_new = PyType_GenericNew;
    if(PyType_Ready(&ChannelBuffer_type) < 0) {
        return NULL;
    }

    Py_INCREF(&ChannelBuffer_type);
    PyModule_AddObject(object, "ChannelBuffer", (PyObject*)&ChannelBuffer_type);

    return object;
}

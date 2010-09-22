#include <Python.h>
#include <stdlib.h>
#include <string.h>
#include "ChannelBuffer.h"

/*
PyMODINIT_FUNC
PyInit_ChannelBuffer(void) {
    PyObject *object;

    // Not sure if we need this...
    // ChannelBuffer_type.tp_new = PyType_GenericNew;
    if(PyType_Ready(&ChannelBuffer_type) < 0) {
        return NULL;
    }

    object = PyModule_Create(&ChannelBuffer_module);
    if(object == NULL) {
        return NULL;
    }

    Py_INCREF(&ChannelBuffer_type);
    PyModule_AddObject(object, "ChannelBuffer", (PyObject*)&ChannelBuffer_type);

    return object;
}
*/

static PyObject*
ChannelBuffer_new(PyTypeObject *type, PyObject *args, PyObject *keywords) {
    printf("Hit new\n");
    ChannelBuffer* self = (ChannelBuffer*)type->tp_alloc(type, 0);
    if(self != NULL) {
        self->length = 0;
        self->sizeInBytes = self->length * sizeof(Sample);

      self->data[0] = NULL;
      self->data[1] = NULL;

        self->readPosition = 0;
        self->writePosition = 0;
    }

    return (PyObject*)self;
}

static int
ChannelBuffer_init(ChannelBuffer *self, PyObject *args, PyObject *keywords) {
    printf("Hit init\n");
    static char *keywordList[] = {"length", NULL};
    if(!PyArg_ParseTupleAndKeywords(args, keywords, "i", keywordList, &self->length)) {
        return -1;
    }

    if(self->length > 0) {
        self->sizeInBytes = self->length * sizeof(Sample);

        self->data[0] = (Sample*)malloc(self->sizeInBytes);
        memset(self->data[0], 0, self->sizeInBytes);

        self->data[1] = (Sample*)malloc(self->sizeInBytes);
        memset(self->data[1], 0, self->sizeInBytes);
      
      Py_INCREF(self->data);
    }

    return 0;
}

static void
ChannelBuffer_dealloc(ChannelBuffer *self) {
    printf("Hit dealloc\n");
    Py_XDECREF(self->data);
    free(self->data[0]);
    free(self->data[1]);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

BufferIndex advanceReadPosition(ChannelBuffer *buffer, BufferIndex numSamples) {
    // TODO: Hacky, not threadsafe, etc. etc.
    if(buffer->readPosition + numSamples > buffer->length) {
        buffer->readPosition = 0;
    }

    if(buffer->readPosition < buffer->writePosition && buffer->readPosition + numSamples > buffer->writePosition) {
        while(buffer->isWriting) {
            usleep(10);
        }
    }

    buffer->readPosition += numSamples;
    return buffer->readPosition;
}

static void
ChannelBuffer_writeData(ChannelBuffer *self, PyObject *args, void *closure) {
    const char *data;
    int numSamples;
    int ok, inputFrame, outputFrame;

    if(args == NULL) {
        PyErr_SetString(PyExc_TypeError, "Null buffer");
        return;
    }
    ok = PyArg_ParseTuple(args, "y#", &data, &numSamples);
    if(!ok) {
        printf("Failed parsing arguments: %d\n", ok);
        return;
    }

    if(self->writePosition + numSamples > self->length) {
        self->writePosition = 0;
    }

    self->isWriting = 1;
    for(inputFrame = 0, outputFrame = 0; inputFrame < numSamples; ++outputFrame) {
      self->data[0][outputFrame] = data[inputFrame++];
      self->data[1][outputFrame] = data[inputFrame++];
    }

    self->writePosition += numSamples;
    self->isWriting = 0;
}

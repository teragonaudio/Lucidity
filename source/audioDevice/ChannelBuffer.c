#include <Python.h>
#include <stdlib.h>
#include <string.h>
#include "ChannelBuffer.h"

static PyObject*
ChannelBuffer_new(PyTypeObject *type, PyObject *args, PyObject *keywords) {
    ChannelBuffer* self = (ChannelBuffer*)type->tp_alloc(type, 0);

    self->length = 0;
    self->sizeInBytes = self->length * sizeof(Sample);

    self->readPosition = 0;
    self->writePosition = 0;

    return (PyObject*)self;
}

static int
ChannelBuffer_init(ChannelBuffer *self, PyObject *args, PyObject *keywords) {
    static char *keywordList[] = {"length", NULL};
    if(!PyArg_ParseTupleAndKeywords(args, keywords, "i", keywordList, &self->length)) {
        return -1;
    }

    if(self->length > 0) {
        Py_INCREF(self->left);
        Py_INCREF(self->right);
        self->sizeInBytes = self->length * sizeof(Sample);
        self->left = (Sample*)malloc(self->sizeInBytes);
        memset(self->left, 0, self->sizeInBytes);
        self->right = (Sample*)malloc(self->sizeInBytes);
        memset(self->right, 0, self->sizeInBytes);
    }
}

static void
ChannelBuffer_dealloc(ChannelBuffer *self) {
    Py_XDECREF(self->left);
    Py_XDECREF(self->right);
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

void writeData(ChannelBuffer *buffer, Sample** data, BufferIndex numSamples) {
    BufferIndex i = 0;
    if(buffer->writePosition + numSamples > buffer->length) {
        buffer->writePosition = 0;
    }

    buffer->isWriting = 1;
    for(i = 0; i < numSamples; ++i) {
        buffer->left[i] = data[0][i];
        buffer->right[i] = data[0][i];
    }

    buffer->writePosition += numSamples;
    buffer->isWriting = 0;
}

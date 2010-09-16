#include <stdlib.h>
#include <string.h>

typedef unsigned short Sample;
typedef unsigned long BufferIndex;

/** Buffer representing one channel, 16-bit PCM data */
typedef struct _ChannelBuffer {
    Sample *left;
    Sample *right;
    BufferIndex length;
    unsigned long sizeInBytes;
    BufferIndex readPosition;
    BufferIndex writePosition;

    // TODO: This MUST be made atomic
    short isWriting;
} ChannelBuffer;

ChannelBuffer* createChannelBuffer(const unsigned long length) {
    ChannelBuffer* result = NULL;

    if(length > 0) {
        result = (ChannelBuffer*)malloc(sizeof(ChannelBuffer));
        result->length = length;
        result->sizeInBytes = length * sizeof(Sample);

        result->left = (Sample*)malloc(result->sizeInBytes);
        memset(result->left, 0, result->sizeInBytes);
        result->right = (Sample*)malloc(result->sizeInBytes);
        memset(result->right, 0, result->sizeInBytes);

        result->readPosition = 0;
        result->writePosition = 0;
    }

    return result;
}

void releaseChannelBuffer(ChannelBuffer *buffer) {
    if(buffer != NULL) {
        free(buffer->left);
        free(buffer->right);
        free(buffer);
    }
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

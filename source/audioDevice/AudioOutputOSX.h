/*
 *  AudioOutputOSX.h
 *  audioDevice
 *
 *  Created by Nik Reiman on 20/09/2010.
 *  Copyright 2010 Teragon Audio. All rights reserved.
 *
 */

#ifndef __AudioOutputOSX_h__
#define __AudioOutputOSX_h__

#include <Python.h>
#include <AudioUnit/AudioUnit.h>
#include "ChannelBuffer.h"

static PyObject*
AudioOutputOSX_doStuff(PyObject *self, PyObject *args);

OSStatus
AudioOutputOSX_render(void *inRefCon,
                      AudioUnitRenderActionFlags *ioActionFlags,
                      const AudioTimeStamp *inTimeStamp,
                      UInt32 inBusNumber,
                      UInt32 inNumberFrames,
                      AudioBufferList *ioData);

#endif

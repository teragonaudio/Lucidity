/*
 *  AudioOutputOSX.c
 *  audioDevice
 *
 *  Created by Nik Reiman on 20/09/2010.
 *  Copyright 2010 Teragon Audio. All rights reserved.
 *
 */

#include <CoreServices/CoreServices.h>
#include <stdio.h>
#include <unistd.h>

#include "AudioOutputOSX.h"

// Global variables (sigh, yes)
AudioUnit gOutputUnit;
ChannelBuffer *gChannelBuffer = NULL;

static PyObject*
AudioOutputOSX_doStuff(PyObject *self, PyObject *args) {
  OSStatus err = noErr;

  if(!PyArg_ParseTuple(args, "o", &gChannelBuffer)) {
    printf("Could not parse args\n");
    return Py_None;
  }

  if(gChannelBuffer == NULL) {
    printf("No channel buffer");
    return Py_None;
  }

  // Open the default output unit
  ComponentDescription desc;
  desc.componentType = kAudioUnitType_Output;
  desc.componentSubType = kAudioUnitSubType_DefaultOutput;
  desc.componentManufacturer = kAudioUnitManufacturer_Apple;
  desc.componentFlags = 0;
  desc.componentFlagsMask = 0;
  
  Component comp = FindNextComponent(NULL, &desc);
  if (comp == NULL) {
    printf ("FindNextComponent\n");
    return Py_None;
  }
  
  err = OpenAComponent(comp, &gOutputUnit);
  if (comp == NULL) {
    printf ("OpenAComponent=%d\n", err);
    return Py_None;
  }
  
  // Set up a callback function to generate output to the output unit
  AURenderCallbackStruct input;
  input.inputProc = AudioOutputOSX_render;
  input.inputProcRefCon = NULL;
  
  err = AudioUnitSetProperty (gOutputUnit,
                              kAudioUnitProperty_SetRenderCallback,
                              kAudioUnitScope_Input,
                              0,
                              &input,
                              sizeof(input));
  if (err) {
    printf ("AudioUnitSetProperty-CB=%d\n", err);
    return Py_None;
  }
  
  AudioStreamBasicDescription streamFormat;
  streamFormat.mSampleRate = 44100.0f;
  streamFormat.mFormatID = kAudioFormatLinearPCM;
  streamFormat.mFormatFlags = kAudioFormatFlagIsSignedInteger | kAudioFormatFlagsNativeEndian | kAudioFormatFlagIsPacked;
  streamFormat.mBytesPerPacket = 4;
  streamFormat.mFramesPerPacket = 1;
  streamFormat.mBytesPerFrame = 4;
  streamFormat.mChannelsPerFrame = 2;
  streamFormat.mBitsPerChannel = 16;
  
  printf("Rendering source:\n\t");
  printf ("SampleRate=%f,", streamFormat.mSampleRate);
  printf ("BytesPerPacket=%d,", streamFormat.mBytesPerPacket);
  printf ("FramesPerPacket=%d,", streamFormat.mFramesPerPacket);
  printf ("BytesPerFrame=%d,", streamFormat.mBytesPerFrame);
  printf ("BitsPerChannel=%d,", streamFormat.mBitsPerChannel);
  printf ("ChannelsPerFrame=%d\n", streamFormat.mChannelsPerFrame);
  
  err = AudioUnitSetProperty (gOutputUnit,
                              kAudioUnitProperty_StreamFormat,
                              kAudioUnitScope_Input,
                              0,
                              &streamFormat,
                              sizeof(AudioStreamBasicDescription));
  
  err = AudioOutputUnitStart (gOutputUnit);
  CFRunLoopRunInMode(kCFRunLoopDefaultMode, 2, false);

  // TODO: This code will be unreached
  verify_noerr (AudioOutputUnitStop (gOutputUnit));
  
  err = AudioUnitUninitialize (gOutputUnit);
  if (err) { printf ("AudioUnitUninitialize=%d\n", err); return Py_None; }
}

OSStatus
AudioOutputOSX_render(void *inRefCon,
                      AudioUnitRenderActionFlags *ioActionFlags,
                      const AudioTimeStamp *inTimeStamp,
                      UInt32 inBusNumber,
                      UInt32 inNumberFrames,
                      AudioBufferList *ioData) {
  int channel, frame;

  for(channel = 0; channel < ioData->mNumberBuffers; ++channel) {
    SInt16 *outputBuffer = ioData->mBuffers[channel].mData;
    for(frame = 0; frame < inNumberFrames; ++frame) {
      outputBuffer[frame] = gChannelBuffer->data[channel][frame];
      gChannelBuffer->data[channel][frame] = 0.0f;
    }
  }
  
  return noErr;
}

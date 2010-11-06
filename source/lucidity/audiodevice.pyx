import cython

cdef extern from "stdlib.h":
    void* malloc(size_t size)

# Generic Mac OSX Types
ctypedef signed short SInt16
ctypedef unsigned short UInt16
ctypedef signed int SInt32
ctypedef unsigned int UInt32
ctypedef SInt16 OSErr
ctypedef SInt32 OSStatus

# Carbon imports
cdef extern from "Carbon/Carbon.h":
    ctypedef struct ComponentInstanceRecord:
        long data[1]
    ctypedef ComponentInstanceRecord* ComponentInstance

# AudioUnit imports
cdef extern from "AudioUnit/AudioUnit.h":
    ctypedef struct ComponentDescription:
        long componentType
        long componentSubType
        long componentManufacturer
        int componentFlags
        int componentFlagsMask

    ctypedef UInt32 AudioUnitRenderActionFlags
    ctypedef struct AudioTimeStamp:
        pass

    ctypedef struct AudioBuffer:
        UInt32 mNumberChannels
        UInt32 mDataByteSize
        void* mData
    ctypedef struct AudioBufferList:
        UInt32 mNumberBuffers
        AudioBuffer mBuffers[1]

    ctypedef OSStatus (*AURenderCallback)(void* inRefCon,
        AudioUnitRenderActionFlags* ioActionFlags,
        AudioTimeStamp* inTimeStamp,
        UInt32 inBusNumber,
        UInt32 inNumberFrames,
        AudioBufferList* ioData)
    
    ctypedef struct AURenderCallbackStruct:
        AURenderCallback inputProc
        void* inputProcRefCon

    ctypedef ComponentInstanceRecord* AudioComponentInstance
    ctypedef AudioComponentInstance AudioUnit

    ctypedef UInt32 AudioUnitPropertyID
    ctypedef UInt32 AudioUnitScope
    ctypedef UInt32 AudioUnitElement
    cdef extern OSStatus AudioUnitSetProperty(AudioUnit inUnit,
        AudioUnitPropertyID inID,
        AudioUnitScope inScope,
        AudioUnitElement inElement,
        void* inData,
        UInt32 inDataSize)

    cdef long kAudioUnitType_Output
    cdef long kAudioUnitType_MusicDevice
    cdef long kAudioUnitType_MusicEffect
    cdef long kAudioUnitType_FormatConverter
    cdef long kAudioUnitType_Effect
    cdef long kAudioUnitType_Mixer
    cdef long kAudioUnitType_Panner
    cdef long kAudioUnitType_Generator
    cdef long kAudioUnitType_OfflineEffect

    cdef long kAudioUnitManufacturer_Apple

    cdef long kAudioUnitSubType_GenericOutput
    cdef long kAudioUnitSubType_HALOutput
    cdef long kAudioUnitSubType_DefaultOutput
    cdef long kAudioUnitSubType_SystemOutput
    cdef long kAudioUnitSubType_RemoteIO

    cdef int kAudioUnitScope_Global
    cdef int kAudioUnitScope_Input
    cdef int kAudioUnitScope_Output
    cdef int kAudioUnitScope_Group
    cdef int kAudioUnitScope_Part
    cdef int kAudioUnitScope_Note

    # TODO: There are lots more of these properties
    cdef int kAudioUnitProperty_SetRenderCallback

# CoreServices imports
cdef extern from "CoreServices/CoreServices.h":
    ctypedef struct ComponentRecord:
        pass
    ctypedef ComponentRecord* Component
    cdef extern Component FindNextComponent(Component aComponent, ComponentDescription *looking)
    cdef extern OSErr OpenAComponent(Component aComponent, ComponentInstance *ci)

ctypedef signed short Sample

# Globals
gOutputUnit = cython.declare(AudioUnit)

cdef class ChannelBuffer:
    cdef Sample *_data
    cdef long length

    def __init__(self, length):
        self.length = length
        self._data = <Sample*>malloc(sizeof(Sample) * length)
        for i in range(length):
            self._data[i] = 0

class AudioDeviceException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

cdef class AudioDeviceFactory:
    def getAudioDevice(self):
        import os
        sysname = os.uname()[0]
        if sysname == "Darwin":
            return AudioDeviceOSX()
        elif sysname == "Windows":
            return AudioDeviceASIO()
        else:
            return AudioDeviceUnavailable()

cdef class AudioDeviceOSX:
    def initialize(self):
        desc = cython.declare(ComponentDescription)
        desc.componentType = kAudioUnitType_Output
        desc.componentSubType = kAudioUnitSubType_DefaultOutput
        desc.componentManufacturer = kAudioUnitManufacturer_Apple
        desc.componentFlags = 0
        desc.componentFlagsMask = 0

        component = FindNextComponent(NULL, &desc)
        if component is NULL:
            print("Could not locate default audio device")
            return False

        err = OpenAComponent(component, &gOutputUnit)
        if component is NULL or err is not 0:
            print("Error opening default audio device")
            return False

        audioUnitCallback = cython.declare(AURenderCallbackStruct)
        audioUnitCallback.inputProc = audioDeviceRenderer
        audioUnitCallback.inputProcRefCon = NULL

        err = AudioUnitSetProperty(gOutputUnit, kAudioUnitProperty_SetRenderCallback,
            kAudioUnitScope_Input, 0, &audioUnitCallback, sizeof(audioUnitCallback))
        if err is not 0:
            print("Could not set output renderer")
            return False

        print("OMFG")
        return True

cdef api OSStatus audioDeviceRenderer(void* inRefCon,
    AudioUnitRenderActionFlags* ioActionFlags,
    AudioTimeStamp* inTimeStamp,
    UInt32 inBusNumber,
    UInt32 inNumberFrames,
    AudioBufferList* ioData):
    return 0

cdef class AudioDeviceASIO:
    def initialize(self):
        pass

cdef class AudioDeviceUnavailable:
    def initialize(self):
        raise AudioDeviceException("Audio device is unavailable on this platform")
        return None

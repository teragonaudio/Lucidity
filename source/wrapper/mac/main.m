//
//  main.m
//  Lucidity
//
//  Created by Nik Reiman on 14/01/2011.
//  Copyright 2011 Teragon Audio. All rights reserved.
//

#import <Cocoa/Cocoa.h>

int main(int argc, char *argv[]) {
  NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
  
  NSBundle *bundle = [NSBundle mainBundle];
  NSURL *resourcesPath = [[bundle resourceURL] absoluteURL];
  NSURL *pythonPath = [resourcesPath URLByAppendingPathComponent:@"python3.1"];
  NSURL *lucidityPath = [resourcesPath URLByAppendingPathComponent:@"main.py"];
  NSArray *arguments = [NSArray arrayWithObject:[lucidityPath path]];

  NSTask *task = [[[NSTask alloc] init] autorelease];
  [task setLaunchPath:[pythonPath path]];
  [task setArguments:arguments];
  [task setCurrentDirectoryPath:[resourcesPath path]];
  [task launch];
  [task waitUntilExit];
  
  [pool release];
  return 0;
}

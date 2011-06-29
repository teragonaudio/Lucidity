#!/bin/bash

# TODO: Should not be like this, heh
LUCIDITY_ROOT=`pwd`
BUILD_DIR=$LUCIDITY_ROOT/build
BUILD_LOG=$BUILD_DIR/build.log
BUILD_CONFIG=Release
BUILT_PRODUCTS_DIR=$BUILD_DIR/$BUILD_CONFIG
UNLOCALIZED_RESOURCES_FOLDER_PATH=Lucidity.app/Contents/Resources
RESOURCES_INSTALL_DIR=$BUILT_PRODUCTS_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH

PYTHON_DEST=$RESOURCES_INSTALL_DIR/python
PYTHONEXE=$RESOURCES_INSTALL_DIR/python3.1

FRAMEWORKS_FOLDER_PATH=Lucidity.app/Contents/Frameworks
FRAMEWORKS_INSTALL_DIR=$BUILT_PRODUCTS_DIR/$FRAMEWORKS_FOLDER_PATH

function startTask() {
  TASK=$1
  echo "== Building $TASK =="

  echo >> $BUILD_LOG
  echo >> $BUILD_LOG
  echo "== Building $TASK ==" >> $BUILD_LOG
}

function startSubTask() {
  TASK=$1
  echo "--- $TASK ---"
  echo "--- $TASK ---" >> $BUILD_LOG
}

function endSubTask() {
  if [ $? -ne 0 ]
  then
    printf "*** Failed ***\n" $BUILD_LOG
    exit $?
  fi
}

function skipTask() {
  TASK=$1
  echo "---- $TASK already installed, skipping ----"
  echo "---- $TASK already installed, skipping ----" >> $BUILD_LOG
}

function help() {
  printf "Options are: \n"
  printf "  - %s: %s\n" \
    "build" "Build the entire app" \
    "clean" "Remove all build files" \
    "full" "Perform a complete rebuild" \
    "dmg" "Make a distribution disk image" \
    "wtf" "Go to the first error in the build log" \
    "help" "This screen"
  exit 1
}

function clean() {
  echo "== Cleaing =="
  rm -rf $BUILD_DIR
}

function buildPython() {
  startTask "Python"
  if ! [ -e $PYTHON_DEST ] ; then
    startSubTask "Untarring"
    tar xj -C $BUILT_PRODUCTS_DIR -f ./third-party/python/Python-*.tar.bz2
    cd $BUILT_PRODUCTS_DIR/Python-*

    startSubTask "Configuring"
    ./configure --prefix=$PYTHON_DEST --with-wide-unicode >> $BUILD_LOG 2>&1
    endSubTask

    startSubTask "Compiling"
    make -j2 >> $BUILD_LOG 2>&1
    endSubTask

    startSubTask "Installing"
    make install >> $BUILD_LOG 2>&1
    endSubTask

    # Link python here so we don't run into weird linker errors
    # Mac OSX assumes that frameworks and dylibs will all be found
    # relative to the parent directory of executables in a bundle
    startSubTask "Linking"
    ln -s $PYTHON_DEST/bin/python3.1 $PYTHONEXE
    endSubTask
  else
    skipTask "Python"
  fi
}

function buildPythonDependencies() {
  cd $LUCIDITY_ROOT
  for x in ./third-party/python-deps/*.gz ; do
    libname=`basename $x | rev | cut -f 3- -d '.' | rev`
    startTask "$libname"
    if ! [ -e $BUILT_PRODUCTS_DIR/$libname ] ; then
      BUILD_ARGS=""
      if [ `echo $libname | cut -f 1 -d '-'` = "numpy" ] ; then
        BUILD_ARGS="--fcompiler=gfortran"
      fi

      cd $LUCIDITY_ROOT
      startSubTask "Untarring"
      tar xz -C $BUILT_PRODUCTS_DIR -f $x
      endSubTask

      cd $BUILT_PRODUCTS_DIR/$libname
      startSubTask "Compiling"
      $PYTHONEXE setup.py build $BUILD_ARGS >> $BUILD_LOG 2>&1
      endSubTask

      startSubTask "Installing"
      $PYTHONEXE setup.py install >> $BUILD_LOG 2>&1
      endSubTask
    else
      skipTask "$libname"
    fi
  done
}

function buildSDLDependencies() {
  cd $LUCIDITY_ROOT
  for x in ./third-party/SDL-deps/*.dmg ; do
    libname=`basename $x | cut -f 1 -d '-'`
    startTask "$libname"
    if ! [ -e $FRAMEWORKS_INSTALL_DIR/$libname.framework ] ; then
      startSubTask "Mounting"
      hdiutil attach $x >> $BUILD_LOG
      endSubTask

      startSubTask "Copying Framework"
      cp -rp /Volumes/$libname/$libname.framework $FRAMEWORKS_INSTALL_DIR
      endSubTask

      startSubTask "Unmounting"
      hdiutil detach /Volumes/$libname >> $BUILD_LOG
      endSubTask
    else
      skipTask "$libname"
    fi
  done
}

function buildSDL() {
  cd $LUCIDITY_ROOT
  startSubTask "Compiling"
  xcodebuild -workspace ./third-party/SDL/Xcode/SDL/SDL.xcodeproj/project.xcworkspace -scheme Framework -configuration Release install >> $BUILD_LOG
  endSubTask

  startSubTask "Installing"
  if ! [ -e $FRAMEWORKS_INSTALL_DIR ] ; then
    mkdir $FRAMEWORKS_INSTALL_DIR
  fi

  cp -rp ./third-party/SDL/Xcode/SDL/build/Frameworks/SDL.framework $FRAMEWORKS_INSTALL_DIR 
  endSubTask
}

function buildPygameDependencies() {
  cd $LUCIDITY_ROOT
  for x in ./third-party/pygame-deps/*.gz ; do
    libname=`basename $x | rev | cut -f 3- -d '.' | rev`
    startTask "$libname"
    UNTAR_DIR=$BUILT_PRODUCTS_DIR/$libname

    if [ `echo $libname | grep 'freetype'` ] ; then
      # Freetype has a stupid makefile config error where it fails
      # to remove this directory because it does not exist.  Lame++
      mkdir -p $RESOURCES_INSTALL_DIR/include/freetype2/freetype/internal
    elif [ `echo $libname | grep 'jpeg'` ] ; then
      # libjpg untars itself to a non-standard name
      UNTAR_DIR=$BUILT_PRODUCTS_DIR/jpeg-8b
    fi

    cd $LUCIDITY_ROOT
    if ! [ -e $UNTAR_DIR ] ; then
      startSubTask "Untarring"
      tar xz -C $BUILT_PRODUCTS_DIR -f $x
      endSubTask

      cd $UNTAR_DIR
      startSubTask "Configuring"
      ./configure --prefix=$RESOURCES_INSTALL_DIR >> $BUILD_LOG 2>&1
      endSubTask

      startSubTask "Compiling"
      make -j2 >> $BUILD_LOG 2>&1
      endSubTask

      startSubTask "Installing"
      make install >> $BUILD_LOG 2>&1
      endSubTask
    else
      skipTask "$libname"
    fi
  done
}

function buildPortMidi() {
  cd $LUCIDITY_ROOT/third-party/portmidi/pm_mac
  startTask "PortMidi"

  if ! [ -e $BUILT_PRODUCTS_DIR/portmidi ] ; then
    startSubTask "Cleaning"
    make clean >> $BUILD_LOG 2>&1
    endSubTask

    startSubTask "Compiling"
    make >> $BUILD_LOG 2>&1
    endSubTask

    startSubTask "Installing"
    cp libportmidi.a $RESOURCES_INSTALL_DIR/lib/libportmidi.a
    endSubTask
  else
    skipTask "PortMidi"
  fi
}

function buildPygame() {
  startTask "Pygame"
  if ! [ -e $PYTHON_DEST/lib/python3.1/site-packages/pygame ] ; then
    cd $LUCIDITY_ROOT/third-party/pygame
    startSubTask "Cleaning"
    rm -rf Setup build >> $BUILD_LOG
    endSubTask

    PATH=$PATH:$RESOURCES_INSTALL_DIR/bin
    startSubTask "Configuring"
    $PYTHONEXE config.py $RESOURCES_INSTALL_DIR $FRAMEWORKS_INSTALL_DIR /System/Library/Frameworks >> $BUILD_LOG 2>&1
    endSubTask

    startSubTask "Compiling"
    $PYTHONEXE setup.py build >> $BUILD_LOG 2>&1
    endSubTask

    startSubTask "Installing"
    $PYTHONEXE setup.py install >> $BUILD_LOG 2>&1
    endSubTask
  else
    skipTask "PyGame"
  fi
}

function buildId3Reader {
  startTask "id3reader"
  cd $LUCIDITY_ROOT/third-party/id3reader

  startSubTask "Cleaning"
  $PYTHONEXE setup.py clean >> $BUILD_LOG
  endSubTask

  startSubTask "Compiling"
  $PYTHONEXE setup.py build >> $BUILD_LOG
  endSubTask

  startSubTask "Installing"
  $PYTHONEXE setup.py install >> $BUILD_LOG
  endSubTask
}

function buildLucidityModules() {
  startTask "Lucidity Modules"
  cd $LUCIDITY_ROOT/source

  startSubTask "Cleaning"
  $PYTHONEXE setup.py clean >> $BUILD_LOG
  endSubTask

  startSubTask "Compiling"
  $PYTHONEXE setup.py build >> $BUILD_LOG
  endSubTask

  startSubTask "Installing"
  $PYTHONEXE setup.py install >> $BUILD_LOG
  endSubTask
}

function buildLucidityResources() {
  startTask "Resources"
  cp -r $LUCIDITY_ROOT/resources $RESOURCES_INSTALL_DIR
}

function buildWrapper() {
  startTask "Wrapper"
  startSubTask "Compiling"
  xcodebuild -configuration $BUILD_CONFIG -project ./source/wrapper/mac/Lucidity.xcodeproj >> $BUILD_LOG
  endSubTask
}

function buildAll() {
  [ ! -e $BUILD_DIR ] && mkdir $BUILD_DIR

  buildWrapper
  buildPython
  buildPythonDependencies
  buildSDL
  buildSDLDependencies
  buildPygameDependencies
  buildPortMidi
  buildPygame
  buildId3Reader
  buildLucidityModules
  buildLucidityResources

  growlnotify -a "Lucidity Builder" -m "Build successful" --image $LUCIDITY_ROOT/icon.png "Build Status"
}

function makeDmg() {
  startTask "DMG"
  # TODO: Bah, need to get this script from Xcode
}

case $1 in
  "") buildAll ;;
  "build") buildAll ;;
  "clean") clean ;;
  "full") clean && buildAll ;;
  "dmg") clean && buildAll && makeDmg ;;
  "wtf") less -p 'error:' $BUILD_LOG ;;
  *) help ;;
esac

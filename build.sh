#!/bin/bash

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

function skipTask() {
  TASK=$1
  echo "---- $TASK already installed, skipping ----"
  echo "---- $TASK already installed, skipping ----" >> $BUILD_LOG
}

function help() {
  echo "God helps those who help themselves"
  exit
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
    startSubTask "Compiling"
    make -j2 >> $BUILD_LOG 2>&1
    startSubTask "Installing"
    make install >> $BUILD_LOG 2>&1
    # Link python here so we don't run into weird linker errors
    # Mac OSX assumes that frameworks and dylibs will all be found
    # relative to the parent directory of executables in a bundle
    startSubTask "Linking"
    ln -s $PYTHON_DEST/bin/python3.1 $PYTHONEXE
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
      cd $BUILT_PRODUCTS_DIR/$libname
      startSubTask "Compiling"
      $PYTHONEXE setup.py build $BUILD_ARGS >> $BUILD_LOG 2>&1
      startSubTask "Installing"
      $PYTHONEXE setup.py install >> $BUILD_LOG 2>&1
    else
      skipTask "$libname"
    fi
  done
}

function buildSDLDependencies() {
  for x in ./third-party/SDL-deps/*.dmg ; do
    libname=`basename $x | cut -f 1 -d '-'`
    startTask "$libname"
    if ! [ -e $FRAMEWORKS_INSTALL_DIR/$libname.framework ] ; then
      startSubTask "Mounting"
      hdiutil attach $x >> $BUILD_LOG
      startSubTask "Copying Framework"
      cp -rp /Volumes/$libname/$libname.framework $FRAMEWORKS_INSTALL_DIR
      startSubTask "Unmounting"
      hdiutil detach /Volumes/$libname >> $BUILD_LOG
    else
      skipTask "$libname"
    fi
  done
}

function buildSDL() {
  cd $LUCIDITY_ROOT
  xcodebuild -workspace ./third-party/SDL/Xcode/SDL/SDL.xcodeproj/project.xcworkspace -scheme Framework -configuration Release install >> $BUILD_LOG
  if ! [ -e $FRAMEWORKS_INSTALL_DIR ] ; then
    mkdir $FRAMEWORKS_INSTALL_DIR
  fi

  cp -rp ./third-party/SDL/Xcode/SDL/build/Frameworks/SDL.framework $FRAMEWORKS_INSTALL_DIR 
}

function buildPygameDependencies() {
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

    if ! [ -e $UNTAR_DIR ] ; then
      startSubTask "Untarring"
      tar xz -C $BUILT_PRODUCTS_DIR -f $x
      cd $UNTAR_DIR
      startSubTask "Configuring"
      ./configure --prefix=$RESOURCES_INSTALL_DIR >> $BUILD_LOG 2>&1
      startSubTask "Compiling"
      make -j2 >> $BUILD_LOG 2>&1
      startSubTask "Installing"
      make install >> $BUILD_LOG 2>&1
    else
      skipTask "$libname"
    fi
  done
}

function buildWrapper() {
  startTask "Wrapper"
  startSubTask "Compiling"
  xcodebuild -configuration $BUILD_CONFIG -project ./source/wrapper/mac/Lucidity.xcodeproj >> $BUILD_LOG
}

function buildAll() {
  buildWrapper
  buildPython
  buildPythonDependencies
  buildSDL
  buildSDLDependencies
  buildPygameDependencies
}

function makeDmg() {
  startTask "DMG"
}

if [ ! -e $BUILD_DIR ] ; then
  mkdir $BUILD_DIR
  echo -n > $BUILD_LOG
fi

if [ -z "$1" ] ; then
  time buildAll
elif [ $1 = "clean" ] ; then
  clean
elif [ $1 = "build" ] ; then
  time buildAll
elif [ $1 = "full" ] ; then
  clean
  build
  makeDmg
elif [ $1 = "help" ] ; then
  help
else
  help
fi

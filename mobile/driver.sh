#!/bin/sh

# A hudson build driver for Titanium Mobile 

export PATH=/bin:/usr/bin:$PATH
scons package_all=1

GIT_BRANCH=$1
GIT_REVISION=`git log --pretty=oneline -n 1 | sed 's/ .*//' | tr -d '\n' | tr -d '\r'`
VERSION=`python $TITANIUM_BUILD/common/get_version.py | tr -d '\r'`
TIMESTAMP=`date +'%Y%m%d%H%M%S'`
BASENAME=dist/mobilesdk-$VERSION-$TIMESTAMP

mv dist/mobilesdk-$VERSION-osx.zip $BASENAME-osx.zip
mv dist/mobilesdk-$VERSION-win32.zip $BASENAME-win32.zip
mv dist/mobilesdk-$VERSION-linux.zip $BASENAME-linux.zip

python $TITANIUM_BUILD/common/s3_cleaner.py mobile $GIT_BRANCH
python $TITANIUM_BUILD/common/s3_uploader.py mobile $BASENAME-osx.zip $GIT_BRANCH $GIT_REVISION $BUILD_URL
python $TITANIUM_BUILD/common/s3_uploader.py mobile $BASENAME-linux.zip $GIT_BRANCH $GIT_REVISION $BUILD_URL
python $TITANIUM_BUILD/common/s3_uploader.py mobile $BASENAME-win32.zip $GIT_BRANCH $GIT_REVISION $BUILD_URL

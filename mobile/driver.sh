#!/bin/sh

# A hudson build driver for Titanium Mobile 

export PATH=/bin:/usr/bin:$PATH

driver_dir=`dirname $0`
root_dir=`python $driver_dir/root.py | tr -d '\r' | tr -d '\n'`

scons package_all=1

GIT_REVISION=`git log --pretty=oneline -n 1 | sed 's/ .*//' | tr -d '\n' | tr -d '\r'`
VERSION=`python $root_dir/common/get_version.py | tr -d '\r'`
TIMESTAMP=`date +'%Y%m%d%H%M%S'`
BASENAME=dist/mobilesdk-$VERSION-$TIMESTAMP

mv dist/mobilesdk-$VERSION-osx.zip $BASENAME-osx.zip
mv dist/mobilesdk-$VERSION-win32.zip $BASENAME-win32.zip
mv dist/mobilesdk-$VERSION-linux.zip $BASENAME-linux.zip

python $root_dir/common/s3_cleaner.py $AWS_KEY $AWS_SECRET mobile
python $root_dir/common/s3_uploader.py $AWS_KEY $AWS_SECRET mobile $BASENAME-osx.zip $GIT_REVISION $BUILD_URL
python $root_dir/common/s3_uploader.py $AWS_KEY $AWS_SECRET mobile $BASENAME-linux.zip $GIT_REVISION $BUILD_URL
python $root_dir/common/s3_uploader.py $AWS_KEY $AWS_SECRET mobile $BASENAME-win32.zip $GIT_REVISION $BUILD_URL

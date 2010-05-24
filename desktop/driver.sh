#!/bin/sh

# A hudson build driver for Titanium Desktop
export PATH=/bin:/usr/bin:$PATH
GIT_REVISION=`git log --pretty=oneline -n 1 | sed 's/\s.*//' | tr -d '\r' | tr -d '\n'`
GIT_REVISION=${GIT_REVISION:0:8}
VERSION=`python -c 'import sdk; print sdk.get_titanium_version()' | tr -d '\r' | tr -d '\n'`
PLATFORM=`python -c "import platform; print ({'Darwin':'osx','Windows':'win32','Linux':'linux'})[platform.system()]" | tr -d '\r' | tr -d '\n'`
TIMESTAMP=`date +'%Y%m%d%H%M%S'`

if [ "$PLATFORM" = "win32" ]; then
	DRILLBIT_APP=Drillbit
	DRILLBIT_EXE=Drillbit.exe
elif [ "$PLATFORM" = "osx" ]; then
	DRILLBIT_APP=Drillbit.app/Contents/MacOS
	DRILLBIT_EXE=Drillbit
else
	DRILLBIT_APP=Drillbit
	DRILLBIT_EXE=Drillbit
fi

# force kroll onto master for now
cd kroll && git checkout master && git pull && cd ../
scons -j $NUM_CPUS debug=1 breakpad=0 drillbit dist || exit
./build/$PLATFORM/$DRILLBIT_APP/$DRILLBIT_EXE --autorun --autoclose

mkdir -p drillbit_results
$TITANIUM_BUILD/desktop/drillbit_collector.py > drillbit_results/index.html

TIMESTAMP_NAME=build/$PLATFORM/dist/sdk-$VERSION-$TIMESTAMP-$PLATFORM.zip
mv build/$PLATFORM/dist/sdk-$VERSION-$PLATFORM.zip $TIMESTAMP_NAME

python $TITANIUM_BUILD/common/s3_cleaner.py $AWS_KEY $AWS_SECRET desktop
python $TITANIUM_BUILD/common/s3_uploader.py $AWS_KEY $AWS_SECRET desktop $TIMESTAMP_NAME

#!/bin/sh

GIT_BRANCH=$1

if [ "$NODE_NAME" = "Win32 Slave" ]; then
	export PATH=/bin:/usr/bin:$PATH
	export APPDATA="C:\\Documents and Settings\All Users"
	export MSPSDK="D:\\Program Files\\Microsoft Platform SDK for Windows Server 2003 R2"
	export MSVS="D:\\Program Files\\Microsoft Visual Studio 8"

	$TITANIUM_BUILD/desktop/driver.sh $GIT_BRANCH
elif [ "$NODE_NAME" = "linux" ]; then
	$TITANIUM_BUILD/desktop/driver.sh $GIT_BRANCH 
fi

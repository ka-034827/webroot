#!/run/current-system/sw/bin/bash

SRDFDIR='/webroot'			# Direcotry for srdf application execution

cd $SRDFDIR				# Changing over to application directory

sqlite3 srdfData.db < srdfDBSchema.sql	# Setting up Sqlite Database



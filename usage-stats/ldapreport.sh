#!/bin/bash

if [ -e $1 ]
then
	exec < $1
else
	echo "Missing filename"
	exit 1
fi

#set -x

LDAPFIELDS="uid sn givenName uvaDisplayDepartment description"

while read USERNAME
do
	RECORD=$(ldapsearch -x -LLL -h ldap.virginia.edu -b "o=University of Virginia,c=US" uid=$USERNAME $LDAPFIELDS)
	LUSER=$USERNAME
	LNAME="(unknown)"
	FNAME="(unknown)"
	DEPT="(unknown)"
	echo "$RECORD" | ( while read FIELD VALUE
	do
		case ${FIELD} in
		uid:)
			LUSER=$VALUE
			;;
		sn:)
			LNAME=$VALUE
			;;
		givenName:)
			FNAME=$VALUE
			;;
		uvaDisplayDepartment:)
			DEPT="$VALUE"
			;;
		description:)
			POSITION="$POSITION,$VALUE"
			;;
		esac
	done
	POSITION=${POSITION:-(unknown)}
	echo "\"$LUSER\",\"$LNAME\",\"$FNAME\",\"$DEPT\",\"${POSITION#,}\"" )
done



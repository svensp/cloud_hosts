#!/bin/bash
################################################################################
#
# Filesystem plugin to mysql_backup
#
# DESCRIBE PLUGIN
#
################################################################################

# Use Variables with default values like this to let parameter be overriden
VARIABLE=${VARIABLE:-Default Value}

#
# fs_upload
#
# Upload a directory to a given identifier name
#
# Parameters:
#   DIRECTORY  - The directory to upload
#   IDENTIFIER - The identifier to which the directory is uploaded
#
fs_upload() {

	local DIRECTORY="${1}"

	local IDENTIFIER="${2}"

	if [ -z "${DIRECTORY}" ] ; then
		log ${LOG_ERROR} "fs_upload: Directory parameter not given"
		exit 2;
	fi

	if [ -z "${IDENTIFIER}" ] ; then
		log ${LOG_ERROR} "fs_upload: Identifier parameter not given"
		exit 2;
	fi

}

#
# fs_download
#
# Download the full backup with the given identifier
#
# Parameters:
#   IDENTIFIER - The identifier to which the directory is uploaded
#   DIRECTORY  - The directory download into
fs_download() {


	local IDENTIFIER="${1}"

	local TARGET_DIRECTORY="${2}"

	if [ -z "${IDENTIFIER}" ] ; then
		log ${LOG_ERROR} "fs_download: Identifier parameter not given"
		exit 2;
	fi

	if [ -z "${TARGET_DIRECTORY}" ] ; then
		log ${LOG_ERROR} "fs_download: Directory parameter not given"
		exit 2;
	fi

}

#
# fs_cat
#
# Output the content of the given file from the directory uploaded with identifier
# If the file does not exist then an empty line is outputed
#
# Parameters:
#   IDENTIFIER - The identifier to which the directory is uploaded
#   FILE       - The file to output
#
fs_cat() {
	local IDENTIFIER="${1}"

	local FILE="${2}"

	if [ -z "${IDENTIFIER}" ] ; then
		log ${LOG_ERROR} "fs_cat: Identifier parameter not given"
		exit 2;
	fi

	if [ -z "${FILE}" ] ; then
		log ${LOG_ERROR} "fs_cat: File parameter not given"
		exit 2;
	fi

	return 0
}

#
# fs_list
#
# Output all available identifiers, one per line
#
# Parameters: NONE
#
fs_list() {
}

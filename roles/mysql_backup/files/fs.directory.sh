#!/bin/bash
################################################################################
#
# Filesystem plugin to mysql_backup
#
# Saves and reads from a directory in the filesystem
#
################################################################################

DIRECTORY_PATH=${DIRECTORY_PATH:-/backup}
DIRECTORY_USER=${DIRECTORY_USER:-}
DIRECTORY_GROUP=${DIRECTORY_GROUP:-}

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

	TARGET="${DIRECTORY_PATH}/${IDENTIFIER}"
	cp -R "${DIRECTORY}/." "${TARGET}"

	if [ ! -z "${DIRECTORY_USER}" ] ; then
		chown -R "${DIRECTORY_USER}" "${TARGET}"
	fi
	if [ ! -z "${DIRECTORY_GROUP}" ] ; then
		chgrp -R "${DIRECTORY_GROUP}" "${TARGET}"
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

	SOURCE="${DIRECTORY_PATH}/${IDENTIFIER}"

	if [ ! -d "${TARGET_DIRECTORY}" ] ; then
		mkdir -p "${TARGET_DIRECTORY}"
	fi

	cp -R "${SOURCE}/." "${TARGET_DIRECTORY}"
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

	TARGET="${DIRECTORY_PATH}/${IDENTIFIER}"
	if [ ! -d "${TARGET}" ] ; then
		log ${LOG_WARNING} Identifier ${IDENTIFIER} does not exist
		return 2
	fi

	if [ ! -f "${TARGET}/${FILE}" ] ; then
		echo ""
		return 0
	fi

	cat "${TARGET}/${FILE}"
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
	find "${DIRECTORY_PATH}" -mindepth 1 -maxdepth 1 -type d -printf "%f\n"
}

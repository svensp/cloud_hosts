#!/bin/bash
################################################################################
#
# Filesystem plugin to mysql_backup
#
# Saves and reads via sftp / scp
# Use Case: save to hetzner storagebox
# 
################################################################################

if [ -f "${DEFAULTS}" ] ; then
	. "${DEFAULTS}"
fi

# Use Variables with default values like this to let parameter be overriden
SFTP_SERVER=${SFTP_SERVER:-localhost}
SFTP_ROOT_DIRECTORY=${SFTP_ROOT_DIRECTORY:-/}
SFTP_USER=${SFTP_USER:-}
SFTP_PASSWORD=${SFTP_PASSWORD:-}
SFTP_KEY=${SFTP_KEY:-/usr/local/lib/mysql_backup/key}


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

	if ! ( fs_list | grep -E -q "^${IDENTIFIER}$" ) ; then
		(sftp -i "${SFTP_KEY}" -b - \
			"${SFTP_USER}@${SFTP_SERVER}:${SFTP_ROOT_DIRECTORY}" > /dev/null ) <<< "mkdir ${IDENTIFIER}"
	fi
	scp -q -r -i "${SFTP_KEY}" \
		"${DIRECTORY}/." \
		"${SFTP_USER}@${SFTP_SERVER}:${SFTP_ROOT_DIRECTORY}/${IDENTIFIER}"

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

	scp -q -r -i "${SFTP_KEY}" \
		"${SFTP_USER}@${SFTP_SERVER}:${SFTP_ROOT_DIRECTORY}/${IDENTIFIER}/." \
		"${TARGET_DIRECTORY}" 
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

	scp -q -i "${SFTP_KEY}" \
		"${SFTP_USER}@${SFTP_SERVER}:${SFTP_ROOT_DIRECTORY}/${IDENTIFIER}/${FILE}" \
		"/dev/stdout" || echo ''

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
	(sftp -i "${SFTP_KEY}" -b - \
		"${SFTP_USER}@${SFTP_SERVER}:${SFTP_ROOT_DIRECTORY}"  | grep -v '^sftp>' ) <<< "ls -1"
}

#
# fs_delete
#
# Delete a backup with the given identifier
#
# Parameters:
#   IDENTIFIER - The identifier of the backup to be deleted
#
fs_delete() {
	local IDENTIFIER="${1}"

	if [ -z "${IDENTIFIER}" ] ; then
		log "${LOG_ERROR}" "fs_delete: Identifier parameter not given"
		exit 2;
	fi
	
	LFTP_PASSWORD= lftp \
		-c "set sftp:connect-program \"ssh -a -x -i ${SFTP_KEY}\" \
		; connect --env-password sftp://${SFTP_USER}@${SFTP_SERVER}/${SFTP_ROOT_DIRECTORY} \
		; rm -r ${IDENTIFIER}"


	return 0
}

#!/bin/bash
set -eo pipefail

FILENAME="kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz"
MIRROR_URL="https://www.apache.org/dyn/closer.lua?path=/kafka/${KAFKA_VERSION}/${FILENAME}&as_json=1"
ARCHIVE_URL="https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/${FILENAME}"

# Check required tools
command -v curl >/dev/null || { echo "curl required"; exit 1; }
command -v jq >/dev/null || { echo "jq required"; exit 1; }

# Get download URL
url=$(curl -sSf "$MIRROR_URL" | jq -r '"\(.preferred)\(.path_info)"')

# Verify mirror availability
if ! curl -sSf -r 0-100 "${url}" >/dev/null; then
    echo "Using archive URL"
    url="$ARCHIVE_URL"
fi

echo "Downloading Kafka from $url"
curl -sSfL "$url" -o "/tmp2/${FILENAME}"

# Checksum verification
if curl -sSfL "$checksum_url" -o "/tmp2/${FILENAME}.sha512"; then
    echo "Verifying checksum"
    
    # Extract published checksum (all lines, remove filename and spaces)
    published_checksum=$(cat "/tmp2/${FILENAME}.sha512" | sed 's/.*://' | tr -d ' \n')
    
    # Calculate actual checksum
    calculated_checksum=$(sha512sum "/tmp2/${FILENAME}" | awk '{print $1}')

    # Compare values (case-insensitive)
    if [ "${published_checksum,,}" = "${calculated_checksum,,}" ]; then
        echo "Checksum verified successfully"
    else
        echo "Checksum verification failed:"
        echo "Expected: $published_checksum"
        echo "Actual:   $calculated_checksum"
        exit 1
    fi
else
    echo "Warning: Skipping checksum verification - unable to download .sha512 file"
fi


echo "Download completed successfully"
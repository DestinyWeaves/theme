#!/bin/bash

set -x
shopt -s globstar extglob

site_path="$1"
url_prefix="$2"

mkdir -p "${site_path}/flat"

for filename in ${site_path}/assets/**/*.@(js|css|jpg|png); do
    orig_name="${filename/#$site_path\/assets\/}"
    flat_name="${orig_name//\//__}"

    # copy to the flattened asset location
    cp "${filename}" "${site_path}/flat/${flat_name}"

    rlink_name="/assets/${orig_name}"
    asset_name="${url_prefix}/${flat_name}"

    # replace the generated links with links to the flattened asset location
    find "${site_path}" -type f -exec sed -i "s#${rlink_name}#${asset_name}#" {} +

done
#!/bin/bash

set -x
shopt -s globstar extglob

replace_token="$1"
site_path="$2"
flat_path="$3"
url_prefix="$4"

mkdir -p "${flat_path}"

for filename in ${site_path}/assets/**/*.@(js|css|jpg|png); do
    orig_name="${filename/#$site_path\/assets\/}"
    flat_name="${orig_name//\//__}"

    # copy to the flattened asset location
    cp "${filename}" "${flat_path}/${flat_name}"

    rlink_name="/${replace_token}/assets/${orig_name}"
    asset_name="${url_prefix}/${flat_name}"

    # replace the generated links with links to the flattened asset location
    find "${site_path}" -type f -exec sed -i "s#${rlink_name}#${asset_name}#" {} +

done
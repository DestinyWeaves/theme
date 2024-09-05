#!/bin/bash

set -x
shopt -s globstar extglob

site_path="$1"
url_prefix="$2"
ver_name="$3"

ver_slug="${ver_name//-/_}"

mkdir -p "${site_path}/files/assets_${ver_slug}"

for filename in ${site_path}/assets/**/*.@(js|css|jpg|png); do
    orig_name="${filename/#$site_path\/assets\/}"
    flat_name="${orig_name}"
    flat_name="${flat_name//\//__}"
    flat_name="${flat_name//-/_}"


    # copy to the flattened asset location
    mkdir -p "$(dirname "${site_path}/files/assets_${ver_slug}/${flat_name}")"
    cp "${filename}" "${site_path}/files/assets_${ver_slug}/${flat_name}"

    rlink_name="/assets/${orig_name}"
    asset_name="${url_prefix}/assets_${ver_slug}/${flat_name}"

    # replace the generated links with links to the flattened asset location
    find "${site_path}" -type f -exec grep -Iq . {} \; -and -exec sed -i "s#${rlink_name}#${asset_name}#" {} +

done
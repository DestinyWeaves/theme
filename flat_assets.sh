#!/bin/bash

set +x

replace_token="$1"
site_path="$2"
flat_path="$3"
url_prefix="$4"

mkdir -p "${flat_path}"

while IFS= read -r -d '' -u 9
do
    orig_name="${REPLY}"
    flat_name="${REPLY//\//__}"

    # copy to the flattened asset location
    cp "${orig_name}" "${flat_path}/${flat_name}"

    rlink_name="/${replace_token}/${orig_name}"
    asset_name="${url_prefix}/${flat_name}"

    # replace the generated links with links to the flattened asset location
    find "${site_path}" -type f -exec sed -i "s#${rlink_name}#${flat_name}#" {} +

done <(
    find "${site_path}/assets/" -type f \( \
        -iname \*.jpg -o -iname \*.png -o -iname \*.css -o -iname \*.js -o -iname \*.json \
    \) -exec printf '%s\0' {} +
)
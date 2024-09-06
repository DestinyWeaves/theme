#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

set -e -x

asset_url_prefix="https://files.jcink.net/uploads2/ajmansfieldtestboard"
theme_name=just-the-docs

bundle exec jekyll build

"$SCRIPT_DIR/flat_assets.sh" _site "${asset_url_prefix}" $(git describe --always --dirty --broken --tags)

for theme_variant in default dark light;
do

  cybertron build \
    --name "${theme_name} ${theme_variant} $(git describe --always --dirty --broken --tags)" \
    --stylesheet "_site/assets/css/just-the-docs-${theme_variant}.css" \
    --wrapper "_site/wrapper.html" \
    --templates-folder "_site/html-templates/" \
    --macros-folder "_site/macros/" \
    --output-directory "_site/"

done

# need to set environment variables:
# - JCINK_ADMINURL
# - JCINK_USERNAME
# - JCINK_PASSWORD

python "$SCRIPT_DIR/jcink_upload/main.py" \
  --assets _site/files/ \
  --assets-root _site/ \
  --skin _site/*default*.xml \
  --skin _site/*dark*.xml \
  --skin _site/*light*.xml \
  --upgrade-regex '^(?P<skin>just-the-docs) (?P<variant>dark|light|default) (?P<version>.*)$' \

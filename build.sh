#!/bin/bash
set -e -x

asset_url_prefix="https://files.jcink.net/uploads2/ajmansfieldtestboard/assets"
theme_name=DestinyWeaves
theme_variant=dark

bundle exec jekyll build

./flat_assets.sh _site "${asset_url_prefix}"

cybertron build \
  --name "${theme_name}-${theme_variant}" \
  --macros-folder "_site/macros" \
  --stylesheet "_site/assets/css/just-the-docs-${theme_variant}.css" \
  --templates-folder "_site/html-templates" \
  --wrapper "_site/wrapper.html"

    


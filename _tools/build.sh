#!/bin/bash
set -e -x

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

asset_url_prefix="https://files.jcink.net/uploads2/ajmansfieldtestboard/assets"
theme_name=JustTheDocs
theme_variant=dark

bundle exec jekyll build

"$SCRIPT_DIR/flat_assets.sh" _site "${asset_url_prefix}"

cybertron build \
  --name "${theme_name} ${theme_variant} $(git describe --always --dirty --broken)" \
  --stylesheet "_site/assets/css/just-the-docs-${theme_variant}.css" \
  --wrapper "_site/wrapper.html" \
  --templates-folder "_site/html-templates/" \
  --macros-folder "_site/macros/" \
  --output-directory "_site/"

# server_path=../ajmansfieldtestboard
# artifact_path=$server_path/artifact/
# cache_path=$server_path/cache/
# artifact_server_addr=192.168.65.254
# # server_addr=172.17.0.2
# cache_server_addr=host.docker.internal


# mkdir -p $artifact_path
# mkdir -p $cache_path

# act \
#   --env-file $server_path/.env \
#   --var-file $server_path/.variables \
#   --secret-file $server_path/.secrets \
#   --artifact-server-addr $artifact_server_addr \
#   --artifact-server-path $artifact_path \
#   --cache-server-addr $cache_server_addr \
#   --cache-server-path $cache_path \
#   $@


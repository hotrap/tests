#!/usr/bin/env sh

mkdir -p ~/.cargo

cat >> ~/.cargo/config.toml <<EOF
[source.crates-io]
replace-with = 'rsproxy'

[source.rsproxy]
registry = "https://rsproxy.cn/crates.io-index"

[registries.rsproxy]
index = "https://rsproxy.cn/crates.io-index"

[net]
git-fetch-with-cli = true
EOF

cat >> ~/.profile <<EOF
export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"
EOF

export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"

tmp=$(mktemp)
curl --proto '=https' --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh > $tmp
sh $tmp -y

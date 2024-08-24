#!/usr/bin/env sh

# frawk is a faster awk
# "cargo install frawk" may not work. So we install it with nix
nix-env -iA nixpkgs.frawk

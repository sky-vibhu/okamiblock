{ pkgs ? import ../../../nix { } }:
let okamid = (pkgs.callPackage ../../../. { });
in
okamid.overrideAttrs (oldAttrs: {
  # Patch the okami binary to:
  # - use the CrossChainSwap contract address in the testing setup
  # - update the corresponding IBC channel to match the tests setup
  patches = oldAttrs.patches or [ ] ++ [
    ./osmosis-outpost.patch
  ];
})


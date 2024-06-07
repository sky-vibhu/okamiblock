{ pkgs ? import ../../../nix { } }:
let okamid = (pkgs.callPackage ../../../. { });
in
okamid.overrideAttrs (oldAttrs: {
  # Patch the okami binary to:
  # - use channel-0 for the stride outpost
  patches = oldAttrs.patches or [ ] ++ [
    ./stride-outpost-channel.patch
  ];
})

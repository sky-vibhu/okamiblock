{ pkgs ? import ../../../nix { } }:
let okamid = (pkgs.callPackage ../../../. { });
in
okamid.overrideAttrs (oldAttrs: {
  patches = oldAttrs.patches or [ ] ++ [
    ./broken-okamid.patch
  ];
})

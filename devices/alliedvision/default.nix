{
  callPackage,
  python3Packages,
}:
let
  vimbax = callPackage ./vimbax.nix { };
  vmbpy = python3Packages.callPackage ./vmbpy.nix { inherit vimbax; };
in {
  inherit vimbax;
  inherit vmbpy;
}
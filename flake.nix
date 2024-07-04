{
  inputs = {
    artiq.url = "github:m-labs/artiq/release-7";
    nixpkgs.follows = "artiq/nixpkgs";
  };

  outputs =
    { self
    , nixpkgs
    , artiq
    }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      alliedvision = pkgs.callPackage ./devices/alliedvision { };

      devices = pkgs.python3Packages.buildPythonPackage rec {
        pname = "devices";
        version = "0.1.0";
        src = self;
        doCheck = false;
        propagatedBuildInputs = [ alliedvision.vmbpy ];
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs.python3Packages; [
          python
          venvShellHook
          numpy
          requests
          artiq.packages.${system}.artiq
          devices
        ];
        venvDir = ".venv";
        postVenvCreation = ''
          unset SOURCE_DATE_EPOCH
        '';
        postShellHook = ''
          # required by the vimba driver
          export GENICAM_GENTL64_PATH=${alliedvision.vimbax}/VimbaX_${alliedvision.vimbax.version}/cti
          export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH

          unset SOURCE_DATE_EPOCH
        '';

      };
    };
}

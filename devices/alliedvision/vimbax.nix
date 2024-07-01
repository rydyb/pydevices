{ stdenv
, fetchurl
}:

stdenv.mkDerivation rec {
  pname = "vimba-x";
  version = "2023-4";

  src = fetchurl {
    url = "https://downloads.alliedvision.com/VimbaX/VimbaX_Setup-${version}-Linux64.tar.gz";
    sha256 = "sha256-9EWLcu09fhZ+LEAmGAeAJU+tdmfppGtj+adMqk5YGHE=";
  };

  unpackPhase = ''
    mkdir -p $out
    tar -xzf $src -C $out
  '';

  phases = [ "unpackPhase" ];
}

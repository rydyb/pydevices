{ python3Packages
, fetchurl
, vimbax
}:

python3Packages.buildPythonPackage rec {
  pname = "vmbpy";
  version = "1.0.4";

  format = "wheel";

  src = "${vimbax}/VimbaX_${vimbax.version}/api/python/${pname}-${version}-py3-none-any.whl";

}

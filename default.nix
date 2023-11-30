{ pkgs ? import <nixpkgs> { } }:
pkgs.python3.pkgs.buildPythonApplication rec {
  pname = "trzr-bip39-deposit";
  version = "0.0.1";
  src = ./.;
  format = "pyproject";
  propagatedBuildInputs = with pkgs.python3.pkgs; [
    setuptools
    trezor
  ];
}

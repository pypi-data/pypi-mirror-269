# -*- coding: utf-8 -*-
# :Project:   PatchDB — Development environment
# :Created:   dom 26 giu 2022, 11:48:09
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022, 2023, 2024 Lele Gaifax
#

{
  description = "metapensiero.sphinx.patchdb";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      # Use the same nixpkgs
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, gitignore }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (builtins) fromTOML readFile;
        pkgs = import nixpkgs { inherit system; };
        inherit (pkgs.lib) flip zipLists;
        inherit (gitignore.lib) gitignoreFilterWith;

        pinfo = (fromTOML (readFile ./pyproject.toml)).project;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        # List of supported Python versions, see also Makefile
        snakes = flip map [ "310" "311"]
          (ver: rec { name = "python${ver}"; value = builtins.getAttr name pkgs;});

        mkPatchDBPkg = python: python.pkgs.buildPythonPackage {
          pname = pinfo.name;
          version = pinfo.version;

          src = getSource "patchdb" ./.;
          pyproject = true;

          dependencies = (with python.pkgs; [
            enlighten
            # As of Sat Apr 20 09:29:59 2024 nixpkgs still has 0.4.4
            (sqlparse.overridePythonAttrs rec {
              pname = "sqlparse";
              version = "0.5.0";
              src = pkgs.fetchPypi {
                inherit pname version;
                hash = "sha256-cU0KSTLAWdFhifWO9UEewih6Q2DxfN0O3S0J1MUIfJM";
              };
              pyproject = true;
              format = null;
              build-system = [ hatchling ];
            })
          ]);

          build-system = (with python.pkgs; [
            pdm-pep517
          ]);

          doCheck = false;
        };

        patchDBPkgs = flip map snakes
          (py: {
            name = "patchdb-${py.name}";
            value = mkPatchDBPkg py.value;
          });

        mkTestShell = python:
          let
            patchdb = mkPatchDBPkg python;
          in
            pkgs.mkShell {
              name = "Test Python ${python.version}";
              packages = [
                python
                patchdb
              ] ++ (with pkgs; [
                gnumake
                just
                postgresql_15
                yq-go
              ]) ++ (with python.pkgs; [
                docutils
                psycopg
                pytest
                sphinx
              ]);

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';

              LANG="C";
            };

        testShells = flip map snakes
          (py: {
            name = "test-${py.name}";
            value = mkTestShell py.value;
          });
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = with pkgs; [
              bump2version
              gnumake
              just
              python3
              twine
              yq-go
            ] ++ (with pkgs.python3Packages; [
              babel
              build
            ]);

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };
        } // builtins.listToAttrs testShells;

        packages = (builtins.listToAttrs patchDBPkgs);
      });
}

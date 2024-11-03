{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = { self, nixpkgs, poetry2nix }:
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
      mkPoetryOverrides = pkgs: defaultPoetryOverrides:
        defaultPoetryOverrides.extend
          (self: super: {
            mkdocs-enumerate-headings-plugin = super.mkdocs-enumerate-headings-plugin.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                }
              );
            mkdocs-glightbox = super.mkdocs-glightbox.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                }
              );
            mkdocs-git-committers-plugin-2 = super.mkdocs-git-committers-plugin-2.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                }
              );
            mkdocs-juvix-plugin = super.mkdocs-juvix-plugin.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                }
              );
            mkdocs-get-deps = super.mkdocs-get-deps.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling ];
                }
              );
            mkdocs-literate-nav = super.mkdocs-literate-nav.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling ];
                }
              );
            mkdocs-section-index = super.mkdocs-section-index.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling ];
                }
              );
            super-collections = super.super-collections.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                }
              );
            urllib3 = super.urllib3.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ (with super; [ hatchling hatch-vcs ]);
                }
              );
            levenshtein = pkgs.python312Packages.levenshtein;
          });
    in
    rec {
      packages = forAllSystems (system: let
        inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs.${system}; }) mkPoetryEnv defaultPoetryOverrides;
        stdenv = pkgs.${system}.stdenv;
      in rec {
        mkdocs-nspec = mkPoetryEnv {
          projectDir = self;
          overrides = mkPoetryOverrides pkgs.${system} defaultPoetryOverrides;
        };

        nspec = stdenv.mkDerivation {
          pname = "nspec";
          version = "dev";
          src = self;

          buildInputs = [
            mkdocs-nspec
            juvix
            pkgs.${system}.graphviz
          ];

          buildPhase = ''
            make
          '';

          installPhase = ''
            mv site $out
          '';
        };

        juvix =
          let
            version = "v0.6.6";
            baseurl = "https://github.com/anoma/juvix/releases/download/${version}";
            srcs = {
              x86_64-linux = {
                url = "${baseurl}/juvix-linux-x86_64.tar.gz";
                sha256 = "1j9zq3dwy1jx1mqjkp9bjiz7cm1wlw701vlld69h3y1adk0b6nyw";
              };
              x86_64-darwin = {
                url = "${baseurl}/juvix-macos-x86_64.tar.gz";
                sha256 = "008b2s1b7xga8m8b06bkpycpdawk84n7nym1di6kflwgxj8rfc0x";
              };
              aarch64-darwin = {
                url = "${baseurl}/juvix-macos-aarch64.tar.gz";
                sha256 = "1053aqdz4gbqhag4jp3hvi5j8fnzbxshkq67lf0r57v83yv4p2sv";
              };
            };
          in
            stdenv.mkDerivation rec {
              pname = "juvix";
              inherit version;

              src = builtins.fetchurl srcs.${system};

              unpackPhase = ''
                mkdir src
                cd src
                tar xvf $src
              '';

              installPhase = ''
                mkdir -p $out/bin
                install juvix $out/bin
              '';
            };

        default = nspec;
      });

      devShells = forAllSystems (system: let
        inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs.${system}; }) mkPoetryEnv defaultPoetryOverrides;
      in {
        default = pkgs.${system}.mkShellNoCC {
          packages = with pkgs.${system}; [
            poetry
            graphviz
            packages.${system}.mkdocs-nspec
            packages.${system}.juvix
          ];
        };
      });
    };
}

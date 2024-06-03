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
            mkdocs-glightbox = super.mkdocs-glightbox.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                }
              );
            mkdocs-ezglossary-plugin = super.mkdocs-ezglossary-plugin.overridePythonAttrs
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
            levenshtein = pkgs.python311Packages.levenshtein;
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
            version = "2024-06-02-0.6.2-823b37c";
            baseurl = "https://github.com/anoma/juvix-nightly-builds/releases/download/nightly-${version}";
            srcs = {
              x86_64-linux = {
                url = "${baseurl}/juvix-linux-x86_64.tar.gz";
                sha256 = "084m27xq39lknqgxkp6rcg65hqr81al0bh4ld0l91rll4k23gwcm";
              };
              x86_64-darwin = {
                url = "${baseurl}/juvix-darwin-x86_64.tar.gz";
                sha256 = "0k2rb0wqvbpa3v05nckgkjcbk45bwwra7ixyswsa3r1vjp5iq5vd";
              };
              aarch64-darwin = {
                url = "${baseurl}/juvix-darwin-aarch64.tar.gz";
                sha256 = "0ry3pd21vy2qyac7g5wmyi2m692vc5dak8rkcpb3w55v6aw2xj06";
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

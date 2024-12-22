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
            mkdocs-git-committers-plugin-2 = super.mkdocs-git-committers-plugin-2.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                }
              );
            mkdocs-juvix-plugin = super.mkdocs-juvix-plugin.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools super.poetry ];
                }
              );
            mkdocs-get-deps = super.mkdocs-get-deps.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling ];
                }
              );
            mkdocs-kroki-plugin = super.mkdocs-kroki-plugin.overridePythonAttrs
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
            bs4 = super.bs4.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling ];
                }
              );
            ncls = super.ncls.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools super.cython ];
                }
              );
            rapidfuzz = super.rapidfuzz.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.scikit-build-core ];
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
            mkdocs build
          '';

          installPhase = ''
            mv site $out
          '';
        };

        juvix =
          let
            version = "v0.6.9";
            baseurl = "https://github.com/anoma/juvix/releases/download/${version}";
            srcs = {
              x86_64-linux = {
                url = "${baseurl}/juvix-linux-x86_64.tar.gz";
                sha256 = "0v4kzj5wyn7fy0vwa3f0cxk9k1fpfi0wxdbgzpgpkybzxw3msiic";
              };
              x86_64-darwin = {
                url = "${baseurl}/juvix-macos-x86_64.tar.gz";
                sha256 = "19d6bd4wv2ljmvd4swlishfg2439yl0n8diisbxv7yllmb6zivqc";
              };
              aarch64-darwin = {
                url = "${baseurl}/juvix-macos-aarch64.tar.gz";
                sha256 = "1mkihdcg2gip4yhkq8lsv177b6bik1ajhf09k4vakg02qbhx9166";
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

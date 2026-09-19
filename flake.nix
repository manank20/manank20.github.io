{
  description = "Develop and build manank.in with Zola 0.23.6";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        releases = {
          aarch64-linux = {
            target = "aarch64-unknown-linux-gnu";
            sha256 = "266448fffbf7c7004ca399d0e76dd699541771096d8a42aede98cebe2a029d02";
          };
          x86_64-linux = {
            target = "x86_64-unknown-linux-gnu";
            sha256 = "8f5132b3522412d04e395e0b25f6d68613ad272a873e54a2b3ebf664873024a4";
          };
          aarch64-darwin = {
            target = "aarch64-apple-darwin";
            sha256 = "cbffbd29b3f59c3f52633507c8cb945a7a02d8b1399b43b235f5932912297aa3";
          };
          x86_64-darwin = {
            target = "x86_64-apple-darwin";
            sha256 = "79a4d0ab51a4d863c068e6e594c6fce36f0aa17429a414ea63066f5910d14460";
          };
        };
        release = releases.${system};
        zola = pkgs.stdenvNoCC.mkDerivation rec {
          pname = "zola";
          version = "0.23.6";
          src = pkgs.fetchurl {
            url = "https://github.com/getzola/zola/releases/download/v${version}/zola-v${version}-${release.target}.tar.gz";
            inherit (release) sha256;
          };
          sourceRoot = ".";
          nativeBuildInputs = [ pkgs.makeWrapper ]
            ++ pkgs.lib.optionals pkgs.stdenv.isLinux [ pkgs.autoPatchelfHook ];
          buildInputs = pkgs.lib.optionals pkgs.stdenv.isLinux [ pkgs.stdenv.cc.cc.lib ];
          dontConfigure = true;
          dontBuild = true;
          installPhase = ''
            runHook preInstall
            install -Dm755 zola "$out/bin/zola"
            runHook postInstall
          '';
          postFixup = ''
            wrapProgram "$out/bin/zola" \
              --set SSL_CERT_FILE "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
          '';
        };
      in {
        packages.default = pkgs.stdenvNoCC.mkDerivation {
          pname = "manank-in";
          version = "0.1.0";
          src = pkgs.lib.cleanSourceWith {
            src = ./.;
            filter = path: type:
              let name = builtins.baseNameOf path;
              in name != ".git" && name != "public" && name != "result";
          };
          nativeBuildInputs = [ zola ];
          dontConfigure = true;
          buildPhase = ''
            runHook preBuild
            test -f themes/DeepThought/theme.toml
            zola build
            runHook postBuild
          '';
          installPhase = ''
            runHook preInstall
            mkdir -p "$out"
            cp -r public/. "$out/"
            runHook postInstall
          '';
        };
        devShells.default = pkgs.mkShell { packages = [ zola ]; };
      });
}

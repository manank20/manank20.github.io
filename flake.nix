{
  description = "A flake for developing and building manank.in";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.deepthought = { url = "github:RatanShreshtha/DeepThought"; flake = false; };
  inputs.nix-filter.url = "github:numtide/nix-filter";

  outputs = inputs@{ self, nixpkgs, flake-utils, deepthought, nix-filter }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        themeName = ((builtins.fromTOML (builtins.readFile "${deepthought}/theme.toml")).name);
      in
      { 
      packages.default = pkgs.stdenvNoCC.mkDerivation {
        pname = "manank.in website";
        version = (builtins.substring 0 8 self.lastModifiedDate);
	src = self;
        nativeBuildInputs = [ pkgs.zola ];
        configurePhase = ''
          mkdir -p "themes/${themeName}"
	        mkdir -p templates
          ln -s ${deepthought}/* "themes/${themeName}"
        '';
        buildPhase = "zola serve";
        dontInstall = true;
      };
    }
  );
}

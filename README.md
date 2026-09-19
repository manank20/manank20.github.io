### Hi there 👋
Repository for personal website hosted at [manank.in](https://www.manank.in)

## Local development

Use **Zola 0.23.6**. The templates now use Tera 2 components and will not work
with Zola 0.22 or earlier. Install the matching release from
[Zola's releases](https://github.com/getzola/zola/releases/tag/v0.23.6).

```sh
git submodule update --init --recursive  # on a fresh checkout only
zola --version                           # zola 0.23.6
zola serve
# Include the existing unpublished kernel-workflow post:
zola serve --drafts
```

The theme is maintained in the separate repository at `themes/DeepThought`.
Site-specific overrides remain in `templates/`. Commit theme changes first and
then record the resulting submodule commit in this repository.

## Verification

```sh
zola build
zola check --drafts --skip-external-links
zola check  # also checks third-party URLs; may fail on blocked/removed links
```

## Nix

The flake uses checksum-pinned official Zola 0.23.6 binaries rather than the old
Zola package in the existing nixpkgs lock. It builds the checked-out submodule,
not a separate upstream theme snapshot.

```sh
nix develop path:. --command zola serve
nix build path:.  # static output in result/, not a long-running server
```

The Nix flake was validated on `aarch64-linux`: `nix flake check`, `nix build`,
and the Zola 0.23.6 development shell all pass.

## Migration notes

- Macros/imports became components; `config` is passed explicitly where needed.
- Optional configuration and absent pagination are guarded under Tera 2's
  stricter undefined-variable rules.
- Invalid content outside inherited template blocks was removed in the theme.
- Theme shortcodes became components, and literal Tera examples in Markdown use
  `{% raw %}` because Markdown content is now templated by default.
- The site's highlighting configuration already used the current format.

References: [Zola 0.23 changelog](https://github.com/getzola/zola/blob/master/CHANGELOG.md#0230-2026-08-05),
[Tera 2 migration](https://github.com/Keats/tera/blob/master/MIGRATION.md).

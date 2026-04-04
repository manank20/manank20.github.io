### Hi there 👋
Repository for personal website hosted at [manank.in](https://www.manank.in)

## Deploy notes

- Zola version is pinned in `.tool-versions` (`0.18.0`).
- On Cloudflare Pages, avoid a brittle pre-build command that always runs `asdf plugin add zola ...` with `&&`, because it fails once the plugin already exists.
- If you need `UNSTABLE_PRE_BUILD`, use an idempotent version instead:

```sh
asdf plugin list | grep -q '^zola$' || asdf plugin add zola https://github.com/salasrod/asdf-zola
asdf install zola 0.18.0
asdf global zola 0.18.0
```

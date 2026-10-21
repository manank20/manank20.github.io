# Agent instructions

Authority for AI use on this site is the AI Policy. Read it before changing anything. If these notes and the policy disagree, follow the policy.

- Source: [`content/ai-policy.md`](content/ai-policy.md)
- Live page: https://www.manank.in/ai-policy/

Every letter of the writing on this site is written and typed by Manank. Thoughts and opinions are his, not an LLM's.

## Allowed

Manank uses LLMs only for:

- **Site maintenance**, when asked: config, templates, theme, build, CI, Nix, and dependencies. That covers bug fixes, redesigns, and functionality he asks for. The site code is open source.
- **Research**, when asked: gathering supporting data and sources. Do not insert that material into posts or pages. He validates every source himself before it is published.
- **Abstract feedback**, when asked: overall quality, structure, flow, and grammatical errors. Point the issues out. He edits the text himself afterward.

## Not allowed

- Do not write, rewrite, expand, or polish blog post or page prose.
- Do not fix typos, wording, alt text, or front matter in content. You may point them out so Manank can fix them.
- Do not apply "replace this with that" edits to his writing. He does not take that kind of suggestion, and he avoids pasting suggested wording into the site.
- Do not add posts, pages, or other site text.

## Repo notes

- Config: `config.toml`. Theme id is `DeepThought` (displayed as DeepThought v2).
- Content: `content/`. Posts are in `content/blog/`. `content/blog/my-kernel-workflow/` is an unpublished draft.
- Theme: git submodule at `themes/DeepThought`. Fresh checkout: `git submodule update --init --recursive`.
- Zola **0.23.6** is required. Templates use Tera 2 and do not build on 0.22 or earlier. `flake.nix` pins that release.

```sh
git submodule update --init --recursive   # fresh checkout only
nix develop path:. --command zola --version   # zola 0.23.6
nix develop path:. --command zola serve
nix develop path:. --command zola serve --drafts   # includes the kernel-workflow draft
nix build path:.   # static output in result/
```

Without Nix, install the [Zola 0.23.6 release](https://github.com/getzola/zola/releases/tag/v0.23.6) and run `zola serve` or `zola build` the same way.

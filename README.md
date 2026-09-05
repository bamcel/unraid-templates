# bamcel's Unraid Community Applications Repository

Unified Unraid Community Applications templates for self-hosted applications maintained by
[bamcel](https://github.com/bamcel).

| Application | Description | Source |
| --- | --- | --- |
| MKV Orchestrator | Browser-based MKV and MP4 media operations console. | [bamcel/mkv-orchestrator](https://github.com/bamcel/mkv-orchestrator) |
| PosterView | Artwork manager for Plex, Jellyfin, and Emby. | [bamcel/poster-view](https://github.com/bamcel/poster-view) |

Application source code and container images remain in their respective repositories. This
repository contains only Community Applications metadata and presentation assets.

## Community Applications

Submit or validate this repository with:

```text
https://github.com/bamcel/unraid-templates
```

Each application has one Docker template under [`templates/`](templates/). Template URLs and
icons are served directly from this repository so the Community Applications scanner has one
canonical source.

## Validation

```bash
python scripts/validate.py
```

GitHub Actions runs the same validation on every push and pull request.

## License

MIT — see [LICENSE](LICENSE).

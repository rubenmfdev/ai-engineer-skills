# Chrome extensions

Original skills here:
- [mv3-extension-development](mv3-extension-development): Manifest V3 architecture and pitfalls.
- [extension-security-and-publishing](extension-security-and-publishing): permissions, hardening, Web Store review.

Curated external skills (category `chrome-extensions` in [external-skills.json](../../../external-skills.json)). Read before using. Extension-specific skills are young and have few stars, so treat them as starting points.

## quangpl/browser-extension-skills (MIT, 12 skills)
[Repo](https://github.com/quangpl/browser-extension-skills). Sponsored by Extension Booster, and each skill credits the sponsor.

| Skill | Default | Topic |
| --- | --- | --- |
| extension-create | yes | Scaffold with WXT or CRXJS |
| extension-dev | yes | Detect stack, implement, debug across contexts |
| extension-manifest | yes | Minimum-permission manifest |
| extension-analyze | yes | Security, performance and CWS audit |
| extension-review | yes | Web Store rejection-risk scan |
| extension-publish | yes | Store listing and CI/CD |
| extension-test | yes | Jest chrome.* mocks, Puppeteer E2E |
| extension-ui | yes | Popup, side panel, options UI |
| extension-migration | optional | MV2 to MV3 |
| extension-assets | optional | Icons and store images |
| extension-backend | optional | NestJS + MongoDB backend |
| extension-payment | optional | Stripe, Paddle, Lemon Squeezy and more |

## thomaslimited/chrome-extension-skills (MIT)
[Repo](https://github.com/thomaslimited/chrome-extension-skills): `chrome-web-store-listing` (default: listing copy, permission justifications, privacy tab), plus optional `chrome-extension-dev`, `chrome-extension-auth`, `chrome-extension-deploy`.

## gandli/browser-extension-skills (MIT)
[Repo](https://github.com/gandli/browser-extension-skills): framework and real-browser testing skills, all optional. Pick the one that matches your build tool: `wxt-extension-dev`, `plasmo-extension-dev`, `crxjs-extension-dev`, plus `chrome-for-testing-extensions` and `chrome-devtools`.

## Install
```bash
python3 scripts/install.py --category chrome-extensions --project                 # defaults
python3 scripts/install.py --category chrome-extensions --topic framework --all --project
```

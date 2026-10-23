---
name: extension-security-and-publishing
description: Harden a Chrome extension and get it through Chrome Web Store review with least-privilege permissions, CSP, message validation, privacy disclosures and a release checklist. Use when auditing extension permissions, preparing a Web Store submission, or handling a review rejection.
---

# Extension Security and Publishing

## Least privilege
1. List every permission and the feature that needs it. Delete any without a feature.
2. Replace broad `host_permissions` (`<all_urls>`, `*://*/*`) with specific origins, `activeTab`, or `optional_host_permissions`.
3. Move rarely used capabilities to `optional_permissions` requested on demand.
4. Avoid `tabs` (exposes URLs and titles of all tabs) when `activeTab` or `chrome.tabs.query` on the active tab suffices.
5. Review `web_accessible_resources` so only needed files are exposed, with narrow `matches`.

Broad permissions slow review and raise rejection risk.

## Code safety
- No `eval`, `new Function`, inline event handlers, or remotely loaded scripts. MV3 forbids remote code and the Store rejects it.
- Never insert untrusted strings with `innerHTML`. Use `textContent`, or a sanitizer such as DOMPurify when HTML is required.
- Validate messages: check `sender.id === chrome.runtime.id` for internal messages and `sender.url`/origin for `externally_connectable` ones. Validate payload shape with a schema.
- Treat content-script input from the page as hostile. Do not forward it to privileged APIs unchecked.
- Do not store secrets in the package. Keep API keys on your server and proxy requests.
- Store tokens in `storage.local` (not `sync`) and request the minimum scope.
- Keep dependencies few, pinned, and audited (`npm audit`). Bundle them, don't load from a CDN.

## Privacy and disclosures
- Publish a privacy policy URL if you handle any user data. State what is collected, why, and where it goes.
- The Web Store "Privacy practices" tab must match actual behavior. Mismatches cause rejection.
- Limited Use: user data may only be used for the single purpose described.
- Single purpose: the extension should do one clearly described thing, and the name, description and screenshots must say so.

## Release checklist
- [ ] `version` bumped (must increase every upload)
- [ ] Unused permissions removed, justifications written for each remaining one
- [ ] No console.log of user data, no source maps containing secrets
- [ ] Icons 16, 48, 128; store assets (1280x800 or 640x400 screenshots, 440x280 promo tile)
- [ ] Privacy policy URL and data-use form complete
- [ ] Tested on a clean profile with the packaged zip, not only unpacked
- [ ] Zip contains the `manifest.json` at the root, no `node_modules` or `.git`
- [ ] Staged rollout percentage chosen for risky releases

## Common rejection reasons
| Reason | Fix |
| --- | --- |
| Excessive permissions | Narrow hosts, use optional or `activeTab`, justify in the form |
| Remote code | Bundle all JS locally |
| Misleading metadata | Match name, description and screenshots to real behavior |
| Missing or weak privacy policy | Add a specific policy URL |
| Keyword stuffing | Write natural, accurate descriptions |

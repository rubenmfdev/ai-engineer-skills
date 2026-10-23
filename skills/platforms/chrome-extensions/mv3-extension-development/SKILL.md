---
name: mv3-extension-development
description: Build Chrome extensions with Manifest V3 covering project layout, manifest fields, service workers, content scripts, messaging, storage, side panel and testing. Use when creating or debugging a Chrome extension, migrating from Manifest V2, or when a service worker keeps going to sleep.
---

# Chrome Extension Development (Manifest V3)

## Anatomy
| Piece | Runs in | Purpose |
| --- | --- | --- |
| `manifest.json` | n/a | Declares permissions, entry points, icons |
| Service worker | Extension background, event-driven | Central logic, listens to events |
| Content script | Web page (isolated world) | Reads and changes page DOM |
| Popup / options / side panel | Extension page | UI |
| Offscreen document | Hidden extension page | DOM-only APIs the worker lacks (audio, parsing) |

## Minimal manifest
```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "description": "One sentence.",
  "action": { "default_popup": "popup.html" },
  "background": { "service_worker": "background.js", "type": "module" },
  "permissions": ["storage"],
  "host_permissions": [],
  "content_scripts": [
    { "matches": ["https://example.com/*"], "js": ["content.js"] }
  ]
}
```
See [references/manifest-notes.md](references/manifest-notes.md) for field details.

## Service worker rules
- It is **terminated when idle** (about 30 seconds). Never keep state in globals. Persist to `chrome.storage.session` or `chrome.storage.local` and reload on start.
- Register **all event listeners synchronously at top level**, not inside promises or callbacks, or events that wake the worker will be missed.
- No `window`, no `document`, no `localStorage`. Use `fetch`, `chrome.storage`, offscreen documents.
- Replace `setInterval` with `chrome.alarms` (minimum period 30 seconds).
- No persistent background pages and no remotely hosted code. All logic must ship in the package.

## Messaging
- One-off: `chrome.runtime.sendMessage` / `chrome.tabs.sendMessage` with `chrome.runtime.onMessage`.
- To respond asynchronously, `return true` from the listener, or return a promise in modern Chrome.
- Define a typed message union (`{ type: "FETCH_DATA", ... }`) and route in one place.
- Validate `sender` (`sender.id`, `sender.url`) before acting on a message.
- Long-lived: `chrome.runtime.connect` ports. Handle `onDisconnect`, since the worker can restart.

## Content scripts
- They live in an isolated world. They share the DOM but not JS variables with the page. To read page JS state, inject a script with `world: "MAIN"` via `chrome.scripting.executeScript` or declare `"world": "MAIN"`.
- Prefer programmatic injection with `activeTab` over broad `matches` when the user triggers the action.
- Use `MutationObserver` for dynamic pages and disconnect when done.
- Namespace injected DOM/CSS or use Shadow DOM to avoid clashing with the host page.

## Storage
| API | Use |
| --- | --- |
| `storage.local` | Large or private data, about 10 MB (unlimitedStorage lifts it) |
| `storage.sync` | Small user settings across devices, about 100 KB total, 8 KB per item |
| `storage.session` | In-memory state for the browser session, cleared on restart |

All calls are async. Listen to `chrome.storage.onChanged` instead of polling.

## Network rules
Use `declarativeNetRequest` for blocking or redirecting. `webRequestBlocking` is gone for normal extensions. Rules are static (JSON in the package) or dynamic/session.

## Dev workflow
1. `chrome://extensions` → Developer mode → Load unpacked.
2. Debug the worker via its "service worker" link. Content script logs are in the page's DevTools.
3. Use a bundler (Vite with `@crxjs/vite-plugin`, WXT or Plasmo) when you use TypeScript or frameworks. Keep the output a plain MV3 folder.
4. Test logic with Vitest by mocking `chrome.*` (for example `jest-chrome` or `vitest-chrome`). Test flows with Playwright launching Chromium with `--load-extension`.

## Common failures
- "Receiving end does not exist": content script not injected yet or tab wasn't reloaded after install.
- Worker "inactive" mid-task: state in memory, or a listener registered asynchronously.
- CSP errors: no inline scripts or `eval` in extension pages. Move scripts to files.

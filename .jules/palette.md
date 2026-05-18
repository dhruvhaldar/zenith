
## 2026-04-26 - Intra-Page Navigation Breathing Room
**Learning:** When navigating via intra-page links, targeted elements are often flush against the top viewport edge, feeling cramped. `scroll-margin-top` solves this cleanly.
**Action:** Always add `scroll-margin-top` to elements with IDs when implementing intra-page navigation to provide visual breathing room.
## 2026-05-18 - Interactive elements and accessibility
**Learning:** Explicit visual states like `cursor: copy` and text like 'click to select' hint at interactivity, but non-native elements (like `<span>`) require JavaScript to implement the action, `role="button"` to be announced as interactive by screen readers, and an `aria-live` region to provide auditory confirmation of the action (like copying to clipboard).
**Action:** When making non-standard elements interactive, always add `role="button"`, keyboard event handlers (Enter/Space), and an `aria-live` region for state changes.


## 2026-04-26 - Intra-Page Navigation Breathing Room
**Learning:** When navigating via intra-page links, targeted elements are often flush against the top viewport edge, feeling cramped. `scroll-margin-top` solves this cleanly.
**Action:** Always add `scroll-margin-top` to elements with IDs when implementing intra-page navigation to provide visual breathing room.
## 2026-05-18 - Interactive elements and accessibility
**Learning:** Explicit visual states like `cursor: copy` and text like 'click to select' hint at interactivity, but non-native elements (like `<span>`) require JavaScript to implement the action, `role="button"` to be announced as interactive by screen readers, and an `aria-live` region to provide auditory confirmation of the action (like copying to clipboard).
**Action:** When making non-standard elements interactive, always add `role="button"`, keyboard event handlers (Enter/Space), and an `aria-live` region for state changes.

## 2026-05-19 - Explicit visual feedback for interactive elements
**Learning:** Relying purely on subtle color changes (like a background color flash) to indicate a successful action (like copying text) violates WCAG 1.4.1 (Use of Color) and can be missed by users. While screen readers get `aria-live` announcements, sighted users need clear, explicit visual confirmation.
**Action:** Always provide explicit visual feedback, such as a Toast notification with text, when a user completes a hidden action like copying to clipboard.

## 2026-05-20 - Ensure exact visible string is included at beginning of aria-labels
**Learning:** When using `aria-label` on elements that contain visible text, replacing the visible text entirely with an expanded description breaks voice navigation software (like Voice Control or Dragon) because users will say the visible text, but the software won't find a matching accessible name.
**Action:** Ensure the exact visible string is included at the beginning of the `aria-label` value to support voice control software and comply with WCAG 2.5.3 (Label in Name).

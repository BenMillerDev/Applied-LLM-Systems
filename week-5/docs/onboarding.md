## Onboarding Flow

A new owner's first login shows an onboarding checklist, rendered by the OnboardingChecklist component, that walks them through the handful of things worth doing before the app is really useful -- most notably, sharing their booking link with an actual client for the first time. Progress through that checklist is tracked by the useOnboarding hook rather than being recalculated from scratch on every visit.

That progress is stored in Firestore as a small, per-owner onboarding document with just two fields: whether the owner has dismissed the checklist, and whether they've shared their booking link at least once. Once both are true there's nothing left for the checklist to prompt, and it stops appearing.

Sharing the booking link itself is a one-tap action available from the settings screen at any time, not just during onboarding -- an owner can go back and re-share or re-copy their link whenever they need to, for example when starting a new marketing push or updating their social media bio.


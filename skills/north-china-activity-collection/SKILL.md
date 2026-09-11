---
name: north-china-activity-collection
description: Collect, verify, refresh, or reconcile upcoming offline activities in Beijing, Tianjin, Shijiazhuang, and Baoding. Use for exhibitions, concerts, theatre, markets, flea markets, talks, and workshops; do not use for ticket purchasing or generic travel recommendations.
---

# North China Activity Collection

Build a trustworthy, source-linked activity calendar for Beijing, Tianjin, Shijiazhuang, and Baoding. The result is a verified activity ledger, not a list of search results or a ticket-resale service.

## Before collecting

- Establish the requested cities, date window, categories, and output format. Default to the next 30 days, all four cities, and all supported categories when the user does not specify them.
- Read [the source registry](references/source-registry.yaml) before a normal collection or refresh. It is a vetted starter set, not a claim that every source is complete.
- Read [the event contract](references/event-contract.md) before saving, publishing, reconciling, or generating calendar data.
- Use only web access, APIs, exports, accounts, and credentials that the user or host has explicitly authorized. Follow source terms, robots directives, and rate limits.

## Source strategy

Use sources in this order of authority:

1. The organizer, venue, museum, gallery, or official government cultural calendar.
2. An official ticketing or registration page that identifies the organizer or venue.
3. A maintained event directory or local activity aggregator.
4. Community posts, newsletters, and user submissions.

Treat tiers 3 and 4 as discovery evidence. A tier-4 lead is never `verified` until an organizer, venue, or official ticket/registration page confirms its essential details.

For a market, flea market, or other fast-moving community event, look for the organizer's own post, the host venue, or a registration page before publication. If that cannot be found, preserve it as a clearly labelled `candidate` with its original source; do not present it as confirmed.

## Collection workflow

1. Select the relevant sources by city and category. Prefer current pages and structured public feeds where they exist.
2. Capture the original event URL and the retrieval time for every candidate. Do not rely on search snippets alone for publication details.
3. Normalize each item to the event contract. Keep the original title and source wording; do not fabricate missing dates, prices, venue names, organizer names, or ticket status.
4. Deduplicate across sources using normalized title, city, venue, date window, and organizer. Merge evidence into one canonical event instead of publishing duplicates.
5. Resolve disagreements using the source hierarchy. Preserve contradictory values in source snapshots and report unresolved conflicts.
6. Assign `verified`, `candidate`, `postponed`, or `canceled` status according to the event contract.
7. Produce the requested output with source links, status, last-verified time, and a concise change summary. Link out for ticketing or registration; never purchase tickets or imply inventory availability.

## Refresh and change detection

When refreshing an existing ledger, compare the new record with its latest source snapshot:

- Add genuinely new activities as `new`.
- Mark date, time, venue, price, status, or source-link changes as `updated` and retain the prior values in history.
- Mark organizer-confirmed cancellations and postponements explicitly; do not silently delete them.
- If a source disappears without a replacement, mark the activity `needs_review` rather than assuming it was canceled.

Keep collection output reversible: append observations and source snapshots instead of overwriting them. Never downgrade a higher-authority value merely because a lower-authority page was fetched more recently.

## Community and account boundaries

Community channels such as WeChat Official Accounts, Xiaohongshu, Douyin, and private groups are valuable for discovery but are not default automation targets. Do not log in, import cookies, bypass access controls, or scrape private/group-only material. Use them only through an authorized host integration or user-provided exports/bookmarks, and require public corroboration before verification.

## Source maintenance

When a source becomes unavailable, rate-limited, or materially changes format, record the failure and move it out of the scheduled path. Add a new source only after confirming its city/category coverage, ownership, access conditions, and an example event page. Keep the registry small and high-signal.

## Stop conditions

Stop and report the gap rather than guessing when essential event details cannot be confirmed, a source requires unprovided authorization, or publication would violate the source's access rules. Return useful candidates with their uncertainty clearly labelled.

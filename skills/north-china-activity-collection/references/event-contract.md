# Event contract

Use one canonical record per real-world activity. Preserve source observations separately so that the canonical record can be corrected without losing provenance.

## Required for any published record

| Field | Requirement |
| --- | --- |
| `title` | Preserve the source title; optionally add a normalized title for matching. |
| `city` | One of 北京市、天津市、石家庄市、保定市. |
| `category` | Use the closest category from the registry; keep source labels as tags when helpful. |
| `start_at` | Date/time and timezone, or an explicitly marked all-day date. |
| `source_url` | Direct source page, not merely a search result. |
| `source_tier` | The tier that supports the published fields. |
| `status` | `candidate`, `verified`, `postponed`, `canceled`, or `needs_review`. |
| `retrieved_at` | When the supporting page was last checked. |

Add `end_at`, `venue`, `address`, `organizer`, `price`, `registration_url`, and `image_url` only when supported by a source. Do not infer them.

## Scope exclusions

This is a non-manga city-activity feed. Exclude `漫展`, `同人展`, `动漫展`, `二次元`, `Cosplay`, `Comicup`, and substantially equivalent anime-focused events. When a matching item exists in the separate manga-calendar ledger, do not publish a duplicate here. Retain a rejected observation with `excluded_reason: manga_calendar_overlap` so the decision remains auditable.

## Verification rules

- A record is `verified` when a tier-1 source provides its essential details, or when a tier-2 page identifies an organizer or venue and there is no higher-tier conflict.
- A tier-3 or tier-4 source alone produces `candidate` status.
- A clear organizer or venue notice changes the record to `postponed` or `canceled`.
- A missing, inaccessible, or conflicting source changes the record to `needs_review`; it does not justify deletion.

## Observations and history

For each fetch, retain an observation with:

```text
observed_at, source_url, source_tier, source_title, extracted_fields,
content_fingerprint, access_notes
```

Track field-level changes for `start_at`, `end_at`, `venue`, `address`, `price`, `registration_url`, and `status`. A refresh must emit `new`, `updated`, `unchanged`, or `needs_review` for every matched canonical record.

## Deduplication key

Begin with normalized title + city + start date + venue. Check the separate manga-calendar ledger first and exclude an overlap rather than merging it. When titles vary, compare organizer, overlapping date ranges, and official ticket/registration links before merging. Never merge events solely because they have a similar title or occur in the same city.

## Minimum output

For a human-readable report, include title, date/time, city, venue, category, status, source link, and last-verified time. For a calendar or data export, include the same provenance fields in the extended description or structured metadata.

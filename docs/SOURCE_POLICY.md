# Source and access policy

Last updated: October 27, 2026.

## Purpose
This is a public *directory*, not a mirror, endorsement, clinical recommendation, or index of patient data. We primarily link to the original resource owner rather than copying their materials.

## Categories of access
- **Free access:** Free public search, downloads, or open-source software (subject to provider licensing, compute resources, and terms).
- **Free with conditions:** Free-to-view portions, account requirements, research-only usage, compute limits, authorization requirements, paid physical materials, academic restrictions, or mixed public/restricted data.
- **Commercial / learning:** Commercial products or services whose educational materials can be accessed publicly.

The user interface groups access conditions heuristically. The **exact provider-specific access field and limitations are always displayed**, and should take precedence over the simplified group. Never represent free scientific information as free laboratory cells, clinical testing, or commercial-use rights.

## Record structure
Each entry in `data/resources.json` includes:
- `id`: stable slug and primary key.
- `name` and `category`.
- `official_url`: official provider website.
- `purpose`: concise independently authored summary.
- `access`: human-readable specific access conditions.
- `limitations`: key restrictions or methodological caveats.
- `official_verification_url`: page used to check the record.
- `integration`: possible integration mode, not a promise of API entitlement.
- `tags`: broad neutral research terms.
- `priority`: editorial discovery ranking, **not scientific evidence strength**.
- `verified_on`: calendar date the information was actually checked.

## Submission and review
1. Accept suggestions through GitHub Issues or a pull request without private data.
2. Verify official ownership, current site, access restrictions, program terms, and API availability where applicable.
3. Record provenance and verification date; do not invent a date or pass older checks off as current.
4. Prefer a link, short original description, and a caveat over copying source content.
5. Avoid importing private patient data, copyrighted publications, photographs, datasets, or paywalled source materials.
6. Check the record against the schema and preview the responsive website before merging.
7. Correct or withdraw entries that are inaccurate, unsafe, unavailable, or misleading.

## Scientific and clinical boundaries
- A listed tool does **not** independently establish mechanism, replication, validity, diagnostic performance, therapeutic efficacy, or suitability for an individual case.
- Simulations depend on underlying evidence, parameters, and external validation.
- ClinicalTrials.gov is a study registry, **not** a guarantee of eligibility or clinical benefit.
- Sensitive health data do not belong in this public repository or user-submitted issues.
- Public data access differs from authorization to reuse or combine datasets. Respect IRB, consent, data-use, and institutional policies.

## Licensing
Original project code: MIT unless otherwise indicated. The MIT license **does not extend** to linked third-party databases, images, APIs, methods, publications, software, research materials, trademarks, or any privately held research.

For the resource metadata itself, contact maintainers about intended reuse if in doubt; official provider documentation governs their respective materials. No license statements are inferred solely from public availability.

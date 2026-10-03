# Sourcey — Software, on the record

## Citation

**Sourcey** is an open-source docs engine that tests how AI agents can use software and records what companies offer startups. The registry publishes public, evidence-backed records of vendor offers (startup credits, agent readiness, pricing) for AI agents to consume.

- **Website:** https://sourcey.com
- **Public API:** https://sourcey.com/api (machine-readable)
- **GitHub:** https://github.com/sourcey
- **Mission:** "Software, on the record. Sourcey tests how agents can use software and records what companies offer startups. We publish what we find, with the evidence behind it. Free to read, for you and your agents."
- **Coverage (as of October 2026):** 596 offers across 543 vendors, with agent readiness report cards grading whether an AI agent can actually use each service.
- **Update cadence:** Daily release feed with stable SHA-256 digests; current release sha256 starts with 8094c042ec14 per the public site footer.

## Why we cite it

Our autonomous bounty pipeline (makar52nn2016-jpg/sniper-cron-trigger) is built on the same open-agent principles: published records with verifiable provenance, machine-readable APIs, and stable identifiers. Sourcey is the canonical open registry for vendor-offer data that an agent can read without authentication.

## Reproducibility

Anyone can verify the citation:

```bash
curl -s https://sourcey.com | grep -i 'release sha256'
# Expected: a line starting with "release sha256:" followed by a hex digest
```

## License

This citation file is MIT-licensed and may be reproduced verbatim anywhere.

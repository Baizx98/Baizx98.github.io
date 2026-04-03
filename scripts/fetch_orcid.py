#!/usr/bin/env python3

import argparse
import json
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


API_ROOT = "https://pub.orcid.org/v3.0"


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "home.baizx.cool ORCID sync script",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def get_nested(obj, *keys, default=None):
    current = obj
    for key in keys:
        if current is None:
            return default
        current = current.get(key)
    return current if current is not None else default


def normalize_type(raw_type: str) -> str:
    labels = {
        "journal-article": "Journal Article",
        "conference-paper": "Conference Paper",
        "preprint": "Preprint",
        "book-chapter": "Book Chapter",
    }
    return labels.get(raw_type, raw_type.replace("-", " ").title())


def parse_works(works_payload: dict) -> list[dict]:
    publications = []
    seen = set()

    for group in works_payload.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue

        summary = summaries[0]
        put_code = summary.get("put-code")
        if put_code in seen:
            continue
        seen.add(put_code)

        publication_date = summary.get("publication-date", {})
        year = get_nested(publication_date, "year", "value", default="")
        month = get_nested(publication_date, "month", "value", default="")
        day = get_nested(publication_date, "day", "value", default="")

        doi = None
        doi_url = None
        for external_id in get_nested(summary, "external-ids", "external-id", default=[]):
            if external_id.get("external-id-type", "").lower() == "doi":
                doi = external_id.get("external-id-value")
                doi_url = get_nested(external_id, "external-id-url", "value")
                break

        publications.append(
            {
                "title": get_nested(summary, "title", "title", "value", default="Untitled"),
                "journal": get_nested(summary, "journal-title", "value", default="Unknown Venue"),
                "type": summary.get("type", "other"),
                "type_label": normalize_type(summary.get("type", "other")),
                "year": year,
                "month": month,
                "day": day,
                "doi": doi,
                "doi_url": doi_url or (f"https://doi.org/{doi}" if doi else ""),
                "url": get_nested(summary, "url", "value", default=""),
                "source": get_nested(summary, "source", "source-name", "value", default="ORCID"),
                "put_code": put_code,
            }
        )

    publications.sort(
        key=lambda item: (
            int(item["year"] or 0),
            int(item["month"] or 0),
            int(item["day"] or 0),
            item["title"],
        ),
        reverse=True,
    )
    return publications


def profile_summary(record_payload: dict) -> dict:
    name = get_nested(record_payload, "person", "name", "given-names", "value", default="")
    family_name = get_nested(record_payload, "person", "name", "family-name", "value", default="")
    keywords = [
        entry.get("content")
        for entry in get_nested(record_payload, "person", "keywords", "keyword", default=[])
        if entry.get("content")
    ]
    urls = [
        {
            "label": entry.get("url-name", "Link"),
            "url": get_nested(entry, "url", "value", default=""),
        }
        for entry in get_nested(record_payload, "person", "researcher-urls", "researcher-url", default=[])
        if get_nested(entry, "url", "value", default="")
    ]

    organization = ""
    employment_groups = get_nested(record_payload, "activities-summary", "employments", "affiliation-group", default=[])
    if employment_groups:
        summaries = employment_groups[0].get("summaries", [])
        if summaries:
            employment = summaries[0].get("employment-summary", {})
            role = employment.get("role-title") or ""
            org_name = get_nested(employment, "organization", "name", default="")
            organization = f"{org_name} · {role}".strip(" ·")

    return {
        "full_name": f"{name} {family_name}".strip(),
        "keywords": keywords,
        "urls": urls,
        "organization": organization or "Not publicly listed",
    }


def build_stats(publications: list[dict]) -> dict:
    year_counter = Counter()
    type_counter = Counter()

    for item in publications:
        if item["year"]:
            year_counter[item["year"]] += 1
        type_counter[item["type_label"]] += 1

    years_sorted = sorted(year_counter.items(), key=lambda pair: int(pair[0]))
    types_sorted = sorted(type_counter.items(), key=lambda pair: (-pair[1], pair[0]))

    return {
        "total_works": len(publications),
        "active_years": len(year_counter),
        "latest_year": max(year_counter, default=""),
        "yearly_counts": [{"year": year, "count": count} for year, count in years_sorted],
        "type_counts": [{"label": label, "count": count} for label, count in types_sorted],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch public ORCID data for Hugo.")
    parser.add_argument("--orcid-id", required=True)
    parser.add_argument("--output", default="data/orcid.json")
    args = parser.parse_args()

    record = fetch_json(f"{API_ROOT}/{args.orcid_id}")
    works = fetch_json(f"{API_ROOT}/{args.orcid_id}/works")
    publications = parse_works(works)

    payload = {
        "orcid_id": args.orcid_id,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "profile": profile_summary(record),
        "stats": build_stats(publications),
        "works": publications,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

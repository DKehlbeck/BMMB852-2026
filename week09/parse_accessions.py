#!/usr/bin/env python3
"""
fetch_srr_accessions.py

Reads design.tsv (columns: Accession, type) and:
  - For each row with type == sample:
      * BioProject accessions (PRJNA/PRJEB/PRJDB) -> expands to all SRR runs
      * Individual SRR/ERR/DRR accessions         -> fetches name directly
    Writes SRR_accessions.tsv (columns: SRR_Accession, Name, Source)

  - For the row with type == reference:
      * Resolves the NCBI FTP directory URL via esummary
    Writes ref_url.txt (single line: the HTTPS FTP URL)

Usage:
    python3 fetch_srr_accessions.py [design.tsv]
"""

import sys
import json
import time
import csv
import urllib.request
import urllib.parse

# ── Configuration ─────────────────────────────────────────────────────────────

NCBI_ESEARCH  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
NCBI_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
NCBI_EFETCH   = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
NCBI_ELINK    = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
REQUEST_DELAY = 0.4   # seconds between requests (NCBI rate limit)
EFETCH_BATCH  = 200   # SRR UIDs per efetch call

# ── Shared HTTP helper ────────────────────────────────────────────────────────

def ncbi_get(url: str, params: dict) -> str:
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{url}?{query}", timeout=30) as resp:
        return resp.read().decode("utf-8")

# ── Reference URL resolution ──────────────────────────────────────────────────

def resolve_ref_url(accession: str) -> str:
    """
    Given a GCF/GCA assembly accession, return the NCBI FTP directory URL
    by querying the assembly DB via esearch + esummary.
    """
    print(f"  Resolving FTP URL for reference {accession} …")

    time.sleep(REQUEST_DELAY)
    search = json.loads(ncbi_get(NCBI_ESEARCH, {
        "db": "assembly",
        "term": f"{accession}[Assembly Accession]",
        "retmode": "json",
        "retmax": 1,
    }))
    ids = search.get("esearchresult", {}).get("idlist", [])
    if not ids:
        raise ValueError(f"No assembly record found for {accession}")

    time.sleep(REQUEST_DELAY)
    summary = json.loads(ncbi_get(NCBI_ESUMMARY, {
        "db": "assembly",
        "id": ids[0],
        "retmode": "json",
    }))
    doc = summary.get("result", {}).get(ids[0], {})
    ftp = doc.get("ftppath_refseq") or doc.get("ftppath_genbank") or ""
    if not ftp or ftp == "na":
        raise ValueError(f"No FTP path in NCBI record for {accession}")

    return ftp.replace("ftp://", "https://")

# ── SRR helpers ───────────────────────────────────────────────────────────────

def fetch_srrs_for_bioproject(bioproject_acc: str) -> list[dict]:
    print(f"  Querying BioProject {bioproject_acc} …")

    time.sleep(REQUEST_DELAY)
    search = json.loads(ncbi_get(NCBI_ESEARCH, {
        "db": "bioproject",
        "term": bioproject_acc,
        "retmode": "json",
        "retmax": 1,
    }))
    ids = search.get("esearchresult", {}).get("idlist", [])
    if not ids:
        print(f"  WARNING: No BioProject record found for {bioproject_acc}")
        return []

    time.sleep(REQUEST_DELAY)
    link_data = json.loads(ncbi_get(NCBI_ELINK, {
        "dbfrom": "bioproject",
        "db": "sra",
        "id": ids[0],
        "retmode": "json",
    }))

    sra_uids = []
    for linkset in link_data.get("linksets", []):
        for linksetdb in linkset.get("linksetdbs", []):
            if linksetdb.get("dbto") == "sra":
                sra_uids.extend(linksetdb.get("links", []))

    if not sra_uids:
        print(f"  WARNING: No SRA records linked to {bioproject_acc}")
        return []

    print(f"  Found {len(sra_uids)} SRA record(s) for {bioproject_acc}")

    results = []
    for i in range(0, len(sra_uids), EFETCH_BATCH):
        batch = sra_uids[i : i + EFETCH_BATCH]
        time.sleep(REQUEST_DELAY)
        csv_text = ncbi_get(NCBI_EFETCH, {
            "db": "sra",
            "id": ",".join(batch),
            "rettype": "runinfo",
            "retmode": "text",
        })
        for row in csv.DictReader(csv_text.splitlines()):
            srr = row.get("Run", "").strip()
            name = (row.get("LibraryName") or row.get("SampleName") or row.get("Experiment") or "").strip()
            if srr[:3] in ("SRR", "ERR", "DRR"):
                results.append({"srr": srr, "name": name, "source": bioproject_acc})

    return results


def fetch_srr_name(srr_acc: str) -> str:
    time.sleep(REQUEST_DELAY)
    try:
        search = json.loads(ncbi_get(NCBI_ESEARCH, {
            "db": "sra",
            "term": srr_acc,
            "retmode": "json",
            "retmax": 1,
        }))
        ids = search.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return ""
        time.sleep(REQUEST_DELAY)
        csv_text = ncbi_get(NCBI_EFETCH, {
            "db": "sra",
            "id": ids[0],
            "rettype": "runinfo",
            "retmode": "text",
        })
        for row in csv.DictReader(csv_text.splitlines()):
            return (row.get("LibraryName") or row.get("SampleName") or row.get("Experiment") or "").strip()
    except Exception as e:
        print(f"  WARNING: Could not fetch name for {srr_acc}: {e}")
    return ""

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    design_file  = sys.argv[1] if len(sys.argv) > 1 else "design.tsv"
    srr_out      = "SRR_accessions.tsv"
    ref_url_out  = "ref_url.txt"

    samples    = []   # accessions with type == sample
    ref_acc    = None # accession with type == reference

    with open(design_file, newline="") as fh:
        for row in csv.DictReader(fh, delimiter=","):
            acc      = row.get("Accession", "").strip()
            row_type = row.get("type", "").strip().lower()
            if not acc:
                continue
            if row_type == "reference":
                ref_acc = acc
            elif row_type == "sample":
                samples.append(acc)

    print(f"Read {len(samples)} sample accession(s) and reference '{ref_acc}' from {design_file}")

    # ── Resolve reference FTP URL ─────────────────────────────────────────────
    if ref_acc:
        try:
            ftp_url = resolve_ref_url(ref_acc)
            with open(ref_url_out, "w") as fh:
                fh.write(ftp_url + "\n")
            print(f"  Reference FTP URL written to {ref_url_out}: {ftp_url}")
        except Exception as e:
            print(f"  ERROR resolving reference URL: {e}")

    # ── Expand sample accessions to SRRs ──────────────────────────────────────
    all_srrs: list[dict] = []
    seen:     set[str]   = set()

    for acc in samples:
        if acc[:5] in ("PRJNA", "PRJEB", "PRJDB"):
            for entry in fetch_srrs_for_bioproject(acc):
                if entry["srr"] not in seen:
                    seen.add(entry["srr"])
                    all_srrs.append(entry)
        elif acc[:3] in ("SRR", "ERR", "DRR"):
            if acc not in seen:
                seen.add(acc)
                print(f"  Fetching name for individual run {acc} …")
                all_srrs.append({"srr": acc, "name": fetch_srr_name(acc), "source": "individual"})
        else:
            print(f"  Skipping unrecognized accession: {acc}")

    with open(srr_out, "w", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["SRR_Accession", "Name", "Source"])
        for entry in all_srrs:
            writer.writerow([entry["srr"], entry["name"], entry["source"]])

    print(f"\nDone. {len(all_srrs)} SRR accession(s) written to {srr_out}")


if __name__ == "__main__":
    main()
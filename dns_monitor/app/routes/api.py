from flask import Blueprint, jsonify
from collections import defaultdict
import requests
import io
from app.db import get_connection

bp = Blueprint("api", __name__)

@bp.route("/api/as_stats")
def as_stats():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT asn, COUNT(*) AS count
            FROM as_info
            WHERE asn IS NOT NULL
            GROUP BY asn
            ORDER BY count DESC
        """)
        result = cur.fetchall()
    # Convert list of tuples to list of dictionaries for jsonify
    return jsonify([{"asn": r[0], "count": r[1]} for r in result])

@bp.route("/api/ripe_as_stats")
def ripe_as_stats():
    url = "https://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-latest"
    try:
        response = requests.get(url)
        response.raise_for_status()

        stats = defaultdict(int)
        for line in io.StringIO(response.text):
            parts = line.strip().split("|")
            if len(parts) >= 7 and parts[0] == "ripencc" and parts[2] == "asn" and parts[1] == "RU":
                try:
                    year = int(parts[5][:4])
                    # parts[4] is the count of ASNs being allocated/assigned
                    count = int(parts[4]) if parts[4].isdigit() else 1
                    if parts[6] in ["allocated", "assigned"]:
                        stats[year] += count
                except ValueError: # Handle cases where parts[5] or parts[4] might not be integers
                    continue

        return jsonify([{"year": y, "count": c} for y, c in sorted(stats.items())])

    except requests.RequestException:
        return jsonify({"error": "Download failed"}), 500
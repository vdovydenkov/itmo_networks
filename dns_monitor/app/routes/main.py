from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from app.db import get_connection
from app.services.ip_lookup import resolve_ip_asn

bp = Blueprint("main", __name__)

@bp.before_app_request
def log_http_request():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    path = request.path
    timestamp = datetime.utcnow().isoformat()

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO http_logs (ip, timestamp, path) VALUES (%s, %s, %s)",
            (ip, timestamp, path)
        )

        cur.execute("SELECT 1 FROM as_info WHERE ip = %s", (ip,))
        if not cur.fetchone():
            asn, desc = resolve_ip_asn(ip)
            cur.execute(
                "INSERT INTO as_info (ip, asn, asn_desc) VALUES (%s, %s, %s)",
                (ip, asn, desc)
            )
        conn.commit() # Added commit

@bp.route("/")
def index():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT h.ip, h.timestamp, h.path, a.asn, a.asn_desc
            FROM http_logs h
            LEFT JOIN as_info a ON h.ip = a.ip
            ORDER BY h.timestamp DESC
            LIMIT 50
        """)
        logs = cur.fetchall()
    return render_template("http_logs.html", logs=logs)

@bp.route("/dns_requests")
def dns_requests():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT d.resolver_ip, d.domain, d.timestamp, a.asn, a.asn_desc
            FROM dns_logs d
            LEFT JOIN as_info a ON d.resolver_ip = a.ip
            ORDER BY d.timestamp DESC
            LIMIT 50
        """)
        records = cur.fetchall()
    return render_template("dns_requests.html", records=records)

@bp.route("/add_dns_log", methods=["POST"])
def add_dns_log():
    resolver_ip = request.form.get("resolver_ip")
    domain = request.form.get("domain")
    timestamp = datetime.utcnow().isoformat()

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO dns_logs (resolver_ip, domain, timestamp) VALUES (%s, %s, %s)",
            (resolver_ip, domain, timestamp)
        )
        cur.execute("SELECT 1 FROM as_info WHERE ip = %s", (resolver_ip,))
        if not cur.fetchone():
            asn, desc = resolve_ip_asn(resolver_ip)
            cur.execute(
                "INSERT INTO as_info (ip, asn, asn_desc) VALUES (%s, %s, %s)",
                (resolver_ip, asn, desc)
            )
        conn.commit() # Added commit

    flash("DNS-запись добавлена")
    return redirect(url_for("main.dns_requests"))

@bp.route("/ripe_asn_chart")
def ripe_stats_page():
    return render_template("ripe_asn_chart.html")

@bp.route("/dns_as_stats")
def dns_as_stats():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.asn, a.asn_desc, COUNT(DISTINCT d.resolver_ip) AS unique_resolvers
            FROM dns_logs d
            JOIN as_info a ON d.resolver_ip = a.ip
            GROUP BY a.asn, a.asn_desc
            ORDER BY unique_resolvers DESC
        """)
        providers = cur.fetchall()
    return render_template("dns_as_stats.html", providers=providers)

@bp.route("/dns_http_correlation")
def dns_http_correlation():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                h.ip,
                h.timestamp AS http_time,
                h.path,
                d.domain,
                d.timestamp AS dns_time,
                a.asn,
                a.asn_desc
            FROM http_logs h
            JOIN dns_logs d ON h.ip = d.resolver_ip
            LEFT JOIN as_info a ON h.ip = a.ip
            ORDER BY h.timestamp DESC
            LIMIT 50
        """)
        results = cur.fetchall()
    return render_template("dns_http_correlation.html", results=results)
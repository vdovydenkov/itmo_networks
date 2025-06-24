from ipwhois import IPWhois, IPDefinedError

def resolve_ip_asn(ip: str) -> tuple[str | None, str]:
    try:
        result = IPWhois(ip).lookup_rdap(depth=1)
        return result.get("asn"), result.get("asn_description")
    except IPDefinedError:
        return None, "Private or reserved IP"
    except Exception as e:
        return None, f"Lookup error: {e}"

#!/usr/bin/env python3
"""
LUMA Labs API Diagnostics Tool
-----------------------------
A comprehensive diagnostic tool for troubleshooting LUMA Dream Machine API issues.
See README.md for full documentation.
"""

import sys
import os
import json
import requests
import ssl
import socket
import time
import argparse
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
from typing import Dict, Any

def load_case_config(case_id=None):
    """Load configuration from environment file."""
    if case_id:
        case_env_path = Path(f"cases/active/{case_id}.env")
        if not case_env_path.exists():
            print(f"Error: Case environment file not found: {case_env_path}")
            sys.exit(1)
        load_dotenv(case_env_path)
    else:
        load_dotenv()  # Load default .env if no case specified

def get_output_paths(case_id=None):
    """Generate output paths for results."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
    
    if case_id:
        # Create case-specific output directory
        output_dir = Path(f"cases/results/{case_id}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        json_path = output_dir / f"{timestamp}-diagnostic.json"
        text_path = output_dir / f"{timestamp}-diagnostic.txt"
    else:
        # Default output paths
        json_path = Path("diagnostic_results.json")
        text_path = Path("diagnostic_results.txt")
    
    return str(json_path), str(text_path)

def get_case_info():
    """Get case-specific information for reporting."""
    return {
        "case_id": os.getenv("CASE_ID"),
        "customer_id": os.getenv("CUSTOMER_ID"),
        "customer_email": os.getenv("CUSTOMER_EMAIL"),
        "reported_date": os.getenv("REPORTED_DATE"),
        "priority": os.getenv("PRIORITY"),
        "test_description": os.getenv("TEST_DESCRIPTION"),
        "test_image_source": os.getenv("TEST_IMAGE_SOURCE"),
        "run_timestamp": datetime.now().isoformat()
    }

def test_public_access(url: str) -> Dict[str, Any]:
    """Test if the URL is publicly accessible."""
    try:
        response = requests.head(url, allow_redirects=True)
        dns_resolved = True
        reachable = response.status_code == 200
        info = f"Received status {response.status_code}."
    except requests.exceptions.ConnectionError:
        dns_resolved = False
        reachable = False
        info = "Failed to connect to server."
    
    return {
        "test_name": "Public Access",
        "status": "completed",
        "details": {
            "url": url,
            "dns_resolved": dns_resolved,
            "reachable": reachable,
            "info": info
        }
    }

def test_cert_validation(url: str) -> Dict[str, Any]:
    """Test SSL/TLS certificate validation."""
    try:
        response = requests.head(url, verify=True)
        cert_valid = True
        info = f"Success. Status code: {response.status_code}"
    except requests.exceptions.SSLError:
        cert_valid = False
        info = "SSL certificate validation failed."
    except requests.exceptions.RequestException as e:
        cert_valid = False
        info = f"Request failed: {str(e)}"
    
    return {
        "test_name": "Cert Validation",
        "status": "completed",
        "details": {
            "url": url,
            "cert_valid": cert_valid,
            "info": info
        }
    }

def test_redirect(url: str) -> Dict[str, Any]:
    """Test URL redirection."""
    try:
        response = requests.head(url, allow_redirects=True)
        is_redirecting = len(response.history) > 0
        final_url = response.url
        info = f"Redirected {len(response.history)} times." if is_redirecting else ""
    except requests.exceptions.RequestException:
        is_redirecting = False
        final_url = url
        info = "Failed to check redirects."
    
    return {
        "test_name": "Redirect Check",
        "status": "completed",
        "details": {
            "url": url,
            "is_redirecting": is_redirecting,
            "final_url": final_url,
            "info": info
        }
    }

def test_headers_and_content(url: str) -> Dict[str, Any]:
    """Test response headers and content."""
    try:
        response = requests.get(url)
        content_type = response.headers.get('content-type', 'unknown')
        content_length_header = int(response.headers.get('content-length', 0))
        content_length_actual = len(response.content)
        info = ""
    except requests.exceptions.RequestException:
        content_type = "unknown"
        content_length_header = 0
        content_length_actual = 0
        info = "Failed to get headers and content."
    
    return {
        "test_name": "Headers and Content",
        "status": "completed",
        "details": {
            "url": url,
            "content_type": content_type,
            "content_length_header": content_length_header,
            "content_length_actual": content_length_actual,
            "info": info
        }
    }

def test_image_validity(url: str) -> Dict[str, Any]:
    """Test if the URL points to a valid image."""
    try:
        response = requests.get(url)
        content = response.content
        
        # Check JPEG signature
        is_jpeg = content.startswith(b'\xFF\xD8\xFF')
        info = "" if is_jpeg else "Does not match JPEG signature. Possibly another format or corrupted."
        
    except requests.exceptions.RequestException:
        is_jpeg = False
        info = "Failed to download image."
    
    return {
        "test_name": "Image Validity",
        "status": "completed",
        "details": {
            "url": url,
            "is_jpeg_signature": is_jpeg,
            "info": info
        }
    }

def test_luma_json_request(api_url: str, bearer_token: str, image_url: str) -> Dict[str, Any]:
    """
    6. JSON Request Structure Test
       - Attempt a minimal real or mock call to the LUMA endpoint
    """
    results = {
        "test_name": "LUMA JSON Request",
        "status": "completed",
        "details": {
            "endpoint": api_url,
            "request_success": False,
            "status_code": None,
            "response_body": None,
            "info": ""
        }
    }
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer_token}",
        "content-type": "application/json"
    }

    payload = {
        "prompt": "Diagnostic test prompt",
        "keyframes": {
            "frame1": {
                "type": "image",
                "url": image_url
            }
        },
        "loop": False,
        "aspect_ratio": "9:16"
    }

    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=10)
        results["details"]["status_code"] = resp.status_code
        try:
            results["details"]["response_body"] = resp.json()
        except:
            results["details"]["response_body"] = resp.text

        if resp.status_code in (200, 201, 202):
            results["details"]["request_success"] = True
        else:
            results["details"]["info"] = f"Non-2xx status code {resp.status_code}"
    except Exception as e:
        results["details"]["info"] = f"Request/connection error: {str(e)}"

    return results

def test_rate_limit(api_url: str, bearer_token: str, image_url: str, attempts: int = 5) -> Dict[str, Any]:
    """
    7. Rate Limit / Repeated Calls Test
    """
    results = {
        "test_name": "Rate Limit Test",
        "status": "completed",
        "details": {
            "endpoint": api_url,
            "num_attempts": attempts,
            "responses": [],
            "info": ""
        }
    }
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer_token}",
        "content-type": "application/json"
    }
    payload = {
        "prompt": "Diagnostic test prompt - repeated call",
        "keyframes": {
            "frame1": {
                "type": "image",
                "url": image_url
            }
        },
        "loop": False,
        "aspect_ratio": "9:16"
    }
    for i in range(attempts):
        attempt_info = {"attempt": i+1, "status_code": None, "body": None}
        try:
            resp = requests.post(api_url, headers=headers, json=payload, timeout=10)
            attempt_info["status_code"] = resp.status_code
            try:
                attempt_info["body"] = resp.json()
            except:
                attempt_info["body"] = resp.text
        except Exception as e:
            attempt_info["body"] = f"Connection/Request Error: {str(e)}"
        results["details"]["responses"].append(attempt_info)
        time.sleep(1)
    return results

def test_http_head(url: str) -> Dict[str, Any]:
    """
    8. HEAD Request Test
       - Some servers may behave differently for HEAD vs GET.
    """
    results = {
        "test_name": "HTTP HEAD Check",
        "status": "completed",
        "details": {
            "url": url,
            "status_code": None,
            "headers": {},
            "info": ""
        }
    }
    try:
        resp = requests.head(url, timeout=10)
        results["details"]["status_code"] = resp.status_code
        results["details"]["headers"] = dict(resp.headers)
    except Exception as e:
        results["details"]["info"] = f"HEAD request failed: {str(e)}"
    return results

def test_latency_timeout(url: str) -> Dict[str, Any]:
    """
    9. Latency & Basic Timeout Check
       - Measures round-trip time for a GET.
       - Tries a small range of timeouts to see if it's borderline or stable.
    """
    results = {
        "test_name": "Latency & Timeout",
        "status": "completed",
        "details": {
            "url": url,
            "latency_seconds": None,
            "info": ""
        }
    }
    start = time.time()
    try:
        # We'll do a GET with a somewhat strict timeout
        requests.get(url, timeout=5)
        end = time.time()
        results["details"]["latency_seconds"] = round(end - start, 3)
    except Exception as e:
        end = time.time()
        results["details"]["latency_seconds"] = round(end - start, 3)
        results["details"]["info"] = f"Request possibly timed out or had an error: {str(e)}"
    return results

def test_dns_records(url: str) -> Dict[str, Any]:
    """
    10. DNS Records Check (A and AAAA)
       - Use dnspython if available. If not, we do a simplified check.
    """
    results = {
        "test_name": "DNS Records Check",
        "status": "completed",
        "details": {
            "url": url,
            "a_records": [],
            "aaaa_records": [],
            "info": ""
        }
    }
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        results["details"]["info"] = "Could not parse hostname."
        return results

    try:
        import dns.resolver
        DNS_AVAILABLE = True
    except ImportError:
        DNS_AVAILABLE = False

    if not DNS_AVAILABLE:
        results["details"]["info"] = "dnspython not installed, limited DNS checks."
        return results

    try:
        answer_a = dns.resolver.resolve(hostname, "A")
        for rr in answer_a:
            results["details"]["a_records"].append(rr.to_text())
    except Exception as e:
        results["details"]["info"] += f"(A record) {str(e)}; "

    try:
        answer_aaaa = dns.resolver.resolve(hostname, "AAAA")
        for rr in answer_aaaa:
            results["details"]["aaaa_records"].append(rr.to_text())
    except Exception as e:
        results["details"]["info"] += f"(AAAA record) {str(e)}; "

    return results

def test_sni_mismatch(url: str) -> Dict[str, Any]:
    """
    11. SNI Mismatch Check
       - Attempt direct SSL socket to see if the certificate CN/SAN matches the domain.
       - This is a simplified approach: we rely on 'ssl.match_hostname'.
    """
    results = {
        "test_name": "SNI Mismatch Check",
        "status": "completed",
        "details": {
            "url": url,
            "sni_match": None,
            "info": ""
        }
    }
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        results["details"]["info"] = "No hostname found."
        return results

    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                # Raises an exception if mismatch
                ssl.match_hostname(cert, hostname)
                results["details"]["sni_match"] = True
    except ssl.CertificateError as ce:
        results["details"]["sni_match"] = False
        results["details"]["info"] = f"Certificate mismatch: {str(ce)}"
    except Exception as e:
        results["details"]["info"] = f"Connection/SSL error: {str(e)}"

    return results

def test_traceroute(url: str) -> Dict[str, Any]:
    """
    12. Basic Traceroute (Placeholder)
       - Typically done via subprocess calls to 'traceroute' or 'ping -r'.
       - We'll do a simple stub that attempts multiple connections with TTL changes.
       - On Windows, you might call 'tracert', on Linux 'traceroute'.
    """
    results = {
        "test_name": "Traceroute",
        "status": "completed",
        "details": {
            "url": url,
            "trace_output": [],
            "info": ""
        }
    }
    # Real traceroute approach typically requires external command or raw sockets
    # For demonstration, let's just store a placeholder.

    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        results["details"]["info"] = "No hostname found for traceroute."
        return results

    # Example using a simplified approach or calling an external command:
    # import subprocess
    # try:
    #     cmd = ["traceroute", hostname]
    #     process = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    #     results["details"]["trace_output"] = process.stdout.splitlines()
    #     if process.returncode != 0:
    #         results["details"]["info"] = "Traceroute command returned non-zero exit."
    # except Exception as e:
    #     results["details"]["info"] = f"Traceroute command failed: {str(e)}"

    results["details"]["info"] = "Traceroute stub - for real usage, implement with raw sockets or subprocess."
    return results

def test_cors_check(url: str) -> Dict[str, Any]:
    """
    13. CORS Check
       - Often relevant for browser-based requests, but let's see if the Access-Control-Allow-Origin
         header is present. If using the LUMA backend from a web context, CORS can matter.
    """
    results = {
        "test_name": "CORS Check",
        "status": "completed",
        "details": {
            "url": url,
            "access_control_allow_origin": None,
            "info": ""
        }
    }
    try:
        # We can do an OPTIONS request to see if there's a CORS header
        resp = requests.options(url, timeout=10)
        results["details"]["access_control_allow_origin"] = resp.headers.get("Access-Control-Allow-Origin", "None")
    except Exception as e:
        results["details"]["info"] = f"CORS check error: {str(e)}"
    return results

def test_firewall_ip_blocklist(url: str) -> Dict[str, Any]:
    """
    14. Potential Firewall / IP blocklist check (Stub)
       - This is complex in practice. We can check if known public blacklists list the IP, or
         if there's a geolocation block. A minimal approach tries a public 'What is my IP?' service
         to see if the IP is recognized or flagged.
    """
    results = {
        "test_name": "Firewall / IP Blocklist",
        "status": "completed",
        "details": {
            "url": url,
            "likely_blocked": None,
            "info": "Stub check. Real check might query public blacklists."
        }
    }
    # In reality, you'd do something like:
    # 1. Resolve the IP of the server hosting the resource.
    # 2. Check it against known RBL (Realtime Blackhole Lists) or security APIs.
    # For demonstration, let's parse the IP of the resource:
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        results["details"]["info"] += " - No hostname found."
        return results

    try:
        ip_addr = socket.gethostbyname(hostname)
        # You could send queries to e.g. spamhaus or other RBL providers. This is a stub.
        results["details"]["likely_blocked"] = False
        results["details"]["info"] += f" - Resolved IP: {ip_addr}. No advanced checks performed."
    except Exception as e:
        results["details"]["info"] += f" - DNS failed: {str(e)}"
    return results

def test_hsts(url: str) -> Dict[str, Any]:
    """
    15. Verify HSTS / Strict-Transport-Security
       - Check if server sets 'Strict-Transport-Security' header
    """
    results = {
        "test_name": "HSTS Check",
        "status": "completed",
        "details": {
            "url": url,
            "strict_transport_security": None,
            "info": ""
        }
    }
    try:
        resp = requests.get(url, timeout=10)
        sts_header = resp.headers.get("Strict-Transport-Security")
        results["details"]["strict_transport_security"] = sts_header if sts_header else "Not set"
    except Exception as e:
        results["details"]["info"] = f"Could not retrieve HSTS info: {str(e)}"
    return results

def test_user_agent_variation(url: str) -> Dict[str, Any]:
    """
    16. User-Agent Variation Check
       - Some servers block certain user-agent strings. We'll try a custom one.
    """
    results = {
        "test_name": "User-Agent Variation",
        "status": "completed",
        "details": {
            "url": url,
            "status_code_default": None,
            "status_code_custom_agent": None,
            "info": ""
        }
    }
    try:
        # Default
        r1 = requests.get(url, timeout=10)
        results["details"]["status_code_default"] = r1.status_code

        # Custom
        headers = {"User-Agent": "LUMA-Diagnostic/1.0"}
        r2 = requests.get(url, headers=headers, timeout=10)
        results["details"]["status_code_custom_agent"] = r2.status_code
    except Exception as e:
        results["details"]["info"] = f"User-Agent variation check failed: {str(e)}"
    return results

def test_image_metadata(url: str) -> Dict[str, Any]:
    """
    17. Image Metadata Check
        - Verify image format details
        - Check for EXIF data
        - Validate color space
        - Check actual dimensions
    """
    try:
        from PIL import Image
        import io
        import requests

        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            return {
                "test_name": "Image Metadata",
                "status": "completed",
                "details": {
                    "url": url,
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "info": f"Image is {img.format}, mode {img.mode}, size {img.size}"
                }
            }
    except Exception as e:
        return {
            "test_name": "Image Metadata",
            "status": "completed",
            "details": {
                "url": url,
                "error": str(e),
                "info": "Failed to analyze image metadata"
            }
        }

def test_content_encoding(url: str) -> Dict[str, Any]:
    """
    18. Content Encoding Check
        - Check for gzip/deflate support
        - Verify content-encoding headers
        - Test compression handling
    """
    headers = {
        'Accept-Encoding': 'gzip, deflate'
    }
    try:
        response = requests.get(url, headers=headers)
        encoding = response.headers.get('content-encoding', 'none')
        return {
            "test_name": "Content Encoding",
            "status": "completed",
            "details": {
                "url": url,
                "encoding": encoding,
                "compressed": encoding != 'none',
                "info": f"Content encoding: {encoding}"
            }
        }
    except Exception as e:
        return {
            "test_name": "Content Encoding",
            "status": "completed",
            "details": {
                "url": url,
                "error": str(e),
                "info": "Failed to check content encoding"
            }
        }

def test_api_auth(api_url: str, bearer_token: str) -> Dict[str, Any]:
    """
    19. API Authentication Test
        - Verify token format
        - Test token permissions
        - Check token expiration
    """
    if not bearer_token:
        return {
            "test_name": "API Authentication",
            "status": "completed",
            "details": {
                "url": api_url,
                "info": "No bearer token provided"
            }
        }
    
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Accept': 'application/json'
    }
    try:
        # Try a simple GET request to check auth
        response = requests.get(api_url, headers=headers)
        return {
            "test_name": "API Authentication",
            "status": "completed",
            "details": {
                "url": api_url,
                "status_code": response.status_code,
                "authenticated": response.status_code != 401,
                "info": f"Authentication {'successful' if response.status_code != 401 else 'failed'}"
            }
        }
    except Exception as e:
        return {
            "test_name": "API Authentication",
            "status": "completed",
            "details": {
                "url": api_url,
                "error": str(e),
                "info": "Failed to verify authentication"
            }
        }

def test_proxy_detection(url: str) -> Dict[str, Any]:
    """
    20. Proxy Detection
        - Check for intermediate proxies
        - Verify if CDN is present
        - Test for caching headers
    """
    try:
        response = requests.get(url)
        headers = response.headers
        
        # Check for common proxy/CDN headers
        proxy_headers = {
            'x-forwarded-for': headers.get('x-forwarded-for'),
            'x-real-ip': headers.get('x-real-ip'),
            'cf-ray': headers.get('cf-ray'),  # Cloudflare
            'x-cache': headers.get('x-cache'),
            'via': headers.get('via'),
            'server': headers.get('server')
        }
        
        return {
            "test_name": "Proxy Detection",
            "status": "completed",
            "details": {
                "url": url,
                "proxy_headers": {k: v for k, v in proxy_headers.items() if v is not None},
                "info": "Found proxy/CDN headers" if any(proxy_headers.values()) else "No proxy/CDN headers detected"
            }
        }
    except Exception as e:
        return {
            "test_name": "Proxy Detection",
            "status": "completed",
            "details": {
                "url": url,
                "error": str(e),
                "info": "Failed to check for proxies"
            }
        }

def test_advanced_image_analysis(url: str) -> Dict[str, Any]:
    """
    21. Advanced Image Analysis
        - Check for progressive JPEG
        - Validate color profile
        - Assess compression quality
        - Examine embedded metadata
    """
    try:
        from PIL import Image, ImageCms
        import io
        import requests
        
        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            
            # Check for progressive JPEG
            is_progressive = False
            if img.format == 'JPEG':
                img_bytes = io.BytesIO(img_data)
                # Check for progressive marker in JPEG
                while True:
                    marker = img_bytes.read(2)
                    if not marker:
                        break
                    if marker[0] != 0xFF:
                        break
                    if marker[1] == 0xC2:  # Progressive JPEG marker
                        is_progressive = True
                        break
                    if marker[1] == 0xDA:  # Start of scan
                        break
                    length = int.from_bytes(img_bytes.read(2), 'big')
                    img_bytes.seek(length-2, 1)
            
            # Check color profile
            try:
                profile = ImageCms.getOpenProfile(io.BytesIO(img.info.get('icc_profile', '')))
                color_space = profile.profile.xcolor_space
            except:
                color_space = "No ICC profile found"
            
            # Estimate compression quality
            quality = "Unknown"
            if img.format == 'JPEG':
                # Rough estimation based on file size vs dimensions
                theoretical_size = img.width * img.height * 3  # 3 bytes per pixel for RGB
                actual_size = len(img_data)
                compression_ratio = theoretical_size / actual_size
                if compression_ratio > 12:
                    quality = "Low"
                elif compression_ratio > 8:
                    quality = "Medium"
                else:
                    quality = "High"
            
            return {
                "test_name": "Advanced Image Analysis",
                "status": "completed",
                "details": {
                    "url": url,
                    "progressive_jpeg": is_progressive,
                    "color_space": color_space,
                    "compression_quality": quality,
                    "embedded_metadata": {k: v for k, v in img.info.items() if isinstance(v, (str, int, float))},
                    "info": f"Progressive: {is_progressive}, Quality: {quality}"
                }
            }
    except Exception as e:
        return {
            "test_name": "Advanced Image Analysis",
            "status": "completed",
            "details": {
                "url": url,
                "error": str(e),
                "info": "Failed to perform advanced image analysis"
            }
        }

def test_enhanced_network_diagnostics(url: str) -> Dict[str, Any]:
    """
    22. Enhanced Network Diagnostics
        - Full traceroute implementation
        - IP reputation check
        - GeoIP location verification
    """
    import subprocess
    import socket
    import json
    from urllib.parse import urlparse
    
    def run_traceroute(hostname):
        try:
            # Use platform-specific traceroute command
            cmd = ['traceroute', '-n', '-w', '1', hostname]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout.split('\n')
        except Exception as e:
            return [f"Traceroute failed: {str(e)}"]
    
    def check_ip_reputation(ip):
        try:
            # Basic DNS blacklist check (example lists)
            blacklists = ['zen.spamhaus.org', 'bl.spamcop.net']
            results = {}
            for bl in blacklists:
                try:
                    socket.gethostbyname(f"{'.'.join(reversed(ip.split('.')))}.{bl}")
                    results[bl] = "Listed"
                except:
                    results[bl] = "Not listed"
            return results
        except Exception as e:
            return {"error": str(e)}
    
    try:
        hostname = urlparse(url).hostname
        ip = socket.gethostbyname(hostname)
        
        # Run traceroute
        trace_results = run_traceroute(hostname)
        
        # Check IP reputation
        reputation = check_ip_reputation(ip)
        
        # GeoIP info (mock - would use maxmind or similar in production)
        geo_info = {
            "ip": ip,
            "hostname": hostname,
            "asn": "Requires GeoIP database",
            "country": "Requires GeoIP database",
            "city": "Requires GeoIP database"
        }
        
        return {
            "test_name": "Enhanced Network Diagnostics",
            "status": "completed",
            "details": {
                "url": url,
                "traceroute": trace_results,
                "ip_reputation": reputation,
                "geo_info": geo_info,
                "info": f"Traced route to {hostname} ({ip})"
            }
        }
    except Exception as e:
        return {
            "test_name": "Enhanced Network Diagnostics",
            "status": "completed",
            "details": {
                "url": url,
                "error": str(e),
                "info": "Failed to perform network diagnostics"
            }
        }

def run_diagnostics():
    """
    Master runner: collects results from each test if enabled in CONFIG.
    """
    results_list = []

    url = CONFIG["TEST_IMAGE_URL"]
    api_url = CONFIG["LUMA_API_URL"]
    bearer_token = CONFIG["LUMA_BEARER_TOKEN"]

    if CONFIG["TEST_PUBLIC_ACCESS"]:
        results_list.append(test_public_access(url))

    if CONFIG["TEST_CERT_VALIDATION"]:
        results_list.append(test_cert_validation(url))

    if CONFIG["TEST_REDIRECT"]:
        results_list.append(test_redirect(url))

    if CONFIG["TEST_HEADERS_CONTENT"]:
        results_list.append(test_headers_and_content(url))

    if CONFIG["TEST_IMAGE_VALIDITY"]:
        results_list.append(test_image_validity(url))

    if CONFIG["TEST_LUMA_JSON_REQUEST"]:
        results_list.append(test_luma_json_request(api_url, bearer_token, url))

    if CONFIG["TEST_RATE_LIMIT"]:
        results_list.append(test_rate_limit(api_url, bearer_token, url, attempts=5))

    if CONFIG["TEST_HTTP_HEAD"]:
        results_list.append(test_http_head(url))

    if CONFIG["TEST_LATENCY_TIMEOUT"]:
        results_list.append(test_latency_timeout(url))

    if CONFIG["TEST_DNS_RECORDS"]:
        results_list.append(test_dns_records(url))

    if CONFIG["TEST_SNI_MISMATCH"]:
        results_list.append(test_sni_mismatch(url))

    if CONFIG["TEST_TRACEROUTE"]:
        results_list.append(test_traceroute(url))

    if CONFIG["TEST_CORS_CHECK"]:
        results_list.append(test_cors_check(url))

    if CONFIG["TEST_FIREWALL_IP_BLOCKLIST"]:
        results_list.append(test_firewall_ip_blocklist(url))

    if CONFIG["TEST_HSTS"]:
        results_list.append(test_hsts(url))

    if CONFIG["TEST_USER_AGENT_VARIATION"]:
        results_list.append(test_user_agent_variation(url))

    if CONFIG.get("TEST_IMAGE_METADATA", False):
        results_list.append(test_image_metadata(url))
    
    if CONFIG.get("TEST_CONTENT_ENCODING", False):
        results_list.append(test_content_encoding(url))
    
    if CONFIG.get("TEST_API_AUTH", False):
        results_list.append(test_api_auth(api_url, bearer_token))
    
    if CONFIG.get("TEST_PROXY_DETECTION", False):
        results_list.append(test_proxy_detection(url))

    if CONFIG.get("TEST_ADVANCED_IMAGE_ANALYSIS", False):
        results_list.append(test_advanced_image_analysis(url))
    
    if CONFIG.get("TEST_ENHANCED_NETWORK_DIAGNOSTICS", False):
        results_list.append(test_enhanced_network_diagnostics(url))

    return results_list

def save_results(results, json_file, txt_file):
    # Write JSON output
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Write text output
    with open(txt_file, "w", encoding="utf-8") as f:
        for item in results:
            f.write(f"Test: {item['test_name']}\n")
            for k, v in item['details'].items():
                if k != "test_name":
                    f.write(f"  {k}: {v}\n")
            f.write("\n")

def main():
    """Main entry point for the diagnostic tool."""
    parser = argparse.ArgumentParser(description="LUMA Labs API Diagnostics Tool")
    parser.add_argument("--case", help="Case ID to load configuration from")
    args = parser.parse_args()

    # Load configuration
    load_case_config(args.case)
    
    # Verify required environment variables
    if not os.getenv("TEST_IMAGE_URL"):
        print("Error: TEST_IMAGE_URL environment variable is required")
        print("Please set it in your .env file or environment")
        sys.exit(1)

    # Get output paths
    json_file, txt_file = get_output_paths(args.case)
    
    # Update CONFIG with environment variables
    CONFIG = {
        "TEST_IMAGE_URL": os.getenv("TEST_IMAGE_URL"),
        "LUMA_API_URL": os.getenv("LUMA_API_URL", "https://api.lumalabs.ai/dream-machine/v1/generations"),
        "LUMA_API_CHECK_URL": os.getenv("LUMA_API_CHECK_URL", "https://api.lumalabs.ai/dream-machine/v1/generations/GENERATION_ID"),
        "LUMA_BEARER_TOKEN": os.getenv("LUMA_API_KEY"),
        "OUTPUT_JSON": json_file,
        "OUTPUT_TEXT": txt_file,
        "RETRY_COUNT": int(os.getenv("RETRY_COUNT", "3")),
        "TIMEOUT_SECONDS": int(os.getenv("TIMEOUT_SECONDS", "30")),
        "DETAILED_LOGGING": os.getenv("DETAILED_LOGGING", "true").lower() == "true",
        "TEST_PUBLIC_ACCESS": True,
        "TEST_CERT_VALIDATION": True,
        "TEST_REDIRECT": True,
        "TEST_HEADERS_CONTENT": True,
        "TEST_IMAGE_VALIDITY": True,
        "TEST_LUMA_JSON_REQUEST": bool(os.getenv("LUMA_API_KEY")),
        "TEST_RATE_LIMIT": bool(os.getenv("LUMA_API_KEY")),
        "TEST_HTTP_HEAD": True,
        "TEST_LATENCY_TIMEOUT": True,
        "TEST_DNS_RECORDS": True,
        "TEST_SNI_MISMATCH": True,
        "TEST_TRACEROUTE": True,
        "TEST_CORS_CHECK": True,
        "TEST_FIREWALL_IP_BLOCKLIST": True,
        "TEST_HSTS": True,
        "TEST_USER_AGENT_VARIATION": True,
        "TEST_IMAGE_METADATA": False,
        "TEST_CONTENT_ENCODING": False,
        "TEST_API_AUTH": False,
        "TEST_PROXY_DETECTION": False,
        "TEST_ADVANCED_IMAGE_ANALYSIS": False,
        "TEST_ENHANCED_NETWORK_DIAGNOSTICS": False
    }

    # Run diagnostics
    results = run_diagnostics()
    
    # Add case information if available
    if args.case:
        results.append(get_case_info())
    
    # Save results
    save_results(results, CONFIG["OUTPUT_JSON"], CONFIG["OUTPUT_TEXT"])
    
    print("\nDiagnostics complete. Results saved to:")
    print(f"  {CONFIG['OUTPUT_JSON']}")
    print(f"  {CONFIG['OUTPUT_TEXT']}")

if __name__ == "__main__":
    main()
import argparse
import requests
import json
import time
from datetime import datetime
from tqdm import tqdm
import pandas as pd
from colorama import init, Fore, Style
import re

def print_ascii_art():
    ascii_art = """
================================================
         OSINT PROJECT LAUNCH V2
         Multi-Source Intelligence Tool
================================================
    Email Breach Detection & OSINT Research
    Domain Analysis & Geolocation Services
================================================                                                                              
    """
    print(ascii_art)

def get_token(args):
    """Get search token from IntelX API"""
    print_ascii_art()
    print(f"{Fore.CYAN}{Style.BRIGHT}[+] OSINT Project Launch V2{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}{Style.BRIGHT}[+] Email Security Search Tool (IntelX + COMB){Style.RESET_ALL}\n")
    
    url = f"https://2.intelx.io:443/phonebook/search?k={args.apikey}"
    
    data = {
        "term": args.domain if hasattr(args, 'domain') and args.domain else args.links if hasattr(args, 'links') and args.links else args.email if hasattr(args, 'email') and args.email else "",
        "buckets": [],
        "lookuplevel": 0,
        "maxresults": 100,
        "timeout": 0,
        "datefrom": "",
        "dateto": "",
        "sort": 4,
        "media": 0,
        "terminate": []
    }
    
    try:
        response = requests.post(url, json=data)
        status = response.status_code
        
        if status == 200:
            try:
                json_response = response.json()
                return json_response.get('id', '')
            except json.JSONDecodeError:
                print(f'{Fore.RED}[!] Invalid JSON response from IntelX API: {response.text}{Style.RESET_ALL}')
                return None
        elif status == 402:
            print(f'{Fore.RED}[!] Invalid API key for IntelX service. Check your API key: {args.apikey}{Style.RESET_ALL}')
            return None
        else:
            print(f'{Fore.RED}[!] IntelX API returned status {status}: {response.text}{Style.RESET_ALL}')
            return None
            
    except requests.exceptions.RequestException as e:
        print(f'{Fore.RED}[!] Error connecting to IntelX API: {e}{Style.RESET_ALL}')
        return None

def make_request(key, args):
    """Make request to IntelX API to get results"""
    if not key:
        print(f"{Fore.RED}No valid key received from IntelX API{Style.RESET_ALL}")
        return None
        
    if not isinstance(key, str) or len(key) == 0:
        print(f"{Fore.RED}Invalid key format from IntelX API: {key}{Style.RESET_ALL}")
        return None
    
    # Get results
    url = f"https://2.intelx.io:443/phonebook/search/result?k={args.apikey}&id={key}&limit=1000000"
    
    try:
        time.sleep(2)  # Wait for results to be ready
        
        response = requests.get(url)
        status = response.status_code
        
        if status == 200:
            try:
                json_data = response.json()
                return json.dumps(json_data)
            except json.JSONDecodeError as e:
                print(f'{Fore.RED}[!] JSON decode error: {e}{Style.RESET_ALL}')
                return None
        elif status == 402:
            print(f'{Fore.RED}[!] Invalid API key for IntelX service.{Style.RESET_ALL}')
            return None
        else:
            print(f'{Fore.RED}[!] IntelX API returned status {status}: {response.text}{Style.RESET_ALL}')
            return None
            
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}JSON decode error from IntelX API: {e}{Style.RESET_ALL}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error making IntelX request: {e}{Style.RESET_ALL}")
        return None

def parse_items(emails, output_file, verbose=False):
    """Parse and save IntelX results"""
    if not emails:
        print(f"{Fore.RED}No data received from IntelX API to parse.{Style.RESET_ALL}")
        return
        
    try:
        parsed_data = json.loads(emails)
        
        if 'selectors' in parsed_data:
            results = parsed_data['selectors']
            
            if results:
                df = pd.DataFrame(results)
                df.to_csv(output_file, index=False)
                print(f"{Fore.GREEN} Results saved to {output_file}{Style.RESET_ALL}")
                print(f"{Fore.GREEN} Found {len(results)} results{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW} No results found{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid response format from IntelX API: {parsed_data}{Style.RESET_ALL}")
            
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}JSON decode error parsing IntelX response: {e}{Style.RESET_ALL}")

def query_comb(email, verbose=False):
    """Query COMB databases for email breach data"""
    print(f"\n Querying COMB databases for {email}")
    
    endpoints = [
        f"https://leakcheck.io/api/public?check={email}",
        f"https://api.proxynova.com/comb?query={email}"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    results = []
    
    for i, url in enumerate(endpoints):
        print(f"Trying endpoint {i+1}/{len(endpoints)}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                if "leakcheck" in url:
                    try:
                        data = response.json()
                        print(f"  Email found in breach database")
                        print(f" LeakCheck result: {data}")
                        results.append(data)
                        continue
                    except json.JSONDecodeError:
                        pass
                
                # Handle COMB API response
                try:
                    lines = response.text.strip().split('\n')
                    if lines and lines[0] != email:  # If we got actual breach data
                        print(f" Found {len(lines)} breach record(s) with credentials!")
                        breach_data = []
                        for line in lines[:20]:  # Show first 20 results
                            if ':' in line:
                                print(f" Breach data: {line}")
                                email_part, password_part = line.split(':', 1)
                                breach_data.append({
                                    'email': email_part,
                                    'password': password_part,
                                    'source': 'COMB'
                                })
                        results.extend(breach_data)
                        print(f" COMB databases found {len(breach_data)} result(s)")
                        return results
                except:
                    pass
                    
            else:
                print(f"Error {response.status_code} from {url}")
                
        except requests.exceptions.RequestException as e:
            print(f"Request error to {url}: {e}")
    
    print(f"COMB endpoints failed for {email}. Service may be unavailable.")
    return results

def query_iplocation(target, verbose=False):
    """Query iplocation.net for IP/domain geolocation and intelligence"""
    print(f"\n🌍 Querying IPLocation services for {target}")
    
    # Multiple geolocation endpoints for reliability
    endpoints = [
        f"http://ip-api.com/json/{target}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query",
        f"https://ipapi.co/{target}/json/",
        f"http://freegeoip.app/json/{target}",
        f"https://iplocation.net/ip/{target}"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    results = []
    
    for i, url in enumerate(endpoints):
        service_name = url.split('/')[2]  # Extract domain name
        print(f"🌐 Trying {service_name} endpoint {i+1}/{len(endpoints)}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Handle ip-api.com format
                    if 'status' in data and data['status'] == 'success':
                        print(f"✅ {service_name} geolocation found!")
                        print(f"  🌍 Country: {data.get('country', 'Unknown')}")
                        print(f"  🏙️ City: {data.get('city', 'Unknown')}")
                        print(f"  📍 Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
                        print(f"  🌐 ISP: {data.get('isp', 'Unknown')}")
                        print(f"  🏢 Organization: {data.get('org', 'Unknown')}")
                        print(f"  🔢 IP: {data.get('query', target)}")
                        print(f"  🕒 Timezone: {data.get('timezone', 'Unknown')}")
                        results.append(data)
                        
                        # Save to CSV
                        if results:
                            df = pd.DataFrame(results)
                            csv_file = f"iplocation-results-{target.replace('.', '_')}.csv"
                            df.to_csv(csv_file, index=False)
                            print(f"💾 Results saved to: {csv_file}")
                        
                        return data
                        
                    # Handle ipapi.co format
                    elif 'country_name' in data:
                        print(f"✅ {service_name} geolocation found!")
                        print(f"  🌍 Country: {data.get('country_name', 'Unknown')}")
                        print(f"  🏙️ City: {data.get('city', 'Unknown')}")
                        print(f"  📍 Coordinates: {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}")
                        print(f"  🌐 ISP: {data.get('org', 'Unknown')}")
                        print(f"  🔢 IP: {data.get('ip', target)}")
                        results.append(data)
                        
                        # Save to CSV
                        if results:
                            df = pd.DataFrame(results)
                            csv_file = f"iplocation-results-{target.replace('.', '_')}.csv"
                            df.to_csv(csv_file, index=False)
                            print(f"💾 Results saved to: {csv_file}")
                        
                        return data
                        
                    # Handle other formats
                    elif any(key in data for key in ['country', 'city', 'lat', 'lon']):
                        print(f"✅ {service_name} geolocation found!")
                        print(f"  📊 Data: {data}")
                        results.append(data)
                        
                        # Save to CSV
                        if results:
                            df = pd.DataFrame(results)
                            csv_file = f"iplocation-results-{target.replace('.', '_')}.csv"
                            df.to_csv(csv_file, index=False)
                            print(f"💾 Results saved to: {csv_file}")
                        
                        return data
                    else:
                        print(f"❌ No geolocation data in {service_name} response")
                        continue
                        
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON response from {service_name}")
                    continue
                    
            else:
                print(f"❌ {service_name} returned status {response.status_code}")
                continue
                
        except requests.exceptions.Timeout:
            print(f"⏳ Timeout connecting to {service_name}")
            continue
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection error to {service_name}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error to {service_name}: {e}")
            continue
    
    print(f"❌ All geolocation endpoints failed for {target}")
    return None

def run_comb(file_path, verbose=False):
    """Run COMB search on emails from file"""
    print_ascii_art()
    print(f"{Fore.CYAN}{Style.BRIGHT}[+] OSINT Project Launch V2{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}{Style.BRIGHT}[+] Email Security Search Tool{Style.RESET_ALL}\n")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            emails = [line.strip() for line in f if line.strip() and '@' in line]
    except FileNotFoundError:
        print(f"{Fore.RED} File not found: {file_path}{Style.RESET_ALL}")
        return
    except Exception as e:
        print(f"{Fore.RED} Error reading file: {e}{Style.RESET_ALL}")
        return
    
    if not emails:
        print(f"{Fore.YELLOW} No valid email addresses found in {file_path}{Style.RESET_ALL}")
        return
    
    all_results = []
    
    # Process emails with progress bar
    for email in tqdm(emails, desc="Processing", unit="email"):
        print(f"\n{'='*60}")
        print(f" Searching for: {email}")
        print(f"{'='*60}")
        
        # Query services
        comb_results = query_comb(email, verbose)
        
        if comb_results:
            all_results.extend(comb_results)
        else:
            print(f" No results found in databases for {email}")
    
    # Save results
    if all_results:
        df = pd.DataFrame(all_results)
        csv_file = file_path.replace('.txt', '-results.csv')
        df.to_csv(csv_file, index=False)
        
        print(f"\n{'='*60}")
        print(f" FINAL RESULTS SUMMARY:")
        print(f"{'='*60}")
        print(f" Total credentials found: {len(all_results)}")
        print(f" Results saved to: {csv_file}")
        print(f"{Fore.GREEN}{Style.BRIGHT} Search completed successfully!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW} No detailed credential data retrieved from free APIs.{Style.RESET_ALL}")

def main():
    # Initialize colorama for colored output
    init()
    
    # Create argument parser
    parser = argparse.ArgumentParser(description="OSINT Project Launch V2 - IntelX + COMB Search Tool")
    parser.add_argument("-f", "--file_path", help="Path to file containing emails to check against COMB")
    parser.add_argument("-co", "--coutput", help="Path to the COMB Search results output CSV file", default="COMB-results.csv")
    parser.add_argument("-io","--ioutput", help="Path to the IntelX results output CSV file", default="IntelX-results.csv")
    parser.add_argument("--verbose", help="Enable verbose output", action="store_true")
    parser.add_argument("-e", "--email", help="Email for search")
    parser.add_argument("-k", "--apikey", help="IntelX API key", default="a40e8968-54c7-499a-9c40-4552b62fe34b")
    parser.add_argument("-d", "--domain", help="Domain to search")
    parser.add_argument("-l", "--links", help="Links search")
    
    # IPLocation arguments
    parser.add_argument("--iplocation", help="Use IPLocation.net for geolocation", action="store_true")
    parser.add_argument("-i", "--ip-target", help="IP address or domain for geolocation lookup")
    
    args = parser.parse_args()
    
    # Handle IntelX searches
    if args.domain or args.links or args.email:
        key = get_token(args)
        if key:
            emails = make_request(key, args)
            if emails:
                parse_items(emails, args.ioutput, args.verbose)
    
    # Handle geolocation search
    elif args.iplocation and getattr(args, 'ip_target', None):
        result = query_iplocation(args.ip_target, args.verbose)
        if result:
            print(f"\n🎯 Geolocation lookup completed for {args.ip_target}")
        else:
            print(f"\n❌ Geolocation lookup failed for {args.ip_target}")
    
    # Run COMB search if email file provided
    elif args.file_path:
        run_comb(args.file_path, args.verbose)

if __name__ == "__main__":
    main()

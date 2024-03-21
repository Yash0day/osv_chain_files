import re
import requests
import json

def parse_json_response(response_json):
    #print(response_json.get('vulns', []))
    
    vulns = response_json.get('vulns',[])

    for vuln in vulns: 
        print("[+] ID: ", vuln['id'])
        print("[+] Description: ", vuln.get('details', vuln.get('summary', 'No description available')))
        
        print("[+] Affected Versions: ", vuln['affected'])
        
        print("[+] Alias: ", vuln.get('aliases', 'No aliases available') )  #Handling the unavailability of aliases gracefully
        print("<---------------------------------------->")

    
    return 

def fetch_vulnerabilities(package_name, version_number):
    url = 'https://api.osv.dev/v1/query'
    payload = {  #OSV Post request
        "version": version_number,
        "package": {
            "name": package_name,
        }
    }

    response = requests.post(url, json=payload)
    
    if response.content != b'{}':  #  Response is not empty
        response_json = response.json()  # Extract JSON content from the response
        #print(response_json)
        parse_json_response(response_json)
            
    else:
        print(f"[-] No vulnerabilities found for package {package_name}.")

def extract_packages(file_path):  #Extract the Packages from the installed_pakages.txt
    packages = {}
    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(r'(\S+)\s+(.+)', line)
            if match:
                package_name, version = match.groups()
                packages[package_name.lower()] = version.split('-')[0]
    return packages  #Returning a Dictionary of the form packageName:versionNumber

def main():
    file_path = "installed_packages.txt"
    packages = extract_packages(file_path)

    for package, version in packages.items():
        print("\t [*] Scanning ^ - ^ ", package , ":", version)
        fetch_vulnerabilities(package,version)


main()

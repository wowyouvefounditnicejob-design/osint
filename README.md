# OSINT Project Launch V2

## Overview
The OSINT Project Launch V2 is a comprehensive Open Source Intelligence (OSINT) tool designed to perform various cybersecurity and intelligence-related searches. It leverages multiple external APIs to query databases and retrieve information related to email addresses, compromised credentials, leaked passwords, domain intelligence, and geolocation data. The tool integrates searches from COMB (Combination Of Many Breaches), IntelX (Phonebook.cz), BreachDirectory, DeHashed, Breach.VIP, OSINT.Industries, and IPLocation services.

## Features
1. **HudsonRock Search:**
   - Queries the HudsonRock database for information related to a given email address.
   - Extracts details such as stealer family, date uploaded, date compromised, computer name, operating system, and antiviruses.
   - Optionally saves the results to an Excel file.

2. **COMB Search:**
   - Performs a leaked password search using the COMB database (Combination Of Many Breaches).
   - Extracts usernames and passwords associated with the provided email addresses.
   - Optionally saves the results to an Excel file.

3. **IntelX Domain Search:**
   - Utilizes the IntelX API to search for emails, subdomains, or links related to a specified domain.
   - Requires a valid IntelX API key.
   - Optionally saves the extracted information to a file.

## What is Cavalier API? 

Hudson Rock provides its clients the ability to query a database of over 20,774,497 computers which were compromised through global info-stealer campaigns performed by threat actors. The database is updated with new compromised computers every day, offering cybersecurity providers the ability to alert security teams ahead of imminent attacks, when users get compromised and have their credentials stolen.

## What is Phonebook.cz? 

Phonebook lists all domains, email addresses, or URLs for the given input domain. You can search 121 billion records. In some instances the path or query part may contain clear-text password.

## Prerequisites
- Python 3.6 or later
- Required Python packages (install using `pip install -r requirements.txt`):
  - `argparse`
  - `requests`
  - `json`
  - `time`
  - `datetime`
  - `tqdm`
  - `pandas`
  - `colorama`

## Usage

### Command Line Arguments
- `-f, --file-path`: Path to the text file containing email addresses for HudsonRock and COMB Search.
- `--houtput`: Path to the HudsonRock Search results output Excel file (default: HudsonRock-results.xlsx).
- `--coutput`: Path to the COMB Search results output Excel file (default: COMB-results.xlsx).
- `--verbose`: Display detailed results in the terminal.
- `-e, --email`: Search all emails for the provided domain.
- `-k, --apikey`: IntelX API key.
- `-d, --domain`: Search all subdomains for the provided domain.
- `-l, --links`: Search all links for the provided domain (may include cleartext passwords from stealer logs).
- `--ioutput`: Stores all items in a file *_cz.txt for IntelX domain search.


### Running the Script
1. Open a terminal.
2. Navigate to the directory containing the script.
3. Run the script using the command:
   ```
   python osintprojectlaunchv2.py [arguments]
   ```

### Examples
- Run HudsonRock search:
  ```
  python osintprojectlaunchv2.py -f emails.txt --verbose
  ```

- Run IntelX domain search:
  ```
  python osintprojectlaunchv2.py -l example.com -k your_intelx_api_key --ioutput
  ```

- Run COMB search:
  ```
  python osintprojectlaunchv2.py -f emails.txt --coutput COMB-results.csv
  ```

### Screenshots

![OSINT Project Launch V2](https://github.com/yasinyilmaz/osint/assets/37842751/3460352d-fb49-4f19-b9b0-4d76b63eccc9)

![OSINT Search Results](https://github.com/yasinyilmaz/osint/assets/37842751/1fef66f3-ce8f-4771-83b9-e9d977c3c970)

![Geolocation and Breach Data](https://github.com/yasinyilmaz/osint/assets/37842751/3dbc4928-c535-47b7-816c-0b92f645dbf0)



## Notes
- Throttling is implemented to avoid exceeding API rate limits (e.g., one request every 10 seconds).
- The IntelX domain search requires a valid API key.

Feel free to customize and extend the script based on your specific use case or integrate additional functionalities.

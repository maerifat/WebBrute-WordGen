import os
import requests
import re
from requests.exceptions import HTTPError

domainfile = open('dfile.txt', 'r')
domains = domainfile.readlines()


for domain in domains:
    cmd= (f"gospider -s {domain}  | egrep -o '{domain}.*$'| egrep -v '(\.png|\.css|\.svg|\.js|\.gif|\.jpg|\?|\.jpeg|\.mp4|\.pdf)'|sort -u |tee -a file.txt; echo {domain} >>file.txt").replace('\r', '').replace('\n', '')
    os.system(cmd)

cmd2="sort -u -o file.txt file.txt"   
os.system(cmd2)

urlfile= open('file.txt', 'r')
urls = urlfile.readlines()
   
    
    
wordlist  = []
for nonurl in urls:
    url= nonurl.strip()
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        for string in re.findall('[a-zA-Z0-9]+', str(response.content)):
            if len(string) < 15 and len(string)> 1 and string.lower() not in wordlist and str(string.isdecimal())=="False":
                wordlist.append(string.lower())

wordlist.sort()               
for word in wordlist:
    wordlistfile= open('wordlist.txt', 'a')
    wordlistfile.write(f'{word}\n')
    wordlistfile.close()
print (len(wordlist))



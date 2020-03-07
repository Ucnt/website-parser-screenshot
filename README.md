# Website Parse and Screenshot

## Purpose
While investigating potentially suspicious domains and webpages, I have had the need to:

1. Get the website's source code
2. See what resources the website loads
3. Take a screenshot of the website.

This does all of that in a docker container, allowing you to mount a volume, keep the results, and destroy it.

## Execution
- Build: docker build -t website-parser . 

- Run: docker run -v ~/website-parser/output:/opt/parser/output --rm -it website-parser google.com

    - Note: This sends results to ~/website-parser/output.  That can be changed as you see fit.

## Output files, e.g. for google.com

- google[.]html: Raw HTML of the webpage

- google[.]har: HTTP Archive file (https://en.wikipedia.org/wiki/HAR_(file_format))

- google[.]png: Screenshot at 1920, 2000 (static values in script)

## Notes
- The script will try to add "http://" and/or "https://" to try and get a result.

- One technique is to 
    - Put this docker image on a VM in something like GCP/AWS
    - Run the command with something like this alias 
    '''
function parse-screenshot (){
    echo "Parsing and getting screenshot for $1"
    # Scrape page
    ssh [VM_IP] bash -c "'sudo docker run -v /tmp/output:/opt/parser/output --rm website-parser $1'"
    # Get scraped files to current directory
    scp [VM_IP]:/tmp/output/* .
    # Remove old scraped files
    ssh [VM_IP] bash -c "'sudo rm /tmp/output/*'"
}
'''
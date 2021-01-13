#!/usr/bin/env python3
'''
Purpose, given a URL:
    - Save a screenshot of it
    - Get its HTML
    - Get its har file (resources loaded)
'''
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import sys
import os
# Get the current directory
cur_dir = os.path.dirname(os.path.realpath(__file__))
# Set the browsermob and geckodriver locations
browsermob_location="{}/browsermob-proxy-2.1.4/bin/browsermob-proxy".format(cur_dir)
geckodriver_location="{}/geckodriver/geckodriver".format(cur_dir)
# Set the output directory
output_dir = "{}/output".format(cur_dir)


def load_page(url):
    # Create a filename for the output files
    file_name = url.lower().replace("http://","").replace("https://","").replace("www.","").split("/")[0].replace("-","_").replace(".","_")

    #Initialize a server/proxy for loading the page
    server = Server(browsermob_location)
    server.start()
    proxy = server.create_proxy()
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    profile.set_proxy(proxy.selenium_proxy())
    opts = Options()
    opts.set_headless()
    assert opts.headless
    driver = webdriver.Firefox(options=opts, firefox_profile=profile, executable_path=geckodriver_location)
    proxy.new_har(url, options={'captureHeaders': True})

    # Try to load the page
    try:
        driver.get(url)
    except Exception as e:
        print("Error during load of {}: {}".format(url, str(e).strip()))
        # Be sure you try HTTP and HTTPS
        if "https://" not in url:
            url = url.replace("http://","https://")
            driver.get(url)

    # Parse the HTML
    try:
        print("Getting HTML")        
        with open('{}/{}.html'.format(output_dir, file_name), 'w+', encoding='utf-8') as save_html:
            save_html.write(str(driver.page_source))
    except Exception as e:
        print("Error getting page source: {}".format(str(e)))

    # Get a screenshot with static size as pages will have different formats.
    try:
        print("Getting Screenshot")
        driver.set_window_size(1920, 2000)
        driver.save_screenshot('{}/{}.png'.format(output_dir, file_name))
    except Exception as e:
        print("Error getting screenshot: {}".format(str(e)))

    # Get the har data (e.g. resources it loads)
    try:
        print("Getting HAR data")
        har_data = json.dumps(proxy.har, indent=4)
        with open('{}/{}.har'.format(output_dir, file_name), 'w+') as save_har:
            save_har.write(str(har_data))
    except Exception as e:
        print("Error getting har: {}".format(str(e)))


    # Kill everything...
    server.stop()
    driver.quit()

    print("Done!")



if __name__ == "__main__":
    # If you don't get a website, you need to give one....
    if len(sys.argv) < 2:
        print("need a website")
    else:
        url = sys.argv[1]
        # Be sure a [.] or [dot] is swapped
        url = url.replace("[.]",".")
        url = url.replace("[dot]",".")
        # Add http:// at first if it's not there.
        if "http://" not in url and "https://" not in url:
            url = "http://{}".format(url)
        # Run the page
        load_page(url=url)

#! /usr/bin/env python

import urllib
import urllib2
import argparse
import sys
import re
import time 
from webbrowser import open_new_tab
from urlparse import urlparse

                      
        
def get_download_links(url):
    """Returns a list of  links to download the video from th url"""
        
    requestHeaders = {
        "Origin": "http://savevideo.me",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": "http://savevideo.me/?lang=en",
        "Accept-Language": "en-US,en;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
        }

    
    request = urllib2.Request('http://savevideo.me/get/',
                                  urllib.urlencode({"url": url}),
                                  requestHeaders)

    try:
        response = urllib2.urlopen(request)
        xml = response.read()
        pattern = r'<a\s+href="(.*?)"\s*>.*?</a>(.*?)<br\s*/>' 
        links =  re.findall(pattern, xml)
        
        return links
    
    except urllib2.HTTPError, error:
        print error.read()        
            

def download_video(url):
    o = urlparse(url)
    timestamp = int(time.mktime(time.localtime()))
    file_name = str(timestamp) + o.path.split('/')[-1]

    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0]) / 1048576.
    print "Downloading: %s Bytes: %.2fM" % (file_name, file_size)
        
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()


def main():        
    parser = argparse.ArgumentParser(description='Download videos\
    from various video hosting sites\
    (youtube, vimeo, bliptv, dailymotion,...)')
    parser.add_argument("-cli",
                        help="Download link on the command line instead\
                        of opening link in the system's default browser ",
                        action='store_true')
    parser.add_argument("url",
                       help="The url of the file you wish to download")

    args = parser.parse_args()                         
    links = get_download_links(args.url)

    if links is not None:
        
        print "Choose File you wish to Download"    
        for i in range(len(links)):
            print "[%d] :  %s" % (i, links[i][1])        

        link = raw_input('> ')

        if args.cli:
            download_video(links[int(link)][0])    
        else:
            open_new_tab(links[int(link)][0])                            
    else:
        print "Service unavailable please try again"


if __name__ == "__main__":
    main()


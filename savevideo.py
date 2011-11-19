import urllib
import urllib2
import argparse
import sys
import re
from webbrowser import open_new_tab
from urlparse import urlparse
from random import randint
                      
        
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
        pattern = r'<a\s+href="(.*?)"\s*>'        
        links =  re.findall(pattern, xml)
        
        return links
    
    except urllib2.HTTPError, error:
        print error.read()        
            

def download_video(url):
    o = urlparse(url)
    file_name = o.path.split('/')[-1] +  str(randint(1,10000))
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
        
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
    parser = argparse.ArgumentParser(description='Download a video')
    parser.add_argument("-nb",
                        help="Download link in console instead\
                        of opening link in the system's default browser ",
                        action='store_true')
    parser.add_argument("url",
                       help="The url of the file you wish to download")

    args = parser.parse_args()                         
    links = get_download_links(args.url)
        
    print "Choose File you wish to Download"    
    for i in range(len(links)):
        print "[%d] :  %s" % (i, links[i])        

    link = raw_input('> ')

    if args.nb:
        download_video(links[int(link)])    
    else:
        open_new_tab(links[int(link)])                            


if __name__ == "__main__":
    main()


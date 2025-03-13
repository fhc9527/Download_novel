# coding=utf-8
# LanMao
# @time: 2025/3/13上午9:55
from optparse import OptionParser
from Books import *
if __name__ == '__main__':
    banner = (
        """
         _                 _        
        | |__   ___   ___ | | _____ 
        | |_ \ / _ \ / _ \| |/ / __|
        | |_) | (_) | (_) | | <\__ \ 
        |_|__/ \___/ \___/|_|\_\___/
        """
    )
    print(banner)
    parser = OptionParser()
    parser.add_option("-u", "--url", dest="web_url",
                     help="web url", metavar="website url")
    (options, args) = parser.parse_args()
    if options.web_url is None:
            #打印提示信息
        parser.print_help()
    else:
        Books.scrape_and_save(options.web_url)
初学python，纯新手，手敲加AI制作了一个网业小说爬取的python脚本，能够获取一些网站的免费书籍，只适用一些适合的网站，主要还是用于python的学习，不做于商用，不要用非法途径，维护网络安全空间人人有责。
主要分为2个部分入口函数的调用和类的制作。
第一个部分：
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
 命令：python Download_novel.py -u https://www.xxx.xom/12




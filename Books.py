import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class Books:
    @staticmethod
    def scrape_chapter(chapter_number, chapter_name, chapter_url, headers):
        """
        爬取章节正文内容
        """
        try:
            time.sleep(1)  # 避免请求过快，添加延时
            chapter_response = requests.get(chapter_url, headers=headers, timeout=10)
            chapter_response.raise_for_status()

            chapter_soup = BeautifulSoup(chapter_response.content, 'html.parser')
            content_div = chapter_soup.find("div", id="content")
            content = content_div.get_text(strip=True) if content_div else "未找到正文内容"

            return chapter_number, chapter_name, content
        except Exception as e:
            return chapter_number, chapter_name, f"发生异常: {str(e)}"

    @staticmethod
    def scrape_and_save(url, output_dir="output"):
        """
        主函数，爬取小说的所有章节并保存到一个文件中
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "未知标题"

        chapter_list_div = soup.find("div", id="list")
        if not chapter_list_div:
            print("未找到 <div id='list'>，确认网页结构是否变化")
            return

        chapter_links = chapter_list_div.find_all("a")
        if not chapter_links:
            print("未找到章节链接，请检查网页结构")
            return

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{title}.txt")

        # 提取章节信息并存储元组
        chapters = [
            (index + 1, chapter.get_text(strip=True), urljoin(url, chapter.get("href")))
            for index, chapter in enumerate(chapter_links)
        ]

        results = []

        # 使用多线程抓取章节内容
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_chapter = {
                executor.submit(Books.scrape_chapter, chapter_number, chapter_name, chapter_url, headers): chapter_number
                for chapter_number, chapter_name, chapter_url in chapters
            }

            for future in as_completed(future_to_chapter):
                chapter_number, chapter_name, content = future.result()
                results.append((chapter_number, chapter_name, content))
                print(f"完成: 第{chapter_number}章 {chapter_name}")

        # 根据章节编号排序
        results.sort(key=lambda x: x[0])

        # 写入文件
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(f"书名: {title}\n\n")
            for chapter_number, chapter_name, content in results:
                file.write(f"章节: 第{chapter_number}章 {chapter_name}\n")
                file.write(f"正文:\n{content}\n\n")

        print(f"内容已成功写入 {output_file}")


if __name__ == "__main__":
    # 调用爬取
    start_url = ""
    Books.scrape_and_save(start_url)

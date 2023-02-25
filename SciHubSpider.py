import requests, re
from bs4 import BeautifulSoup as BS


class Scihub_Downloader:
    def __init__(self, doi):
        self.doi = doi
        self.downloadable = False
        try:
            self.pdf_url = self.get_pdf()
        except IndexError:
            self.pdf_url = None
        else:
            self.downloadable = True

    def get_pdf(self):
        url = f"https://sci-hub.wf/{self.doi}"
        header = {
            "authority": "sci-hub.wf", 
            "referer": "https://sci-hub.wf/", 
            "user-agent": "Mozilla/5.0"
        }
        r = requests.get(url, timeout=10, headers=header)
        soup = BS(r.text, "html.parser")
        button = soup.select("#buttons > ul > li > a")
        click = button[1].attrs["onclick"]
        pdf_url = re.findall(r"href='(.+?)'", click)[0]
        pdf_url = pdf_url.replace("\\/", '/')
        return pdf_url

    def save_pdf(self, name):
        header = {
            "user-agent": "Mozilla/5.0"
        }
        r_pdf = requests.get(self.pdf_url, headers=header)
        # if len(name) > 100:
        #     name = name[:100]  # 如果名字超过100字符，就只取前100个字符
        name = name if ".pdf" in name else name + ".pdf"
        with open(name, "wb") as fo:
            fo.write(r_pdf.content)


def test():
    # 正常情况下，顺利下载
    doi = "10.1109/tit.2011.2182033"
    sd = Scihub_Downloader(doi)
    # print(sd.pdf_url)
    # sd.save_pdf("thesis/test")
    print("success.")
    
    # 通常情况下，没有这个文献
    doi = "NeverGonnaGiveYouUp"
    sd = Scihub_Downloader(doi)
    if sd.downloadable:
        sd.save_pdf("thesis/test")
    else:
        print(f"{doi}\tis fail to download.")
    
    # 多次爬虫导致封ip测试
    for i in range(1000):
        print(f"\r{i+1}/1000", end='')
        doi = "10.1109/tit.2011.2182033"
        sd = Scihub_Downloader(doi)
        if not sd.downloadable:
            print(f"\n第 {i+1} 次时ip被封")
            break
    pass


if __name__ == "__main__":
    test()
    print("finished.")
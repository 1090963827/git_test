import requests
import json

#你的github用户名
USERNAME = "1090963827"

#1.定义 API URL
url = f"https://api.github.com/users/{USERNAME}/repos"

#2.发送GET请求
print(f"正在请求:{url}")
response = requests.get(url)

if response.status_code == 200:
    repos = response.json() #将json字符串转换为python列表
    print(f"用户{USERNAME} 共有 {len(repos)} 个仓库。")
    print("-" * 40)

    for repo in repos:
        name = repo['name']
        description = repo['description'] or "(无描述)" #处理空描述
        stars = repo['stargazers_count']
        language = repo['language'] or "未标记"

        print(f"仓库:{name}")
        print(f"  描述:{description}")
        print(f"  星标:{stars} | 语言: {language}")
        print("-"*30)

    else:
        print(f"请求失败，状态码：{response.status_code}")


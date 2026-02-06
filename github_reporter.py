import requests
import json
import time

USERNAME = "1090963827"
url = f"https://api.github.com/users/{USERNAME}/repos"

# 设置请求头，添加User-Agent是访问许多API（包括GitHub）的良好实践
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Python-Requests-Learner/1.0'
}

try:
    print(f"正在请求: {url}")
    # 将headers参数加入请求
    response = requests.get(url, headers=headers, timeout=10)  # 设置10秒超时

    # 如果状态码不是200，主动抛出异常
    response.raise_for_status()

    repos = response.json()
    print(f"请求成功！用户 {USERNAME} 共有 {len(repos)} 个仓库。\n")

    # ... (前面的导入和url定义不变)

    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json()  # 将JSON字符串转换为Python列表
        print(f"用户 {USERNAME} 共有 {len(repos)} 个仓库。")
        print("=" * 40)

        for repo in repos:
            name = repo['name']
            description = repo['description'] or "（无描述）"  # 处理空描述
            stars = repo['stargazers_count']
            language = repo['language'] or "未标记"
            print(f"仓库: {name}")
            print(f"  描述: {description}")
            print(f"  星标: {stars} | 语言: {language}")
            print("-" * 30)
    else:
        print(f"请求失败，状态码: {response.status_code}")

    # ... (成功获取repos后)
    # 生成报告内容
    report_content = f"""# GitHub仓库报告
    > 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}
    > 用户：{USERNAME}
    > 仓库总数：{len(repos)}

    ## 仓库列表
    """
    for repo in repos:
        report_content += f"""
    ### [{repo['name']}]({repo['html_url']})
    - **描述**: {repo['description'] or 'N/A'}
    - **星标**: ⭐ {repo['stargazers_count']}
    - **语言**: {repo['language'] or 'N/A'}
    - **更新时间**: {repo['updated_at'][:10]}
    ---
    """

    # 将报告写入文件
    report_filename = f"github_report_{USERNAME}.md"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"报告已生成：{report_filename}")

except requests.exceptions.Timeout:
    print("错误：请求超时，请检查网络。")
except requests.exceptions.ConnectionError:
    print("错误：网络连接失败。")
except requests.exceptions.HTTPError as e:
    print(f"HTTP错误: {e}")
    # 如果是速率限制，可以给出友好提示
    if response.status_code == 403 and 'rate limit' in response.text.lower():
        print("提示：GitHub API速率限制可能已达到，请稍后再试。")
except Exception as e:
    print(f"发生未知错误: {e}")
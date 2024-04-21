from tdf_tool.tools.env import EnvTool
from tdf_tool.tools.print import Print
import requests


class TLOwner:

    def __init__(self):
        self.tl_package_name = "tdf-tool"
        self.tl_current_version = EnvTool.tdfToolVersion()

    def check_for_package_updates(self):
        Print.title("tl 版本检测中...")
        try:
            # 获取GitHub上包的最新版本
            response = requests.get(f'https://pypi.org/pypi/{self.tl_package_name}/json')
            if response.status_code == 200:
                latest_version = response.json()['info']['version']
                result = self.compare_version(latest_version, self.tl_current_version)
                if result == 1:
                    Print.str("当前 tl 版本：{0}".format(self.tl_current_version))
                    Print.yellow("发现新版本：{0}，请使用 tl upgrade 命令升级，以使用最新功能".format(latest_version))
                elif result == -1:
                    Print.warning("当前版本{0}高于远端最新版本{1}".format(latest_version, self.tl_current_version))
                else:
                    Print.str("已是最新版本")
            else:
                Print.warning("远端版本获取失败：status_code：{0}，content：{1}".format(response.content))
        except Exception:
            Print.warning("版本获取异常")


    # 比较两个版本号的大小
    def compare_version(self, version1: str, version2: str):
        v1 = list(map(int, version1.split('.')))
        v2 = list(map(int, version2.split('.')))

        for i in range(max(len(v1), len(v2))):
            num1 = v1[i] if i < len(v1) else 0
            num2 = v2[i] if i < len(v2) else 0

            if num1 > num2:
                return 1
            elif num1 < num2:
                return -1

        return 0

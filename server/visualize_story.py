import os
import subprocess
import sys

def visualize_story():
    try:
        # 使用 'rasa visualize' 命令生成故事的 HTML 可视化文件
        subprocess.run(["rasa", "visualize", "--domain", "domain"], check=True)

        current_dir = os.path.dirname(os.path.abspath(__file__))

        graph_html_path = os.path.join(current_dir, '..', 'graph.html')
        # 读取生成的 HTML 文件内容
        with open(graph_html_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        return html_content
    except Exception as e:
        print("Error: ", e)
        return None


import sys,os

#__file__获取执行文件相对路径，整行为取上一级目录
BASE_DIR1=os.path.dirname(os.path.abspath(__file__))

# 添加路径
sys.path.append(BASE_DIR1)
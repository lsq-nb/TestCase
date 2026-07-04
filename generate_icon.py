"""
为 TestCraft 生成应用图标

流程：
1. 用 agnes-image 生成 PNG 图标
2. 用 Pillow 将 PNG 转为 ICO 格式
"""

import subprocess
import sys
import os

def generate_icon():
    """生成 TestCraft 图标"""
    icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(icon_dir, exist_ok=True)

    icon_png = os.path.join(icon_dir, "testcraft.png")
    icon_ico = os.path.join(icon_dir, "testcraft.ico")

    # 检查是否已存在
    if os.path.exists(icon_ico):
        print(f"图标已存在: {icon_ico}")
        return icon_ico

    print(f"请先手动将生成的图标保存到: {icon_png}")
    print("然后运行: python generate_icon.py (会自动转为 .ico 格式)")

    return icon_png


def convert_to_ico(png_path, ico_path):
    """使用 Pillow 将 PNG 转为 ICO"""
    try:
        from PIL import Image
        # 创建不同尺寸的图标（ICO 支持多分辨率）
        sizes = [16, 32, 48, 64, 128, 256]
        images = []

        for size in sizes:
            img = Image.open(png_path).convert("RGBA")
            img = img.resize((size, size), Image.Resampling.LANCZOS)
            images.append(img)

        images[0].save(ico_path, format="ICO", sizes=[(i.size[0], i.size[1]) for i in images])
        print(f"图标已生成: {ico_path}")
        return True
    except ImportError:
        print("Pillow 未安装，尝试用命令行工具转换...")
        return False


if __name__ == "__main__":
    icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(icon_dir, exist_ok=True)

    png_path = os.path.join(icon_dir, "testcraft.png")
    ico_path = os.path.join(icon_dir, "testcraft.ico")

    if os.path.exists(ico_path):
        print(f"图标已存在: {ico_path}")
        sys.exit(0)

    if os.path.exists(png_path):
        success = convert_to_ico(png_path, ico_path)
        if not success:
            print("请安装 Pillow: pip install Pillow")
            print("然后重新运行此脚本")
            sys.exit(1)
    else:
        print(f"请先在 assets/ 目录下放置 testcraft.png")
        print("可以手动创建或使用图片生成工具")
        sys.exit(1)

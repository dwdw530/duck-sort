"""
生成小鸭子图标 - 老王出品
用 pygame 绘制鸭子，然后用 PIL 转成 ico 格式
"""
import pygame
import io

# 初始化
pygame.init()

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 50)
DARK_YELLOW = (240, 200, 30)
ORANGE = (255, 140, 0)
DARK_ORANGE = (230, 120, 0)
TRANSPARENT = (255, 0, 255)  # 透明色


def draw_duck_icon(size=256):
    """绘制一只可爱的小鸭子图标"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # 透明背景

    scale = size / 100  # 基准缩放
    cx, cy = size // 2, size // 2 + int(5 * scale)  # 中心点

    # 身体 - 圆润的椭圆
    body_width = int(50 * scale)
    body_height = int(38 * scale)
    body_rect = pygame.Rect(
        cx - body_width // 2,
        cy - body_height // 2 + int(8 * scale),
        body_width,
        body_height
    )
    pygame.draw.ellipse(surface, YELLOW, body_rect)
    pygame.draw.ellipse(surface, DARK_YELLOW, body_rect, max(2, int(2 * scale)))

    # 翅膀
    wing_width = int(20 * scale)
    wing_height = int(16 * scale)
    wing_rect = pygame.Rect(
        cx - wing_width // 2 + int(3 * scale),
        cy - wing_height // 2 + int(10 * scale),
        wing_width,
        wing_height
    )
    pygame.draw.ellipse(surface, DARK_YELLOW, wing_rect)
    pygame.draw.ellipse(surface, (200, 170, 30), wing_rect, max(1, int(1 * scale)))

    # 尾巴
    tail_x = cx - int(26 * scale)
    tail_y = cy + int(5 * scale)
    tail_points = [
        (tail_x, tail_y),
        (tail_x - int(10 * scale), tail_y - int(12 * scale)),
        (tail_x - int(6 * scale), tail_y - int(6 * scale)),
        (tail_x - int(12 * scale), tail_y - int(8 * scale)),
        (tail_x - int(4 * scale), tail_y + int(2 * scale))
    ]
    pygame.draw.polygon(surface, YELLOW, tail_points)
    pygame.draw.polygon(surface, DARK_YELLOW, tail_points, max(2, int(2 * scale)))

    # 头 - 圆形
    head_radius = int(18 * scale)
    head_x = cx + int(20 * scale)
    head_y = cy - int(8 * scale)
    pygame.draw.circle(surface, YELLOW, (head_x, head_y), head_radius)
    pygame.draw.circle(surface, DARK_YELLOW, (head_x, head_y), head_radius, max(2, int(2 * scale)))

    # 扁嘴巴 - 上片
    beak_x = head_x + head_radius - int(2 * scale)
    beak_y = head_y + int(3 * scale)
    beak_width = int(18 * scale)
    beak_height = int(10 * scale)

    # 上嘴
    upper_rect = pygame.Rect(beak_x, beak_y - beak_height // 2, beak_width, int(beak_height * 0.45))
    pygame.draw.ellipse(surface, ORANGE, upper_rect)
    pygame.draw.ellipse(surface, DARK_ORANGE, upper_rect, max(1, int(1 * scale)))

    # 下嘴
    lower_rect = pygame.Rect(beak_x, beak_y, beak_width, int(beak_height * 0.55))
    pygame.draw.ellipse(surface, ORANGE, lower_rect)
    pygame.draw.ellipse(surface, DARK_ORANGE, lower_rect, max(1, int(1 * scale)))

    # 嘴缝
    pygame.draw.line(surface, DARK_ORANGE, (beak_x, beak_y + 1), (beak_x + beak_width - 2, beak_y + 1), max(1, int(1.5 * scale)))

    # 眼睛
    eye_x = head_x + int(5 * scale)
    eye_y = head_y - int(3 * scale)
    # 眼白
    pygame.draw.circle(surface, WHITE, (eye_x, eye_y), int(5 * scale))
    # 眼珠
    pygame.draw.circle(surface, BLACK, (eye_x + int(1 * scale), eye_y), int(3 * scale))
    # 高光
    pygame.draw.circle(surface, WHITE, (eye_x + int(2 * scale), eye_y - int(1 * scale)), int(1.5 * scale))

    # 腮红
    blush_surface = pygame.Surface((int(8 * scale), int(5 * scale)), pygame.SRCALPHA)
    pygame.draw.ellipse(blush_surface, (255, 180, 180, 120), (0, 0, int(8 * scale), int(5 * scale)))
    surface.blit(blush_surface, (head_x - int(6 * scale), head_y + int(3 * scale)))

    return surface


def save_ico(output_path="duck_icon.ico"):
    """保存为 ICO 格式（多尺寸）"""
    try:
        from PIL import Image
    except ImportError:
        print("需要安装 Pillow: pip install pillow")
        return False

    # 生成多个尺寸
    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        # 用 pygame 绘制
        surface = draw_duck_icon(size)

        # 转换为 PIL Image
        data = pygame.image.tostring(surface, "RGBA")
        img = Image.frombytes("RGBA", (size, size), data)
        images.append(img)

    # 保存为 ICO（包含所有尺寸）
    images[-1].save(
        output_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[:-1]
    )

    print(f"图标已保存: {output_path}")
    return True


def save_png(output_path="duck_icon.png", size=256):
    """保存为 PNG 格式（预览用）"""
    try:
        from PIL import Image
    except ImportError:
        print("需要安装 Pillow: pip install pillow")
        return False

    surface = draw_duck_icon(size)
    data = pygame.image.tostring(surface, "RGBA")
    img = Image.frombytes("RGBA", (size, size), data)
    img.save(output_path, format="PNG")
    print(f"PNG 预览已保存: {output_path}")
    return True


if __name__ == "__main__":
    # 生成图标
    save_png("duck_icon.png", 256)  # PNG 预览
    save_ico("duck_icon.ico")       # ICO 图标

    pygame.quit()
    print("\n打包命令:")
    print('pyinstaller --onefile --windowed --icon=duck_icon.ico --name "鸭子排序" duck_sort.py')

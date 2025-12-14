"""
鸭子冒泡排序动画 - 老王出品 v2
用PyGame绘制12只小鸭子和1只大白鹅，展示冒泡排序过程
修复：嘴巴改成扁扁的椭圆形，大白鹅重新设计
"""
import pygame
import random
import math

# 初始化PyGame
pygame.init()

# 窗口设置 - 比默认值高，画面清晰
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("鸭子冒泡排序 - 老王出品")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 50)         # 小鸭子身体
DARK_YELLOW = (240, 200, 30)    # 小鸭子翅膀
ORANGE = (255, 140, 0)          # 嘴巴
DARK_ORANGE = (230, 120, 0)     # 嘴巴深色
GOOSE_WHITE = (255, 255, 255)   # 大白鹅身体
GOOSE_GRAY = (240, 240, 240)    # 大白鹅翅膀
RED_ORANGE = (255, 80, 50)      # 鹅的肉冠
SKY_BLUE = (135, 206, 235)      # 天空背景
GRASS_GREEN = (124, 185, 85)    # 草地
WATER_BLUE = (100, 149, 237)    # 水面

# 动画状态
STATE_WAITING = 0
STATE_COMPARING = 1
STATE_CHECKING = 2
STATE_SWAPPING = 3
STATE_MOVING = 4
STATE_DONE = 5

# 帧率
FPS = 60
clock = pygame.time.Clock()


def draw_duck_beak(surface, x, y, width, height, facing_right=True):
    """
    绘制扁扁的鸭嘴 - 椭圆形，分上下两片
    """
    flip = 1 if facing_right else -1

    # 上嘴 - 稍微小一点的椭圆
    upper_rect = pygame.Rect(
        x - (width // 2 if not facing_right else 0),
        y - height // 2,
        width,
        int(height * 0.45)
    )
    pygame.draw.ellipse(surface, ORANGE, upper_rect)
    pygame.draw.ellipse(surface, DARK_ORANGE, upper_rect, 1)

    # 下嘴 - 稍微大一点
    lower_rect = pygame.Rect(
        x - (width // 2 if not facing_right else 0),
        y,
        width,
        int(height * 0.55)
    )
    pygame.draw.ellipse(surface, ORANGE, lower_rect)
    pygame.draw.ellipse(surface, DARK_ORANGE, lower_rect, 1)

    # 嘴缝 - 一条线
    line_y = y + 1
    line_start = (x - (width // 2 if not facing_right else 0), line_y)
    line_end = (x + (width if facing_right else width // 2), line_y)
    pygame.draw.line(surface, DARK_ORANGE, line_start, line_end, 2)

    # 鼻孔 - 两个小点
    nostril_x = x + flip * int(width * 0.3)
    pygame.draw.circle(surface, DARK_ORANGE, (int(nostril_x), int(y - height * 0.15)), 2)


def draw_duck(surface, x, y, scale, facing_right=True):
    """
    绘制一只可爱的小鸭子 - 扁嘴版
    """
    flip = 1 if facing_right else -1

    # 身体 - 圆润的椭圆
    body_width = int(55 * scale)
    body_height = int(40 * scale)
    body_x = x
    body_y = y + int(10 * scale)

    body_rect = pygame.Rect(
        body_x - body_width // 2,
        body_y - body_height // 2,
        body_width,
        body_height
    )
    pygame.draw.ellipse(surface, YELLOW, body_rect)
    pygame.draw.ellipse(surface, (200, 170, 30), body_rect, 2)

    # 翅膀 - 小椭圆
    wing_width = int(22 * scale)
    wing_height = int(18 * scale)
    wing_x = x + flip * int(3 * scale)
    wing_y = y + int(12 * scale)
    wing_rect = pygame.Rect(
        wing_x - wing_width // 2,
        wing_y - wing_height // 2,
        wing_width,
        wing_height
    )
    pygame.draw.ellipse(surface, DARK_YELLOW, wing_rect)
    pygame.draw.ellipse(surface, (200, 170, 30), wing_rect, 1)

    # 尾巴 - 翘起来的小羽毛
    tail_x = x - flip * int(28 * scale)
    tail_y = y + int(5 * scale)
    tail_points = [
        (tail_x, tail_y),
        (tail_x - flip * int(12 * scale), tail_y - int(15 * scale)),
        (tail_x - flip * int(8 * scale), tail_y - int(8 * scale)),
        (tail_x - flip * int(15 * scale), tail_y - int(10 * scale)),
        (tail_x - flip * int(5 * scale), tail_y + int(3 * scale))
    ]
    pygame.draw.polygon(surface, YELLOW, tail_points)
    pygame.draw.polygon(surface, (200, 170, 30), tail_points, 2)

    # 头 - 圆形
    head_radius = int(18 * scale)
    head_x = x + flip * int(25 * scale)
    head_y = y - int(8 * scale)
    pygame.draw.circle(surface, YELLOW, (int(head_x), int(head_y)), head_radius)
    pygame.draw.circle(surface, (200, 170, 30), (int(head_x), int(head_y)), head_radius, 2)

    # 扁嘴巴
    beak_width = int(20 * scale)
    beak_height = int(10 * scale)
    beak_x = head_x + flip * (head_radius - int(2 * scale))
    beak_y = head_y + int(3 * scale)
    draw_duck_beak(surface, int(beak_x), int(beak_y), beak_width, beak_height, facing_right)

    # 眼睛 - 大眼睛更可爱
    eye_x = head_x + flip * int(5 * scale)
    eye_y = head_y - int(3 * scale)
    # 眼白
    pygame.draw.circle(surface, WHITE, (int(eye_x), int(eye_y)), int(5 * scale))
    # 眼珠
    pygame.draw.circle(surface, BLACK, (int(eye_x) + flip * int(1 * scale), int(eye_y)), int(3 * scale))
    # 高光
    pygame.draw.circle(surface, WHITE, (int(eye_x) + flip * int(2 * scale), int(eye_y) - int(1 * scale)), int(1.5 * scale))

    # 腮红 - 更可爱
    blush_x = head_x - flip * int(2 * scale)
    blush_y = head_y + int(5 * scale)
    blush_surface = pygame.Surface((int(8 * scale), int(5 * scale)), pygame.SRCALPHA)
    pygame.draw.ellipse(blush_surface, (255, 180, 180, 100), (0, 0, int(8 * scale), int(5 * scale)))
    surface.blit(blush_surface, (int(blush_x) - int(4 * scale), int(blush_y) - int(2 * scale)))


def draw_goose_beak(surface, x, y, width, height, facing_right=True):
    """
    绘制大白鹅的扁嘴 - 更大更宽
    """
    flip = 1 if facing_right else -1

    # 嘴基部的肉瘤
    knob_x = x - flip * int(width * 0.1)
    knob_y = y - height
    pygame.draw.circle(surface, RED_ORANGE, (int(knob_x), int(knob_y)), int(height * 0.6))
    pygame.draw.circle(surface, (200, 60, 40), (int(knob_x), int(knob_y)), int(height * 0.6), 2)

    # 上嘴
    upper_rect = pygame.Rect(
        x - (width // 2 if not facing_right else 0),
        y - height // 2,
        width,
        int(height * 0.45)
    )
    pygame.draw.ellipse(surface, ORANGE, upper_rect)
    pygame.draw.ellipse(surface, DARK_ORANGE, upper_rect, 2)

    # 下嘴
    lower_rect = pygame.Rect(
        x - (width // 2 if not facing_right else 0),
        y + int(height * 0.05),
        int(width * 0.9),
        int(height * 0.5)
    )
    pygame.draw.ellipse(surface, ORANGE, lower_rect)
    pygame.draw.ellipse(surface, DARK_ORANGE, lower_rect, 2)

    # 嘴缝
    line_y = y + 2
    line_start = (x - (width // 2 if not facing_right else 0) + 3, line_y)
    line_end = (x + (int(width * 0.85) if facing_right else width // 2 - 3), line_y)
    pygame.draw.line(surface, DARK_ORANGE, line_start, line_end, 2)

    # 鼻孔
    nostril_x = x + flip * int(width * 0.25)
    pygame.draw.circle(surface, DARK_ORANGE, (int(nostril_x), int(y - height * 0.12)), 3)


def draw_goose(surface, x, y, facing_right=True):
    """
    绘制大白鹅 - 优雅的长脖子，扁嘴
    """
    scale = 1.5
    flip = 1 if facing_right else -1

    # 身体 - 大椭圆，稍微倾斜
    body_width = int(90 * scale)
    body_height = int(55 * scale)
    body_x = x
    body_y = y + int(25 * scale)

    body_rect = pygame.Rect(
        body_x - body_width // 2,
        body_y - body_height // 2,
        body_width,
        body_height
    )
    pygame.draw.ellipse(surface, GOOSE_WHITE, body_rect)
    pygame.draw.ellipse(surface, (180, 180, 180), body_rect, 2)

    # 翅膀 - 优雅的弧形
    wing_width = int(50 * scale)
    wing_height = int(35 * scale)
    wing_x = x + flip * int(5 * scale)
    wing_y = y + int(25 * scale)
    wing_rect = pygame.Rect(
        wing_x - wing_width // 2,
        wing_y - wing_height // 2,
        wing_width,
        wing_height
    )
    pygame.draw.ellipse(surface, GOOSE_GRAY, wing_rect)
    pygame.draw.ellipse(surface, (180, 180, 180), wing_rect, 1)

    # 翅膀纹理 - 几条弧线
    for i in range(3):
        arc_rect = pygame.Rect(
            wing_x - wing_width // 2 + i * 8,
            wing_y - wing_height // 2 + i * 5,
            wing_width - i * 15,
            wing_height - i * 8
        )
        pygame.draw.arc(surface, (200, 200, 200), arc_rect, -0.5, 1.5, 1)

    # 尾巴 - 翘起的羽毛
    tail_x = x - flip * int(48 * scale)
    tail_y = y + int(18 * scale)
    tail_points = [
        (tail_x, tail_y),
        (tail_x - flip * int(18 * scale), tail_y - int(20 * scale)),
        (tail_x - flip * int(12 * scale), tail_y - int(12 * scale)),
        (tail_x - flip * int(22 * scale), tail_y - int(15 * scale)),
        (tail_x - flip * int(8 * scale), tail_y - int(5 * scale)),
        (tail_x - flip * int(15 * scale), tail_y + int(5 * scale)),
    ]
    pygame.draw.polygon(surface, GOOSE_WHITE, tail_points)
    pygame.draw.polygon(surface, (180, 180, 180), tail_points, 2)

    # 长脖子 - S形曲线，用多个圆形绘制
    neck_start_x = x + flip * int(35 * scale)
    neck_start_y = y + int(5 * scale)

    neck_thickness = int(14 * scale)
    neck_points = []

    # 生成S形脖子的点
    for i in range(20):
        t = i / 19
        # S形曲线
        curve_x = neck_start_x + flip * int(25 * scale) * math.sin(t * math.pi * 0.6)
        curve_y = neck_start_y - int(70 * scale) * t
        neck_points.append((curve_x, curve_y))

    # 绘制脖子（用多个圆形）
    for i, (nx, ny) in enumerate(neck_points):
        thickness = neck_thickness - i * 0.3  # 脖子往上变细
        pygame.draw.circle(surface, GOOSE_WHITE, (int(nx), int(ny)), int(max(thickness, 8)))

    # 脖子轮廓
    if len(neck_points) > 1:
        pygame.draw.lines(surface, (180, 180, 180), False, [(int(p[0]), int(p[1])) for p in neck_points], 2)

    # 头 - 椭圆形
    head_x = neck_points[-1][0] + flip * int(12 * scale)
    head_y = neck_points[-1][1] - int(5 * scale)
    head_width = int(32 * scale)
    head_height = int(24 * scale)

    head_rect = pygame.Rect(
        head_x - head_width // 2,
        head_y - head_height // 2,
        head_width,
        head_height
    )
    pygame.draw.ellipse(surface, GOOSE_WHITE, head_rect)
    pygame.draw.ellipse(surface, (180, 180, 180), head_rect, 2)

    # 扁嘴巴
    beak_width = int(30 * scale)
    beak_height = int(14 * scale)
    beak_x = head_x + flip * (head_width // 2 - int(3 * scale))
    beak_y = head_y + int(4 * scale)
    draw_goose_beak(surface, int(beak_x), int(beak_y), beak_width, beak_height, facing_right)

    # 眼睛
    eye_x = head_x + flip * int(5 * scale)
    eye_y = head_y - int(2 * scale)
    # 眼白
    pygame.draw.circle(surface, WHITE, (int(eye_x), int(eye_y)), int(6 * scale))
    pygame.draw.circle(surface, (180, 180, 180), (int(eye_x), int(eye_y)), int(6 * scale), 1)
    # 眼珠
    pygame.draw.circle(surface, BLACK, (int(eye_x) + flip * int(1 * scale), int(eye_y)), int(4 * scale))
    # 高光
    pygame.draw.circle(surface, WHITE, (int(eye_x) + flip * int(2 * scale), int(eye_y) - int(2 * scale)), int(2 * scale))

    # 脚 - 橙色蹼
    foot_y = body_y + body_height // 2 - int(5 * scale)
    for foot_offset in [-15, 15]:
        foot_x = x + foot_offset * scale
        # 腿
        pygame.draw.line(surface, ORANGE, (int(foot_x), int(foot_y)), (int(foot_x), int(foot_y + 20 * scale)), int(4 * scale))
        # 蹼
        webbed_points = [
            (int(foot_x), int(foot_y + 20 * scale)),
            (int(foot_x - 12 * scale), int(foot_y + 30 * scale)),
            (int(foot_x), int(foot_y + 25 * scale)),
            (int(foot_x + 12 * scale), int(foot_y + 30 * scale)),
        ]
        pygame.draw.polygon(surface, ORANGE, webbed_points)
        pygame.draw.polygon(surface, DARK_ORANGE, webbed_points, 2)


def draw_background(surface):
    """绘制背景"""
    # 渐变天空
    for y in range(SCREEN_HEIGHT - 200):
        ratio = y / (SCREEN_HEIGHT - 200)
        r = int(135 + (200 - 135) * ratio * 0.3)
        g = int(206 + (230 - 206) * ratio * 0.3)
        b = int(235 + (255 - 235) * ratio * 0.3)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # 太阳
    pygame.draw.circle(surface, (255, 250, 150), (100, 80), 45)
    pygame.draw.circle(surface, (255, 255, 200), (100, 80), 35)

    # 云朵
    for cx, cy in [(300, 100), (600, 70), (900, 120), (1100, 80)]:
        for dx, dy, r in [(-30, 0, 25), (0, -10, 30), (30, 0, 25), (0, 10, 20)]:
            pygame.draw.circle(surface, WHITE, (cx + dx, cy + dy), r)

    # 草地
    pygame.draw.rect(surface, GRASS_GREEN, (0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 100))
    # 草地纹理
    for i in range(50):
        gx = random.randint(0, SCREEN_WIDTH)
        gy = SCREEN_HEIGHT - 200 + random.randint(5, 90)
        pygame.draw.line(surface, (100, 160, 70), (gx, gy), (gx + random.randint(-3, 3), gy - random.randint(5, 15)), 2)

    # 水面
    pygame.draw.rect(surface, WATER_BLUE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    # 水波纹
    for i in range(12):
        wave_y = SCREEN_HEIGHT - 80 + (i % 3) * 25
        wave_x = i * 110 - 20
        pygame.draw.arc(surface, (130, 170, 255), (wave_x, wave_y, 80, 15), 0, math.pi, 2)


def lerp(a, b, t):
    """线性插值"""
    return a + (b - a) * t


class Duck:
    """小鸭子类"""
    def __init__(self, size_index, x, y):
        self.size_index = size_index  # 0-11，决定大小
        self.scale = 0.5 + size_index * 0.07
        self.x = x
        self.y = y
        self.target_x = x
        self.facing_right = True

    def update(self):
        """更新位置"""
        if abs(self.x - self.target_x) > 1:
            direction = 1 if self.target_x > self.x else -1
            self.facing_right = direction > 0
            self.x = lerp(self.x, self.target_x, 0.12)
            return True
        else:
            self.x = self.target_x
            return False

    def draw(self, surface):
        """绘制鸭子"""
        draw_duck(surface, int(self.x), int(self.y), self.scale, self.facing_right)


class Goose:
    """大白鹅类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.facing_right = True

    def update(self):
        """更新位置"""
        if abs(self.x - self.target_x) > 2:
            self.facing_right = self.target_x > self.x
            self.x = lerp(self.x, self.target_x, 0.1)
            return True
        else:
            self.x = self.target_x
            return False

    def draw(self, surface):
        """绘制大白鹅"""
        draw_goose(surface, int(self.x), int(self.y), self.facing_right)


class BubbleSortAnimation:
    """冒泡排序动画控制器"""
    def __init__(self):
        # 固定随机种子生成背景草地
        random.seed(42)
        self.grass_positions = [(random.randint(0, SCREEN_WIDTH),
                                 SCREEN_HEIGHT - 200 + random.randint(5, 90),
                                 random.randint(-3, 3),
                                 random.randint(5, 15)) for _ in range(50)]
        random.seed()  # 恢复随机
        self.reset()

    def reset(self):
        """重置/初始化"""
        # 鸭子参数
        self.duck_spacing = 85
        self.start_x = 120
        self.duck_y = SCREEN_HEIGHT - 150

        # 创建12只不同大小的鸭子，随机打乱
        sizes = list(range(12))
        random.shuffle(sizes)

        self.ducks = []
        for i, size in enumerate(sizes):
            x = self.start_x + i * self.duck_spacing
            duck = Duck(size, x, self.duck_y)
            self.ducks.append(duck)

        # 大白鹅
        self.goose = Goose(self.start_x, self.duck_y - 130)

        # 排序状态
        self.state = STATE_WAITING
        self.current_pass = 0
        self.current_index = 0
        self.compare_count = 0
        self.swap_count = 0
        self.wait_timer = 0
        self.start_delay = 90

    def get_duck_x(self, index):
        """获取指定位置的x坐标"""
        return self.start_x + index * self.duck_spacing

    def update(self):
        """更新动画状态 - 标准冒泡排序"""
        if self.state == STATE_WAITING:
            self.wait_timer += 1
            if self.wait_timer >= self.start_delay:
                self.state = STATE_COMPARING
                # 大白鹅移动到第一对鸭子中间
                self.goose.target_x = (self.get_duck_x(0) + self.get_duck_x(1)) / 2

        elif self.state == STATE_COMPARING:
            if not self.goose.update():
                self.state = STATE_CHECKING
                self.wait_timer = 0

        elif self.state == STATE_CHECKING:
            self.wait_timer += 1
            if self.wait_timer >= 25:
                self.compare_count += 1
                i = self.current_index

                # 冒泡排序：如果左边比右边大，就交换（从小到大排序）
                if self.ducks[i].size_index > self.ducks[i + 1].size_index:
                    self.state = STATE_SWAPPING
                    # 交换目标位置
                    self.ducks[i].target_x = self.get_duck_x(i + 1)
                    self.ducks[i + 1].target_x = self.get_duck_x(i)
                    self.swap_count += 1
                else:
                    self.state = STATE_MOVING

        elif self.state == STATE_SWAPPING:
            moving = False
            for duck in self.ducks:
                if duck.update():
                    moving = True

            if not moving:
                # 交换数组中的位置
                i = self.current_index
                self.ducks[i], self.ducks[i + 1] = self.ducks[i + 1], self.ducks[i]
                self.state = STATE_MOVING

        elif self.state == STATE_MOVING:
            self.current_index += 1
            n = len(self.ducks)

            # 当前轮是否结束
            if self.current_index >= n - 1 - self.current_pass:
                self.current_pass += 1
                self.current_index = 0

                # 排序完成检查
                if self.current_pass >= n - 1:
                    self.state = STATE_DONE
                    self.goose.target_x = SCREEN_WIDTH // 2
                    return

            # 移动到下一对
            next_x = (self.get_duck_x(self.current_index) + self.get_duck_x(self.current_index + 1)) / 2
            self.goose.target_x = next_x
            self.state = STATE_COMPARING

        elif self.state == STATE_DONE:
            self.goose.update()

    def draw_background_cached(self, surface):
        """绘制背景（草地位置固定）"""
        # 渐变天空
        for y in range(0, SCREEN_HEIGHT - 200, 4):
            ratio = y / (SCREEN_HEIGHT - 200)
            r = int(135 + 20 * ratio)
            g = int(206 + 8 * ratio)
            b = int(235 + 7 * ratio)
            pygame.draw.rect(surface, (r, g, b), (0, y, SCREEN_WIDTH, 4))

        # 太阳
        pygame.draw.circle(surface, (255, 250, 150), (100, 80), 45)
        pygame.draw.circle(surface, (255, 255, 200), (100, 80), 35)

        # 云朵
        for cx, cy in [(300, 100), (600, 70), (900, 120), (1100, 80)]:
            for dx, dy, r in [(-30, 0, 25), (0, -10, 30), (30, 0, 25), (0, 10, 20)]:
                pygame.draw.circle(surface, WHITE, (cx + dx, cy + dy), r)

        # 草地
        pygame.draw.rect(surface, GRASS_GREEN, (0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 100))
        for gx, gy, gdx, gh in self.grass_positions:
            pygame.draw.line(surface, (100, 160, 70), (gx, gy), (gx + gdx, gy - gh), 2)

        # 水面
        pygame.draw.rect(surface, WATER_BLUE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        for i in range(12):
            wave_y = SCREEN_HEIGHT - 80 + (i % 3) * 25
            wave_x = i * 110 - 20
            pygame.draw.arc(surface, (130, 170, 255), (wave_x, wave_y, 80, 15), 0, math.pi, 2)

    def draw(self, surface):
        """绘制所有元素"""
        self.draw_background_cached(surface)

        # 绘制鸭子
        for duck in self.ducks:
            duck.draw(surface)

        # 绘制大白鹅
        self.goose.draw(surface)

        # 高亮当前比较的鸭子
        if self.state in [STATE_COMPARING, STATE_CHECKING, STATE_SWAPPING]:
            i = self.current_index
            for idx in [i, i + 1]:
                duck = self.ducks[idx] if self.state != STATE_SWAPPING else None
                if duck:
                    x = duck.x
                else:
                    x = self.get_duck_x(idx)
                # 用虚线框标记
                rect = pygame.Rect(int(x) - 40, self.duck_y - 50, 80, 90)
                pygame.draw.rect(surface, (255, 80, 80), rect, 3)

        # UI信息
        try:
            font = pygame.font.SysFont('simhei', 26)
            small_font = pygame.font.SysFont('simhei', 18)
        except:
            font = pygame.font.Font(None, 30)
            small_font = pygame.font.Font(None, 22)

        # 标题
        title = font.render("鸭子冒泡排序 - 大白鹅指挥官", True, BLACK)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 15))

        # 统计
        stats = font.render(f"轮次: {self.current_pass + 1}/11  比较: {self.compare_count}  交换: {self.swap_count}", True, BLACK)
        surface.blit(stats, (20, 55))

        # 状态
        state_texts = {
            STATE_WAITING: "准备开始...",
            STATE_COMPARING: "大白鹅移动中...",
            STATE_CHECKING: f"比较第 {self.current_index + 1} 和第 {self.current_index + 2} 只鸭子",
            STATE_SWAPPING: "交换位置中...",
            STATE_DONE: "排序完成! 按 R 重新开始"
        }
        state_text = state_texts.get(self.state, "")
        state_surface = font.render(state_text, True, (50, 50, 150))
        surface.blit(state_surface, (20, 90))

        # 鸭子大小标签
        for duck in self.ducks:
            size_label = small_font.render(str(duck.size_index + 1), True, BLACK)
            surface.blit(size_label, (int(duck.x) - 6, self.duck_y + 45))


def main():
    """主函数"""
    animation = BubbleSortAnimation()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    animation.reset()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        animation.update()
        animation.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

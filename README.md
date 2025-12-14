# 鸭子冒泡排序动画 - Windows 运行指南

## 方法一：打包成 EXE（推荐）

### 1. 安装打包工具

```bash
pip install pyinstaller
```

### 2. 生成小鸭子图标（可选）

```bash
python create_icon.py
```

会生成 `duck_icon.ico` 图标文件。

### 3. 打包命令

在项目目录下执行：

```bash
pyinstaller --onefile --windowed --icon=duck_icon.ico --name "鸭子排序" duck_sort.py
```

参数说明：
- `--onefile`：打包成单个 exe 文件
- `--windowed`：运行时不显示命令行黑窗口
- `--icon`：指定 exe 图标
- `--name`：指定生成的 exe 名称

### 4. 找到 EXE

打包完成后，exe 文件在：

```
dist/鸭子排序.exe
```

双击即可运行！

---

## 方法二：创建快捷方式（不打包）

如果不想打包，可以创建一个 bat 脚本：

### 1. 新建 `运行鸭子排序.bat`

```bat
@echo off
cd /d %~dp0
python duck_sort.py
```

### 2. 双击 bat 文件运行

---

## 环境要求

- Python 3.8+
- PyGame 库

安装 PyGame：

```bash
pip install pygame
```

---

## 操作说明

- **自动运行**：程序启动后自动开始排序动画
- **R 键**：重新开始
- **ESC 键**：退出程序

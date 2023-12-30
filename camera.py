import cv2
from tkinter import *
from PIL import Image, ImageTk
import os
import time

# 摄像头捕获函数
def capture_video():
    global cap, photo, canvas_img_id, rotate_angle  # 使用全局变量
    ret, frame = cap.read()  # 从摄像头读取一帧
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色从BGR到RGB
        frame = cv2.resize(frame, (int(frame.shape[1]*scale), int(frame.shape[0]*scale)))  # 根据缩放比例调整图像大小

        # 进行旋转
        if rotate_angle == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotate_angle == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif rotate_angle == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        if canvas_img_id is None:
            canvas_img_id = canvas.create_image(0, 0, image=photo, anchor=NW)
        else:
            canvas.itemconfig(canvas_img_id, image=photo)
    window.after(20, capture_video)  # 每30ms捕获一次

# 放大函数
def zoom_in():
    global scale
    scale *= 1.1
    update_canvas_size()

# 缩小函数
def zoom_out():
    global scale
    scale *= 0.9
    update_canvas_size()

# 顺时针旋转90度
def rotate_cw():
    global rotate_angle
    rotate_angle += 90
    if rotate_angle >= 360:
        rotate_angle = 0

# 逆时针旋转90度
def rotate_ccw():
    global rotate_angle
    rotate_angle -= 90
    if rotate_angle < 0:
        rotate_angle = 270

# 更新画布大小
def update_canvas_size():
    global photo
    if photo:  # 确保photo已经被定义
        width, height = photo.width(), photo.height()
        canvas.config(width=width, height=height)

# 开始拖动函数
def start_drag(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

# 执行拖动函数
def do_drag(event):
    global last_x, last_y
    canvas.move(canvas_img_id, event.x - last_x, event.y - last_y)
    last_x, last_y = event.x, event.y

# 退出程序
def exit_program():
    cap.release()
    cv2.destroyAllWindows()
    window.quit()

# 创建关于对话框
def show_about_dialog():
    about_window = Toplevel(window)
    about_window.title("关于")
    about_window.geometry("300x150")

    # 显示应用程序名称、版本号和开发者信息
    app_name_label = Label(about_window, text="摄像头展台")
    app_name_label.pack(pady=10)

    version_label = Label(about_window, text="版本号：0.5")
    version_label.pack()

    developer_label = Label(about_window, text="开发者：pigeons2023")
    developer_label.pack()

# 拍照函数
def take_photo():
    global cap, photo, save_dir
    ret, frame = cap.read()  # 从摄像头读取一帧
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色从BGR到RGB
        frame = cv2.resize(frame, (int(frame.shape[1]*scale), int(frame.shape[0]*scale)))  # 根据缩放比例调整图像大小

        # 进行旋转
        if rotate_angle == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotate_angle == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif rotate_angle == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # 创建保存目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 保存图片
        file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".jpg"
        save_path = os.path.join(save_dir, file_name)
        cv2.imwrite(save_path, frame)

# 打开图片目录
def open_directory():
    os.startfile(save_dir)

# 主窗口
window = Tk()
window.title("摄像头展台")

# 全屏显示
window.attributes('-fullscreen', True)

# 初始化变量
scale = 1.0
last_x = 0
last_y = 0
canvas_img_id = None
rotate_angle = 0

# 创建按钮的框架
button_frame = Frame(window)
button_frame.pack(side=TOP, fill=X)

# 创建放大和缩小按钮
zoom_in_button = Button(button_frame, text="放大", command=zoom_in)
zoom_in_button.pack(side=LEFT)

zoom_out_button = Button(button_frame, text="缩小", command=zoom_out)
zoom_out_button.pack(side=LEFT)

# 创建旋转按钮
rotate_cw_button = Button(button_frame, text="顺时针旋转", command=rotate_cw)
rotate_cw_button.pack(side=LEFT)

rotate_ccw_button = Button(button_frame, text="逆时针旋转", command=rotate_ccw)
rotate_ccw_button.pack(side=LEFT)

# 创建拍照按钮
take_photo_button = Button(button_frame, text="拍照", command=take_photo)
take_photo_button.pack(side=LEFT)

# 创建打开目录按钮
open_dir_button = Button(button_frame, text="打开目录", command=open_directory)
open_dir_button.pack(side=LEFT)

# 创建关于按钮
about_button = Button(button_frame, text="关于", command=show_about_dialog)
about_button.pack(side=RIGHT)

# 创建退出按钮
exit_button = Button(button_frame, text="退出", command=exit_program)
exit_button.pack(side=RIGHT)

# 创建画布
canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=YES)

# 绑定事件
canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", do_drag)

# 打开摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("无法打开视频设备")

# 设置摄像头分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# 设置保存目录
save_dir = "photos"

# 开始视频捕获
capture_video()

# 运行主循环
window.mainloop()

# 释放资源
cap.release()
cv2.destroyAllWindows()

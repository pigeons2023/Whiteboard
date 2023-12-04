import cv2
from tkinter import *
from PIL import Image, ImageTk

# 摄像头捕获函数
def capture_video():
    global cap, photo, canvas_img_id  # 使用全局变量
    ret, frame = cap.read()  # 从摄像头读取一帧
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色从BGR到RGB
        frame = cv2.resize(frame, (int(frame.shape[1]*scale), int(frame.shape[0]*scale)))  # 根据缩放比例调整图像大小
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        if canvas_img_id is None:
            canvas_img_id = canvas.create_image(0, 0, image=photo, anchor=NW)
        else:
            canvas.itemconfig(canvas_img_id, image=photo)
    window.after(10, capture_video)  # 每10ms捕获一次

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

# 创建按钮的框架
button_frame = Frame(window)
button_frame.pack(side=TOP, fill=X)

# 创建放大和缩小按钮
zoom_in_button = Button(button_frame, text="放大", command=zoom_in)
zoom_in_button.pack(side=LEFT)

zoom_out_button = Button(button_frame, text="缩小", command=zoom_out)
zoom_out_button.pack(side=LEFT)

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

# 开始视频捕获
capture_video()

# 运行主循环
window.mainloop()

# 释放资源
cap.release()
cv2.destroyAllWindows()

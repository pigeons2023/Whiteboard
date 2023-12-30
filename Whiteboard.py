#
#        *                            _ooOoo_
#        *                           o8888888o
#        *                           88" . "88
#        *                           (| -_- |)
#        *                            O\ = /O
#        *                        ____/`---'\____
#        *                      .   ' \\| |// `   .
#        *                       / \\||| : |||// \
#        *                     / _||||| -:- |||||- \
#        *                       | | \\\ - /// | |
#        *                     | \_| ''\---/'' | |
#        *                      \ .-\__ `-` ___/-. /
#        *                   ___`. .' /--.--\ `. . __
#        *                ."" '< `.___\_<|>_/___.' >'"".
#        *               | | : `- \`.;`\ _ /`;.`/ - ` : | |
#        *                 \ \ `-. \_ __\ /__ _/ .-` / /
#        *         ======`-.____`-.___\_____/___.-`____.-'======
#        *                            `=---='
#        *
#        *         .............................................
#        *                  佛祖镇楼                  BUG辟易
#        *          佛曰:
#        *                  写字楼里写字间，写字间里程序员；
#        *                  程序人员写程序，又拿程序换酒钱。
#        *                  酒醒只在网上坐，酒醉还来网下眠；
#        *                  酒醉酒醒日复日，网上网下年复年。
#        *                  但愿老死电脑间，不愿鞠躬老板前；
#        *                  奔驰宝马贵者趣，公交自行程序员。
#        *                  别人笑我忒疯癫，我笑自己命太贱；
#        *                  不见满街漂亮妹，哪个归得程序员？
#        *
#
from datetime import datetime
from tkinter import Scale, ttk
from tkinter import colorchooser
from PIL import ImageGrab
from webbrowser import open as web_open
from tkinter import filedialog
from csv import reader as csv_reader
import random
import os
from sys import exit as sys_exit
import time
import atexit
import msvcrt
from tempfile import gettempdir
import tkinter as tk
from tkinter import messagebox
import threading
# from httpx import get as httpx_get
# import easygui as eg

# 图标Base64
icon_data = '''
        iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABjSURBVDhP7Y5LCgAhDEN7/0uPZFEInX5S3A3zIKgxjdpP5Am6hkvWhfwTVS1SiBjzmzJHLvTXXaDySvgy20/eC1xykAUqryULql6KOpx5KdMwC/haMgYC60KcJ7Vswkrm+5gdXxRZp8nnFLkAAAAASUVORK5CYII=
    '''

class AnnotationApp:
    def __init__(self, root):
        # 创建一个临时文件作为进程锁
        lock_file_path = os.path.join(gettempdir(), 'my_program_lock')
        lock_file = open(lock_file_path, 'w')

        try:
            # 尝试获取进程锁，若已经被其他实例获取，则显示启动失败信息框并退出
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        except IOError:
            messagebox.showinfo("启动失败", "程序已经在运行中")
            sys_exit()

        # 当程序退出时删除临时文件并释放进程锁
        atexit.register(lambda: os.remove(lock_file_path))
        atexit.register(lambda: lock_file.close())
        self.root = root

        # 设置关闭时的状态阶段
        self.confirmation_stage = 0  # 确认阶段，0表示初始阶段

        # 获取长宽数据
        self.screen_width = root.winfo_screenwidth()  
        self.screen_height = root.winfo_screenheight()  

        # 定义生成画布Canvas
        self.canvas = tk.Canvas(root, width=600, height=600, bg='white', highlightthickness=0)  # 设置画布大小为width=root.winfo_screenwidth(), height=root.winfo_screenheight()-105
        self.canvas.pack(side="top")

        # 定义初始笔的粗细
        self.pen_width = 5  # 默认笔的粗细为5
        self.current_pen_width = 5  # 当前的笔宽度

        # 定义初始橡皮大小
        self.eraser_width = 10  # 默认橡皮的粗细为10
        self.current_eraser_width = 10  # 当前的橡皮宽度
        
        # 定义初始笔的颜色
        # self.color = "black"  # 默认笔的颜色为黑色
        self.current_color = "black"  # 当前的颜色值

        # 定义Canvas的状态
        self.is_drawing = False
        self.start_x = None
        self.start_y = None
        
        # 定义鼠标按键
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)

        # 页数以及页面绘画内容
        self.page_number = 1  # 当前页数
        self.pages = [[]]  # 每一页的绘画内容
        
        # 上一页按钮
        self.prev_button = ttk.Button(root, text="上一页", command=self.prev_page)
        self.prev_button.pack(side="left", padx=10, pady=10)

        # 下一页按钮
        self.next_button = ttk.Button(root, text="下一页", command=self.next_page)
        self.next_button.pack(side="left", padx=10, pady=10)

        # 目录按钮
        self.directory_button = ttk.Button(root, text="目录", command=self.open_directory)
        self.directory_button.pack(side="left", padx=10, pady=10)

        # 新增一页按钮
        self.add_page_button = ttk.Button(root, text="新增一页", command=self.add_page)
        self.add_page_button.pack(side="left", padx=10, pady=10)

        # 笔的大小调节控件
        self.pen_label = ttk.Label(root, text="笔的粗细:")
        self.pen_label.pack(side="left", padx=10, pady=10)
        self.pen_width_scale = Scale(root, from_=0, to=15, orient=tk.HORIZONTAL,tickinterval=1, command=self.change_pen_width, length=300,showvalue=True)
        self.pen_width_scale.set(self.pen_width)
        self.pen_width_scale.pack(side="left", padx=10, pady=10)

        # 橡皮的调节控件
        self.iferaser = False #是否使用橡皮
        self.eraser_label = ttk.Label(root, text="橡皮大小:")
        self.eraser_label.pack(side="left", padx=10, pady=10)
        self.eraser_width_scale = Scale(root, from_=0, to=50, orient=tk.HORIZONTAL,tickinterval=5, command=self.change_eraser_width,length=250,showvalue=True)
        self.eraser_width_scale.set(self.eraser_width)
        self.eraser_width_scale.pack(side="left", padx=10, pady=10)

        # 定义窗口关闭事件处理函数
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #CSV示例
        #写入标题行  
        #           'name'    ,   'weight'
        #            Alice    ,    5
        #            Bob      ,    6 
        #            Charlie  ,    7 
        #            David    ,    8
        #            Eve      ,    9 

    def activate_drawing(self):
        self.iferaser = False
        # self.current_color = "black"
        self.canvas.bind("<Button-1>", self.start_drawing)  # 绑定鼠标左键点击事件到开始绘画方法
        self.canvas.bind("<B1-Motion>", self.draw)  # 绑定鼠标拖动事件到绘画方法
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)  # 绑定鼠标左键释放事件到结束绘画方法
    def start_drawing(self, event):
        self.is_drawing = True
        self.start_x = event.x
        self.start_y = event.y

    def draw(self, event):
        if self.is_drawing:
            if self.iferaser == True:  # 使用橡皮擦
                self.canvas.create_oval(event.x - self.current_eraser_width, event.y - self.current_eraser_width,
                                        event.x + self.current_eraser_width, event.y + self.current_eraser_width,
                                        fill=self.canvas.cget("background"), outline="")
            else:  # 使用笔
                distance = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5  # 计算距离
                acceleration = 0.6  # 设置加速度
                width = int(self.current_pen_width * (1 - distance / 80) + acceleration)  # 根据距离和加速度计算线条宽度（模拟笔锋）
                if width < 7:
                    minimum_width = int(self.current_pen_width * 0.4)
                else:
                    minimum_width = int(self.current_pen_width * 0.2)
                width = max(width, minimum_width)  # 确保线条宽度不低于最低粗细
                cx = (self.start_x + event.x) / 2  # 计算控制点x坐标
                cy = (self.start_y + event.y) / 2  # 计算控制点y坐标
                self.canvas.create_line(self.start_x, self.start_y, cx, cy, event.x, event.y,fill=self.current_color, width=width, smooth=True,splinesteps=500, joinstyle=tk.ROUND,tags='pen')  # 使用二次贝塞尔曲线绘制
                self.start_x = event.x
                self.start_y = event.y

    def stop_drawing(self, event):
        self.is_drawing = False

    def change_color(self, color):
        # self.color = color
        self.current_color = color
    
    def change_pen_width(self, width):
        self.pen_width = int(float(width))
        self.current_pen_width = int(float(width))
    
    def change_eraser_width(self, width):
        self.eraser_width = int(float(width))
        self.current_eraser_width = int(float(width))

    def use_eraser(self):
        # self.current_color = self.color
        # self.color = self.canvas.cget("background")
        self.iferaser = True
        self.current_pen_width = self.pen_width
        self.current_eraser_width = self.eraser_width
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.page_number = 1  # 重置页数为1
        self.pages = [[]]  # 清空所有绘画内容
    
    def prev_page(self):
        if self.page_number > 1:
            self.save_page_content()
            self.page_number -= 1
            self.redraw_canvas()
    
    def next_page(self):
        total_pages = len(self.pages)
        if self.page_number < total_pages:
            self.save_page_content()
            self.page_number += 1
            self.redraw_canvas()
        elif self.page_number == total_pages:  # 到达最后一页时，添加新的一页
            self.add_page()
    
    def open_directory(self):
        directory_window = tk.Toplevel(self.root)
        directory_window.title("目录")
        # 设置滚动条
        scrollbar = ttk.Scrollbar(directory_window)
        scrollbar.pack(side="right", fill="y")
        # 创建目录列表框
        directory_listbox = tk.Listbox(directory_window, yscrollcommand=scrollbar.set)
        directory_listbox.pack(side="left", fill="both", expand=True)
        # 添加目录内容
        for i, page_title in enumerate(self.directory):
            directory_listbox.insert(tk.END, page_title)
        # 绑定滚动条与列表框
        scrollbar.config(command=directory_listbox.yview)
        # 点击目录项跳转到对应页面
        directory_listbox.bind("<<ListboxSelect>>", lambda event: self.goto_page(directory_listbox.curselection()[0]))
    
    def goto_page(self, page_index):
        self.save_page_content()
        self.page_number = page_index + 1
        self.redraw_canvas()
    
    def add_page(self):
        self.save_page_content()
        self.canvas.delete("all")  # 清空画布
        self.pages.append([])  # 添加一个新的空白页面
        self.page_number = len(self.pages)  # 更新页数为最新的页数

        self.update_directory()  # 更新目录
        
    def update_directory(self):
        self.directory = []
        for i in range(len(self.pages)):
            self.directory.append(f"第 {i+1} 页")
        
    def redraw_canvas(self):
        item : list
        self.canvas.delete("all")
        for item in self.pages[self.page_number-1]:
            # if len(item) == 8 :
            #     item.pop(2)
            #     item.pop(3)
            # print(item)
            if item[-2] == self.canvas.cget("background") and item[-1] == 'pen':  # 使用橡皮擦
                print(item)
                self.canvas.create_line(item[0], item[1], item[2], item[3]
                                         ,fill=self.canvas.cget("background"), width=item[5],tags='pen')
            if item[-1] == 'pen':  
                print(item)
                self.canvas.create_line(item[0], item[1], item[2], item[3], item[4] ,item[5]
                                        ,fill=item[6], width=item[7],tags='pen')
            if item[-1] == 'line':
                self.canvas.create_line(item[0], item[1], item[2], item[3],
                                        fill=item[4], width=item[5],tags='line')
            if item[-2] == 'dotted':
                self.canvas.create_line(item[0], item[1], item[2], item[3],
                                        fill=item[4], width=item[5],dash=item[-1],tags='dotted')
            if item[-1] == 'rectangle':
                self.canvas.create_rectangle(item[0],item[1],item[2],item[3],outline=item[4],width=item[5],tags='rectangle')
            if item[-1] == 'triangle':
                # print(len(item))
                self.canvas.create_polygon(item[0],item[1],item[2],item[3],item[4],item[5],outline=item[6],width=item[7],fill=item[8],tags='triangle')
            if item[-1] == 'circle':
                self.canvas.create_oval(item[0],item[1],item[2],item[3],outline=item[4],width=item[5],tags='circle')

    
    def save_page_content(self):
        content = []
        for item in self.canvas.find_all():
            if self.canvas.itemcget(item,'tags') == 'pen' and self.canvas.itemcget(item, "fill") == self.canvas.cget("background"):  # 使用橡皮擦
                content.append(self.canvas.coords(item) + [self.canvas.itemcget(item, "fill"), self.canvas.itemcget(item, "width"), self.canvas.itemcget(item,'tags')])
            if self.canvas.itemcget(item,'tags') == 'pen':  # 使用笔
                content.append(self.canvas.coords(item) + [self.canvas.itemcget(item, "fill"), self.canvas.itemcget(item, "width"), self.canvas.itemcget(item,'tags')])
            if self.canvas.itemcget(item,'tags') == 'dotted':
                content.append(self.canvas.coords(item) + [self.canvas.itemcget(item, "fill"), self.canvas.itemcget(item, "width"), self.canvas.itemcget(item,'tags'), self.canvas.itemcget(item,'dash')])
            if self.canvas.itemcget(item,'tags') == 'line':  # 使用直线
                content.append(self.canvas.coords(item) + [self.canvas.itemcget(item, "fill"), self.canvas.itemcget(item, "width"), self.canvas.itemcget(item,'tags')])
            if self.canvas.itemcget(item,'tags') == 'rectangle':
                content.append(self.canvas.coords(item) + [self.canvas.itemcget(item, "outline"), self.canvas.itemcget(item, "width"), self.canvas.itemcget(item,'tags')])
            if self.canvas.itemcget(item,'tags') == 'triangle':
                content.append(self.canvas.coords(item) + [self.canvas.itemcget(item, "outline"), self.canvas.itemcget(item, "width"), self.canvas.itemcget(item,'fill') ,self.canvas.itemcget(item,'tags')])
            if self.canvas.itemcget(item,'tags') == 'circle':
                content.append(self.canvas.coords(item) + [self.canvas.itemcget(item, "outline"), self.canvas.itemcget(item, "width"), self.canvas.itemcget(item,'tags')])    

        self.pages[self.page_number-1] = content
    
    def save_current_page(self):
        self.save_page_content()
    
    def save_all_pages(self):
        for i in range(len(self.pages)):
            self.page_number = i+1
            self.save_page_content()
 
    def about(self):
        messagebox.showinfo("关于软件", "软件名称：Whiteboard\n版本：0.6\n作者：Pigeons2023 wuqi9277")

    def open_website(self):
        url = "https://pigeonserver.xyz"  # 打开官网
        web_open(url)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose color")
        if color[1] is not None:
            self.current_color = color[1]
            # self.color = color[1]

    def close_window(self, event=None):
        if self.confirmation_stage == 0:
            if messagebox.askyesno("退出", "您要退出白板吗？"):
                self.confirmation_stage = 1
                self.close_window()  # 立即进行下一轮确认
            else:
                self.confirmation_stage = 0  # 重置确认阶段
        elif self.confirmation_stage == 1:
            if messagebox.askyesno("退出", "请再确认一下，您是否要退出白板？"):
                self.confirmation_stage = 2
                self.close_window()  # 立即进行下一轮确认
            else:
                self.confirmation_stage = 0  # 重置确认阶段
        else:  # 确认阶段为2
            if messagebox.askyesno("退出", "亲，不退出白板行吗？"):
                self.confirmation_stage = 0  # 重置确认阶段
            else:
                root.destroy()

    def on_closing(self):
        if self.confirmation_stage == 0:
            if messagebox.askyesno("退出", "您要退出白板吗？"):
                self.confirmation_stage = 1
                self.close_window()  # 立即进行下一轮确认
            else:
                self.confirmation_stage = 0  # 重置确认阶段
        elif self.confirmation_stage == 1:
            if messagebox.askyesno("退出", "请再确认一下，您是否要退出白板？"):
                self.confirmation_stage = 2
                self.close_window()  # 立即进行下一轮确认
            else:
                self.confirmation_stage = 0  # 重置确认阶段
        else:  # 确认阶段为2
            if messagebox.askyesno("退出", "亲，不退出白板行吗？"):
                self.confirmation_stage = 0  # 重置确认阶段
            else:
                root.destroy()

    # 创建抽奖功能
    def choujiang(self):
        self.choujiang = tk.Toplevel(root) 
        self.choujiang.title("抽奖程序")
        self.choujiang.wm_attributes("-topmost", True)  
        self.participants = []

        # 创建界面元素
        self.import_button = tk.Button(self.choujiang, text="导入参与者名单", command=self.import_participants)
        self.import_button.pack(pady=10)
        self.num_winners_label = tk.Label(self.choujiang, text="抽奖人数：")
        self.num_winners_label.pack()
        self.num_winners_entry = tk.Entry(self.choujiang)
        self.num_winners_entry.pack()

        self.draw_button = tk.Button(self.choujiang, text="开始抽奖", command=self.draw_winners)
        self.draw_button.pack(pady=10)

        self.draw_one_button = tk.Button(self.choujiang, text="抽取一个人", command=lambda: self.draw_specific_number(1))
        self.draw_one_button.pack(pady=5)
        self.result_label = tk.Label(self.choujiang, text="")
        self.result_label.pack(pady=10)

    def import_participants(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv_reader(file)
                next(reader)  # 跳过标题行
                for row in reader:
                    name = row[0]
                    weight = int(row[1])
                    self.participants.extend([(name, weight)])
            self.result_label.config(text="成功导入参与者名单")

    def draw_winners(self):
        # 在以后实现多抽，目前抽一个
        if self.participants:
            # num_winners = int(self.num_winners_entry.get())
            num_winners = int(1)
            total_weight = sum([weight for _, weight in self.participants])
            if num_winners <= len(self.participants):
                winners = random.choices(self.participants, [weight/total_weight for _, weight in self.participants], k=num_winners)
                result_text = f"恭喜以下人员获奖：\n"
                for winner, _ in winners:
                    result_text += f"{winner}\n"
                self.result_label.config(text=result_text)
                for winner in winners:
                    self.participants.remove(winner)
            else:
                self.result_label.config(text="抽奖人数超过参与者总数")
        else:
            self.result_label.config(text="请先导入参与者名单")

    def draw_specific_number(self, num_winners):
        if self.participants:
            total_weight = sum([weight for _, weight in self.participants])
            if num_winners <= len(self.participants):
                winners = random.choices(self.participants, [weight/total_weight for _, weight in self.participants], k=num_winners)
                result_text = f"恭喜以下人员获奖：\n"
                for winner, _ in winners:
                    result_text += f"{winner}\n"
                self.result_label.config(text=result_text)
                for winner in winners:
                    self.participants.remove(winner)
            else:
                self.result_label.config(text="抽奖人数超过参与者总数")
        else:
            self.result_label.config(text="请先导入参与者名单")

    def time(self):
        self.time = tk.Toplevel(root)
        self.time.title("计时器")
        self.time.wm_attributes("-topmost", True)
        self.participants = []

        # 时钟部分
        self.clock_label = tk.Label(self.time, font=('calibri', 40, 'bold'), background='purple', foreground='white')
        self.clock_label.pack(fill='both', expand=1)
        self.clock_running = True
        self.update_clock()

        # 计时器部分
        self.timer_label = tk.Label(self.time, text="计时器", font=('calibri', 20, 'bold'))
        self.timer_label.pack()
        self.start_time = None
        self.timer_running = False
        self.timer_text = tk.StringVar()
        self.timer_text.set("00:00:00")
        self.timer_display = tk.Label(self.time, textvariable=self.timer_text, font=('calibri', 40, 'bold'))
        self.timer_display.pack()
        self.start_button = tk.Button(self.time, text="开始", command=self.start_timer)
        self.start_button.pack()
        self.stop_button = tk.Button(self.time, text="停止", command=self.stop_timer)
        self.stop_button.pack()

        # 倒计时部分
        self.countdown_label = tk.Label(self.time, text="倒计时", font=('calibri', 20, 'bold'))
        self.countdown_label.pack()
        self.countdown_time = tk.IntVar()
        self.countdown_time.set(0)
        self.countdown_entry = tk.Entry(self.time, textvariable=self.countdown_time, font=('calibri', 20, 'bold'))
        self.countdown_entry.pack()
        self.add_button = tk.Button(self.time, text="  +  ", command=self.add_time)
        self.add_button.pack(side='left')
        self.subtract_button = tk.Button(self.time, text="  -  ", command=self.subtract_time)
        self.subtract_button.pack(side='right')
        self.start_countdown_button = tk.Button(self.time, text="开始倒计时", command=self.start_countdown)
        self.start_countdown_button.pack()

    def update_clock(self):
        if self.clock_running:
            current_time = time.strftime('%H:%M:%S')
            self.clock_label.configure(text=current_time)
        self.time.after(1000, self.update_clock)

    def start_timer(self):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            self.timer_text.set(time_str)
            self.time.after(1000, self.update_timer)

    def add_time(self):
        current_time = self.countdown_time.get()
        self.countdown_time.set(current_time + 1)

    def subtract_time(self):
        current_time = self.countdown_time.get()
        if current_time > 0:
            self.countdown_time.set(current_time - 1)

    def start_countdown(self):
        countdown_seconds = self.countdown_time.get()
        if countdown_seconds > 0:
            self.countdown_timer(countdown_seconds)
        else:
            messagebox.showerror("错误", "请输入一个大于0的数字")

    def countdown_timer(self, seconds):
        if seconds > 0:
            self.countdown_time.set(seconds)
            self.time.after(1000, self.countdown_timer, seconds - 1)
        else:
            messagebox.showinfo("提示", "倒计时结束")

    def start_drawing_line(self):
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw_line)
        self.canvas.bind('<ButtonRelease-1>', self.finish_drawing_line)

    def draw_line(self, event):
        if self.is_drawing:
            self.canvas.delete("temp_line")  # 删除临时线条，以便更新位置
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                    fill=self.current_color, width=self.current_pen_width, tags="temp_line")

    def finish_drawing_line(self, event):
        self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                fill=self.current_color, width=self.current_pen_width,tags='line')
        self.is_drawing = False
        self.canvas.delete("temp_line")  # 删除临时线条

    def start_drawing_dotted_line(self):
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw_dotted_line)
        self.canvas.bind('<ButtonRelease-1>', self.finish_drawing_dotted_line)

    def draw_dotted_line(self, event):
        if self.is_drawing:
            self.canvas.delete("temp_line")  # 删除临时线条，以便更新位置
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                    fill=self.current_color, width=self.current_pen_width, dash=(4, 4),
                                    tags="temp_line")

    def finish_drawing_dotted_line(self, event):
        self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                fill=self.current_color, width=self.current_pen_width, dash=(4, 4),tags='dotted')
        self.is_drawing = False
        self.canvas.delete("temp_line")  # 删除临时线条

    def draw_rectangle(self, event):
        if self.is_drawing:
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                         outline=self.current_color, width=self.current_pen_width)
            self.is_drawing = False

    def start_drawing_rectangle(self):
        self.canvas.bind('<Button-1>', self.start_rectangle_draw)
        self.canvas.bind('<B1-Motion>', self.continue_rectangle_draw)
        self.canvas.bind('<ButtonRelease-1>', self.finish_rectangle_draw)

    def start_rectangle_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def continue_rectangle_draw(self, event):
        if self.start_x is not None and self.start_y is not None:
            self.canvas.delete("temp_rectangle")  # 删除临时矩形，以便更新位置
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                         outline=self.current_color, width=self.current_pen_width,
                                         tags="temp_rectangle")

    def finish_rectangle_draw(self, event):
        if self.start_x is not None and self.start_y is not None:
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                         outline=self.current_color, width=self.current_pen_width,tags='rectangle')
            self.start_x = None
            self.start_y = None

    def draw_triangle(self, event):
        if self.is_drawing:
            coords = [self.start_x, event.y, event.x, event.y, (self.start_x + event.x) / 2, self.start_y]
            self.canvas.create_polygon(coords, outline=self.current_color, width=self.current_pen_width)
            self.is_drawing = False

    def start_triangle_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def continue_triangle_draw(self, event):
        if self.start_x is not None and self.start_y is not None:
            self.canvas.delete("temp_triangle")  # 删除临时三角形，以便更新位置
            coords = [self.start_x, event.y, event.x, event.y, (self.start_x + event.x) / 2, self.start_y]
            self.canvas.create_polygon(coords, outline=self.current_color, width=self.current_pen_width,fill='',
                                       tags="temp_triangle")

    def finish_triangle_draw(self, event):
        if self.start_x is not None and self.start_y is not None:
            coords = [self.start_x, event.y, event.x, event.y, (self.start_x + event.x) / 2, self.start_y]
            self.canvas.create_polygon(coords, outline=self.current_color, width=self.current_pen_width,fill='',tags='triangle')  # 将多边形设置为有颜色的轮廓
            self.start_x = None
            self.start_y = None

    def start_drawing_triangle(self):
        self.canvas.bind('<Button-1>', self.start_triangle_draw)
        self.canvas.bind('<B1-Motion>', self.continue_triangle_draw)
        self.canvas.bind('<ButtonRelease-1>', self.finish_triangle_draw)

    def start_drawing_circle(self, event):
        self.is_drawing = True
        self.start_x = event.x
        self.start_y = event.y

    def draw_circle(self, event):
        if self.is_drawing:
            self.canvas.delete("temp_circle")  # 删除之前的临时圆形
            radius = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
            # 绘制临时圆形作为预览效果
            self.canvas.create_oval(self.start_x - radius, self.start_y - radius,
                                    self.start_x + radius, self.start_y + radius,
                                    outline=self.current_color, width=self.current_pen_width,
                                    tags="temp_circle")  # 使用tags标记临时圆形

    def finish_drawing_circle(self, event):
        if self.is_drawing:
            radius = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
            self.canvas.create_oval(self.start_x - radius, self.start_y - radius,
                                    self.start_x + radius, self.start_y + radius,
                                    outline=self.current_color, width=self.current_pen_width,tags='circle')
        self.is_drawing = False

    def switch_to_circle(self):
        self.current_shape = "circle"
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.canvas.bind('<Button-1>', self.start_drawing_circle)
        self.canvas.bind('<B1-Motion>', self.draw_circle)
        self.canvas.bind('<ButtonRelease-1>', self.finish_drawing_circle)



def save_as_png():
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        default_file_name = f"image_{current_time}.png"
        folder_path = os.path.join(os.path.expanduser('~'),"Desktop")
        # 创建文件夹
        os.makedirs(folder_path, exist_ok=True)
        # 拼接文件夹路径和文件名
        file_path = os.path.join(folder_path, default_file_name)
        # 保存图像
        ImageGrab.grab().save(file_path, "PNG")
    

def runner() -> int :
    # 添加一个菜单栏，用于选择颜色和橡皮的大小
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # 创建抽奖按钮
    close_button = ttk.Button(root, text="抽奖", command=app.choujiang)
    close_button.pack(side="left", padx=10, pady=10)

    # 创建时间按钮
    close_button = ttk.Button(root, text="计时器", command=app.time)
    close_button.pack(side="left", padx=10, pady=10)

    def minimize_window():
        root.iconify()
    # 创建最小化按钮
    minimize_button = ttk.Button(root, text="最小化", command=minimize_window)
    minimize_button.pack(side="left", padx=10, pady=10)

    # 创建关闭按钮
    close_button = ttk.Button(root, text="关闭", command=app.close_window)
    close_button.pack(side="left", padx=10, pady=10)
    # 画笔
    menu_bar.add_command(label="使用画笔", command=app.activate_drawing)
    # 绘制图形
    draw_graphics = tk.Menu(menu_bar, tearoff=0)
    draw_graphics.add_command(label="直线", command=app.start_drawing_line)
    draw_graphics.add_command(label="虚线", command=app.start_drawing_dotted_line)
    draw_graphics.add_command(label="矩形", command=app.start_drawing_rectangle)
    draw_graphics.add_command(label="三角形", command=app.start_drawing_triangle)
    draw_graphics.add_command(label="圆", command=app.switch_to_circle)
    menu_bar.add_cascade(label="绘画图像", menu=draw_graphics)
    # 颜色子菜单
    color_menu = tk.Menu(menu_bar, tearoff=0)
    color_menu.add_command(label="黑色", command=lambda: app.change_color("black"))
    color_menu.add_command(label="红色", command=lambda: app.change_color("red"))
    color_menu.add_command(label="绿色", command=lambda: app.change_color("green"))
    color_menu.add_command(label="蓝色", command=lambda: app.change_color("blue"))
    # 新增更多颜色选项
    color_menu.add_command(label="自定义颜色", command=app.choose_color)
    menu_bar.add_cascade(label="颜色", menu=color_menu)

    # 笔的大小调节子菜单
    pen_width_menu = tk.Menu(menu_bar, tearoff=0)
    pen_width_menu.add_command(label="3px", command=lambda: app.change_pen_width(3))
    pen_width_menu.add_command(label="5px", command=lambda: app.change_pen_width(5))
    pen_width_menu.add_command(label="7px", command=lambda: app.change_pen_width(7))
    pen_width_menu.add_command(label="9px", command=lambda: app.change_pen_width(9))
    menu_bar.add_cascade(label="笔的粗细", menu=pen_width_menu)

    # 橡皮的大小调节子菜单
    eraser_width_menu = tk.Menu(menu_bar, tearoff=0)
    eraser_width_menu.add_command(label="1px", command=lambda: app.change_eraser_width(1))
    eraser_width_menu.add_command(label="5px", command=lambda: app.change_eraser_width(5))
    eraser_width_menu.add_command(label="10px", command=lambda: app.change_eraser_width(10))
    eraser_width_menu.add_command(label="20px", command=lambda: app.change_eraser_width(20))
    menu_bar.add_cascade(label="橡皮大小", menu=eraser_width_menu)

    # 橡皮擦子菜单
    menu_bar.add_command(label="使用橡皮", command=app.use_eraser)

    # # 清空画布子菜单
    # menu_bar.add_command(label="重载白板", command=app.clear_canvas)

    # # 保存当前页子菜单
    # menu_bar.add_command(label="保存当前页面", command=app.save_current_page)

    # # 保存所有页子菜单
    # menu_bar.add_command(label="保存所有页面", command=app.save_all_pages)

    # 保存图片
    menu_bar.add_command(label="保存图片", command=lambda: save_as_png())

    # 打开官网
    menu_bar.add_command(label="直达官网", command=app.open_website)

    # 关于软件
    menu_bar.add_command(label="关于软件", command=app.about)


# def check_update() :
#     try:
#         if os.path.exists("Whiteboard_New.exe"):
#             try:
#                 os.remove("Whiteboard_New.exe")
#             except: pass
#         data = httpx_get(url=cdn_url)
#         version_new = data.json()['version']
#         if version_new != version :
#             choose = eg.buttonbox("检测到新版本，是否更新？",title='',choices=('NO','YES'))
#             print("new version found")
#             if os.path.exists("updata.vbs"):
#                     try:
#                         os.remove("updata.vbs")
#                     except: pass
#             if not os.path.exists("updata.vbs"):
#                 try:
#                     with open("updata.vbs",'w',encoding='utf-8') as f:
#                         f.write(upgrade_vbs)
#                 except: pass
#             if choose == 'YES':
#                 print("user allowed download")
#                 d_url = data.json()['download_url']
#                 download = httpx_get(url=d_url)
#                 with open("Whiteboard_New.exe","wb") as f :
#                     f.write(download.content)
#                 if os.path.exists("Whiteboard_New.exe"):
#                     try:
#                         os.system("cmd.exe /c start updata.vbs")
#                     except: pass
#             else:
#                 print("cancel")
#         else:
#             print("no new version")
#     except: pass
#     return 0

def check_updata():
    try:
        runs = os.system("cmd.exe /c start updata.exe")
        print(runs)
    except: pass

if __name__ == '__main__':
    try:
        threading.Thread(target=check_updata,args=()).start()
    except: pass
    root = tk.Tk()
    root.state('zoomed')
    root.title('Whiteboard')
    # root.attributes('-fullscreen', True)
    root.wm_state('zoomed')
    app = AnnotationApp(root)
    icon_image = tk.PhotoImage(data=icon_data)
    root.iconphoto(True, icon_image)
    runner()
    root.mainloop()

# 后续完成的功能：
# 1、优化书写时卡顿，
# 2、增加抗锯齿，
# 3、支持屏幕批注、
# 4、支持PPT.dll，PPT批注，
# 5、支持单指、多指书写，
# 6、双指缩放，移动，
# 7、图形识别，
# 8、画几何图形，
# 9、背景颜色改变，
# 10、笔画选择、移动，克隆、旋转、删除，
# 11、视频展台以及其批注等功能,支持导入图片等类型文件的功能
# 12、保存独有后缀文件，并可以打开，一键生成所有页的PDF、Image,
# 13、目录可以查看缩略图,
# 14、重画icon，优化部分图标，重写readme，开源，使用github action编译，上传release，
# 15、支持检测并更新的功能，优化界面布局。
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
import time
from datetime import datetime
import tkinter as tk
from tkinter import Scale, ttk
import os
from tkinter import messagebox
from tkinter import colorchooser
from PIL import ImageGrab
import webbrowser
from tkinter import filedialog
import csv
import random
# 图标Base64
icon_data = '''
        iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABjSURBVDhP7Y5LCgAhDEN7/0uPZFEInX5S3A3zIKgxjdpP5Am6hkvWhfwTVS1SiBjzmzJHLvTXXaDySvgy20/eC1xykAUqryULql6KOpx5KdMwC/haMgYC60KcJ7Vswkrm+5gdXxRZp8nnFLkAAAAASUVORK5CYII=
    '''

class AnnotationApp:
    def __init__(self, root):
        self.root = root
        # 设置关闭时的状态阶段
        self.confirmation_stage = 0  # 确认阶段，0表示初始阶段

        # 获取长宽数据
        self.screen_width = root.winfo_screenwidth()  
        self.screen_height = root.winfo_screenheight()  

        # 定义生成画布Canvas
        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight()-105, bg='white')  # 设置画布大小为width=root.winfo_screenwidth(), height=root.winfo_screenheight()-105
        self.canvas.pack(side="top")

        # 定义初始笔的粗细
        self.pen_width = 5  # 默认笔的粗细为3
        self.current_pen_width = 5  # 当前的笔宽度

        # 定义初始橡皮大小
        self.eraser_width = 10  # 默认橡皮的粗细为10
        self.current_eraser_width = 10  # 当前的橡皮宽度
        
        # 定义初始笔的颜色
        self.color = "black"  # 默认笔的颜色为黑色
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
        self.pen_width_scale = Scale(root, from_=0, to=10, orient=tk.HORIZONTAL,tickinterval=1, command=self.change_pen_width, length=200,showvalue=True)
        self.pen_width_scale.set(self.pen_width)
        self.pen_width_scale.pack(side="left", padx=10, pady=10)

        # 橡皮的大小调节控件
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

    def start_drawing(self, event):
        self.is_drawing = True
        self.start_x = event.x
        self.start_y = event.y
    
    def draw(self, event):
        if self.is_drawing:
            if self.current_color == self.canvas.cget("background"):  # 使用橡皮擦
                self.canvas.create_oval(event.x-self.current_eraser_width, event.y-self.current_eraser_width,
                                        event.x+self.current_eraser_width, event.y+self.current_eraser_width,
                                        fill=self.current_color, outline="")
            else:  # 使用笔
                distance = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5  # 计算距离
                width = int(self.current_pen_width * (1 - (distance / 100)))  # 根据距离计算线条宽度
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                        fill=self.current_color, width=width)
                self.start_x = event.x
                self.start_y = event.y
        
    def stop_drawing(self, event):
        self.is_drawing = False
        
    def change_color(self, color):
        self.color = color
        self.current_color = color
    
    def change_pen_width(self, width):
        self.pen_width = int(float(width))
        self.current_pen_width = int(float(width))
    
    def change_eraser_width(self, width):
        self.eraser_width = int(float(width))
        self.current_eraser_width = int(float(width))
    
    def use_eraser(self):
        self.current_color = self.color
        self.color = self.canvas.cget("background")
        self.current_pen_width = self.pen_width
        self.current_eraser_width = self.eraser_width
    
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
        self.canvas.delete("all")
        for item in self.pages[self.page_number-1]:
            if item[4] == self.canvas.cget("background"):  # 使用橡皮擦
                self.canvas.create_oval(item[0]-item[5], item[1]-item[5],
                                         item[2]+item[5], item[3]+item[5],
                                         fill=item[4], outline="")
            else:  # 使用笔
                self.canvas.create_line(item[0], item[1], item[2], item[3], fill=item[4], width=item[5])
    
    def save_page_content(self):
        content = []
        for item in self.canvas.find_all():
            if self.canvas.itemcget(item, "fill") == self.canvas.cget("background"):  # 使用橡皮擦
                content.append(self.canvas.coords(item) + [self.canvas.itemcget(item, "fill"), self.eraser_width])
            else:  # 使用笔
                content.append(self.canvas.coords(item) + [self.canvas.itemcget(item, "fill"), self.pen_width])
        self.pages[self.page_number-1] = content
    
    def save_current_page(self):
        self.save_page_content()
    
    def save_all_pages(self):
        for i in range(len(self.pages)):
            self.page_number = i+1
            self.save_page_content()
 
    def about(self):
        messagebox.showinfo("关于软件", "软件名称：Whiteboard\n版本：0.6\n作者：Pigeons2023")

    def open_website(self):
        url = "https://pigeonserver.xyz"  # 打开官网
        webbrowser.open(url)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose color")
        if color[1] is not None:
            self.current_color = color[1]
            self.color = color[1]

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
                reader = csv.reader(file)
                next(reader)  # 跳过标题行
                for row in reader:
                    name = row[0]
                    weight = int(row[1])
                    self.participants.extend([(name, weight)])
            self.result_label.config(text="成功导入参与者名单")

    def draw_winners(self):
        if self.participants:
            num_winners = int(self.num_winners_entry.get())
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

def save_as_png():
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        default_file_name = f"image_{current_time}.png"
        folder_path = "pic"
        # 创建文件夹
        os.makedirs(folder_path, exist_ok=True)
        # 拼接文件夹路径和文件名
        file_path = os.path.join(folder_path, default_file_name)
        # 保存图像
        ImageGrab.grab().save(file_path, "PNG")
    
if __name__ == '__main__':
    root = tk.Tk()
    root.state('zoomed')
    root.title('Whiteboard')
    root.attributes('-fullscreen', True)
    root.wm_state('zoomed')
    app = AnnotationApp(root)
    icon_image = tk.PhotoImage(data=icon_data)
    root.iconphoto(True, icon_image)
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

    # 清空画布子菜单
    menu_bar.add_command(label="重载白板", command=app.clear_canvas)

    # 保存当前页子菜单
    menu_bar.add_command(label="保存当前页面", command=app.save_current_page)

    # 保存所有页子菜单
    menu_bar.add_command(label="保存所有页面", command=app.save_all_pages)

    # 保存图片
    menu_bar.add_command(label="保存图片", command=lambda: save_as_png())

    # 打开官网
    menu_bar.add_command(label="直达官网", command=app.open_website)

    # 关于软件
    menu_bar.add_command(label="关于软件", command=app.about)

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
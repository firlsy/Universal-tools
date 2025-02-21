import tkinter as tk
from tkinter import ttk, messagebox
from pypinyin import pinyin, Style, lazy_pinyin

def convert_to_pinyin():
    text = input_text.get("1.0", "end-1c")
    add_tone = tone_var.get()
    capitalize = capitalize_var.get()
    add_space = space_var.get()

    try:
        # 获取拼音和多音字信息
        pinyin_list = pinyin(text, style=Style.TONE3 if add_tone else Style.NORMAL, heteronym=True)
        lazy_pinyin_list = lazy_pinyin(text, style=Style.TONE3 if add_tone else Style.NORMAL)

        # 处理拼音结果
        result = []
        for word in lazy_pinyin_list:
            if capitalize:
                word = word.capitalize()
            result.append(word)

        separator = " " if add_space else ""
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", separator.join(result))
        output_text.configure(state="disabled")

        # 检查多音字
        polyphone_text.configure(state="normal")
        polyphone_text.delete("1.0", "end")
        line_num = 0
        char_count = 0
        for i, char in enumerate(text):
            if char == '\n':
                line_num += 1
                char_count = 0
                continue
            if len(pinyin_list[i]) > 1:
                polyphone_text.insert("end", 
                    f"第{line_num+1}行第{char_count+1}字「{char}」是多音字：{', '.join(pinyin_list[i])}\n",
                    "warning")
            char_count += 1
        polyphone_text.configure(state="disabled")
        
    except Exception as e:
        messagebox.showerror("转换错误", f"发生错误：{str(e)}")

def paste_text():
    try:
        input_text.delete("1.0", "end")
        input_text.insert("1.0", root.clipboard_get())
        input_text.see("end")
    except tk.TclError:
        messagebox.showerror("错误", "剪贴板中没有文本")

def copy_pinyin():
    pinyin_text = output_text.get("1.0", "end-1c")
    if pinyin_text:
        root.clipboard_clear()
        root.clipboard_append(pinyin_text)
        messagebox.showinfo("成功", "拼音已复制到剪贴板")
    else:
        messagebox.showerror("错误", "没有可复制的拼音")

# 创建主窗口
root = tk.Tk()
root.title("文字转拼音 - 专业版")
root.geometry("800x700")
root.minsize(800, 600)
root.configure(bg="#f0f3f5")

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f0f3f5")
style.configure("TLabel", background="#f0f3f5", foreground="#2d3436", font=("微软雅黑", 10))
style.configure("TButton", font=("微软雅黑", 10), padding=6)
style.map("TButton",
    background=[("active", "#0984e3"), ("!disabled", "#00b894")],
    foreground=[("!disabled", "white")]
)
style.configure("TCheckbutton", background="#f0f3f5", font=("微软雅黑", 9))

# 主布局框架
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# 输入区域
input_frame = ttk.LabelFrame(main_frame, text=" 输入文字 ", padding=15)
input_frame.grid(row=0, column=0, sticky="nsew", pady=5)

input_text = tk.Text(input_frame, height=8, wrap=tk.WORD, 
                    font=("微软雅黑", 10), bg="white", padx=10, pady=10)
input_text.pack(fill="both", expand=True)

btn_frame = ttk.Frame(input_frame)
btn_frame.pack(fill="x", pady=5)
ttk.Button(btn_frame, text="📋 粘贴文字", command=paste_text, style="TButton").pack(side="right")

# 选项区域
options_frame = ttk.Frame(main_frame)
options_frame.grid(row=1, column=0, sticky="ew", pady=10)

tone_var = tk.BooleanVar(value=True)
capitalize_var = tk.BooleanVar()
space_var = tk.BooleanVar(value=True)

ttk.Checkbutton(options_frame, text="添加声调", variable=tone_var).pack(side="left", padx=15)
ttk.Checkbutton(options_frame, text="首字母大写", variable=capitalize_var).pack(side="left", padx=15)
ttk.Checkbutton(options_frame, text="空格间隔", variable=space_var).pack(side="left", padx=15)
ttk.Button(options_frame, text="🔄 立即转换", command=convert_to_pinyin, style="TButton").pack(side="right")

# 输出区域
output_frame = ttk.LabelFrame(main_frame, text=" 拼音结果 ", padding=15)
output_frame.grid(row=2, column=0, sticky="nsew", pady=5)

output_text = tk.Text(output_frame, height=8, wrap=tk.WORD, 
                     font=("Consolas", 11), bg="#f8f9fa", state="disabled", padx=10, pady=10)
output_text.pack(fill="both", expand=True)

btn_frame_out = ttk.Frame(output_frame)
btn_frame_out.pack(fill="x", pady=5)
ttk.Button(btn_frame_out, text="📄 复制结果", command=copy_pinyin, style="TButton").pack(side="right")

# 多音字提示
poly_frame = ttk.LabelFrame(main_frame, text=" 多音字提示 ", padding=15)
poly_frame.grid(row=3, column=0, sticky="nsew", pady=5)

polyphone_text = tk.Text(poly_frame, height=6, wrap=tk.WORD, 
                         font=("微软雅黑", 9), bg="#fff3cd", padx=10, pady=10)
polyphone_text.tag_configure("warning", foreground="#856404")
polyphone_text.pack(fill="both", expand=True)

# 布局权重配置
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(2, weight=1)
main_frame.rowconfigure(3, weight=1)

root.mainloop()

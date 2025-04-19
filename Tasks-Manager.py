# Gerenciador de Tarefas com customtkinter
# Requisitos: customtkinter, psutil, GPUtil, matplotlib

import customtkinter as ctk
import psutil
import GPUtil
import locale
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque

IDIOMAS = {
    "pt": {
        "net": "Rede", "tasks": "Tarefas em Execução", "dashboard": "Dashboard de Uso",
        "compare": "Comparativo de Uso", "cpu": "CPU", "gpu": "GPU", "memory": "Memória",
        "language": "Idioma", "kill": "Matar Tarefa", "confirm_kill": "Deseja encerrar esta tarefa?"
    },
    "en": {
        "net": "Network", "tasks": "Running Tasks", "dashboard": "Usage Dashboard",
        "compare": "Usage Comparison", "cpu": "CPU", "gpu": "GPU", "memory": "Memory",
        "language": "Language", "kill": "Kill Task", "confirm_kill": "Do you want to kill this task?"
    }
}

lang = "pt"
def traduzir(chave): return IDIOMAS[lang].get(chave, chave)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Gerenciador de Tarefas")
app.geometry("1250x850")

def trocar_idioma(event):
    global lang
    lang = lang_var.get()
    atualizar_rotulos()

def atualizar_rotulos():
    net_title.configure(text=traduzir("net"))
    task_title.configure(text=traduzir("tasks"))
    dash_title.configure(text=traduzir("dashboard"))
    compare_title.configure(text=traduzir("compare"))
    language_label.configure(text=traduzir("language"))
    kill_button.configure(text=traduzir("kill"))

# Frames
net_frame = ctk.CTkFrame(app, corner_radius=15)
net_frame.place(relx=0.02, rely=0.05, relwidth=0.45, relheight=0.2)
net_title = ctk.CTkLabel(net_frame, text="", font=ctk.CTkFont(weight="bold", size=16))
net_title.pack(anchor="w", padx=10, pady=5)
net_label = ctk.CTkLabel(net_frame, text="")
net_label.pack(padx=10, pady=10)

task_frame = ctk.CTkFrame(app, corner_radius=15)
task_frame.place(relx=0.02, rely=0.28, relwidth=0.45, relheight=0.4)
task_title = ctk.CTkLabel(task_frame, text="", font=ctk.CTkFont(weight="bold", size=16))
task_title.pack(anchor="w", padx=10, pady=5)
task_listbox = tk.Listbox(task_frame, font=("Consolas", 10))
task_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
kill_button = ctk.CTkButton(task_frame, text="", command=lambda: matar_tarefa())
kill_button.pack(pady=5)

def matar_tarefa():
    selected = task_listbox.curselection()
    if selected:
        pid_nome = task_listbox.get(selected[0])
        pid = int(pid_nome.split(' - ')[0])
        if messagebox.askyesno("Confirm", traduzir("confirm_kill")):
            try:
                psutil.Process(pid).terminate()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

dash_frame = ctk.CTkFrame(app, corner_radius=15)
dash_frame.place(relx=0.5, rely=0.05, relwidth=0.45, relheight=0.25)
dash_title = ctk.CTkLabel(dash_frame, text="", font=ctk.CTkFont(weight="bold", size=16))
dash_title.pack(anchor="w", padx=10, pady=5)
dash_label = ctk.CTkLabel(dash_frame, text="")
dash_label.pack(padx=10, pady=10)

compare_frame = ctk.CTkFrame(app, corner_radius=15)
compare_frame.place(relx=0.5, rely=0.32, relwidth=0.45, relheight=0.25)
compare_title = ctk.CTkLabel(compare_frame, text="", font=ctk.CTkFont(weight="bold", size=16))
compare_title.pack(anchor="w", padx=10, pady=5)
compare_label = ctk.CTkLabel(compare_frame, text="")
compare_label.pack(padx=10, pady=10)

lang_var = tk.StringVar(value=lang)
language_label = ctk.CTkLabel(app, text="")
language_label.place(relx=0.02, rely=0.7)
lang_menu = ttk.Combobox(app, textvariable=lang_var, values=["pt", "en"])
lang_menu.place(relx=0.02, rely=0.74, width=100)
lang_menu.bind("<<ComboboxSelected>>", trocar_idioma)

# Gráfico
data_len = 60
cpu_hist = deque([0]*data_len, maxlen=data_len)
memory_hist = deque([0]*data_len, maxlen=data_len)

graph_frame = ctk.CTkFrame(app, corner_radius=15)
graph_frame.place(relx=0.02, rely=0.8, relwidth=0.93, relheight=0.18)
fig, ax = plt.subplots(figsize=(8, 2.5))
line_cpu, = ax.plot(cpu_hist, label="CPU")
line_mem, = ax.plot(memory_hist, label="Memória", color='orange')
ax.legend()
ax.set_ylim(0, 100)
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Atualizações
def atualizar_interface():
    # Redes
    net_io = psutil.net_io_counters()
    net_label.configure(text=f"Enviados: {net_io.bytes_sent / 1024:.2f} KB\nRecebidos: {net_io.bytes_recv / 1024:.2f} KB")

    # Tarefas
    task_listbox.delete(0, tk.END)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            task_listbox.insert(tk.END, f"{proc.info['pid']} - {proc.info['name']}")
        except: continue

    # CPU/Mem/GPU
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    gpu = GPUtil.getGPUs()[0].load * 100 if GPUtil.getGPUs() else 0

    dash_label.configure(text=f"{traduzir('cpu')}: {cpu}%\n{traduzir('memory')}: {mem.percent}%\n{traduzir('gpu')}: {gpu:.2f}%")
    compare_label.configure(text=f"CPU vs GPU: {cpu:.1f}% / {gpu:.1f}%\nCPU vs Mem: {cpu:.1f}% / {mem.percent:.1f}%")

    cpu_hist.append(cpu)
    memory_hist.append(mem.percent)
    line_cpu.set_ydata(cpu_hist)
    line_mem.set_ydata(memory_hist)
    canvas.draw()

    app.after(2000, atualizar_interface)  # Chamada recursiva

# Inicialização
atualizar_rotulos()
atualizar_interface()
app.mainloop()

# Gerenciador de Tarefas com customtkinter
# Requisitos: customtkinter, psutil, GPUtil, matplotlib

import customtkinter as ctk
import psutil
import GPUtil
import threading
import locale
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque

# Configurar idioma do sistema
IDIOMAS = {
    "pt": {
        "net": "Rede",
        "tasks": "Tarefas em Execução",
        "dashboard": "Dashboard de Uso",
        "compare": "Comparativo de Uso",
        "cpu": "CPU",
        "gpu": "GPU",
        "memory": "Memória",
        "language": "Idioma"
    },
    "en": {
        "net": "Network",
        "tasks": "Running Tasks",
        "dashboard": "Usage Dashboard",
        "compare": "Usage Comparison",
        "cpu": "CPU",
        "gpu": "GPU",
        "memory": "Memory",
        "language": "Language"
    }
}

lang = "pt"

def traduzir(chave):
    return IDIOMAS[lang].get(chave, chave)

# Criando janela principal
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Gerenciador de Tarefas")
app.geometry("1200x800")

# Função para atualizar o idioma
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

# Frame de Redes
net_frame = ctk.CTkFrame(app)
net_frame.place(relx=0.02, rely=0.05, relwidth=0.45, relheight=0.2)

net_title = ctk.CTkLabel(net_frame, text="", font=ctk.CTkFont(weight="bold", size=16))
net_title.pack(anchor="w", padx=10, pady=5)

net_label = ctk.CTkLabel(net_frame, text="")
net_label.pack(padx=10, pady=10)

# Frame de Tarefas
task_frame = ctk.CTkFrame(app)
task_frame.place(relx=0.02, rely=0.28, relwidth=0.45, relheight=0.35)

task_title = ctk.CTkLabel(task_frame, text="", font=ctk.CTkFont(weight="bold", size=16))
task_title.pack(anchor="w", padx=10, pady=5)

task_listbox = tk.Listbox(task_frame)
task_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame de Dashboard
dash_frame = ctk.CTkFrame(app)
dash_frame.place(relx=0.5, rely=0.05, relwidth=0.45, relheight=0.3)

dash_title = ctk.CTkLabel(dash_frame, text="", font=ctk.CTkFont(weight="bold", size=16))
dash_title.pack(anchor="w", padx=10, pady=5)

dash_label = ctk.CTkLabel(dash_frame, text="")
dash_label.pack(padx=10, pady=10)

# Frame de Comparativo
compare_frame = ctk.CTkFrame(app)
compare_frame.place(relx=0.5, rely=0.38, relwidth=0.45, relheight=0.3)

compare_title = ctk.CTkLabel(compare_frame, text="", font=ctk.CTkFont(weight="bold", size=16))
compare_title.pack(anchor="w", padx=10, pady=5)

compare_label = ctk.CTkLabel(compare_frame, text="")
compare_label.pack(padx=10, pady=10)

# Dropdown para idioma
lang_var = tk.StringVar(value=lang)
language_label = ctk.CTkLabel(app, text="")
language_label.place(relx=0.02, rely=0.65)

lang_menu = ttk.Combobox(app, textvariable=lang_var, values=["pt", "en"])
lang_menu.place(relx=0.02, rely=0.69, width=100)
lang_menu.bind("<<ComboboxSelected>>", trocar_idioma)

# Histórico para os gráficos
data_len = 60
cpu_hist = deque([0]*data_len, maxlen=data_len)
memory_hist = deque([0]*data_len, maxlen=data_len)

# Frame com gráfico
graph_frame = ctk.CTkFrame(app)
graph_frame.place(relx=0.02, rely=0.75, relwidth=0.93, relheight=0.2)

fig, ax = plt.subplots(figsize=(8,2.5))
line_cpu, = ax.plot(cpu_hist, label="CPU")
line_mem, = ax.plot(memory_hist, label="Memória", color='orange')
ax.legend()
ax.set_ylim(0, 100)
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Funções de atualização dos dados
def atualizar_redes():
    net_io = psutil.net_io_counters()
    net_label.configure(text=f"Enviados: {net_io.bytes_sent / 1024:.2f} KB\nRecebidos: {net_io.bytes_recv / 1024:.2f} KB")

def atualizar_tarefas():
    task_listbox.delete(0, tk.END)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            task_listbox.insert(tk.END, f"{proc.info['pid']} - {proc.info['name']}")
        except:
            continue

def atualizar_dashboard():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    gpus = GPUtil.getGPUs()
    gpu = gpus[0].load * 100 if gpus else 0

    dash_label.configure(text=f"{traduzir('cpu')}: {cpu}%\n{traduzir('memory')}: {mem.percent}%\n{traduzir('gpu')}: {gpu:.2f}%")

    cpu_hist.append(cpu)
    memory_hist.append(mem.percent)
    line_cpu.set_ydata(cpu_hist)
    line_mem.set_ydata(memory_hist)
    canvas.draw()

def atualizar_comparativo():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    gpus = GPUtil.getGPUs()
    gpu = gpus[0].load * 100 if gpus else 0

    compare_label.configure(text=f"CPU vs GPU: {cpu:.1f}% / {gpu:.1f}%\nCPU vs Mem: {cpu:.1f}% / {mem:.1f}%")

def atualizador():
    while True:
        atualizar_redes()
        atualizar_tarefas()
        atualizar_dashboard()
        atualizar_comparativo()
        app.after(2000)

# Thread para não travar a interface
threading.Thread(target=atualizador, daemon=True).start()

# Inicializa os textos traduzidos
atualizar_rotulos()
app.mainloop()

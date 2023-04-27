import psutil
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# プロット用のリスト
x_list = []
y_lists = [[] for _ in range(5)]
names_list = []

# グラフの初期設定
fig, ax = plt.subplots()
plt.subplots_adjust(top=0.8)
lines = []
for i in range(5):
    line, = ax.plot([], [], label="")
    lines.append(line)
ax.set_ylim(0, 100)
ax.set_xlabel("Time")
ax.set_ylabel("Usage [%]")
ax.set_title("Top 5 CPU usage processes")
ax.legend()

# プロセス情報の取得
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            if proc.info['name'] != 'systemd':  # systemdプロセスは除外
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:5]

# グラフの更新処理
def update_graph(frame):
    # 時刻の取得
    x_list.append(frame)

    # CPU使用率の取得
    processes = get_processes()
    for i, proc in enumerate(processes):
        pid, name, cpu_percent = proc['pid'], proc['name'], proc['cpu_percent']
        y_lists[i].append(cpu_percent)
        if frame == 0:
            names_list.append(f"{name} ({pid})")

    # グラフの更新
    for i, line in enumerate(lines):
        line.set_data(x_list, y_lists[i])
        if frame == 0:
            line.set_label(names_list[i])
        ax.legend(loc="upper left")
    ax.set_xlim(max(0, frame-60), frame)
    ax.figure.canvas.draw()

# アニメーションの作成
ani = animation.FuncAnimation(fig, update_graph, interval=500)

root = tk.Tk()
root.title("Top 5 CPU usage processes")

canvas = plt.gcf().canvas
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill='both', expand=True)

plt.show()

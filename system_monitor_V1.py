#!/usr/bin/env python3

"""
 by frank38
 V. 1.0
"""
import tkinter as tk
import tkinter.ttk as ttk
import sys
import shutil
import time
import subprocess
from collections import deque
import psutil

# window width and height
app_width = 1150
app_height = 850
# font size
font_size = 18
# background color
dia_color = "gray70"
# 
line_width = 2

# loop interval
LOOP_INTERVAL = 1000
# program argument - integer
if len(sys.argv) > 1:
    if sys.argv[1].isdigit():
        if int(sys.argv[1]) > 0:
            LOOP_INTERVAL = int(sys.argv[1]) * 1000

# number of points in the diagram, one per time defined by LOOP_INTERVAL
deque_size = 30
### CPU LOAD
dcpu = deque('', deque_size)
for i in range(deque_size):
    dcpu.append('0')
### CPU TEMPERATURE
dcpu2 = deque('', deque_size)
for i in range(deque_size):
    dcpu2.append('0')
### CPU FREQUENCIES
dcpuf = deque('', deque_size)
for i in range(deque_size):
    dcpuf.append('0')
### GPU LOAD
dgpu3 = deque('', deque_size)
for i in range(deque_size):
    dgpu3.append('0')
### GPU TEMPERATURE
dgpu4 = deque('', deque_size)
for i in range(deque_size):
    dgpu4.append('0')
### GPU FREQUENCIES
dgpuf = deque('', deque_size)
for i in range(deque_size):
    dgpuf.append('0')
    
###############
class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.pack(fill="both", expand=True)
        self.master.update_idletasks()
        
        self.create_widgets()
        
    def create_widgets(self):
        # font family and size
        self.s = ttk.Style(self.master)
        self.s.configure('.', font=('', font_size))
        #
        # exit
        quit_button = ttk.Button(self, text="Exit", command=quit)
        quit_button.grid(column=0, row=0)
        # pause
        self.pause_btn = ttk.Button(self, text="Pause", command=self.fpause_btn)
        self.pause_btn.grid(column=0, row=0, columnspan=4)
        # 0 pause
        self.p_btn = 1
        #
        # width of canvas
        self.c_width = 750
        # height of canvas
        self.c_height = 150
        ##################### CPU
        ## LOAD
        #
        # TOTAL CPU description label
        total_cpu = ttk.Label(self, text="CPU load")
        total_cpu.grid(column=0, row=2)
        ## label: cpoint
        self.cpl = tk.StringVar()
        self.cpl.set("0")
        cpoint_label = ttk.Label(self, textvariable=self.cpl, width=5, anchor="e", relief="sunken")
        cpoint_label.grid(column=1, row=2)
        #
        self.cb1_var = tk.IntVar()
        self.cb1 = ttk.Checkbutton(self, text="On/Off", variable=self.cb1_var)
        # 1 is selected
        self.cb1_var.set(1)
        self.cb1.grid(column=3, row=2)
        #
        # first canvas: cpu load - all cores
        self.canvas1 = tk.Canvas(self, width=self.c_width, height=self.c_height)
        self.canvas1.configure(bg=dia_color)
        self.canvas1.grid(column=2, row=2, sticky="NE")
        self.master.update_idletasks()
        #
        self.canvas1.bind("<Motion>", lambda event, a=0: self.canvas1Move(event, a))
        #
        self.canvas1.bind("<Enter>", self.canvas1Enter)
        #
        self.canvas1.bind("<Leave>", self.canvas1Leave)
        #
        self.canvas1.create_line(0, self.c_height/2, self.c_width, self.c_height/2, width=1, fill="black")
        ##
        # let to know the mouse position in canvas
        self.x1 = 0
        self.y1 = 0
        # if the mouse is not outside canvas
        self.in_canvas1 = 0
        #
        ## TEMPERATURES
        #
        # description label
        temp_cpu = ttk.Label(self, text="CPU Temp")
        temp_cpu.grid(column=0, row=4)
        ## label: cpoint
        self.cpl2 = tk.StringVar()
        self.cpl2.set("0")
        cpoint_label = ttk.Label(self, textvariable=self.cpl2, width=5, anchor="e", relief="sunken")
        cpoint_label.grid(column=1, row=4)
        #
        #
        self.cb2_var = tk.IntVar()
        self.cb2 = ttk.Checkbutton(self, text="On/Off", variable=self.cb2_var)
        # 1 selected - 0  deselected
        self.cb2_var.set(0)
        self.cb2.grid(column=3, row=4)
        #
        # second canvas: temperature
        self.canvas2 = tk.Canvas(self, width=self.c_width, height=self.c_height)
        self.canvas2.configure(bg=dia_color)
        self.canvas2.grid(column=2, row=4, sticky="NE")
        self.master.update_idletasks()
        # 
        self.canvas2.bind("<Motion>", lambda event, a=1:self.canvas1Move(event,a))
        # 
        self.canvas2.bind("<Enter>", self.canvas1Enter)
        # 
        self.canvas2.bind("<Leave>", self.canvas1Leave)
        #
        self.canvas2.create_line(0, self.c_height/2, self.c_width, self.c_height/2, width=1, fill="black")
        ## FREQUENCIES
        # frame
        self.freq_frame = ttk.Frame(self)
        #
        self.freq_frame.grid(column=0, row=6, columnspan=4, sticky="wens")
        # label
        core_real_lbl = ttk.Label(self.freq_frame, text="Cpu frequencies", anchor="center")
        core_real_lbl.grid(column=0, row=0, columnspan=4, sticky="wens")
        #
        #
        self.cbf_var = tk.IntVar()
        self.cbf = ttk.Checkbutton(self.freq_frame, text="On/Off", variable=self.cbf_var, command=self.fcbf)
        # 1 selected
        self.cbf_var.set(0)
        #
        core_real = psutil.cpu_count(logical=False)
        # labels: number of row
        num_row = int(core_real/5)
        if core_real%5:
            num_row += 1
        #
        self.cbf.grid(column=4, row=1, rowspan=num_row)
        # list of StringVar of label: frequencies
        self.freq_list = []
        # label list
        self.freq_label = []
        #
        # fill the two lists above
        for ii in range(core_real):
            self.freq_var = tk.StringVar()
            self.freq_var.set("0")
            self.freq_list.append(self.freq_var)
            self.freq_lbl = ttk.Label(self.freq_frame, textvariable=self.freq_var)
            self.freq_label.append(self.freq_lbl)
        #
        ii = 0
        # 
        for rrow in range(num_row):
            for ccolumn in range(4):
                # only real core
                if ii == core_real:
                    break
                #
                self.freq_label[ii].grid(column=ccolumn, row=rrow+1)
                self.freq_frame.columnconfigure(ccolumn, weight = 1)
                ii += 1
        #
        ######################## GPU Nvidia
        ## LOAD
        #
        # description label
        temp_gpu = ttk.Label(self, text="GPU Load")
        temp_gpu.grid(column=0, row=8)
        ## label: cpoint
        self.cpl3 = tk.StringVar()
        self.cpl3.set("0")
        gtemp_label = ttk.Label(self, textvariable=self.cpl3, width=5, anchor="e", relief="sunken")
        gtemp_label.grid(column=1, row=8)
        #
        ## third canvas: gpu load
        self.canvas3 = tk.Canvas(self, width=self.c_width, height=self.c_height)
        self.canvas3.configure(bg=dia_color)
        self.canvas3.grid(column=2, row=8, sticky="NE")
        self.master.update_idletasks()
        # 
        self.canvas3.bind("<Motion>", lambda event, a=3:self.canvas1Move(event,a))
        # 
        self.canvas3.bind("<Enter>", self.canvas1Enter)
        # 
        self.canvas3.bind("<Leave>", self.canvas1Leave)
        #
        # checkbutton
        self.cb3_var = tk.IntVar()
        self.cb3 = ttk.Checkbutton(self, text="On/Off", variable=self.cb3_var, command=self.fcb3)
        # 1 selected - 0 deselected
        self.cb3_var.set(0)
        self.cb3.grid(column=3, row=8)
        # 
        self.canvas3.create_line(0, self.c_height/2, self.c_width, self.c_height/2, width=1, fill="black")
        ## TEMPERATURE
        #
        # description label
        temp_gpu = ttk.Label(self, text="GPU Temp")
        temp_gpu.grid(column=0, row=9)
        ## label: cpoint
        self.cpl4 = tk.StringVar()
        self.cpl4.set("0")
        gtemp_label = ttk.Label(self, textvariable=self.cpl4, width=5, anchor="e", relief="sunken")
        gtemp_label.grid(column=1, row=9)
        #
        ## fourth canvas: gpu temperature
        self.canvas4 = tk.Canvas(self, width=self.c_width, height=self.c_height)
        self.canvas4.configure(bg=dia_color)
        self.canvas4.grid(column=2, row=9, sticky="NE")
        self.master.update_idletasks()
        # 
        self.canvas4.bind("<Motion>", lambda event, a=4:self.canvas1Move(event,a))
        # 
        self.canvas4.bind("<Enter>", self.canvas1Enter)
        # 
        self.canvas4.bind("<Leave>", self.canvas1Leave)
        #
        # checkbutton
        self.cb4_var = tk.IntVar()
        self.cb4 = ttk.Checkbutton(self, text="On/Off", variable=self.cb4_var)
        # 1 selected - 0 deselected
        self.cb4_var.set(0)
        self.cb4.grid(column=3, row=9)
        # 
        self.canvas4.create_line(0, self.c_height/2, self.c_width, self.c_height/2, width=1, fill="black")
        #
        # if nvidia-smi doesn't exist
        if not shutil.which("nvidia-smi"):
            self.cb3.configure(state="disabled")
            self.cb4.configure(state="disabled")
        ## FREQUENCY
        # frame
        self.gfreq_frame = ttk.Frame(self)
        #
        self.gfreq_frame.grid(column=0, row=10, columnspan=4, sticky="wens")
        # label
        gpu_lbl = ttk.Label(self.gfreq_frame, text="Gpu frequency", anchor="center")
        gpu_lbl.grid(column=0, row=0, columnspan=4, sticky="wens")
        #
        # checkbox
        self.gbf_var = tk.IntVar()
        self.gbf = ttk.Checkbutton(self.gfreq_frame, text="On/Off", variable=self.gbf_var, state="disabled", command=self.fgbf)
        self.gbf.grid(column=5, row=1)
        # 1 selected
        self.gbf_var.set(0)
        #
        # label: frequency
        self.gb1_var = tk.StringVar()
        self.gb1_var.set("0")
        #
        for ccolumn in range(4):
            self.gfreq_frame.columnconfigure(ccolumn, weight = 1)
        #
        self.gb1_lbl = ttk.Label(self.gfreq_frame, textvariable=self.gb1_var)
        self.gb1_lbl.grid(column=0, row=1, columnspan=4)
        #
        ########################
        # list: coordinate x for each point
        self.x_point = []
        #
        ii = 0
        # 
        for i in range(deque_size):
            x_space = (self.c_width/(deque_size-1))*ii
            self.x_point.append(x_space)
            ii += 1
        #
        self.pop_deque()

    # gpu checkboxs: toggle
    def fcb3(self):
        if self.cb3_var.get():
            self.gbf.configure(state="enabled")
        else:
            self.gbf_var.set(0)
            self.gbf.configure(state="disabled")
        
    def fcbf(self):
        if self.cbf_var.get():
            self.pop_freq()
    
    def fgbf(self):
        if self.gbf_var.get():
            self.pop_gfreq()
    
    def pop_freq(self):
        time.sleep(0.1)
        # frequencies
        if self.cbf_var.get():
            if self.p_btn:
                cpu_freq = psutil.cpu_freq(percpu=True)
                dcpuf.append(cpu_freq)

                self.master.after(LOOP_INTERVAL, self.pop_freq)
    
    def pop_gfreq(self):
        # 
        time.sleep(0.1)
        # frequencies
        if self.gbf_var.get():
            if self.p_btn:
                gpu_freq = str(subprocess.check_output("nvidia-smi --query-gpu=clocks.gr --format=csv,noheader -i 0", shell=True).decode().replace("MHz", "").strip())
                dgpuf.append(gpu_freq)
                #
                self.master.after(LOOP_INTERVAL, self.pop_gfreq)
    
    def canvas1Enter(self, event):
        self.in_canvas1 = 1

    def canvas1Leave(self, event):
        self.in_canvas = 0
        self.cpl.set("0")
        self.cpl2.set("0")
        for item in self.freq_list:
            item.set("0")
        self.cpl3.set("0")
        self.cpl4.set("0")
        self.gb1_var.set("0")

    def canvas1Move(self, event, n):
        #
        time.sleep(0.1)
        #
        self.x1 = event.x
        self.y1 = event.y
        # if 0 return
        if self.x1 == 0 or self.y1 == 0:
            return
        #
        ### 
        width_frame = self.c_width/deque_size
        c_point = int(event.x/width_frame)
        if event.x > (width_frame*c_point)+(width_frame/2):
            c_point = c_point+1
        #
        # CPU LOAD
        if n == 0:
            if self.cb1_var.get():
                if c_point == deque_size:
                    self.cpl.set(str(self.last_cpu_pc))
                else:
                    self.cpl.set(str(dcpu[c_point]))
                    #
                    if self.cbf_var.get():
                        # freq_list
                        for item in self.freq_list:
                            item_idx = self.freq_list.index(item)
                            try:
                                item.set(str(dcpuf[c_point][item_idx].current))
                            except:
                                item.set("0")
        # CPU TEMPERATURES
        elif n == 1:
            if self.cb2_var.get():
                if c_point == deque_size:
                    self.cpl2.set(str(self.last_cpu_pc2))
                else:
                    self.cpl2.set(str(dcpu2[c_point]))
        # GPU LOAD
        elif n == 3:
            if self.cb3_var.get():
                if c_point == deque_size:
                    self.cpl3.set(str(self.last_gpu_pc3))
                else:
                    self.cpl3.set(str(dgpu3[c_point]))
                    if self.gbf_var.get():
                        self.gb1_var.set(dgpuf[c_point])
        # GPU TEMP
        elif n == 4:
            if self.cb4_var.get():
                if c_point == deque_size:
                    self.cpl4.set(str(self.last_gpu_pc4))
                else:
                    self.cpl4.set(str(dgpu4[c_point]))

    # pause button
    def fpause_btn(self):
        self.p_btn = not self.p_btn
        if self.p_btn:
            self.pause_btn.configure(text="Pause")
            self.pop_deque()
        else:
            self.pause_btn.configure(text="Paused")

    def fpop_deque(self):
        ########### CPU LOAD
        self.canvas1.delete("line")
        # 
        if self.cb1_var.get():
            list_point = []
            #
            ii = 0
            for item in dcpu:
                line_h = (100-float(item))*self.c_height/100
                # 
                list_point.append(line_h)

                ii += 1

            list_line = []
            for x,y in zip(self.x_point, list_point):
                list_line.append(x)
                list_line.append(y)

            self.canvas1.create_line(list_line, width=line_width, fill="red", smooth=True, tags=("line",))
        #
        ############# CPU TEMPERATURE
        self.canvas2.delete("line")
        if self.cb2_var.get():
            list_point2 = []
            
            ii = 0
            for item in dcpu2:
                line_h = (100-float(item))*self.c_height/100
                # 
                list_point2.append(line_h)
                
                ii += 1
            #
            list_line = []
            for x,y in zip(self.x_point, list_point2):
                list_line.append(x)
                list_line.append(y)

            self.canvas2.create_line(list_line, width=line_width, fill="red", smooth=True, tags=("line",))
            #
        ############# GPU LOAD
        self.canvas3.delete("line")
        #
        if self.cb3_var.get():
            list_point = []
            #
            ii = 0
            for item in dgpu3:
                line_h = (100-float(item))*self.c_height/100
                # 
                list_point.append(line_h)

                ii += 1

            list_line = []
            for x,y in zip(self.x_point, list_point):
                list_line.append(x)
                list_line.append(y)

            self.canvas3.create_line(list_line, width=line_width, fill="red", smooth=True, tags=("line",))
        #
        ############# GPU TEMPERATURE
        self.canvas4.delete("line")
        #
        if self.cb4_var.get():
            list_point = []
            #
            ii = 0
            for item in dgpu4:
                line_h = (100-float(item))*self.c_height/100
                # 
                list_point.append(line_h)

                ii += 1

            list_line = []
            for x,y in zip(self.x_point, list_point):
                list_line.append(x)
                list_line.append(y)

            self.canvas4.create_line(list_line, width=line_width, fill="red", smooth=True, tags=("line",))
        #

    def pop_deque(self):
        if self.p_btn:
            #
            self.fpop_deque()
            ######### cpu load
            if self.cb1_var.get():
                cpu_pc = psutil.cpu_percent()
                dcpu.append(cpu_pc)
            
            self.last_cpu_pc = psutil.cpu_percent()
            
            ########### cpu temperature
            if self.cb2_var.get():
                core_temp = psutil.sensors_temperatures()['coretemp'][0].current
                dcpu2.append(core_temp)
            
            self.last_cpu_pc2 = psutil.sensors_temperatures()['coretemp'][0].current
            
            ########### gpu load
            if self.cb3_var.get():
                gpu_load = str(subprocess.check_output("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader -i 0", shell=True).decode().replace('%', '').strip())
                dgpu3.append(gpu_load)
                #
            self.last_gpu_pc3 = str(subprocess.check_output("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader -i 0", shell=True).decode().replace('%', '').strip())
            
            ########### gpu temperature
            if self.cb4_var.get():
                gpu_temp = str(subprocess.check_output("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader -i 0", shell=True).decode().replace('%', '').strip())
                dgpu4.append(gpu_temp)
                #
            self.last_gpu_pc4 = str(subprocess.check_output("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader -i 0", shell=True).decode().replace('%', '').strip())
            
            #
            self.master.after(LOOP_INTERVAL, lambda:self.pop_deque())
        else:
            #
            self.fpop_deque()
            # cpu load 
            self.last_cpu_pc = psutil.cpu_percent()
            # cpu temperature
            self.last_cpu_pc2 = psutil.sensors_temperatures()['coretemp'][0].current
            # gpu load
            self.last_gpu_pc3 = str(subprocess.check_output("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader -i 0", shell=True).decode().replace('%', '').strip())
            # gpu temperatue
            self.last_gpu_pc4 = str(subprocess.check_output("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader -i 0", shell=True).decode().replace('%', '').strip())
            
            return

###########
def main():
    root = tk.Tk()
    root.title("System Monitor")
    root.update_idletasks()
    
    width = app_width
    height = app_height
    root.geometry('{}x{}'.format(width, height))
    
    # style
    s = ttk.Style()
    s.theme_use("clam")
    
    app = Application(master=root)
    app.mainloop()
    
if __name__ == "__main__":
    main()

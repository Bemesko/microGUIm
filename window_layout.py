from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import ioh_backend
import constants
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
matplotlib.use("TkAgg")


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        self.last_frame = PageSystemInfo

        self.mas = ioh_backend.MultiagentSystem()

        tk.Tk.__init__(self, *args, **kwargs)

        self.setup_fixed_items()

        self.setup_frame_container()

        self.update_mas_data(self.mas)

    def setup_fixed_items(self):
        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.grid(row=0, column=0, sticky="nws", padx=5, pady=5)

        self.button_system_info = tk.Button(
            self.frame_buttons, text="System Info", command=lambda: self.show_frame(PageSystemInfo))
        self.button_system_info.grid(sticky="wen")

        self.button_graph_next_consumption = tk.Button(
            self.frame_buttons, text="Graph", command=lambda: self.show_frame(PageGraphNextConsumption))
        self.button_graph_next_consumption.grid(sticky="we")

        self.button_info = tk.Button(
            self.frame_buttons, text="Info", command=lambda: self.show_frame(PageAgentInfo))
        self.button_info.grid(sticky="we")

        self.frame_middle = tk.Frame(self)
        self.frame_middle.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.frame_logs = tk.Frame(
            self, highlightbackground="black", highlightthickness=1)
        self.frame_logs.grid(row=0, column=2, sticky="nes")

        self.label = tk.Label(self.frame_logs, text="SYSTEM LOGS")
        self.label.grid(sticky="w")

    def setup_frame_container(self):

        self.frames = {}

        # PageAgentMainWindow, PageEnergyTransactions, PageOptimization, PageOverview, PagePredictions, PageEnergyData, PageGraph,
        for new_frame in (PageSystemInfo, PageGraphNextConsumption, PageAgentInfo):

            frame = new_frame(self.frame_middle, self, self.mas)

            self.frames[new_frame] = frame

            frame.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)

        self.show_frame(PageSystemInfo)

    def show_frame(self, desired_frame):
        self.last_frame.is_visible = False
        frame = self.frames[desired_frame]
        frame.is_visible = True
        frame.tkraise()
        self.last_frame = desired_frame

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            try:
                self.mas.shutdown()
            except:
                pass
            finally:
                self.destroy()

    def update_mas_data(self, multiagent_system):
        try:
            multiagent_system.get_agent_attributes()
        except:
            pass
        finally:
            self.after(1000, lambda: self.update_mas_data(multiagent_system))


class PageSystemInfo(tk.Frame):
    def __init__(self, parent, controller, multiagent_system, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.multiagent_system = multiagent_system
        self.is_visible = False

        self.label_system_active = tk.Label(
            self, text="System is ON")
        self.label_system_active.pack()

        self.button_start_script = tk.Button(
            self, text="Start Script", command=self.run_mas_script)
        self.button_start_script.pack(fill=tk.X)

        self.button_kill_server = tk.Button(
            self, text="Kill Server", command=self.mas_shutdown)
        self.button_kill_server.pack(fill=tk.X)

        self.label_active_time = tk.Label(
            self, text="Active for 00:00:00")
        self.label_active_time.pack()

        self.update_labels()

    def update_labels(self):
        if(self.is_visible):
            try:
                agents = self.multiagent_system.nameserver.agents()
                system_is_on = "ON" if len(agents) > 0 else "OFF"
                self.label_system_active.configure(
                    text=f"System is {system_is_on}")
            except:
                pass
        self.after(500, self.update_labels)

    def run_mas_script(self):
        try:
            self.multiagent_system.run_auction_script()
        except:
            pass

    def mas_shutdown(self):
        try:
            self.multiagent_system.shutdown()
        except:
            pass


class PageGraphNextConsumption(tk.Frame):
    def __init__(self, parent, controller, multiagent_system, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.multiagent_system = multiagent_system
        self.is_visible = False

        # the figure that will contain the plot
        self.graph_figure = Figure(figsize=(10, 7),
                                   dpi=100)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.graph_figure,
                                        master=self)
        self.canvas.draw()

        # creating the Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas,
                                            self)
        self.toolbar.update()

        # placing the toolbar on the Tkinter window
        self.canvas.get_tk_widget().pack()

        self.update_graph()

    def update_graph(self):
        if(self.is_visible):
            self.graph_figure.clear()

            # adding the subplot
            self.plot1 = self.graph_figure.add_subplot()

            agent_i = 0
            # plotting the graph
            try:
                for attributes in self.multiagent_system.agent_attributes[constants.NEXT_ENERGY_CONSUMPTION]:
                    self.plot1.plot(attributes, label=f"Prosumer{agent_i}")
                    self.plot1.legend(
                        loc='upper left', borderaxespad=0.)
                    self.plot1.set_title("Next Energy Consumption")
                    self.plot1.set_xlabel("System Cycles")
                    self.plot1.set_ylabel("Predicted Energy Consumption (Wh)")
                    agent_i += 1
            except:
                pass

            self.canvas.draw()

        self.after(500, self.update_graph)


class PageAgentInfo(tk.Frame):
    def __init__(self, parent, controller, multiagent_system):
        tk.Frame.__init__(self, parent)

        self.is_visible = False

        self.labels_active_agents = []

        self.label_title_agents = tk.Label(self, text="SYSTEM AGENTS")
        self.label_title_agents.pack()

        self.display_active_agents(multiagent_system)

    def display_active_agents(self, multiagent_system):
        if(self.is_visible):
            for agent in self.labels_active_agents:
                agent.destroy()

            try:
                self.active_agents = multiagent_system.nameserver.agents()

                for agent in self.active_agents:
                    new_active_agent = ttk.Label(
                        self, text=f"(ON) {agent}: WAITING")
                    self.labels_active_agents.append(new_active_agent)
                    new_active_agent.pack(fill=tk.X)
            except:
                return
        self.after(500, lambda: self.display_active_agents(multiagent_system))


if __name__ == "__main__":
    app = tkinterApp()
    app.title("Agent Monitoring System")
    app.protocol("WM_DELETE_WINDOW", app.on_closing)

    app.mainloop()

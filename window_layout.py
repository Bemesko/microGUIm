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
            self.frame_buttons, text="Next Consumption", command=lambda: self.show_frame(PageGraphNextConsumption))
        self.button_graph_next_consumption.grid(sticky="we")

        self.button_graph_next_generation = tk.Button(
            self.frame_buttons, text="Next Generation", command=lambda: self.show_frame(PageGraphNextGeneration))
        self.button_graph_next_generation.grid(sticky="we")

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

        for new_frame in (PageSystemInfo, PageGraphNextConsumption, PageGraphNextGeneration, PageAgentInfo):

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
        self.after(1000, lambda: self.update_mas_data(multiagent_system))


class PageSystemInfo(tk.Frame):
    def __init__(self, parent, controller, multiagent_system, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.mas = multiagent_system
        self.is_visible = False

        self.label_system_active = tk.Label(
            self, text="System is ON")
        self.label_system_active.pack()

        self.button_start_script = tk.Button(
            self, text="Start Script", command=self.run_mas_script)
        self.button_start_script.pack(fill=tk.X)

        # O botão abaixo causa uns erros muito bizarros e não vou mexer nele por enquanto
        # self.button_kill_server = tk.Button(
        #     self, text="Kill Server", command=lambda: self.mas_shutdown(multiagent_system))
        # self.button_kill_server.pack(fill=tk.X)

        self.label_active_time = tk.Label(
            self, text="Active for 00:00:00")
        self.label_active_time.pack()

        self.update_labels()

    def update_labels(self):
        if(self.is_visible):
            try:
                agents = self.mas.nameserver.agents()
                system_is_on = "ON" if len(agents) > 0 else "OFF"
                self.label_system_active.configure(
                    text=f"System is {system_is_on}")
            except:
                pass
        self.after(500, self.update_labels)

    def run_mas_script(self):
        try:
            self.mas.run_auction_script()
        except:
            pass

    def mas_shutdown(self, multiagent_system):
        try:
            self.mas.shutdown()
        except:
            pass


class PageGraph(tk.Frame):
    def __init__(self, parent, controller, multiagent_system, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.mas = multiagent_system
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

    def update_graph(self, attribute, title, xlabel, ylabel):
        if(self.is_visible):
            self.graph_figure.clear()

            # adding the subplot
            self.plot1 = self.graph_figure.add_subplot()

            agent_i = 0
            try:
                for attributes in self.mas.agent_attributes[attribute]:
                    self.plot1.plot(attributes, label=f"Prosumer{agent_i}")
                    self.plot1.legend(
                        loc='upper left', borderaxespad=0.)
                    self.plot1.set_title(title)
                    self.plot1.set_xlabel(xlabel)
                    self.plot1.set_ylabel(ylabel)
                    agent_i += 1
            except:
                pass

            self.canvas.draw()

        self.after(500, lambda: self.update_graph(
            attribute, title, xlabel, ylabel))


class PageGraphNextConsumption(PageGraph):
    def __init__(self, parent, controller, multiagent_system, *args, **kwargs):
        PageGraph.__init__(self, parent, controller,
                           multiagent_system, *args, **kwargs)
        self.update_graph(constants.NEXT_ENERGY_CONSUMPTION, "Next Energy Consumption",
                          "System Cycles", "Predicted Energy Consumption (W)")

    def update_graph(self, attribute, title, xlabel, ylabel):
        PageGraph.update_graph(self, constants.NEXT_ENERGY_CONSUMPTION,
                               "Next Energy Consumption", "System Cycles", "Predicted Energy Consumption (W)")


class PageGraphNextGeneration(PageGraph):
    def __init__(self, parent, controller, multiagent_system, *args, **kwargs):
        PageGraph.__init__(self, parent, controller,
                           multiagent_system, *args, **kwargs)
        self.update_graph(constants.NEXT_ENERGY_GENERATION, "Next Energy Generation",
                          "System Cycles", "Predicted Energy Generation (W)")

    def update_graph(self, attribute, title, xlabel, ylabel):
        PageGraph.update_graph(self, constants.NEXT_ENERGY_GENERATION,
                               "Next Energy Generation", "System Cycles", "Predicted Energy Generation (W)")


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

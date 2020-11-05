import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import ioh_backend


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        self.mas = ioh_backend.MultiagentSystem()

        tk.Tk.__init__(self, *args, **kwargs)

        self.setup_top_bar()

        self.setup_frame_container()

    def setup_top_bar(self):
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side="top", fill="x")

        self.button_overview = tk.Button(self.top_frame, text="Energy Info",
                                         command=lambda: self.show_frame(PageOverview))
        self.button_overview.pack(side="left")

        self.button_agent_window = tk.Button(self.top_frame, text="Agent Info",
                                             command=lambda: self.show_frame(PageAgentMainWindow))
        self.button_agent_window.pack(side="left")

        self.button_start_agents = tk.Button(
            self.top_frame, text="Start Agents", command=self.mas.run_auction_script)
        self.button_start_agents.pack(side="left")

        self.button_stop_nameserver = tk.Button(
            self.top_frame, text="Stop Nameserver", command=self.mas.shutdown)
        self.button_stop_nameserver.pack(side="left")

    def setup_frame_container(self):
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for new_frame in (PageAgentMainWindow, PageEnergyTransactions, PageOptimization, PageOverview, PagePredictions, PageEnergyData):

            frame = new_frame(self.container, self, self.mas)

            self.frames[new_frame] = frame

            frame.grid(row=1, column=0, sticky="nswe", padx=15, pady=15)

        self.show_frame(PageAgentMainWindow)

    def show_frame(self, desired_frame):
        frame = self.frames[desired_frame]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            try:
                self.mas.shutdown()
            except:
                pass
            finally:
                self.destroy()


""" General Info 
    Frames belonging to the General Info section are set up below:
"""


class PageOverview(tk.Frame):

    def __init__(self, parent, controller, multiagent_system):
        tk.Frame.__init__(self, parent)

        """Left Frame"""

        self.frame_left = tk.Frame(self)
        self.frame_left.grid(row=0, column=0, sticky="nsw")

        self.button_overview = tk.Button(
            self.frame_left, text="Overview", command=lambda: controller.show_frame(PageOverview), bg="#256697")
        self.button_overview.pack()

        self.button_predictions = tk.Button(
            self.frame_left, text="Predictions", command=lambda: controller.show_frame(PagePredictions))
        self.button_predictions.pack()

        self.button_energy_transactions = tk.Button(
            self.frame_left, text="Energy Transactions", command=lambda: controller.show_frame(PageEnergyTransactions))
        self.button_energy_transactions.pack()

        self.button_energy_data = tk.Button(
            self.frame_left, text="Transactive Energy Data", command=lambda: controller.show_frame(PageEnergyData))
        self.button_energy_data.pack()

        """Middle Frame"""

        self.frame_middle = tk.Frame(self)
        self.frame_middle.grid(row=0, column=1, sticky="ns")

        # Currently active agents
        self.title_active_agents = ttk.Label(
            self.frame_middle, text="CURRENTLY ACTIVE AGENTS")
        self.title_active_agents.pack()

        # TODO fazer ser dinâmico
        self.active_agents = multiagent_system.nameserver.agents()

        for agent in self.active_agents:
            new_active_agent = ttk.Label(
                self.frame_middle, text=agent)
            new_active_agent.pack()

        # Current messages
        self.title_current_messages = ttk.Label(
            self.frame_middle, text="\nCURRENT MESSAGES")
        self.title_current_messages.pack()

        # TODO Mock para teste; Retirar depois
        self.current_messages = [1, 3, 4, 2]

        self.frame_messages = tk.Frame(self.frame_middle)
        self.frame_messages.pack()

        for message in self.current_messages:
            new_message = ttk.Label(self.frame_messages, text=message)
            new_message.grid(
                row=0, column=self.current_messages.index(message))

        """Right Frame"""

        self.frame_right = tk.Frame(self)
        self.frame_right.grid(row=0, column=2, sticky="nes")

        # Update Messages
        self.button_update_messages = tk.Button(
            self.frame_right, text="Update Messages", command=self.update_messages)
        self.button_update_messages.pack()

    def update_messages(self):
        print("Messages updated!")


class PageEnergyTransactions(tk.Frame):
    def __init__(self, parent, controller, multiagent_system):
        tk.Frame.__init__(self, parent)

        """Left Frame"""

        self.frame_left = tk.Frame(self)
        self.frame_left.grid(row=0, column=0)

        self.button_overview = tk.Button(
            self.frame_left, text="Overview", command=lambda: controller.show_frame(PageOverview))
        self.button_overview.pack()

        self.button_predictions = tk.Button(
            self.frame_left, text="Predictions", command=lambda: controller.show_frame(PagePredictions))
        self.button_predictions.pack()

        self.button_energy_transactions = tk.Button(
            self.frame_left, text="Energy Transactions", command=lambda: controller.show_frame(PageEnergyTransactions), bg="#256697")
        self.button_energy_transactions.pack()

        self.button_energy_data = tk.Button(
            self.frame_left, text="Transactive Energy Data", command=lambda: controller.show_frame(PageEnergyData))
        self.button_energy_data.pack()

        """Right Frame"""
        self.frame_right = tk.Frame(self)
        self.frame_right.grid(row=0, column=1)
        self.title_energy_transactions = tk.Label(
            self.frame_right, text="Energy Transactions")
        self.title_energy_transactions.pack()

        self.frame_info = tk.Frame(self.frame_right)
        self.frame_info.pack()
        # Week
        self.subtitle_week = tk.Label(self.frame_info, text="Week")
        self.subtitle_week.grid(row=0)

        self.text_week_to_grid = tk.Label(self.frame_info, text="To Grid: --W")
        self.text_week_to_grid.grid(row=1, column=0)
        self.text_week_to_energy = tk.Label(
            self.frame_info, text="To Transacted Energy: --W")
        self.text_week_to_energy.grid(row=1, column=1)
        self.text_week_from_grid = tk.Label(
            self.frame_info, text="From Grid: --W")
        self.text_week_from_grid.grid(row=2, column=0)
        self.text_week_from_energy = tk.Label(
            self.frame_info, text="From Transacted Energy: --W")
        self.text_week_from_energy.grid(row=2, column=1)
        self.text_week_grid_balance = tk.Label(
            self.frame_info, text="Balance (Grid): --W")
        self.text_week_grid_balance.grid(row=3, column=0)
        self.text_week_energy_balance = tk.Label(
            self.frame_info, text="Balance (Energy): --W")
        self.text_week_energy_balance.grid(row=3, column=1)

        # Month
        self.subtitle_month = tk.Label(self.frame_info, text="Month")
        self.subtitle_month.grid(row=4)

        self.text_month_to_grid = tk.Label(
            self.frame_info, text="To Grid: --W")
        self.text_month_to_grid.grid(row=5, column=0)
        self.text_month_to_energy = tk.Label(
            self.frame_info, text="To Transacted Energy: --W")
        self.text_month_to_energy.grid(row=5, column=1)
        self.text_month_from_grid = tk.Label(
            self.frame_info, text="From Grid: --W")
        self.text_month_from_grid.grid(row=6, column=0)
        self.text_month_from_energy = tk.Label(
            self.frame_info, text="From Transacted Energy: --W")
        self.text_month_from_energy.grid(row=6, column=1)
        self.text_month_grid_balance = tk.Label(
            self.frame_info, text="Balance (Grid): --W")
        self.text_month_grid_balance.grid(row=7, column=0)
        self.text_month_energy_balance = tk.Label(
            self.frame_info, text="Balance (Energy): --W")
        self.text_month_energy_balance.grid(row=7, column=1)


class PageEnergyData(tk.Frame):
    def __init__(self, parent, controller, multiagent_system):
        tk.Frame.__init__(self, parent)

        """Left Frame"""

        self.frame_left = tk.Frame(self)
        self.frame_left.grid(row=0, column=0)

        self.button_overview = tk.Button(
            self.frame_left, text="Overview", command=lambda: controller.show_frame(PageOverview))
        self.button_overview.pack()

        self.button_predictions = tk.Button(
            self.frame_left, text="Predictions", command=lambda: controller.show_frame(PagePredictions))
        self.button_predictions.pack()

        self.button_energy_transactions = tk.Button(
            self.frame_left, text="Energy Transactions", command=lambda: controller.show_frame(PageEnergyTransactions))
        self.button_energy_transactions.pack()

        self.button_energy_data = tk.Button(
            self.frame_left, text="Transactive Energy Data", command=lambda: controller.show_frame(PageEnergyData), bg="#256697")
        self.button_energy_data.pack()

        """Right Frame"""
        self.frame_right = tk.Frame(self)
        self.frame_right.grid(row=0, column=1)

        self.title_energy_data = tk.Label(
            self.frame_right, text="Transactive Energy Data")
        self.title_energy_data.pack()

        self.frame_info = tk.Frame(self.frame_right)
        self.frame_info.pack()

        # Next Hour
        self.subtitle_next_hour = tk.Label(self.frame_info, text="Next Hour")
        self.subtitle_next_hour.grid(row=0)

        self.text_to_buy_next = tk.Label(self.frame_info, text="To Buy: --W")
        self.text_to_buy_next.grid(row=1, column=0)
        self.text_to_sell_next = tk.Label(self.frame_info, text="To Sell: --W")
        self.text_to_sell_next.grid(row=1, column=1)
        self.text_bought_next = tk.Label(self.frame_info, text="Bought: --W")
        self.text_bought_next.grid(row=2, column=0)
        self.text_sold_next = tk.Label(self.frame_info, text="Sold: --W")
        self.text_sold_next.grid(row=2, column=1)

        # Current Hour
        self.subtitle_current_hour = tk.Label(
            self.frame_info, text="Current Hour")
        self.subtitle_current_hour.grid(row=3)

        self.text_to_buy_current = tk.Label(
            self.frame_info, text="To Buy: --W")
        self.text_to_buy_current.grid(row=4, column=0)
        self.text_to_sell_current = tk.Label(
            self.frame_info, text="To Sell: --W")
        self.text_to_sell_current.grid(row=4, column=1)
        self.text_bought_current = tk.Label(
            self.frame_info, text="Bought: --W")
        self.text_bought_current.grid(row=5, column=0)
        self.text_sold_current = tk.Label(self.frame_info, text="Sold: --W")
        self.text_sold_current.grid(row=5, column=1)

        # Last Hour
        self.subtitle_last_hour = tk.Label(
            self.frame_info, text="Last Hour")
        self.subtitle_last_hour.grid(row=6)

        self.text_to_buy_last = tk.Label(
            self.frame_info, text="To Buy: --W")
        self.text_to_buy_last.grid(row=7, column=0)
        self.text_to_sell_last = tk.Label(
            self.frame_info, text="To Sell: --W")
        self.text_to_sell_last.grid(row=7, column=1)
        self.text_bought_last = tk.Label(
            self.frame_info, text="Bought: --W")
        self.text_bought_last.grid(row=8, column=0)
        self.text_sold_last = tk.Label(self.frame_info, text="Sold: --W")
        self.text_sold_last.grid(row=8, column=1)


class PagePredictions(tk.Frame):
    def __init__(self, parent, controller, multiagent_system):
        tk.Frame.__init__(self, parent)

        """Left Frame"""

        self.frame_left = tk.Frame(self)
        self.frame_left.grid(row=0, column=0)

        self.button_overview = tk.Button(
            self.frame_left, text="Overview", command=lambda: controller.show_frame(PageOverview))
        self.button_overview.pack()

        self.button_predictions = tk.Button(
            self.frame_left, text="Predictions", command=lambda: controller.show_frame(PagePredictions), bg="#256697")
        self.button_predictions.pack()

        self.button_energy_transactions = tk.Button(
            self.frame_left, text="Energy Transactions", command=lambda: controller.show_frame(PageEnergyTransactions))
        self.button_energy_transactions.pack()

        self.button_energy_data = tk.Button(
            self.frame_left, text="Transactive Energy Data", command=lambda: controller.show_frame(PageEnergyData))
        self.button_energy_data.pack()

        """Right Frame"""
        self.frame_right = tk.Frame(self)
        self.frame_right.grid(row=0, column=1)

        self.title_predictions = tk.Label(
            self.frame_right, text="Predictions")
        self.title_predictions.pack()

        self.frame_info = tk.Frame(self.frame_right)
        self.frame_info.pack()

        # Next 15 Minutes
        self.frame_minutes = tk.Frame(self.frame_info)
        self.frame_minutes.grid(row=0, column=0)

        self.subtitle_minutes = tk.Label(
            self.frame_minutes, text="Next 15 Minutes")
        self.subtitle_minutes.pack()

        self.text_consumption = tk.Label(
            self.frame_minutes, text="Consumption: --W")
        self.text_consumption.pack()
        self.text_error_consumption = tk.Label(
            self.frame_minutes, text="Error: --%")
        self.text_error_consumption.pack()
        self.text_generation = tk.Label(
            self.frame_minutes, text="Generation: --W")
        self.text_generation.pack()
        self.text_error_generation = tk.Label(
            self.frame_minutes, text="Error: --%")
        self.text_error_generation.pack()

        # Next Hour
        self.frame_hour = tk.Frame(self.frame_info)
        self.frame_hour.grid(row=0, column=1)

        self.subtitle_hour = tk.Label(
            self.frame_hour, text="Next Hour")
        self.subtitle_hour.pack()

        self.text_consumption = tk.Label(
            self.frame_hour, text="Consumption: --W")
        self.text_consumption.pack()
        self.text_error_consumption = tk.Label(
            self.frame_hour, text="Error: --%")
        self.text_error_consumption.pack()
        self.text_generation = tk.Label(
            self.frame_hour, text="Generation: --W")
        self.text_generation.pack()
        self.text_error_generation = tk.Label(
            self.frame_hour, text="Error: --%")
        self.text_error_generation.pack()


""" Agent Info 
    Frames belonging to the Agent Info section are set up below:
"""


class PageAgentMainWindow(tk.Frame):
    def __init__(self, parent, controller, multiagent_system):
        tk.Frame.__init__(self, parent)

        """Left Frame"""

        self.frame_left = tk.Frame(self)
        self.frame_left.grid(row=0, column=0)

        self.button_agent_main_window = tk.Button(
            self.frame_left, text="Agent Main Window", command=lambda: controller.show_frame(PageAgentMainWindow), bg="#256697")
        self.button_agent_main_window.pack()

        self.page_button_optimization = tk.Button(
            self.frame_left, text="Optimization", command=lambda: controller.show_frame(PageOptimization))
        self.page_button_optimization.pack()

        """Right Frame"""
        self.frame_right = tk.Frame(self)
        self.frame_right.grid(row=0, column=1)

        self.title_main_window = tk.Label(
            self.frame_right, text="Agent Main Window")
        self.title_main_window.pack()

        self.frame_info = tk.Frame(self.frame_right)
        self.frame_info.pack()

        # Resources
        self.subtitle_resources = tk.Label(self.frame_info, text="Resources")
        self.subtitle_resources.grid(row=0, column=0)

        self.frame_resources = tk.Frame(self.frame_info)
        self.frame_resources.grid(row=1, column=0)

        self.resources = ["Tv", "Lights", "Socket"]

        for resource in self.resources:
            text_resource_name = tk.Label(
                self.frame_resources, text=resource)
            text_resource_name.pack()

            text_resource_consuming = tk.Label(
                self.frame_resources, text="Consuming: --W")
            text_resource_consuming.pack()

            button_toggle_resource = tk.Button(
                self.frame_resources, text="Turn On/Off", command=lambda: print(f"Turned On/Off {resource}"))
            button_toggle_resource.pack()

        # Agent Data
        self.subtitle_agent_data = tk.Label(self.frame_info, text="Agent Data")
        self.subtitle_agent_data.grid(row=0, column=1)

        self.frame_agent_data = tk.Frame(self.frame_info)
        self.frame_agent_data.grid(row=1, column=1)

        self.text_agent_id = tk.Label(
            self.frame_agent_data, text="Agent ID: --")
        self.text_agent_id.pack()
        self.text_agent_id = tk.Label(
            self.frame_agent_data, text="Agent IP Address: --")
        self.text_agent_id.pack()
        self.text_current_consumption = tk.Label(
            self.frame_agent_data, text="Current Total Consumption: --W")
        self.text_current_consumption.pack()
        self.text_currentgeneration = tk.Label(
            self.frame_agent_data, text="Current Total Generation: --W")
        self.text_currentgeneration.pack()
        self.text_flex = tk.Label(self.frame_agent_data, text="Flex: --W")
        self.text_flex.pack()

        self.button_kill_agent = tk.Button(
            self.frame_agent_data, text="Kill Agent", command=lambda: print("Agent Killed!"))
        self.button_kill_agent.pack()


class PageOptimization(tk.Frame):
    def __init__(self, parent, controller, multiagent_system):
        tk.Frame.__init__(self, parent)

        """Left Frame"""

        self.frame_left = tk.Frame(self)
        self.frame_left.grid(row=0, column=0)

        self.button_agent_main_window = tk.Button(
            self.frame_left, text="Agent Main Window", command=lambda: controller.show_frame(PageAgentMainWindow))
        self.button_agent_main_window.pack()

        self.page_button_optimization = tk.Button(
            self.frame_left, text="Optimization", command=lambda: controller.show_frame(PageOptimization), bg="#256697")
        self.page_button_optimization.pack()

        """Right Frame"""
        self.frame_right = tk.Frame(self)
        self.frame_right.grid(row=0, column=1)

        self.title_optimization = tk.Label(
            self.frame_right, text="Optimization")
        self.title_optimization.pack()

        self.frame_optimization = tk.Frame(self.frame_right)
        self.frame_optimization.pack()

        # Activate/Deactivate optimization toggle
        self.button_optimization = tk.Button(
            self.frame_optimization, text="Turn On/Off", command=lambda: print("Optimized"))
        self.button_optimization.grid(row=0, column=1)

        self.text_activate_optimization = tk.Label(
            self.frame_optimization, text="Activate/Deactivate Optimization")
        self.text_activate_optimization.grid(row=0, column=0)

        # Execution Time
        self.text_execution_time = tk.Label(
            self.frame_optimization, text="Execution Time: --s")
        self.text_execution_time.grid(row=1)

        # Reduced Consumption
        self.text_reduced_consumption = tk.Label(
            self.frame_optimization, text="Reduced Consumption: --W")
        self.text_reduced_consumption.grid(row=2)


# Driver Code
if __name__ == "__main__":
    app = tkinterApp()
    app.title("Agent Monitoring System")
    app.geometry("600x400")
    app.protocol("WM_DELETE_WINDOW", app.on_closing)

    app.mainloop()

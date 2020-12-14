from Packages.window_layout import tkinterApp

if __name__ == "__main__":
    app = tkinterApp()
    app.title("µGUIm")
    app.protocol("WM_DELETE_WINDOW", app.on_closing)

    app.mainloop()

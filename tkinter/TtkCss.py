from tkinter import ttk

def apply_ttk_style():
    style = ttk.Style()
    style.theme_use('clam')

    bg_color = "#1a1a1a"

    style.configure("TButton",background=bg_color,foreground="white",focuscolor="none",focusthickness=0, relief="flat")
    style.map("TButton",background=[("active", "#3a3a3a")],foreground=[("active", "white")])

    style.configure("TCheckbutton", background=bg_color, foreground="white")
    style.map("TCheckbutton", foreground=[("active", "white")], background=[("active", bg_color)])

    style.configure("Vertical.TScrollbar", gripcount=0,background="#2a2a2a",troughcolor=bg_color,bordercolor="white",arrowcolor="white",lightcolor=bg_color,darkcolor=bg_color,relief="flat")
    style.map("Vertical.TScrollbar",background=[("active", "#3a3a3a")])

    style.configure("TFrame", background="black", bordercolor="#5a5a5a", darkcolor="#5a5a5a", lightcolor="#5a5a5a", borderwidth=1, relief="solid")

    style.configure("TLabel", background=bg_color, foreground="white")

    style.configure("TEntry", fieldbackground="white", foreground=bg_color)

    style.configure("TCombobox", fieldbackground="white", foreground=bg_color, background="#3a3a3a")
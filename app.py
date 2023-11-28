#!/usr/bin/env python3
import sqlite3
import webbrowser
import tkinter as tk
from tkinter import messagebox, PhotoImage

class ChampionBuildApp:
    def __init__(self, main):
        self.main = main
        main.title("League Build Searcher")
        main.iconphoto(False, PhotoImage(file='./img/logo.png')) 

        self.text_results = tk.Text(main)

        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.results: str = ""
        self.links: list = [["https://mobalytics.gg/lol/champions/XchampionX/build", False], ["https://blitz.gg/lol/champions/XchampionX/build", False], ["https://www.op.gg/champions/XchampionX/build", False], ["https://www.leagueofgraphs.com/champions/builds/XchampionX", True], ["https://champion.gg/champion/XchampionX/build", False], ["https://lolalytics.com/lol/XchampionX/build/", True], ["https://www.counterstats.net/league-of-legends/XchampionX", False], ["https://www.lolvvv.com/champion/XchampionX/build", False], ["https://www.metasrc.com/lol/build/XchampionX", False], ["https://loltheory.gg/lol/champion/XchampionX/build-runes", True], ["https://koreanbuilds.net/champion/XchampionX", False], ["https://europeanbuilds.net/champion/XchampionX", False]]
        self.link_title: list = ["Mobalytics.gg", "Blitz.gg", "OP.GG", "LeagueOfGraphs", "Champion.gg", "lolalytics", "CounterStats.net", "lolvvv", "MetaSrc", "LolTheory.gg", "KoreanBuilds.net", "EuropeanBuilds.net"]
        self.link: list = [self.links[0][0], self.links[0][1]] # default

        self.__window_width: int = 400
        self.__window_height: int = 400
        self.__screen_width: int = main.winfo_screenwidth()
        self.__screen_height: int = main.winfo_screenheight()
        self.__x_coordinate: int = (self.__screen_width - self.__window_width) // 2
        self.__y_coordinate: int = (self.__screen_height - self.__window_height) // 2
        
        main.geometry(f"{self.__window_width}x{self.__window_height}+{self.__x_coordinate}+{self.__y_coordinate}")

        self.tk_vars: list = [tk.IntVar() for _ in range(len(self.links))]
        self.clist: list = [tk.Checkbutton(main, text=self.link_title[i],variable=self.tk_vars[i], onvalue=1, offvalue=0, command=self.print_selection) for i in range(len(self.links))]

        for i, c in enumerate(self.clist):
            c.grid(row=i//2 + 1, column=i%2, sticky='w')

        self.setup_ui()
    
    def setup_ui(self):
        self.link_label = tk.Label(self.main, bg='white', width=20, text=f'{self.link_title[0]} (Default)')
        self.label_data = tk.Label(self.main, text="Enter a Champion:")
        self.entry_data = tk.Entry(self.main)
        self.search_button = tk.Button(self.main, text="search", command=self.open_on_site)
        self.text_results = tk.Text(self.main, height=10, width=50)

        self.link_label.grid(row=0, column=0, columnspan=2)
        self.label_data.grid(row=len(self.links) // 2 + 2, column=0, columnspan=2, pady=10)
        self.entry_data.grid(row=len(self.links) // 2 + 3, column=0, columnspan=2, pady=10)
        self.search_button.grid(row=len(self.links) // 2 + 3, column=1, columnspan=2, pady=10)
        self.text_results.grid(row=len(self.links) // 2 + 4, column=0, columnspan=2, pady=10)

        self.entry_data.bind("<KeyRelease>", self.execute_query)

    def execute_query(self, event=None):
        data: str = self.entry_data.get()
        query: str = "SELECT Champions.nom, Champions.description, Difficulties.difficulty, Roles.role FROM Champions JOIN Roles ON Champions.role = Roles.id JOIN Difficulties ON Champions.difficulty = Difficulties.id WHERE Champions.nom LIKE ?"

        self.cursor.execute(query, (f'{data}%',))
        self.results = self.cursor.fetchall()

        self.text_results.delete(1.0, tk.END)

        if not data:
            return 0

        if self.results:
            for row in self.results:
                self.text_results.insert(tk.END, str(row) + "\n")
        else:
            self.text_results.tag_configure("color_error_tag", foreground="red")
            self.text_results.insert(tk.END, "No matching Champion found.\n", "color_error_tag")

    def print_selection(self):
        for i in range(len(self.tk_vars)):
            if self.tk_vars[i].get() == 1:
                self.link = [self.links[i][0], self.links[i][1]]
                self.link_label.config(text=self.link_title[i])

    def open_on_site(self):
        if self.results and self.results[0]:
            if self.link[1]:
                webbrowser.open(self.link[0].replace('XchampionX', self.results[0][0].lower()))
            else:
                webbrowser.open(self.link[0].replace('XchampionX', self.results[0][0]))
        else:
            messagebox.showerror(title="ResultError", message="No result found to open on internet")

root = tk.Tk()
app = ChampionBuildApp(root)
root.mainloop()
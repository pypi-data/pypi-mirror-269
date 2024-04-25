from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
import tkinter as tk

global option_manager

class OptimalParameterView(CTkScrollableFrame):
    def __init__(self, *args,
                 option_manager: None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        
        self.option_manager = option_manager
        
        self.render()

    def clear(self):
        self.containerFrame.destroy()
        
    def render(self):
        row = 0
        
        self.containerFrame = CTkFrame(self)
        self.containerFrame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.containerFrame.grid_columnconfigure((0, 1), weight=1)
        
        #CTkLabel(self.containerFrame, text="Name:").grid(row=row, column=0, columnspan=1, padx=5, pady=5, sticky="")
        #CTkLabel(self.containerFrame, text="Value:").grid(row=row, column=1, columnspan=1, padx=5, pady=5, sticky="")
        #row += 1
        
        self.steps = self.option_manager.get_steps()

        for step in self.steps:
            name = step['name'].get()
            CTkLabel(self.containerFrame, text=name).grid(row=row, column=0, columnspan=1, padx=5, pady=5, sticky="")
            row += 1
            
            for param in step['param']:
                CTkEntry(self.containerFrame, textvariable=param['name']).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
            
                bb = CTkEntry(self.containerFrame)
                bb.grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
                bb.configure(textvariable=param['optimal_value'])
                row += 1
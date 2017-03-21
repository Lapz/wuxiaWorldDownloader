#!/bin/ python3

""" Gui for the downloader """

import argparse

import queue
import time
import threading
import download

from tkinter import Frame, messagebox, HORIZONTAL, Button, Tk, BOTH, BOTTOM, Entry

from tkinter import ttk


class ThreadedTask(threading.Thread):
    def __init__(self, queue, url):
        threading.Thread.__init__(self)
        self.queue = queue
        self.url = url

    def run(self):
        download.download_chapters(self.url)
        self.queue.put("Chapter Downloaded")


class DownloadUI(Frame):
    """
    The UI, responsilbe for handling user interaction
    """

    def __init__(self, parent):
        self.parent = parent

        Frame.__init__(self, parent)

        self.initUI()

    def initUI(self):
        self.parent.title("Wuxia World Downloader")
        self.pack(fill=BOTH, expand=1)
        self.bind()

        self.url_entry = Entry(
            self, text="http://www.wuxiaworld.com/desolate-era-index/")
# self.__download_novel
        download_button = Button(self,
                                 text="Save novel",
                                 command=(lambda: self.download_button_clicked()))
        self.url_entry.pack()

        download_button.pack(fill=BOTH, side=BOTTOM)

    def progess(self):
        self.prog_bar = ttk.Progressbar(
            self.parent, orient=HORIZONTAL, length=200, mode='determinate')
        self.prog_bar.pack()

    def download_button_clicked(self):
        self.progess()
        self.prog_bar.start()
        self.queue = queue.Queue()

        download.check_for_dir("./wuxia_world")
        links = download.get_chap_links(self.url_entry.get())

        if(links == 0):
            print("Invalid index page")
        else:
            for link in links:
                ThreadedTask(self.queue, link).start()
                self.master.after(100, self.process_queue)
        messagebox.showinfo("Sucesss", "All chapters downloaded")

    def process_queue(self):
        try:
            self.prog_bar.stop()
            self.prog_bar.pack_forget()
        except queue.Empty:
            self.parent.after(100, self.process_queue)


if __name__ == '__main__':
    root = Tk()
    DownloadUI(root)
    root.mainloop()

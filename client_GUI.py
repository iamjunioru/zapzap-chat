import socket
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
import time
import threading
import os

class GUI:
    
    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))

        self.janela = tk.Tk()
        self.janela.withdraw()

        self.login = tk.Toplevel()

        self.login.title("ZAP-ZAP®")
        self.login.resizable(False, False)
        self.login.configure(width = 400, height = 350)
        self.login.config(bg = "#13FF00")

        self.pls = tk.Label(self.login, 
        text = '''ZAPZAP® - o App
que vai superar o WhatsApp''', 
        justify = tk.LEFT,
        bg = "#13FF00",
        fg = "white",
        font = "arial 12 bold")

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.userLabelName = tk.Label(self.login,
                                      text= "nome: ",
                                      bg = "#13FF00",
                                      fg = "green",
                                      font="arial 11 bold")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login,
                                      fg = "red",
                                      font="arial 11 bold")
        self.userEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(self.login, text="sala: ",
                                      fg = "green",
                                      bg = "#13FF00",
                                      font="arial 11 bold")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(self.login,
                                      fg = "#FF00A6",
                                      font="arial 11 bold",
                                      show = "😈")
        self.roomEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.45)
        
        self.go = tk.Button(self.login, 
                            text="entrar no zap", 
                            bd = 0,
                            fg = "white",
                            bg = "green",
                            font="arial 11 bold", 
                            command = lambda: self.goAhead(self.userEntryName.get(), self.roomEntryName.get()))
        
        self.go.place(relx=0.35, rely=0.62, width= 160, height= 34)

        self.janela.mainloop()


    def goAhead(self, username, room_id=0):
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(room_id))
        
        self.login.destroy()
        self.layout()

        rcv = threading.Thread(target=self.receive) 
        rcv.start()


    def layout(self):
        self.janela.deiconify()
        self.janela.title("sala do zap - mande um zap")
        self.janela.resizable(width=False, height=False)
        self.janela.configure(width=470, height=550, bg="green")
        self.chatBoxHead = tk.Label(self.janela, 
                                    bg = "#13FF00",  # frame do topo
                                    fg = "white", 
                                    text = self.name , 
                                    font = "arial 11 bold", 
                                    pady = 5)

        self.chatBoxHead.place(relwidth = 1)

        self.line = tk.Label(self.janela, width = 450, bg = "#13FF00")  # fitinha do topo
		
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012) 
		
        self.textCons = tk.Text(self.janela, 
                                width=20, 
                                height=2, 
                                bg="green",  # fundo do chat
                                fg="white",  # cor do texto do chat
                                font="arial 11 bold", 
                                padx=5, 
                                pady=5) 
		
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08) 
		
        self.labelBottom = tk.Label(self.janela, bg="#13FF00", height=80)  # caixa do input de digitar algo
		
        self.labelBottom.place(relwidth = 1, 
							    rely = 0.8) 
		
        self.entryMsg = tk.Entry(self.labelBottom, 
                                bg = "white", # textbox p enviar msg
                                fg = "green", 
                                font = "arial 11")
        self.entryMsg.place(relwidth = 0.74, 
							relheight = 0.03, 
							rely = 0.008, 
							relx = 0.011) 
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom, 
								text = "mande o zap", 
								font = "arial 9 bold", fg = "white",
								width = 20, 
								bg = "green", bd = 0,
								command = lambda : self.sendButton(self.entryMsg.get())) 
        self.buttonMsg.place(relx = 0.77, 
							rely = 0.008, 
							relheight = 0.03, 
							relwidth = 0.22) 


        self.labelFile = tk.Label(self.janela, bg="#13FF00", height=70) # bottom frame 
		
        self.labelFile.place(relwidth = 1, 
							    rely = 0.9) 
		
        self.fileLocation = tk.Label(self.labelFile, 
                                text = "ver arquivo", 
                                bg = "green", 
                                fg = "white", 
                                bd = 0,
                                font = "arial 12 bold")
        self.fileLocation.place(relwidth = 0.65, 
                                relheight = 0.03, 
                                rely = 0.008, 
                                relx = 0.011) 

        self.browse = tk.Button(self.labelFile, 
								text = "procurar", 
								font = "arial 10 bold", 
								width = 13, bd = 0,
								bg = "green", fg = "white",
								command = self.browseFile)
        self.browse.place(relx = 0.67, 
							rely = 0.008, 
							relheight = 0.03, 
							relwidth = 0.15) 

        self.sengFileBtn = tk.Button(self.labelFile, 
								text = "enviar", 
								font = "arial 10 bold", 
								width = 13, 
								bg = "green", bd = 0, fg = "white",
								command = self.sendFile)
        self.sengFileBtn.place(relx = 0.84, 
							rely = 0.008, 
							relheight = 0.03, 
							relwidth = 0.15)
    

        self.textCons.config(cursor = "arrow",) # tipo de cursor
        scrollbar = tk.Scrollbar(self.textCons) 
        scrollbar.place(relheight = 1, 
						relx = 0.974)

        scrollbar.config(command = self.textCons.yview)
        self.textCons.config(state = tk.DISABLED)


    def browseFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/", 
                                    title="selecionar uma img",
                                    filetypes = (("imagem receba obrigado meu deus", 
                                                "*.jpg*"), 
                                                ("zapzapzap", 
                                                "*.*")))
        self.fileLocation.configure(text="imagem aberta: "+ self.filename)


    def sendFile(self):
        self.server.send("FILE".encode())
        time.sleep(0.1)
        self.server.send(str("client_" + os.path.basename(self.filename)).encode())
        time.sleep(0.1)
        self.server.send(str(os.path.getsize(self.filename)).encode())
        time.sleep(0.1)

        file = open(self.filename, "rb")
        data = file.read(1024)
        while data:
            self.server.send(data)
            data = file.read(1024)
        self.textCons.config(state=tk.DISABLED)
        self.textCons.config(state = tk.NORMAL)
        self.textCons.insert(tk.END, "arquivo: "
                                     + str(os.path.basename(self.filename)) 
                                     + " en viado\n\n")
        self.textCons.config(state = tk.DISABLED) 
        self.textCons.see(tk.END)


    def sendButton(self, msg):
        self.textCons.config(state = tk.DISABLED) 
        self.msg=msg 
        self.entryMsg.delete(0, tk.END) 
        snd= threading.Thread(target = self.sendMessage) 
        snd.start() 


    def receive(self):
        while True:
            try:
                message = self.server.recv(1024).decode()

                if str(message) == "FILE":
                    file_name = self.server.recv(1024).decode()
                    lenOfFile = self.server.recv(1024).decode()
                    send_user = self.server.recv(1024).decode()

                    if os.path.exists(file_name):
                        os.remove(file_name)

                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = self.server.recv(1024)
                            total = total + len(data)     
                            file.write(data)
                    
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END, "😍 o " + str(send_user) + " 😍 enviou: " + file_name + " \nobrigado meuDEUs\n")
                    self.textCons.config(state = tk.DISABLED) 
                    self.textCons.see(tk.END)

                else:
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END, 
                                    message+"\n\n") 

                    self.textCons.config(state = tk.DISABLED) 
                    self.textCons.see(tk.END)

            except: 
                print("ocorreu um erro no servidor, servir dor... servir a dor? 😢") 
                self.server.close() 
                break

    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED) 
        while True:  
            self.server.send(self.msg.encode())
            self.textCons.config(state = tk.NORMAL)
            self.textCons.insert(tk.END, 
                            "vc disse: " + self.msg + "\nenviado pelo zap\n\n") 

            self.textCons.config(state = tk.DISABLED) 
            self.textCons.see(tk.END)
            break



if __name__ == "__main__":
    ip_address = "localhost"
    port = 12345
    g = GUI(ip_address, port)

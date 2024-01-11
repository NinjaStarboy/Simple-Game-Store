from tkinter import *
from tkinter import ttk,messagebox

import mysql.connector

class TestDB:
    def __init__(self) -> None:

        self.connect = mysql.connector.connect(host='localhost', user='root', passwd='123456789')
        self.cur = self.connect.cursor()
        self.create_tables()
        self.cur.execute('USE Steam')

    def create_tables(self):
        self.cur.execute('CREATE DATABASE IF NOT EXISTS Steam')
        self.cur.execute('USE Steam')
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Games (
                Game_ID INT PRIMARY KEY,
                Game_Name VARCHAR(50),
                Category VARCHAR(50),
                Price varchar(20),
                Discounted_Price DECIMAL(7,2),
                Rating DECIMAL(4,1),
                Friend_List VARCHAR(120),
                Player_Support VARCHAR(55)
            )
        ''')

    def retrive(self,id):
            self.cur.execute(f"SELECT * FROM Games WHERE Game_ID = {id}")
            result=self.cur.fetchall()
            return result
    
    def insert(self,data_list):
        Game_ID = data_list[0]
        Game_Name = data_list[1]
        Category = data_list[2]
        Price = data_list[3]
        Discounted_Price = data_list[4]
        Rating = data_list[5]
        Friends_List = data_list[6]
        Player_Support = data_list[7]

        insert_query = '''
            INSERT INTO Games 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        data = (Game_ID, Game_Name, Category, Price, Discounted_Price, Rating, Friends_List, Player_Support)
        try:
            self.cur.execute(insert_query, data)
        except:
            self.__init__()
            self.insert()
        self.connect.commit()  

db=TestDB()

class add_game():
    def __init__(self) -> None:
        main.withdraw()
        
        self.add_game_frame=Tk()

        self.add_game_frame.title("Add Game")
        self.add_game_frame.geometry("400x500")
        self.add_game_frame.maxsize(400,500)
        self.add_game_frame.minsize(400, 500)

        # game id
        game_id_label=Label(self.add_game_frame,text="Game id:")
        game_id_label.grid(row=0,column=0,padx=30,pady=10,sticky=E)

        self.game_id_entry=Entry(self.add_game_frame)
        self.game_id_entry.grid(row=0,column=1,padx=10,pady=10)

        # game name
        game_name_label=Label(self.add_game_frame,text="Game Name:")
        game_name_label.grid(row=1,column=0,padx=30,pady=10,sticky=E)

        self.game_name_entry=Entry(self.add_game_frame)
        self.game_name_entry.grid(row=1,column=1,padx=10,pady=10)

        self.game_category_label=Label(self.add_game_frame,text="Game Category:")
        self.game_category_label.grid(row=2,column=0,padx=30,pady=10,sticky=E)

        # game category
        options=["Action","Adventure","RPG","FPS","Battle Royale","Puzzle","Casual","Story","Sports& Racing","Horror","Simulation","Strategy"]

        self.game_category_drop= ttk.Combobox(
            self.add_game_frame,
            state="readonly",
            values=options
        )
        self.game_category_drop.set("Select a Game Category")
        self.game_category_drop.grid(row=2,column=1,padx=10,pady=10)

        # Price
        price_label=Label(self.add_game_frame,text="Price: ")
        price_label.grid(row=3,column=0,padx=30,pady=10,sticky=E)

        self.price_entry=Entry(self.add_game_frame)
        self.price_entry.grid(row=3,column=1,padx=10,pady=10)

        # discount
        discound_label=Label(self.add_game_frame,text="Discount: ")
        discound_label.grid(row=4,column=0,padx=30,pady=10,sticky=E)

        self.discount_entry=Entry(self.add_game_frame)
        self.discount_entry.grid(row=4,column=1,padx=10,pady=10)

        # Rating
        rating_label=Label(self.add_game_frame,text="Rating : ")
        rating_label.grid(row=5,column=0,padx=30,pady=10,sticky=E)

        self.rating_entry=Entry(self.add_game_frame)
        self.rating_entry.grid(row=5,column=1,padx=10,pady=10)

        # Friend List
        friend_list_label=Label(self.add_game_frame,text="Friend List : ")
        friend_list_label.grid(row=6,column=0,padx=30,pady=10,sticky=E)

        self.friend_list_entry=Entry(self.add_game_frame)
        self.friend_list_entry.grid(row=6,column=1,padx=10,pady=10)

        # Player Support
        player_support_label=Label(self.add_game_frame,text="Player Support : ")
        player_support_label.grid(row=7,column=0,padx=30,pady=10,sticky=E)
        options=["Singleplayer","Multiplayer","Co-Op","MMO"]
        self.player_support_drop= ttk.Combobox(
            self.add_game_frame,
            state="readonly",
            values=options
        )
        self.player_support_drop.set("Select Player Support")
        self.player_support_drop.grid(row=7,column=1,padx=10,pady=10)

        clear_button=Button(self.add_game_frame,text="Clear",command=lambda: self.clearentry())
        clear_button.grid(row=8,column=0,padx=10,pady=10)

        save_button=Button(self.add_game_frame,text="Save",command=lambda: self.insert())
        save_button.grid(row=8,column=1,padx=10,pady=10)
        self.add_game_frame.protocol("WM_DELETE_WINDOW", lambda:[main.deiconify(),self.add_game_frame.destroy()])

    def insert(self):

        
        if self.already_exist():
            return
        
        data_list=[
            int(self.game_id_entry.get()),
            self.game_name_entry.get(),
            self.game_category_drop.get(),
            int(self.price_entry.get()),
            int(self.price_entry.get()) - (int(self.price_entry.get()) * int(self.discount_entry.get()) / 100),
            self.rating_entry.get(),
            self.friend_list_entry.get(),
            self.player_support_drop.get()
            ]

        db.insert(data_list=data_list)

    def already_exist(self):
        try:
            id=int(self.game_id_entry.get())
        except:
            messagebox.showinfo(
            message=f"Please enter a valid Id",
            title="Invalid Input"
            )
            return

        result=db.retrive(id)
        
        if len(result)>0:            
            messagebox.showinfo(
            message=f"There is already a game with id: {id}",
            title="Invalid Game ID"
            )
            return True
        else:
            return False
        
    def clearentry(self):
        for child in self.add_game_frame.winfo_children():
            if isinstance(child,Entry):
                child.delete(0,END)
        
        self.game_category_drop.set("Select a Game Category")


class search_game():
    def __init__(self) -> None:
        main.withdraw()
        
        self.search_game_frame=Tk()

        self.search_game_frame.title("Game Search")
        self.search_game_frame.geometry("400x500")
        self.search_game_frame.maxsize(400, 500)
        self.search_game_frame.minsize(400, 500)

        game_id_label=Label(self.search_game_frame,text="Search Game by ID",font=(("Arial",18)))
        game_id_label.grid(row=0,column=0,padx=70,pady=30)

        self.game_id_entry=Entry(self.search_game_frame,font=(("Arial",18)))
        self.game_id_entry.grid(row=1,column=0,padx=70,pady=10)
        self.search_game_frame.protocol("WM_DELETE_WINDOW", lambda:[main.deiconify(),self.search_game_frame.destroy()])

        game_search_button=Button(self.search_game_frame,text="Search",command=lambda: self.search())
        game_search_button.grid(row=2,column=0)
        
    def search(self):
        try:
            id=int(self.game_id_entry.get())
        except:
            messagebox.showinfo(
            message=f"Please enter a valid Id",
            title="Invalid Input"
            )
            return

        result=db.retrive(id)
        if len(result)<1:            
            messagebox.showinfo(
            message=f"There is no game with id: {id}",
            title="Game Not Found"
            )
            
        else:
            data=result[0]
            messagebox.showinfo(
            message=f"Game: {data[0]}\nGame Name:{data[1]}\nGame Category: {data[2]}\nPrice: {data[3]}\nDiscounted Price: {data[4]}\nRating: {data[5]}\nFriend List: {data[6]}\nPlayer Support: {data[7]}\n",
            title=f"Game Found: {data[1]}"
            )


main=Tk()

main.title("Gaming Store")
main.geometry("400x500")
main.maxsize(400,500)
main.minsize(400, 500)

welcome_label=Label(main,text="Welcome to Gaming Store",font=(("Arial",18)))
welcome_label.grid(row=0,column=0,padx=52,pady=40,columnspan=6)

add_button=Button(main,text="Add Game",command=lambda: add_game())
add_button.grid(row=1,column=0,padx=75,pady=80)

search_button=Button(main,text="Search Game",command=lambda: search_game())
search_button.grid(row=1,column=1)


main.mainloop()

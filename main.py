from tkinter import *
import mysql.connector as mysql


class TestDB:
    def __init__(self) -> None:
        pass
        self.connect = mysql.connect(host='localhost', user='root', passwd='123456789',auth_plugin='mysql_native_password')
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
            self.cur.execute(f"SELECT * FROM Steam WHERE Game_ID = {id}")
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
        self.cur.close()

db=TestDB()

class add_game():
    def __init__(self) -> None:
        self.add_game_frame=Tk()

        self.add_game_frame.title("Add Item")
        self.add_game_frame.geometry("400x500")
        self.add_game_frame.maxsize(400,500)
        self.add_game_frame.minsize(400, 500)

        # game id
        game_id_label=Label(self.add_game_frame,text="Game id:")
        game_id_label.grid(row=0,column=0,padx=10,pady=10)

        self.game_id_entry=Entry(self.add_game_frame)
        self.game_id_entry.grid(row=0,column=1,padx=10,pady=10)

        # game name
        game_name_label=Label(self.add_game_frame,text="Game Name:")
        game_name_label.grid(row=1,column=0,padx=10,pady=10)

        self.game_name_entry=Entry(self.add_game_frame)
        self.game_name_entry.grid(row=1,column=1,padx=10,pady=10)

        # game category
        options=["Action","Adventure","RPG","FPS","Battle Royale","Puzzle","Casual","Story","Sports& Racing","Horror","Simulation","Strategy"]

        self.clicked=StringVar()
        self.clicked.set("Select Game Category")
        self.game_category_drop=OptionMenu(self.add_game_frame,self.clicked,*options)
        self.game_category_drop.grid(row=2,column=1,padx=10,pady=10)

        # Price
        price_label=Label(self.add_game_frame,text="Price: ")
        price_label.grid(row=3,column=0,padx=10,pady=10)

        self.price_entry=Entry(self.add_game_frame)
        self.price_entry.grid(row=3,column=1,padx=10,pady=10)

        # discount
        discound_label=Label(self.add_game_frame,text="Discount: ")
        discound_label.grid(row=4,column=0,padx=10,pady=10)

        self.discount_entry=Entry(self.add_game_frame)
        self.discount_entry.grid(row=4,column=1,padx=10,pady=10)

        # Rating
        rating_label=Label(self.add_game_frame,text="Rating : ")
        rating_label.grid(row=5,column=0,padx=10,pady=10)

        self.rating_entry=Entry(self.add_game_frame)
        self.rating_entry.grid(row=5,column=1,padx=10,pady=10)

        # Friend List
        friend_list_label=Label(self.add_game_frame,text="Friend List : ")
        friend_list_label.grid(row=6,column=0,padx=10,pady=10)

        self.friend_list_entry=Entry(self.add_game_frame)
        self.friend_list_entry.grid(row=6,column=1,padx=10,pady=10)

        # Player Support
        player_support_label=Label(self.add_game_frame,text="Player Support : ")
        player_support_label.grid(row=7,column=0,padx=10,pady=10)

        self.player_support_entry=Entry(self.add_game_frame)
        self.player_support_entry.grid(row=7,column=1,padx=10,pady=10)

        clear_button=Button(self.add_game_frame,text="Clear",command=lambda: self.clearentry())
        clear_button.grid(row=8,column=0,padx=10,pady=10)

        save_button=Button(self.add_game_frame,text="Save",command=lambda: self.insert())
        save_button.grid(row=8,column=1,padx=10,pady=10)

        self.add_game_frame.mainloop()

    def insert(self):

        data_list=[
            self.game_id_entry.get(),
            self.game_name_entry.get(),
            self.clicked.get(),
            int(self.price_entry.get()),
            int(self.price_entry.get()) - (int(self.price_entry.get()) * int(self.discount_entry.get()) / 100),
            self.rating_entry.get(),
            self.friend_list_entry.get(),
            self.player_support_entry.get()
            ]
        
        db.insert(data_list=data_list)

    def clearentry(self):
        for child in self.add_game_frame.winfo_children():
            if isinstance(child,Entry):
                child.delete(0,END)
        
        self.game_category_drop.selection_clear()

add_game()
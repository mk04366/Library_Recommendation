from tkinter import *


#bookfilename='C:\\Users\\Salman\\Documents\\GitHub\\project-ammark\\Code\\Booklist.csv'
bookfilename='Booklist.csv'
def openbookfile(name):
    import csv
    with open(name) as csv_file:
        x=csv.reader(csv_file)
        d=tuple()
        F=[]
        for y in x:
            for z in y:
                d+=(z,)
            F.append(d)
            d=tuple()
        bookdict={}
        for x in F:   
            bookdict[x[0]]=[x[2].split(','),x[1],x[3]]
    return bookdict
book_data=openbookfile(bookfilename)

def addNodes(G, nodes):
    for item in nodes:
        G.update({item : []})
    return


def userdataload(name):
    import csv
    with open(name) as csv_file:
        x=csv.reader(csv_file)
        d=tuple()
        F=[]
        for y in x:
            for z in y:
                d+=(z,)
            F.append(d)
            d=tuple()   
        bookdict2={}
        for x in F:
            if x!=():
                final={}
                for y in range(len(x)):
                    if y!=0:
                        M=x[y].split(',')
                        o=M[1]
                        final[M[0]]=eval(o)
                bookdict2[x[0]]=final
        return bookdict2
datafile='Userdata.csv'
#datafile= 'C:\\Users\\Salman\\Documents\\GitHub\\project-ammark\\Code\\Userdata.csv'
user_data=userdataload(datafile)

def addEdges(G, edges, directed=False):
    for i in range(len(edges)):
        for key in G.keys():
            if key == edges[i][0]:
                if not directed:
                    G[key] += (edges[i][1:],)
                    G[edges[i][1]] += (edges[i][:1]+edges[i][2:],)
                    break
                else:
                    G[key] += (edges[i][ 1:],)
                    break
    return

def WeightedEdge_Create(datadict):
    final_lst=[]
    alrdy_traversed = [] 
    for person in datadict.keys():
        alrdy_traversed.append(person)
        books_read=datadict[person]
        for neighbor in datadict.keys():
            weight=0
            if neighbor in alrdy_traversed:
                continue
            for n_books in datadict[neighbor].keys():
                if n_books in books_read.keys():
                    currentchoice=books_read[n_books]
                    neighborchoice=datadict[neighbor][n_books]
                    if currentchoice==neighborchoice:
                        weight+=1
                    else:
                        weight-=1
            if weight != 0:
                final_lst.append((person, neighbor, weight))

    return final_lst

edge_list = WeightedEdge_Create(user_data)
##print(edge_list)


G = {}

def create_adjlst(G):
    addNodes(G, user_data.keys())
    addEdges(G,edge_list)
    return

create_adjlst(G)

#name=input('Your name?')

def GetMeADuo(G,name):
    Final=[]
    a=G[name]
    t=0
    for x in a:
        if x[1]>t:
            Final.append(x[0])
            t=x[1]
    if Final==[]:
        print('You have no match :c')
    else:
        print('Your highest duo score is with ',end='')
    print(Final[-1]+'.')
    return Final
#b=GetMeADuo(G,name)

genre_output = ''
def recommend_genre(bookdata,name,c):
    global genre_output
    try:
        userbooks=c[name]
    except:
        genre_output = 'User record not found!'
        return
    for x,y in userbooks.items():
        if y==True:
            genre=bookdata[x][0]
            author=bookdata[x][1]
            price=bookdata[x][2]
            rec=[]
            for gen in genre:
                for i,j in bookdata.items():
                    if gen in j[0] and i not in rec and i!=x:
                        rec.append((i,j[2]))
            
            for x in rec:
                genre_output+= x[0] + ' for $' + x[1] + '\n'
    return                
#recommend_genre(book_data,name,user_data)

def top_picks(G, name):
    global user_data
    links = G[name]
    counter = 0
    toplist = []                          #list maintained to track best edges
    
    while counter <2:
        maxval = 0
        max_index = None
        for person in range(len(links)):
            if links[person][1] > maxval:
                maxval = links[person][1]
                max_index = person
        if max_index:
            toplist.append(links.pop(max_index)[0])
            counter +=1
        else:
            break
    
    recommendation = []
    
    for connection in toplist:
        read_books = user_data[connection]
        for book in read_books.keys():
            if book not in user_data[name].keys() and read_books[book]:
                recommendation.append(book)

    return recommendation

top_picks_display = ''

def show_top_picks(G, name, book_data):    
    global top_picks_display
    top_picks_display = ''
    try:
        picks = top_picks(G, name)
        for entry in picks:
            top_picks_display+= entry+'\t Genres: '+str(', '.join(book_data[entry][0]))+'\n'
    except:
        top_picks_display = 'User record not found!'
        return

    

#show_top_picks(G, name ,book_data)

def display_main():
    global G
    global book_data
    global window1
    window1 = Tk()
    window1.title('Book Butler')

    inputframe = LabelFrame(window1, width = 650, height = 300)
    inputframe.pack()

    outputframe = LabelFrame(window1, width = 650, height = 500)
    outputframe.pack()


    def call_toppick(G, name, book_data):
        show_top_picks(G, name, book_data)
        toppicklabel.configure(text=top_picks_display)

    def call_genre(book_data, name, user_data):
        recommend_genre(book_data, name, user_data)
        topgenrelabel.configure(text=genre_output)

        
    text_prompt = Label(inputframe, text = 'Enter your name:')
    text_prompt.place(relx = 0.2, rely= 0.2, anchor = 'center')
    
    Entry1 = Entry(inputframe, bd = 3, width = 25)
    Entry1.place(relx = 0.5, rely = 0.2, anchor = 'center')
    

    Addbutton = Button(inputframe, text = 'Add a new user', anchor = 'center', command = lambda: display_add(Entry1.get()))
    Addbutton.place(relx = 0.2, rely = 0.5)

    Bytaste_button = Button(inputframe, text = 'Top Picks for You', anchor = 'center', command=lambda: call_toppick(G, Entry1.get(), book_data))
    Bytaste_button.place(relx = 0.4, rely = 0.5)

    Bygenre_button = Button(inputframe, text = 'Books of similar genre',anchor = 'center', command = lambda: call_genre(book_data, Entry1.get(), user_data))
    Bygenre_button.place(relx = 0.63, rely = 0.5)

    toppicklabel = Label(outputframe, text= '')
    toppicklabel.place(relx = 0.5, rely = 0.1, anchor = 'center')
    
    topgenrelabel = Label(outputframe, text= '')
    topgenrelabel.place(relx = 0.5, rely = 0.6, anchor = 'center')

##from tkinter import *      
##root = Tk()      
##canvas = Canvas(root, width = 300, height = 300)      
##canvas.pack()      
##image = PhotoImage(file="sample.ppm")      
##canvas.create_image(20,20, anchor=NW, image=image)      
##mainloop() 
##window1.mainloop()


def display_add(pass_name):
    global window1
    window1.destroy()
    window2 = Tk()

    frame1 = Frame(window2, width = 650, height = 350)
    frame1.pack()
    
    book1 = Entry(frame1, bd = 2, width = 25)
    book1.place(relx = 0.3, rely = 0.1)

    book2 = Entry(frame1, bd = 2, width = 25)
    book2.place(relx = 0.3, rely = 0.25)

    book3 = Entry(frame1, bd = 2, width = 25)
    book3.place(relx = 0.3, rely = 0.4)

    book4 = Entry(frame1, bd = 2, width = 25)
    book4.place(relx = 0.3, rely = 0.55)

    book5 = Entry(frame1, bd = 2, width = 25)
    book5.place(relx = 0.3, rely = 0.7)

    label1 = Label(frame1, text = 'Enter title for book #1: ')
    label1.place(relx = 0.1, rely = 0.1)

    label2 = Label(frame1, text = 'Enter title for book #2: ')
    label2.place(relx = 0.1, rely = 0.25)

    label3 = Label(frame1, text = 'Enter title for book #3: ')
    label3.place(relx = 0.1, rely = 0.4)

    label4 = Label(frame1, text = 'Enter title for book #4: ')
    label4.place(relx = 0.1, rely = 0.55)

    label5 = Label(frame1, text = 'Enter title for book #5: ')
    label5.place(relx = 0.1, rely = 0.7)


    preflabel1 = Label(frame1, text = 'Liked? ')
    preflabel1.place(relx = 0.6, rely = 0.1)

    preflabel2 = Label(frame1, text = 'Liked? ')
    preflabel2.place(relx = 0.6, rely = 0.25)

    preflabel3 = Label(frame1, text = 'Liked? ')
    preflabel3.place(relx = 0.6, rely = 0.4)

    preflabel4 = Label(frame1, text = 'Liked? ')
    preflabel4.place(relx = 0.6, rely = 0.55)

    preflabel5 = Label(frame1, text = 'Liked? ')
    preflabel5.place(relx = 0.6, rely = 0.7)

    pref1 = Entry(frame1, bd = 2, width = 10)
    pref1.place(relx = 0.7, rely = 0.1)

    pref2 = Entry(frame1, bd = 2, width = 10)
    pref2.place(relx = 0.7, rely = 0.25)

    pref3 = Entry(frame1, bd = 2, width = 10)
    pref3.place(relx = 0.7, rely = 0.4)

    pref4 = Entry(frame1, bd = 2, width = 10)
    pref4.place(relx = 0.7, rely = 0.55)

    pref5 = Entry(frame1, bd = 2, width = 10)
    pref5.place(relx = 0.7, rely = 0.7)

    def save():
        addbooklst = [book1.get()+','+pref1.get(), book2.get()+','+pref2.get(), book3.get()+','+pref3.get(), book4.get()+','+pref4.get(), book5.get()+','+pref5.get()]
        addusername = pass_name
        Add_to_records(datafile, addusername, addbooklst)
        window2.destroy()

    submitbutton = Button(frame1, text = 'Submit', anchor = 'center', command = save)
    submitbutton.place(relx = 0.3, rely = 0.8)

    window2.mainloop()

new_user_data=[]
def save_new_entries(user_name, user_books):
    global new_user_data
    new_user_data=[user_name]
    for x in user_books:
        new_user_data.append(x)


#we will use the function, save_new_entries via GUI and the use the function, Add_to_records to save every new record from save_new_entry into the Userdata.csv file.       
def New_User(datafile,new_user_data):  #datafile is the Userdata.csv file
    import csv
    with open(datafile, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(new_user_data)
##New_User(datafile,new_user_data)



def Add_to_records(datafile, user_name, user_books):
    global new_user_data
    save_new_entries(user_name, user_books)
    New_User(datafile,new_user_data)

#Add_to_records(datafile, 'Test', ['test1,True', 'test2,False'])

display_main()


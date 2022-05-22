#bookfilename=input('Enter the excel file name here (csv) for the book data file.')
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
            d=tuple()   #After this, csv file is stored in a list of nested lists.
        bookdict={}
        for x in F:     #Used to create a dictionary of desired format.
            bookdict[x[0]]=[x[2].split(','),x[1],x[3]]
        return bookdict
print(openbookfile(bookfilename))

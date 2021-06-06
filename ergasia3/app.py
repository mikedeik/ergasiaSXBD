# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db
import random
from collections import Counter

def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)
    
    return con
# Creating n-grams function
def create_ngrams(text,num):

    # we lower the cases of the text input
    text = text.lower()
    count = 0
    # we use split to split then text into single words
    strt = text.split()
    # we init 3 lists we are going to use 
    result = []
    temp_list = []
    words_list = []
    
    # first we check for evey word on the list to have if every character is a letter using the is_letter function
    while count<len(strt) :
        for ch in strt[count]:
            if not is_letter(ch):
                strt[count] = strt[count].replace(ch,"")
    # we add the new formed words into the new list        
        temp_list.append(strt[count])
        count += 1
    # we check if any word is a stopwords then if not we add it into a new list we are going to use further to make the n-grams
    for item in temp_list:
        if is_not_stopword(item):
            words_list.append(item)  

    # depending on the number n for the n gram we forge the strings of our result list to have 1,2 or 3 words accordingly or print an error message if the input was wrong   
    if num == 1:
            result = words_list
    elif num == 2:
        for i in range(len(words_list)-1):
            result.append(words_list[i] + " " + words_list[i+1])
    elif num == 3:
        for i in range(len(words_list)-2):
            result.append(words_list[i] + " " + words_list[i+1] + " " + words_list[i+2])
    else :
        print("Error input for n-gram")
        # we return a 1-gram instead of none if input was wrong
        result = words_list
 

    return result

# returns true if a char is a letter
def is_letter(char):
    return ("a" <= char <= "z")
# returns True if the given string is NOT a stopword or False if it is 
def is_not_stopword(string):
    stopwords = {"this","is","the","","vaccine","after","covid","injection","with","those","days","patient","that","from","symptoms",
                  "ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during","very", "having", "with",
                  "they",  "some", "yours", "such", "into", "most", "itself", "other", "from", "each","themselves", "until", "below",
                  "these", "your", "through", "were", "more", "himself", "this", "down", "should" , "their", "while", "above", "both" , "ours",
                  "when", "before", "them", "same","been", "have", "will", "does", "yourselves", "then", "that", "because", "what", "over", 
                  "under", "herself",  "just", "where" , "only", "myself", "which", "those", "after", "whom", "being","theirs", "against",
                  "doing", "further", "here", "than","dose" , "around" ,"spontaneous","report","reported","test","possitive","first","second",
                  "third","received","site","i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                  "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                  "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those"
                  , "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a",
                  "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against",
                  "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "out",  "off",
                  "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
                  "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", 
                  "can", "will", "just", "don", "should", "now","medical","history","information","unknown","result","results"}
    if string in stopwords or len(string) <= 3 :
        return False
    else:
        return True    

    

def mostcommonsymptoms(vax_name):
    

    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    # We init the lists we will need for this function
    results = []
    words =[]
    # this is the querry that will return the Symptoms Column for a given vaccine
    q = """SELECT Symptoms FROM vaccination WHERE vaccines_vax_name = %s"""
    # We execute the querry and fetch all the results
    cur.execute(q,vax_name)
    rows = cur.fetchall()
    
    # for every row we have we create a new list of n-grams 
    for i in range (cur.rowcount) :
        # Here you will need to swap between 1,2 and 3 to form the required n-grams
        strt = create_ngrams(rows[i][0],1) 
        # we insert every item of every row into our list as an n-gram now
        for item in strt:
            words.append(item)
    # here we find the most common n-grams in our list             
    count = Counter(words)
    # and we get the 5 most common (you can swap this to get more or less)
    most_occur = count.most_common(5)

   
    # finally we make a list to print on our final results to show on the website        
    for item in most_occur :
        results.append(item[0]) 
    


    
    
    
    
    

    return [("vax_name","result"),(vax_name,results)] 


def buildnewblock(blockfloor):
    
   # Create a new connection
    con=connection()
    

    # Create a cursor on the connection
    cur=con.cursor()
    # Querry to select the number of blocks in the given floor # We check for distinct in case there is an error in the db
    q = """SELECT count(distinct BlockCode) FROM block WHERE Blockfloor = %s """

    # Executing the querry    
    cur.execute(q,blockfloor)
    
    # Since it's a single row we fetch the result to check if there is space for a new block
    check = cur.fetchone()
    
    # Init of the list of results we gonna print
    results = []
    
    
    # Checking if the floor is full on blocks if it's full we return the error as requested
    if check[0] >= 9 :
        print("The Floor is Full")
        results.append(('Error',))
    # If the floor is not empty
        
    else :
        
        # We exectute a question to get the existing block codes 
        q1 = """ SELECT BlockCode FROM block WHERE BlockFloor = %s """
        cur.execute(q1,blockfloor)    
        for i in range(9):
            # For 9 times (max amount of blocks we can have) we fetch the blockCode and check where we should insert the new block
            n = cur.fetchone()
            
            # first checking the case that the floor has all blocks with continues codes (ex. lets say floor 2 has block codes (1,2,3,4,5) then on 6th loop n = None and we need to insert after)
            # since i goes from 0 - 8 we set the block to be i+1 and break the loop. (from the first if that won't break if we have exactly 9 rows)
            if n is None : 
                block = i+1
                break;
                
            # Now we check if there is a "gap" between the block codes (ex. on our db floor 2 has block codes (1,2,5) so new block will have the code 3) and break the loop
            else :    
                if n[0] != (i+1) :
                    block = i+1
                    break;
        # we set the data we will insert later          
        data = (blockfloor,block)  
        
        # Querry to insert the new values and we execute it
        insert_block = """ INSERT INTO block(BlockFloor,BlockCode) VALUES(%s,%s) """
        cur.execute(insert_block,data)
        
        # Querry to insert the new rooms now into the room table
        insert_room = """ INSERT INTO room(RoomNumber,RoomType,BlockFloor,BlockCode,Unavailable) VALUES(%s,%s,%s,%s,%s) """
    
        #making the variables to insert a new room
        num = random.randint(1,5) # we get a random No bettween 1 and 5
        room_type = ('single','double','triple','quadruple') # those are the types of the room we can insert 
        unavailable = (0,1) # this will show if the room is available or not (imo should allways be available since we just created the block with the rooms but it was asked to be random)
        room_no = [] 
        tempint = (int(blockfloor))*1000 + block*100 #we set a temp int to help make the code of the room 
        
        # now for a a random amount of times between 1 and 5
        for i in range(num):
            
            # We create here the room_no which we will import
            room_no.append(tempint+i)
            # and execute the insert querry with the correct data to import
            cur.execute(insert_room,(room_no[i],random.choice(room_type),(int(blockfloor)),block,random.choice(unavailable)))    

        #finally commit the changes and set the results we gonna print to the website to ok
        con.commit()
        results.append(('ok',))
    
    return [("result",),] + results

def findnurse(x,y):

    # Create a new connection
    
    con=connection()
    
    
    # Create a cursor on the connection
    cur=con.cursor()
    # we init the list of the results we gonna print

    results = []    
    
    # checking first if the floor No is correct
    cur.execute("""Select 'yes' as answer Where exists (SELECT BlockFloor FROM block where BlockFloor = %s) """,x)
    f = cur.fetchone()
    if f is None :
        results.append(('Given floor No does not exist',))
    else :    
        
        # Setting the data for the querry 
        data = (x,x,y)
        # Querry to find the nurses with the required attributes ( having been in all the the blocks of a floor and having been present at the apointments of at least the given  different patients 
        q = """ select nurse.EmployeeID 
                from on_call , nurse , appointment
                where on_call.Nurse = nurse.EmployeeID and on_call.BlockFloor = %s and nurse.EmployeeID = appointment.PrepNurse
                group by on_call.Nurse 
                having count(distinct on_call.BlockCode) = (select count(block.BlockCode) from block where block.BlockFloor = %s ) and count(distinct appointment.Patient) >= %s """ 
    
        # We execyte the querry
        cur.execute(q,data)
        # and fetch all the results (we know here the rows have a single integer provided as tuple )
        t = cur.fetchall()
    

    
        # So for every single row (this means for every nurse we found earlier    
        for i in range(len(t)):
    
            # we set a new querry that will return to us the required data to print
        
            q1 = """select nurse.Name , nurse.EmployeeID , count(distinct vaccination.patient_SSN)
                    from nurse,vaccination
                    where nurse.EmployeeID = %s and vaccination.nurse_EmployeeID = nurse.EmployeeID """

            # we execute the querry setting as the nurse id the corresponding nurse id we got from the first querry
            cur.execute(q1,t[i][0])
            # We fetch all the results we asked for (again we know this will return a single row since the nurse id is a PK and we can't have doubles) and import the row into our results 
            n = cur.fetchall() 
            results.append(n[0]) 
        # Finally we print the results in the website    
    return [("Nurse", "ID", "Number of patients"),] + results 

def patientreport(patientName):
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    # Create a 2nd cursor on the conection we will need 
    cur2 = con.cursor()
    
    # This is  the first querry checking if there is a record in the table undergoes of the given patient
    qtemp = """ select patient.Name 
                from undergoes,patient
                where undergoes.Patient = patient.SSN and patient.Name = %s """
 
    # This is a second querry checking if there is a record in the table stay of the given patient
    qtemp1 = """select patient.Name
                from stay,patient
                where stay.Patient = patient.SSN and patient.Name = %s"""        

    # We execute both querries # The reason we do this is because there might be missing data on either the table undergoes or the table stay
    cur.execute(qtemp,patientName)
    cur2.execute(qtemp1,patientName)
    
    # if there is no record on any of the two tables we print that the given patient has not been treated ( this is printed in the terminal while in the website we have no results)
    if cur.rowcount == 0 and cur2.rowcount ==0:
        n = cur.fetchall()
        print(f"{patientName} has not been treated")
        
    # else if there is at least one record on any table we fetch the patient name that has records on undergoes (cause there might be multiple undergoes during a stay of a patient and we want to get those records )   
    elif cur.rowcount >= cur2.rowcount :    
        n = cur.fetchall()
        
    # else that means only the stay table has records of this patient we fetch the results    
    else :
        n = cur2.fetchall()
    # What we actually need from those querries is the amount of rows returned 
    # We init the list for the results we are going to print on the website
    results = [] 
    # We start a for loop for each row we are going to import on our final results
    for i in range(len(n)) :
        
        # querry to fill and check name   
        q1 = f"SELECT patient.name  from patient where patient.name = '{patientName}' " 
        
        # we init the list we are going to fill with the requested results on every querry (it will have diferent rows depending on the history of the patient)
        row_list =[]
        # We execute and fetch the results and append our row list with the name that corresponds 
        # (here we take the first result every time (notice name_row[0][0]) since if there are different patients with the same name it will not affect this input the name will still be the same)
        # but if there are multiple rows in other querries for a single patient there won't be a 2nd row in the tuple name_row
        cur.execute(q1)
        name_row = cur.fetchall()
        row_list.append(name_row[0][0])
        
        
        #querry for doctor which is only recorded in table undergoes not in table stay    
        q2 = """select physician.Name 
            from physician,undergoes,patient
            where undergoes.Patient = patient.SSN and patient.Name = %s and undergoes.Physician = physician.EmployeeID"""
        # we execute the querry and fetch all results
        cur.execute(q2,patientName)
        phys_row = cur.fetchall()
        # if there is no result we append the list with "No value"
        if cur.rowcount == 0:
            strt ="No value"
            row_list.append(strt)
        # else we insert the phys_row that coresponds to our for loop in our row_list      
        else :
            row_list.append(phys_row[i][0])
        #querry for nurse again the nurse record is only in the undergoes table               
        q3 = """select nurse.Name
                from nurse,undergoes,patient    
                where undergoes.patient = patient.SSN and patient.Name = %s and undergoes.AssistingNurse = nurse.EmployeeID"""
        # we execute the querry and fetch all results    
        cur.execute(q3,patientName)
        nurse_row = cur.fetchall()        
        
        # if there is no result we append the list with "No value"
        if cur.rowcount == 0:
            strt ="No value"
            row_list.append(strt)
        # else we insert the nurse_row that coresponds to our for loop in our row_list   
        else :
            row_list.append(nurse_row[i][0]) 
            
        #querry for date we start by checking if there is a record in undergoes
        cur.execute(qtemp,patientName)
        
        # If there is we need to make our querry so that it will show the date twice or more in case our patient has more than one treatment during a single stay
        if cur.rowcount > 0 :
            q4 = """select stay.StayEnd
                    from patient,stay, undergoes
                    where stay.Patient = patient.SSN and patient.Name = %s and undergoes.Stay = stay.StayID
                    group by undergoes.DateUndergoes"""
        # else we just return the stay end date records from the stay table           
        else :
            q4 = """select stay.StayEnd
                    from patient,stay   
                    where stay.Patient = patient.SSN and patient.Name = %s"""
        # we execute the correct querry and fethch the results            
        cur.execute(q4,patientName)
        date_row = cur.fetchall()        
        # if there is no record we append our row_list with 'No Value'
        if cur.rowcount == 0:
            strt ="No value"
            row_list.append(strt)
        # else we insert the date_row that coresponds to our for loop in our row_list
        else :
        
            row_list.append(date_row[i][0])
        # querry for treatment name and cost here we could have split again the querries to 1 by 1 for name and cost just like previously but since in our current db every treatment has a cost 
        # we decided to import both at the same time (so that the code is cleaner)    
        q5 = """select treatment.Name, treatment.Cost
                from treatment, undergoes, patient
                where treatment.Code = undergoes.Treatment and undergoes.Patient = patient.SSN and patient.Name = %s"""
            
        cur.execute(q5,patientName)
        treat_row = cur.fetchall()        
        if cur.rowcount == 0:
            strt ="No value"
            row_list.append(strt)
            row_list.append(strt)
        else :
            row_list.append(treat_row[i][0])
            row_list.append(treat_row[i][1])
                       
            
        # querry for room/block/floor again we import all 3 at the same time as we did with the treatment table (could have split into 3 diferent querries instead)
        # here again just like we did with the date we need to check if there are multiple undergoes during 1 stay and make the querry acoordingly
        cur.execute(qtemp,patientName)
        if cur.rowcount > 0 :
            q6 = """select room.RoomNumber , room.BlockFloor , room.BlockCode
                from room, patient , stay , undergoes
                where room.RoomNumber = stay.Room and stay.Patient = patient.SSN and patient.Name = %s and undergoes.Patient = patient.SSN 
                group by undergoes.DateUndergoes"""
        else :
            q6 = """select room.RoomNumber , room.BlockFloor, room.BlockCode
                    from room, patient, stay
                    where room.RoomNumber = stay.Room and stay.Patient = patient.SSN and patient.Name = %s"""
        cur.execute(q6,patientName)
        room_row = cur.fetchall()        
        if cur.rowcount == 0:
            strt ="No value"
            row_list.append(strt)
            row_list.append(strt)
            row_list.append(strt)
        else :

            row_list.append(room_row[i][0])  
            row_list.append(room_row[i][1])  
            row_list.append(room_row[i][2])  
   
         




        # in the end of the for loop when the row_list has all the data for a row we insert the whole row into our results list
        results.append(row_list)
        
    print(results)    
    return [("Patient","Physician", "Nurse", "Date of release", "Treatement going on", "Cost", "Room", "Floor", "Block")]+ results

    # Please test for the names : 'Spinka Cynthia' , has 2 undergoes records during 1 stay
    #                             'Jacobs Marian' , has 1 stay record but no undergoes records
    #                             'Carroll Nelson' , has 1 undergoes record but no stay record  
    #                             'Purdy Maurice'  , has no record in any of those tables
    #                             'Cronin Tressa' , has record for both tables 
    # There is no patient with more than 1 stay ID to test 
# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db

def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)
    
    return con

def mostcommonsymptoms(vax_name):
    
    # Create a new connection
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    return [("vax_name","result")]


def buildnewblock(blockfloor):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    
 
    return [("result",),]

def findnurse(x,y):

    # Create a new connection
    
    con=connection()
    
    
    # Create a cursor on the connection
    cur=con.cursor()
    data = (x,x,y)
    
    q = """ select nurse.EmployeeID 
            from on_call , nurse , appointment
            where on_call.Nurse = nurse.EmployeeID and on_call.BlockFloor = %s and nurse.EmployeeID = appointment.PrepNurse
            group by on_call.Nurse 
            having count(distinct on_call.BlockCode) = (select count(block.BlockCode) from block where block.BlockFloor = %s ) and count(distinct appointment.Patient) >= %s """ 
    
    
    cur.execute(q,data)
    t = cur.fetchall()
    print(cur.rowcount)
    print(t)
    for i in range (len(t)):
        print(t[i])
    results = []
    
    for i in range(len(t)):
        q1 = """select nurse.Name , nurse.EmployeeID , count(distinct vaccination.patient_SSN)
                 from nurse,vaccination
                 where nurse.EmployeeID = %s and vaccination.nurse_EmployeeID = nurse.EmployeeID """
        cur.execute(q1,t[i][0])
        n = cur.fetchall()
        print(n)    
        results.append(n[0]) 
    print(results)
    return [("Nurse", "ID", "Number of patients"),] + results 

def patientreport(patientName):
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    cur2 = con.cursor()
    qtemp = """ select patient.Name 
                from undergoes,patient
                where undergoes.Patient = patient.SSN and patient.Name = %s """
    qtemp1 = """select patient.Name
                from stay,patient
                where stay.Patient = patient.SSN and patient.Name = %s"""        
    cur.execute(qtemp,patientName)
    cur2.execute(qtemp1,patientName)
    if cur.rowcount == 0 and cur2.rowcount ==0:
        n = cur.fetchall()
        print(f"{patientName} has not been treated")
    elif cur.rowcount >= cur2.rowcount :    
        n = cur.fetchall()
    else :
        n = cur2.fetchall()
        
    results = []        
    for i in range(len(n)) :
        sql = f"select patient.name ,Physician.name as physician ,nurse.Name as nurse ,stay.StayEnd as date , treatment.Name as treatment , treatment.Cost as treatment_cost , room.RoomNumber as Room , room.BlockCode as Block ,room.BlockFloor as Floor from patient,physician,treatment,undergoes,nurse, stay, room where patient.SSN = undergoes.Patient and patient.name = '{patientName}' and physician.EmployeeID = undergoes.Physician and nurse.EmployeeID = undergoes.AssistingNurse and undergoes.Stay = stay.StayID and treatment.Code = undergoes.Treatment and stay.Room = room.RoomNumber  order by stay.StayEnd" 
    #querry to fill and check name   
        q1 = f"SELECT patient.name  from patient where patient.name = '{patientName}' " 
    
        row_list =[]
        cur.execute(q1)
        name_row = cur.fetchall()
        row_list.append(name_row[0][0])
        
        
    #querry for doctor    
        q2 = """select physician.Name 
            from physician,undergoes,patient
            where undergoes.Patient = patient.SSN and patient.Name = %s and undergoes.Physician = physician.EmployeeID"""
    
        cur.execute(q2,patientName)
        phys_row = cur.fetchall()
        if cur.rowcount == 0:
            strt ="No value"
            row_list.append(strt)
        else :
            row_list.append(phys_row[i][0])
    #querry for nurse                
        q3 = """select nurse.Name
                from nurse,undergoes,patient    
                where undergoes.patient = patient.SSN and patient.Name = %s and undergoes.AssistingNurse = nurse.EmployeeID"""
            
        cur.execute(q3,patientName)
        nurse_row = cur.fetchall()        
        if cur.rowcount == 0:
            strt ="No value"
            row_list.append(strt)
        else :
            row_list.append(nurse_row[i][0]) 
    #querry for date 
        cur.execute(qtemp,patientName)
        if cur.rowcount > 0 :
            q4 = """select stay.StayEnd
                    from patient,stay, undergoes
                    where stay.Patient = patient.SSN and patient.Name = %s and undergoes.Stay = stay.StayID
                    group by undergoes.DateUndergoes"""
        else :
            q4 = """select stay.StayEnd
                    from patient,stay   
                    where stay.Patient = patient.SSN and patient.Name = %s"""
        cur.execute(q4,patientName)
        date_row = cur.fetchall()        
        if cur.rowcount == 0:
            strt ="No value"
            row_list.append(strt)
        else :
            row_list.append(date_row[i][0])
    #querry for treatment name and cost       
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
                       
            
      #querry for room/block/floor
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
            #strtemp = " ".join(map(str, room_row[i][0]))
            row_list.append(room_row[i][0])  
            row_list.append(room_row[i][1])  
            row_list.append(room_row[i][2])  
   
         





        results.append(row_list)
        
        
    return [("Patient","Physician", "Nurse", "Date of release", "Treatement going on", "Cost", "Room", "Floor", "Block")]+ results

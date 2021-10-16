# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 19:13:53 2020

@author: johan
"""



# Python Project Using Python-mySQL connection

print('\t\t\t BANK ACCOUNTS MANAGEMENT')
print('\t\t\t *-*-*-*-*-*-*-*-*-*-*-*-*')


# acc_id, username, creditcard_no, balance,    pin,   issue_date,   expiry_date
# index-0  index-1     index-2     index-3    index-4   index-5        index-6

"""
mysql> desc bank;
+---------------+---------------+------+-----+---------+-------+
| Field         | Type          | Null | Key | Default | Extra |
+---------------+---------------+------+-----+---------+-------+
| acc_id        | int(3)        | NO   | PRI | NULL    |       |
| username      | varchar(25)   | NO   |     | NULL    |       |
| creditcard_no | varchar(19)   | NO   |     | NULL    |       |
| balance       | decimal(10,2) | YES  |     | NULL    |       |
| pin           | varchar(4)    | NO   |     | NULL    |       |
| issue_date    | date          | YES  |     | NULL    |       |
| expiry_date   | date          | YES  |     | NULL    |       |
+---------------+---------------+------+-----+---------+-------+
"""

import random
import datetime
import mysql.connector as m

con=m.connect(host='localhost',user='root',passwd='jimon2000')




#encryption
def encrypt(num):
    code=["/","!","@","#","$","%","^","&","*","?"]
    num_edit=list(str(num))
    for index_1 in range(len(num_edit)):
        char=int(num_edit[index_1])
        num_edit[index_1]=code[char]
    num=''
    for edit in num_edit:
        num+=edit
    return num




#dencryption
def decrypt(word):
    code=["/","!","@","#","$","%","^","&","*","?"]
    word_edit=list(str(word))
    for index_2 in range(len(word_edit)):
        spec_char=word_edit[index_2]
        word_edit[index_2]=str(code.index(spec_char))
    word=''
    for translated in word_edit:
        word+=translated
    return word



#generate credit card number
def gen_credit():
    while True:
        def gen():
            while True:
                a=str(random.randint(1001,9998))
                if a[0]==a[1]==a[2]==a[3]:
                    continue
                else:
                    break
            return a
        final=str("{}-{}-{}-{}".format(gen(),gen(),gen(),gen()))

        cursor=con.cursor()
        cursor.execute('select * from bank')
        resultset=cursor.fetchall()
        count=0    
        for line in resultset:
            if line[2]==final:
                count+=1
        if count==0:
            break
            
    return final

#to create new account
def addAcc():
    loop_count=0
    while True:
        cursor=con.cursor()
        cursor.execute('select * from bank')
        resultset=cursor.fetchall()
        if resultset==[]:
            acc_id=99
        else:
            acc_id=resultset[-1][0]
        
        acc_id=int(acc_id)+1   #index-0
        username = input("Username: ")   #index-1
        while True:
            check=None
            for i in resultset:
                if i[1]==username:
                    check=True
            if check==True:
                break
            
            creditcard_no = gen_credit()   #index-2
            balance = float(input("Amount deposited: "))   #index-3
            pin = encrypt(random.randint(1001,9998))    #index-4
            valid = int(input("Validity (in years): "))
            issue_date = datetime.date.today()  #index-5
            expiry_date = issue_date + datetime.timedelta(days=valid*365) #index-6
            sql="insert into bank values({},'{}','{}',{},'{}','{}','{}')".format(acc_id,username,creditcard_no,balance,pin,issue_date,expiry_date)
            cursor.execute(sql)
            con.commit()
            loop_count+=1
            break
        
        
        condition = input(("\nDo you want to add more accounts? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break

    print("{} Record(s) added successfully! ".format(loop_count))
        
    
#to withdraw or deposit
def editBalance(index,L):
    edit=input("Do you want to withdraw or deposit (w/d) ?: ")
    cursor=con.cursor()
    if edit.upper()=='W':
        while True:
            amount=float(input("Enter amount to withdraw: "))
            if (float(L[index][3]))-amount<500:
                print("You cannot withdraw more than min balance!\a")
                condition = input(("\nDo you want to withdraw? (Y/N) "))
                condition=condition.upper()
                if condition != 'Y':
                    break
            else:
               new_balance=float(L[index][3])-amount
               cursor.execute("update bank set balance={} where username='{}'".format(new_balance,L[index][1]))
               con.commit()
               print("You have successfully withdrawn ", amount)
               print("New Balance is: ",new_balance)
               break
        
    elif edit.upper()=='D':
        print("Current Balance is: ",L[index][3])
        amount=int(input("Enter amount to deposit: "))
        new_balance=int(L[index][3])+amount
        cursor.execute("update bank set balance={} where username='{}'".format(new_balance,L[index][1]))
        con.commit()
        print("You have successfully deposited ", amount)
        print("New Balance is: ",new_balance)
        
    else:
        print("Invalid input!")


#to renew account
def renew(index,L):
    cursor=con.cursor()
    valid = int(input("Validity (in years): "))
    new_issue_date = datetime.date.today()
    new_expiry_date = datetime.date.today() + datetime.timedelta(weeks=valid*52)
    cursor.execute("update bank set issue_date='{}',expiry_date='{}' where username='{}'".format(new_issue_date,new_expiry_date,L[index][1]))
    con.commit()


#to edit details from account
def edit():
    while True:
        username=input("Enter username to edit: ")
        control=0
        cursor=con.cursor()
        cursor.execute('select * from bank')
        resultset=cursor.fetchall()
        for index in range(len(resultset)):
            if resultset[index][1]==username:
                control+=1
            
                print("\n\nDo you want to: \n")
                print("1: Edit Balance")
                print("2: Renew")
                choice=int(input("\n Enter choice: "))
                    
                if choice==1:
                    editBalance(index,resultset)
                elif choice==2:
                    renew(index,resultset)
                else:
                    print("invalid input")
        
        if control==0:
            print("Record not found! ")
        condition = input(("\nDo you want to edit again? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break
    
    print("Account(s) successfully edited")
    
    
    
#to search specific account    
def search():
    

    cursor=con.cursor()
    cursor.execute('select * from bank')
    resultset=cursor.fetchall()
    
    while True:
        control=0
        user = input("Enter username: ")
        for line in resultset:
            if line[1] == user:
                control+=1
                fields=['Acount ID', 'Username','Creditcard Number','Acc Balance','PIN','issue date','expiry date']
                for field in fields:
                    print(field,'\t\t',end='' )
                print()
                for data in line:
                    print(data,'\t\t',end='')
                print()
        if control==0:
            print("No record with username {} found".format(user))
        condition = input(("\nDo you want to search again? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break
        
    
#to identify accounts past expiry date
def pastexpiry():
    L=[]
    cursor=con.cursor()
    cursor.execute('select * from bank')
    resultset=cursor.fetchall()
    
    while True:
        today=datetime.date.today()
        
        year_today = today.strftime("%Y")
        month_today = today.strftime("%m")
        day_today = today.strftime("%d")
        
        for row in resultset:
            
            year = row[6].strftime("%Y")
            month = row[6].strftime("%m")
            day = row[6].strftime("%d")
            
            if year < year_today:
                L.append(row)
            elif year == year_today:
                if month < month_today:
                    L.append(row)
                elif month == month_today:
                    if day < day_today:
                        L.append(row)
        if L==[]:
            print("No expired Accounts!")
            break
        else:
            print("\nExpired accounts ")
            for line in L:
                print('\n')
                for data in line:
                    print(data,"\t",end='')
    
            print("\nDo want to \n 1- Renew account \n 2- Delete account \n 0- Exit")
            choice=int(input("Enter choice(0/1/2):"))
            if choice==1:
                user=input("Enter username of account to renew: ")
                count=0
                for row in L:
                    if row[1]==user:
                        renew(resultset.index(row),resultset)
                        count+=1
                if count==0:
                    print("username not present")
            elif choice==2:
                user=input("Enter username of account to delete: ")
                count=0
                for row in L:
                    if row[1]==user:
                        count=1
                        check=input("Are you sure you want to delete this record {} ? (Y/N) ".format(row))
                        if check.upper() == 'Y':
                            cursor.execute("delete from bank where username='{}'".format(user) )
                            print("deleted successfully")
                if count==0:
                    print("username not present")
        
        condition = input(("\nDo you want to renew/delete more accounts? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break    
        

#to delete account
def delete():
    cursor=con.cursor()
    cursor.execute('select * from bank')
    resultset=cursor.fetchall()
    
    while True:

        
        user = input("Enter username: ")
        control=0
        for line in resultset:
            if line[1] == user:
                control+=1
                check=input("Are you sure you want to delete this record {} ? (Y/N) ".format(line))
                if check.upper() == 'Y':
                    cursor.execute("delete from bank where username='{}'".format(user) )
                    print("deleted successfully")
            
        if control==0:
            print("Account not found! ")
        
        condition = input(("\nDo you want to delete more accounts? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break

#to sort accounts of diffrent basis
def sort():
    L=[]
    print("Sort using: ")
    print("1: Account ID")
    print("2: Username")
    print("3: Issue Date")
    print("4: Expiry Date")
    choice=int(input("Enter choice(1-4): "))
    if choice==1:
        n=0
    elif choice==2:
        n=1
    elif choice==3:
        n=5
    elif choice==4:
        n=6
    else:
        n=-1
        print("Invalid input!\nReturning to Admin page.....")
    if n!=-1:
        cursor=con.cursor()
        cursor.execute('select * from bank')
        resultset=cursor.fetchall()
        for i in resultset:
            L.append(i)
        if len(L)>1:
            for index1 in range(len(L)):
                for index2 in range(1,len(L)-1-index1):
                    if L[index2][n] > L[index2+1][n]:
                        L[index2] , L[index2+1] = L[index2+1] , L[index2]
        
        
    
        else:
            print("Only 1 account present!!")
            
        fields=['Acount ID', 'Username','Creditcard Number','Acc Balance','PIN','issue date','expiry date']
        for field in fields:
            print(field,'\t\t',end='' )
        print()
        for i in L:
            print('\n')
            for data in i:
                print(data,'\t\t',end='')
        print()
        
      
        
#to display all accounts
def display():
    L=[]
    cursor=con.cursor()
    cursor.execute('select * from bank')
    resultset=cursor.fetchall()
    for i in resultset:
        L.append(i)
        
    fields=['Acount ID', 'Username','Creditcard Number','Acc Balance','PIN','issue date','expiry date']
    
    for field in fields:
        print(field,'\t\t',end='' )
    print()
    
    for i in L:
        print('\n')
        for data in i:
            print(data,'\t\t',end='')
    print()
    


#to change pin from admin interface
def changepin():
    while True:
        
        print("You are now entering restricted area!\a")
        print("Unauthorised access is a criminal offense!\a")
        choice=input("Do you want to continue (y/n)? ")
        if choice.upper()!="Y":
            break
        else:
            control=0
            user=input("Enter username: ")
            cursor=con.cursor()
            cursor.execute('select * from bank')
            resultset=cursor.fetchall()
            for row in resultset:
                if row[1]==user:
                    control+=1
                    print("The current PIN is: ",decrypt(row[4]))
                    check=input("Do you want to change PIN (y/n)? ")
                    if check.upper()=='Y':
                        new_pin = encrypt(random.randint(1001,9998))
                        cursor.execute("update bank set pin='{}' where username='{}'".format(new_pin,user))
                        con.commit()
                        print("PIN has been changed successfully!")
            
            
            if control==0:
                print("No records with username {} found".format(user))
                break
            
            else:
                break   
            
          
            
          
            
          
            

#admin interface
def admin_pg():
    while True:
        print('\n\n \t MENU :')
        print('1: Add Accounts')
        print('2: Edit Accounts')
        print('3: Search Accounts')
        print('4: Delete/Renew expired Accounts')
        print('5: Delete Account')
        print('6: Sort Accounts')
        print('7: Display all Accounts')
        print('8: Display/Change password(Pin)')
        print('9: Edit validity of accounts')
        print("O: Log out")
        
        choice=input('\n Enter your choice: ')
        if choice=='1':
            addAcc()
        
        elif choice=='2':
            edit()
        
        elif choice=='3':
            search()
        
        elif choice=='4':
            pastexpiry()
        
        elif choice=='5':
            delete()
        
        elif choice=='6':
            sort()
        
        elif choice=='7':
            display()
            
        elif choice=='8':
            changepin()
            
        elif choice=='9':
            user=str(input("Enter username to edit validity: "))
            cursor=con.cursor()
            cursor.execute('select * from bank')
            resultset=cursor.fetchall()
            count=0
            for row in resultset:
                if user==row[1]:
                   count+=1
                   renew(resultset.index(row),resultset)
                   cursor=con.cursor()
                   cursor.execute("select * from bank where username='{}'".format(user))
                   resultset=cursor.fetchone()
                   print('new expiry date is {}'.format(resultset[6]))
            if count==0:
                print("Username does not exist!")
        elif choice=='0':
             print("Thank you...")
             break
        
        else:
            print("Invalid input! Please Try again......")











#customer interface
def customer_pg(user):

    cursor=con.cursor()
    cursor.execute('select * from bank')
    resultset=cursor.fetchall()
    for row in resultset:
        if row[1]==user:
            i=resultset.index(row)
    
            
    
    
    while True:
        print('\n\n \t MENU :')
        print('1: Deposit/Withdraw')
        print('2: Check Balance')
        print('3: Check Expiry date')
        print('4: Renew Account')
        print('5: View Account details')
        print('6: Change PIN')
        print("O: Log out")
        
        choice=input('\n Enter your choice: ')
        if choice=='1':
            editBalance(i,resultset)
        
        elif choice=='2':
            cursor.execute('select * from bank')
            resultset=cursor.fetchall()
            print("Your Account Balance is: ",resultset[i][3])
            
           
        elif choice=='3':
            cursor.execute('select * from bank')
            resultset=cursor.fetchall()
            print("Your Account will expire on: ",resultset[i][6])
            
        
        elif choice=='4':
                
                print("Dear Customer,\n")
                print("Please note, you will be charged 500 per year you wish to renew for ")
                choice=input("Do you want to continue (y/n)? ")
                if choice.upper()=='Y':
                    valid = int(input("Enter Validity (in years): "))
                    new_issue_date=datetime.date.today()
                    new_expiry_date=datetime.date.today() + datetime.timedelta(weeks=valid*52)
                    sql="update bank set issue_date='{}',expiry_date='{}', balance=balance-(500*{}) where username='{}'".format(new_issue_date,new_expiry_date,valid,user)
                    cursor.execute(sql)
                    con.commit()

        
        elif choice=='5':
            cursor.execute('select * from bank')
            resultset=cursor.fetchall()
            print("Your account details: \n")
            for data in resultset[i]:
                print(data,"\t\t",end='')
                
        
        elif choice=='6':
            control=0
            cursor.execute('select * from bank')
            resultset=cursor.fetchall()
            
            
            for row in resultset:
                if row[1]==user:
                    control+=1
                    print("The current PIN is: ",decrypt(row[4]))
                    check=input("Do you want to change PIN (y/n)? ")
                    if check.upper()=='Y':
                        
                        print("\nGuidelines for pin:")
                        print("Only 4 digit numbers are allowed\nLetters or other keys are invaild\nPin cannot start with 0")
                        while True:
                            try:
                                new_pin=int(input("Enter new pin:"))
                                if new_pin in range(1000,10000):
                            
                                    new_pin_encrypted = encrypt(new_pin)
                                    cursor=con.cursor()
                                    cursor.execute("update bank set pin='{}' where username='{}'".format(new_pin_encrypted,user))
                                    print("PIN has been changed successfully!")
                                    print("Your new PIN is: ", decrypt(new_pin_encrypted))
                                    break
                                else:
                                    print("\aOnly number between 1000 and 9999 allowed")
                            except ValueError:
                                print("\aOnly numbers are allowed")
                                
                            condition = input(("\nDo you want to try again? (Y/N) "))
                            condition=condition.upper()
                            if condition != 'Y':
                                break    
            
        elif choice=='0':
             print("Thank you...")
             break
        
        else:
            print("Invalid input! Please Try again......")








#main starts here

if con.is_connected():   

    cursor=con.cursor()
    sql='show databases'
    cursor.execute(sql)
    dbs=cursor.fetchall()
    count_dbs=0
    count_tables=0
    
    for db in dbs:
        if db==('bank_accounts',):
            count_dbs=1
            cursor.execute('use bank_accounts')
            cursor.execute('show tables')
            tables=cursor.fetchall()

            for table in tables:
                if table==('bank',):
                    count_tables=1

                
            if count_tables!=1:
                sql='create table bank(acc_id int(3) Primary key ,username varchar(25) NOT NULL,creditcard_no varchar(19) NOT NULL,balance decimal(10,2),pin varchar(4) NOT NULL,issue_date date, expiry_date date)'
                cursor.execute(sql)
                con.commit()
                
    if count_dbs!=1:
        sql1='create database bank_accounts'
        sql2='use bank_accounts'
        sql3='create table bank(acc_id int(3) Primary key ,username varchar(25) NOT NULL,creditcard_no varchar(19) NOT NULL,balance decimal(10,2),pin varchar(4) NOT NULL,issue_date date, expiry_date date)'
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        con.commit()


    print("Connected to MySQL sucessfully")
    
    
    print("Please wait. Loading Project........")
    for i in range(59000000):
        pass
    
    check=4
    while True:

        print("\nPlease Sign in: \n")
        username=input("Name: ")
        pin=input("Password(Pin): ")
        if username.upper()=='ADMIN' and pin=="password":
            print("You are now entering Admin page...\a")
            admin_pg()
        else:
            sql="select * from bank"
            cursor=con.cursor()
            cursor.execute(sql)
            resultset=cursor.fetchall()
            found=0
            for i in resultset:
                if i[1]==username and decrypt(i[4])==pin:
                    print("Welcome {} \n".format(username))
                    customer_pg(username)
                    found+=1
            if found==0:
                if check==1:
                    print("\nIncorect credintials!")
                    print("Connection Terminated!!\a")
                    break
                elif check>1:
                    check-=1
                    print("\aIncorect credintials! \nPlease try again ({} try left)".format(check))

        control=input("\nDo you want to sign in again (Y/N): ")
        if control.upper()!='Y':
            break
else:
     print("Connection unsuscessful....Check connectivity")

print("Enter anykey to exit!")
input()
        
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:30:02 2020

@author: johan
"""


# Python Project Using CSV File Handling

print('\t\t\t BANK ACCOUNTS MANAGEMENT')
print('\t\t\t *-*-*-*-*-*-*-*-*-*-*-*-*')

# acc_id, username, creditcard_no, balance,    pin,   issue_date,   expiry_date
# index-0  index-1     index-2     index-3    index-4   index-5        index-6

import csv
import random
import datetime
import os


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
        try:
            with open("bank.csv",'r',newline='') as csvfile:
                count=0
                csvobj=csv.reader(csvfile)
                for row in csvobj:
                    if row[2]==final:
                        count+=1
                if count==0:
                    break
        except FileNotFoundError:
            break
    return final
        

#add accounts
def addAcc(): 

    loop_count=0
    while True:
        info=[]
        if os.path.isfile("bank.csv")==True:
            with open('bank.csv','r',newline='') as f:
                csvobj=csv.reader(f)
                for row in csvobj:
                    acc_id=row[0]
        else:
            acc_id=0
    

        acc_id = int(acc_id)+1 #index-0
        username = input("Username: ")   #index-1
        while True:
            if os.path.isfile("bank.csv")==True:
                with open("bank.csv",'r',newline='') as f:
                    csvobj=csv.reader(f)
                    check=None
                    for row in csvobj:
                        if row[1]==username:
                            print("Username already exists")
                            check=True
                            break
                    if check==True:
                        break
            creditcard_no = gen_credit()   #index-2
            balance = int(input("Amount deposited: "))   #index-3
            pin = encrypt(random.randint(1001,9998))    #index-4
            valid = int(input("Validity (in years): "))
            issue_date = datetime.date.today()  #index-5
            expiry_date = issue_date + datetime.timedelta(days=valid*365) #index-6

        
            info.append([acc_id, username, creditcard_no, balance, pin, str(issue_date), str(expiry_date)])
        
            loop_count+=1
            break
        
        if os.path.isfile("bank.csv")!=True:
            fields=['Account ID', 'Username','Creditcard Number','Acc Balance','PIN','issue date','expiry date']
            c=1
            
        else:
            c=0
            
            
        with open("bank.csv",'a',newline='') as csvfile:
            csvobj=csv.writer(csvfile)
            if c==1:
                csvobj.writerow(fields)
            csvobj.writerows(info)   
            csvfile.flush()

        condition = input(("\nDo you want to add more accounts? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break

    print("{} Record(s) added successfully! ".format(loop_count))



#edit Balance
def editBalance(index,L):
    edit=input("Do you want to withdraw or deposit (w/d) ?: ")
    
    if edit.upper()=='W':
        while True:
            amount=int(input("Enter amount to withdraw: "))
            if (int(L[index][3]))-amount<500:
                print("You cannot withdraw more than min balance!\a")
                condition = input(("\nDo you want to withdraw? (Y/N) "))
                condition=condition.upper()
                if condition != 'Y':
                    break
            else:
               L[index][3]=int(L[index][3])-amount
               print("You have successfully withdrawn ", amount)
               print("New Balance is: ",L[index][3])
               break
        
    elif edit.upper()=='D':
        print("Current Balance is: ",L[index][3])
        amount=int(input("Enter amount to deposit: "))
        L[index][3]=int(L[index][3])+amount
        print("You have successfully deposited ", amount)
        print("New Balance is: ",L[index][3])
        
    else:
        print("Invalid input!")

#renew account
def renew(index,L):
    valid = int(input("Validity (in years): "))
    L[index][5] = datetime.date.today()
    L[index][6] = datetime.date.today() + datetime.timedelta(weeks=valid*52)
    

#edit records with username
def edit():
    L=[]
    with open('bank.csv','r',newline='') as csvfile:
        csvobj=csv.reader(csvfile)
        for row in csvobj:
            L.append(row)
    while True:
        username=input("Enter username to edit: ")
        control=0
        for index in range(len(L)):
            if L[index][1]==username:
                control+=1
            
                print("\n\nDo you want to: \n")
                print("1: Edit Balance")
                print("2: Renew")
                choice=int(input("\n Enter choice: "))
                    
                if choice==1:
                    editBalance(index,L)
                elif choice==2:
                    renew(index,L)
                else:
                    print("invalid input")
        
        if control==0:
            print("Record not found! ")
        condition = input(("\nDo you want to edit again? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break
    with open('bank.csv','w',newline='') as f:
        csvobj1=csv.writer(f)
        csvobj1.writerows(L)
        f.flush()
        f.close()
    print("Account(s) successfully edited")



#search
def search():
    L=[]

    with open('bank.csv','r',newline='') as csvfile:
        csvobj=csv.reader(csvfile)
        for row in csvobj:
            L.append(row)
    while True:
        control=0
        user = input("Enter username: ")
        for line in L:
            if line[1] == user:
                control+=1
                for data in line:
                    print(data,'\t',end='')
        if control==0:
            print("No record with username {} found".format(user))
        condition = input(("\nDo you want to search again? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break



#delete
def delete():
    while True:
        new_data = []
        with open('bank.csv','r',newline='') as csvfile1:
            csvobj1 = csv.reader(csvfile1)
            user = input("Enter username: ")
            control=0
            for line in csvobj1:
                if line[1] == user:
                    control+=1
                    check=input("Are you sure you want to delete this record {} ? (Y/N) ".format(line))
                    if check.upper() != 'Y':
                        new_data.append(line)
                    else:
                        print("deleted successfully")
                else:
                    new_data.append(line)
            if control==0:
                print("Account not found! ")
        with open('bank.csv','w',newline='') as csvfile2:
            csvobj2 = csv.writer(csvfile2)
            csvobj2.writerows(new_data)
            csvfile2.flush()
        condition = input(("\nDo you want to delete more accounts? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break
#accounts past expiry date:
def pastexpiry():
    while True:
        L=[]
        with open('bank.csv','r',newline='') as csvfile:
            csvobj=csv.reader(csvfile)
            today=str(datetime.date.today())
            for row in csvobj:
                if row[6][0:4]<today[0:4]:
                    L.append(row)
                elif row[6][0:4]==today[0:4]:
                    if row[6][5:7]<today[5:7]:
                        L.append(row)
                    elif row[6][5:7]==today[5:7]:
                        if row[6][8:10]<today[8:10]:
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
                        renew(L.index(row),L)
                        count+=1
                if count==0:
                    print("username not present")
            elif choice==2:
                user=input("Enter username of account to delete: ")
                count=0
                for row in L:
                    if row[1]==user:
                        final=input("Are you sure you want to delete {} (y/n)? ".format(user))
                        if final.upper()=='Y':
                            L.remove(row)
                            print("Successfully deleted:",row)
                        count+=1
                if count==0:
                    print("username not present")
        
        condition = input(("\nDo you want to renew/delete more accounts? (Y/N) "))
        condition=condition.upper()
        if condition != 'Y':
            break    
             

#sort
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
        with open('bank.csv','r',newline='') as csvfile:
            csvobj=csv.reader(csvfile)
            for line in csvobj:
               L.append(line)
        if len(L)>1:
            for index1 in range(len(L)):
                for index2 in range(1,len(L)-1-index1):
                    if L[index2][n] > L[index2+1][n]:
                        L[index2] , L[index2+1] = L[index2+1] , L[index2]
            with open('bank.csv','w',newline='') as f:
                fobj=csv.writer(f)
                fobj.writerows(L)
                f.flush()
        
    
        else:
            print("Only 1 account present!!")
        display()
        
#display accounts
def display():
    with open("bank.csv",'r',newline='') as csvfile:
        csvobj=csv.reader(csvfile)
        for row in csvobj:
            print("")
            d0,d1,d2,d3,d4,d5,d6=row
            print("{:<10} \t {:<8} \t {:<20} \t {:<12} \t {:<4} \t {:<10} \t {:<10}".format(d0,d1,d2,d3,d4,d5,d6))

#change pin
def changepin():
    while True:
        L=[]
        print("You are now entering restricted area!\a")
        print("Unauthorised access is a criminal offense!\a")
        choice=input("Do you want to continue (y/n)? ")
        if choice.upper()!="Y":
            break
        else:
            control=0
            user=input("Enter username: ")
            csvfile=open("bank.csv",'r',newline='')
            read=csv.reader(csvfile)
            for row in read:
                L.append(row)
                if row[1]==user:
                    control+=1
                    print("The current PIN is: ",decrypt(row[4]))
                    check=input("Do you want to change PIN (y/n)? ")
                    if check.upper()=='Y':
                        L[L.index(row)][4] = encrypt(random.randint(1001,9998))
                        print("PIN has been changed successfully!")
            csvfile.close()
            
            if control==0:
                print("No records with username {} found".format(user))
                break
            
            else:
                with open('bank.csv','w',newline='') as f:
                    csvobj=csv.writer(f)
                    csvobj.writerows(L)
                    f.flush()
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
            L=[]
            with open("bank.csv") as f:
                csvobj=csv.reader(f)
                for row in csvobj:
                    L.append(row)
            user=input("Enter username to extend validity: ")
            count=0
            for line in L:
                if line[1]==user:
                    renew(L.index(line),L)
                    count=1
                    print("New expiry date is",line[6])
                    with open("bank.csv",'w',newline='') as f:
                        csvobj=csv.writer(f)
                        csvobj.writerows(L)
                    
            if count==0:
                print("Username not present!")
                
        elif choice=='0':
             print("Thank you...")
             break
        
        else:
            print("Invalid input! Please Try again......")

#customer interface
def customer_pg(user):
    L=[]
    f=open('bank.csv','r',newline='')
    csvobj=csv.reader(f)
    for row in csvobj:
        L.append(row)
        if row[1]==user:
            i=L.index(row)
            
    f.close()
    
    
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
            editBalance(i,L)
        
        elif choice=='2':
            with open('bank.csv','r',newline='') as f:
                csvobj=csv.reader(f)
                for row in csvobj:
                    if row[1]==user:
                        print("Your Account Balance is: ",row[3])
        
        elif choice=='3':
            with open('bank.csv','r',newline='') as f:
                csvobj=csv.reader(f)
                for row in csvobj:
                    if row[1]==user:
                        print("Your Account will expire on: ",row[6])
        
        elif choice=='4':
            with open('bank.csv','r',newline='') as f:
                csvobj=csv.reader(f)
                for row in csvobj:
                    if row[1]==user:
                        print("Dear Customer,\n")
                        print("Please note, you will be charged 500 per year you wish to renew for ")
                        choice=input("Do you want to continue (y/n)? ")
                        if choice.upper()=='Y':
                            valid = int(input("Enter Validity (in years): "))
                            L[i][5] = datetime.date.today()
                            L[i][6] = datetime.date.today() + datetime.timedelta(weeks=valid*52)
                            cost=500*valid
                            L[i][3]==int(L[i][3])-cost
        
        elif choice=='5':
            print("Your account details: \n")
            for data in L[i]:
                print(data,"\t",end='')
        
        elif choice=='6':
            control=0

            for row in L:
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
                            
                                    L[i][4] = encrypt(new_pin)
                                    print("PIN has been changed successfully!")
                                    print("Your new PIN is: ", decrypt(L[i][4]))
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
        
        with open("bank.csv",'w',newline='') as csvfile:
            csvobj=csv.writer(csvfile)
            csvobj.writerows(L)
            csvfile.flush()


#main starts here

check=4
while True:

    print("\nPlease Sign in: \n")
    username=input("Name: ")
    pin=input("Password(Pin): ")
    if username.upper()=='ADMIN' and pin=="password":
        print("You are now entering Admin page...\a")
        admin_pg()
    else:
        csvfile=open("bank.csv",'r',newline='')
        csvobj=csv.reader(csvfile)
        found=0
        for row in csvobj:
            if row[1]==username and decrypt(row[4])==pin:
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
        csvfile.flush()
        csvfile.close()
                
    control=input("\nDo you want to sign in again (Y/N): ")
    if control.upper()!='Y':
        break
    
input("Press any key to exit")


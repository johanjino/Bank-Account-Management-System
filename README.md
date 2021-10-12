# Bank-Account-Management-System

Synopsis

Bank Accounts Management System which starts with a manual data entry by admin to editing accounts. Customers get access to their account to withdraw or deposit money, as well as change their pin and renew account. Admin can access all accounts and edit all data. Credit-card number and pin number are auto-generated and duplicate credit-card numbers cannot be made. All contents are stored in a csv file. Cyber security for such systems is of huge importance, thus, pin numbers are encrypted. Hence, anyone viewing the file cannot access customers’ pin.


The program is subdivided into 2 domains:


1.	Admin interface:
 	Add accounts
 	Edit accounts
 	Search accounts
 	Delete/renew accounts which has expired
 	Delete accounts
 	Sort accounts
 	Project all accounts
 	Display/change pin
 	Renew accounts
  
2.	Customer interface:
 	Deposit/withdraw money
 	Check balance
 	Renew account
 	View account details
 	Change pin



The new system is built with the following objectives: -
•	Information retrieval will become easy.
•	Security of data stored is optimised.
•	Maintenance of data as will become easy.
•	Modification of the data will become easy.

File used:
bank.csv 

Variables used:
acc_id – Account ID number
username – Username of account
creditcard_no – Credit card number
balance - Balance in account
pin – password of the account
issue_date – Date of issue
expiry_date – Date of expiry


Modules imported:
1.	csv module
2.	random module
3.	datetime module
4.	os module



Functions:

User defined functions:

	encrypt(num): this function is used to encrpt a pin entered as parameter
	decrypt(word): this function is used to decrypt the pin from encrypted format so that the customer can view and change.
	gen_credit(): this function is used to auto-generate credit card number in such a way that a number is not repeated four times together as well as ensures that no duplicate credit card number is generated.
	addAcc(): this function is used to add new accounts. This function can only be accessed by admin user.
	editBalance(): this function is used to edit the balance of the account from admin interface.
	renew(): this function is used to renew accounts
	edit(): this function is used to edit the details of an account.
	search(): this function is used to search accounts using username. This can only be accessed by admin user.
	delete(): this function is used to delete accounts. This can only be accessed by admin user.
	pastexpiry(): this function is used to display accounts which has passed expiry date. This can only be accessed by admin user.
	sort(): this function is used to sort accounts using account ID, username, issue date or expiry date according to admin’s choice.
	display(): this function is used to display all accounts. This function can only be accessed by admin user.
	changepin(): this function is used to display or change the pin of any account. This code can only be accessed by admin. The new generated pin is randomised.
	admin_pg(): this function called if entered credentials is matches to that of admin, and redirects to the admin interface, where the admin can choose desired function from the displayed menu.
	customer_pg(): this function called if entered credentials is matched, and redirected to customer interface, where the customer can choose desired function from the displayed menu.


Built-in functions:

	int(<data>): this function is used to convert datatype to integer.
	list(<data>): this function is used to convert datatype to list.
	str(<data>): this function is used to convert datatype to string.
	input(<display>): this function allows user to input data when given string parameter is displayed.
	print(<items>): this function displays all the given items in parameter.
	open(<filename>): this function opens a file given as parameter.
	Randint(a,b): this function, imported from random module, is used to generate random integers between a and b
	date.today(): this function, imported from datetime module, is used to retrieve current data.
	reader(<file>): this function, imported from csv module, is used to return reader object of the file given as parameter.
	writer(<file>): this function, imported from csv module, is used to return writer object of the file given as parameter.
	close(<file>): this function, imported from csv module, is used to close a file after the operations are completed.
	flush(): this function, imported from csv module, is used to flush the buffer, the data will be immediately written to the file in the buffer, clear the buffer at the same time.

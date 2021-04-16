import mysql.connector  
#Create the connection object   
myconn = mysql.connector.connect(host = "localhost", user = " ",passwd = " ", database = "fraud")  
  
#printing the connection object   
print(myconn)   
  
#creating the cursor object  
cur = myconn.cursor()  
  
print(cur) 
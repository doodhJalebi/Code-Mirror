# from merkletree import *
import matplotlib.pyplot as plt


# a_dir = r"C:\Users\User\Desktop\Niha\DS2-project\New folder"
# b_dir = r"C:\Users\User\Desktop\Niha\DS2-project\folder\b"

# start_time = time.time()
# MT_a = merkletree(a_dir)
# end_time = time.time()
# print("Total time = ", end_time - start_time)


# Graph Window
w = 5
h = 5
d = 70
plt.figure(figsize=(w, h), dpi=d)

# Values of x and y are plotted after testing each case

# x-axis values 
x =  [0,100,200,300,400,500, 600, 700, 800, 900, 1000]

# y-axis values 
y =  [0.001,0.196,0.617,0.859,1.1539,1.320,1.702,2.162,2.564,2.914,3.3433]
  

plt.plot(x, y, label= "Time Taken In Building Merkle Tree Of Folder Containing n Files",marker = "*", color = "red") 

# x-axis label 
plt.xlabel('Number of Files in Source Folder') 

# y-axis label 
plt.ylabel('Time Taken In Building Merkle Tree (in seconds)') 

# plot title 
plt.title('Merkel Tree - Build Time Analysis') 

# showing legend 
plt.legend() 
  
# function to show the plot 
plt.show() 
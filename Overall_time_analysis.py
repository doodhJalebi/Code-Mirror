# from mirror import *
import matplotlib.pyplot as plt


# a_dir = r"C:\Users\User\Desktop\Niha\DS2-project\folder\a"
# b_dir = r"C:\Users\User\Desktop\Niha\DS2-project\folder\b"

# while True:
#     try:
#         start_time = time.time()
#         mirror(a_dir, b_dir)
#         end_time = time.time()
#         print("Total time = ", end_time - start_time)
#         break
#     except:
#         pass


# Values of x and y are plotted after testing each case
# x-axis values 
x =  [0,100,200,300,400,500, 600, 700, 800, 900, 1000]
# y-axis values 
y =  [1.008073091506958,1.0302975177764893,3.9004528522491455,6.805618524551392,6.246065139770508,
 7.656027317047119,7.5103678703308105,11.54430866241455,13.878087520599365,16.903316020965576,
 18.9206485748291]
  
# plotting points as a scatter plot 
plt.plot(x, y, label= "Time Taken Per n Files", color= "red",  
            marker= "*") 
  
# y-axis label 
plt.ylabel('Time Taken In Mirroring (in seconds)') 
# x-axis label 
plt.xlabel('Number of Files in Source Folder') 
# plot title 
plt.title('Code Mirror - Time Graph') 
# showing legend 
plt.legend() 
  
# function to show the plot 
plt.show() 

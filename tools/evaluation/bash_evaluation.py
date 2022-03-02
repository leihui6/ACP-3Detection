import os  
for i in range(530):
    if i > 0 and i % 20 == 0:
	    os.system('python evaluation.py {}'.format(i+1)) 
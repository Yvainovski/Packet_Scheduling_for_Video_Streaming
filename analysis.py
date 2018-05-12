import numpy as np
import matplotlib.pyplot as plt


eds_log = open('./eds_streaming_log.txt','r')
fbs_log = open('./fbs_streaming_log.txt','r')
FRAME_NUM = 510


def loss_analysis(logs,title):
	print('Analyzing EDS loss:')
	X = range(FRAME_NUM)
	Y = [1]*FRAME_NUM
	I_loss = 0
	P_loss = 0
	type_loss = [0]*5

	logs = logs.readlines()
	logs = [x.strip() for x in logs]
	#print(logs)
	for l in logs:
		if(l.split()[0] == 'Lost'):
			Y[int(l.split()[1])] = 5
			type_loss[(int(l.split()[1]) % 5)] +=1
			if(int(l.split()[1])%5==0):
				I_loss += 1
			else:
				P_loss += 1
	
	

	print(X)
	print(Y)
	print('I_loss',I_loss)
	print('P_loss',P_loss)
	uniq,counts = np.unique(Y,return_counts=True)
	print(zip(uniq,counts))
	 
	# ----------first 50 --------------------#
	plt.bar(X[:50],Y[:50])
	for i in range(0,55,5):
		plt.axvline(x=i,color='r')
	plt.title(title+' [0-50]')
	plt.xlabel('Frames')
	plt.ylabel('If Lost')
	plt.show()

	#--------------all data-------------------#
	plt.bar(X,Y)
	plt.title(title)
	plt.xlabel('Frames')
	plt.ylabel('If Lost')
	plt.show()
	
	#---------------I vs P -------------------#
	plt.bar(['P Frame','I Frame'],[I_loss, P_loss],color='lightgreen')
	plt.title(title+' I Frame Loss VS P Frame Loss')
	plt.xlabel('Frame Type')
	plt.ylabel('Lost Number')
	plt.show()
	 



def type_loss():
	print('Analyzing type loss:')
	X = range(FRAME_NUM)
	Y = [1]*FRAME_NUM
	I_loss = 0
	P_loss = 0
	eds_type_loss = [0]*5
	fbs_type_loss = [0]*5

	eds = eds_log.readlines()
	eds = [x.strip() for x in eds]
	fbs = fbs_log.readlines()
	fbs = [x.strip() for x in fbs]

	for l in eds:
		if(l.split()[0] == 'Lost'):
			eds_type_loss[(int(l.split()[1]) % 5)] +=1

	for l in fbs:
		if(l.split()[0] == 'Lost'):
			fbs_type_loss[(int(l.split()[1]) % 5)] +=1
			
	eds_type_loss = np.asarray(eds_type_loss)/float(sum(eds_type_loss))
	fbs_type_loss = np.asarray(fbs_type_loss)/float(sum(fbs_type_loss))
	
	#-----------------Type loss line------------#
	fig, ax = plt.subplots()
	ax.plot(range(5),eds_type_loss, 'r--', label='Earliest Deadline')
	ax.plot(range(5),fbs_type_loss, 'b-' , label='Frame Based Scheduling')
	legend = ax.legend( shadow=True)
	plt.title(' Type Loss Ratio')
	plt.xlabel('Frame Type')
	plt.ylabel('Lost Ratio')
	plt.xticks(np.arange(0, 5))
	plt.show()



def loss_20():
	print('Server side log with 20 percent loss rate...')
	I_num = 0
	P_num = 0
	sent_frame = [1]*FRAME_NUM 

	with open('server_log_20lossrate.txt','r') as f:
		lines = f.readlines()
		lines = [x.strip() for x in lines if(x[:4]=='Sent')]
		
		for d in lines:
			if(d.split()[1]=='FIN'):
				continue
			sent_frame[int(d.split()[1])] = 5
			if(d.split()[2]=='I'):
				I_num += 1
			elif(d.split()[2]=='P'):
				P_num += 1 

	print(sent_frame)
	print(I_num,P_num)
	plt.bar(['P Frames','I Frames'],[  P_num,I_num],color='red')
	plt.title('Frames Sent from Server - 20% Loss Rate')
	plt.xlabel('Frame Type')
	plt.ylabel('Frame Number')
	plt.show()




def loss_5():
	print('Server side log with 5 percent loss rate...')
	I_num = 0
	P_num = 0
	sent_frame = [1]*FRAME_NUM
	with open('server_log_5lossrate.txt','r') as f:
		lines = f.readlines()
		lines = [x.strip() for x in lines if(x[:4]=='Sent')]
		
		for d in lines:
			if(d.split()[1]=='FIN'):
				continue
			sent_frame[int(d.split()[1])] = 5
			if(d.split()[2]=='I'):
				I_num += 1
			elif(d.split()[2]=='P'):
				P_num += 1

	print(sent_frame)
	print(I_num,P_num)
	plt.bar(['P Frames','I Frames'],[  P_num,I_num],color='red')
	plt.title('Frames Sent from Server - 5% Loss Rate')
	plt.xlabel('Frame Type')
	plt.ylabel('Frame Number')
	plt.show()

def loss_1():
	print('Server side log with 1 percent loss rate...')
	I_num = 0
	P_num = 0
	sent_frame = [1]*FRAME_NUM
	with open('server_log_1lossrate.txt','r') as f:
		lines = f.readlines()
		lines = [x.strip() for x in lines if(x[:4]=='Sent')]
		
		for d in lines:
			if(d.split()[1]=='FIN'):
				continue
			sent_frame[int(d.split()[1])] = 5
			if(d.split()[2]=='I'):
				I_num += 1
			elif(d.split()[2]=='P'):
				P_num += 1

	print(sent_frame)
	print(I_num,P_num)
	plt.bar(['P Frames','I Frames'],[  P_num,I_num],color='red')
	plt.title('Frames Sent from Server -1% Loss Rate')
	plt.xlabel('Frame Type')
	plt.ylabel('Frame Number')
	plt.show()


def type_loss_1vs5vs20():
	print('Type loss line for various loss rates')

	loss_type_1 = [0] * 5
	loss_type_5 = [0] * 5
	loss_type_20 = [0] * 5

	# 1 percent loss rate
	with open('server_log_10lossrate.txt','r') as f:
		lines = f.readlines()
		lines = [x.strip() for x in lines if(x[:4]=='Sent')]
		
		for d in lines:
			if(d.split()[1]=='FIN'):
				continue
			loss_type_1[int(d.split()[1])%5] += 1

	# 5 percent loss rate
	with open('server_log_5lossrate.txt','r') as f:
		lines = f.readlines()
		lines = [x.strip() for x in lines if(x[:4]=='Sent')]
		
		for d in lines:
			if(d.split()[1]=='FIN'):
				continue
			loss_type_5[int(d.split()[1])%5] += 1

	# 20 percent loss rate
	with open('server_log_20lossrate.txt','r') as f:
		lines = f.readlines()
		lines = [x.strip() for x in lines if(x[:4]=='Sent')]
		
		for d in lines:
			if(d.split()[1]=='FIN'):
				continue
			loss_type_20[int(d.split()[1])%5] += 1

	print(sum(loss_type_1))
	print(sum(loss_type_5))
	print(sum(loss_type_20))

	loss_type_1 = np.asarray(loss_type_1) / float(sum(loss_type_1))
	loss_type_5 = np.asarray(loss_type_5) / float(sum(loss_type_5))
	loss_type_20 = np.asarray(loss_type_20) / float(sum(loss_type_20))
	print(loss_type_1)
	print(loss_type_5)
	print(loss_type_20)
	#----------------Type loss------------------------------------
	fig, ax = plt.subplots()
	ax.plot(range(5),loss_type_20, 'b-', label='0.20 loss rate')
	ax.plot(range(5),loss_type_1, 'r-', label='0.10 loss rate')
	ax.plot(range(5),loss_type_5, 'g-', label='0.05 loss rate')
	legend = ax.legend( shadow=True)
	plt.title('Frame Sent Ratio from Server')
	plt.xlabel('Frame Type')
	plt.ylabel('Sent Number')
	plt.xticks(np.arange(0, 5))
	plt.show()


if __name__ == '__main__':
	#loss_analysis(eds_log,'Earliest Deadline Scheduling')
	#loss_analysis(fbs_log,'Frame Based Scheduling')
	#type_loss()
	#loss_20()
	#loss_5()
	#loss_1()
	type_loss_1vs5vs20()
	
	eds_log.close()
	fbs_log.close()
	

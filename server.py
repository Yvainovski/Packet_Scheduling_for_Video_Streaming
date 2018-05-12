#Server code

import socket
import numpy as np
import cv2
import sys
import time
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
port = 8888
ack_port = 9999
ip = '10.0.0.2'
frames = list()
SEND_SIZE = 38400

M = 5
fps=25
beta=0.7
fbs_info = list()
ack_list  = [False]*510
sent_list = [False]*510
display_head = 0
start_time = None


def load_video():
	cap = cv2.VideoCapture('out.mp4')
	frame_count = 0
	pkt_count = 0
	while(cap.isOpened()):
		ret, frame = cap.read()
		if(ret == False):
			break
		else:
			# segment frames
			frame = frame.tostring()
			for k in range(6):
				bytes = frame[k*SEND_SIZE:(k+1)*SEND_SIZE]
				frames.append(bytes)
				a = frame_count % M
				d = (beta*a)/float(M-1)
				info = {'frame_num':frame_count,
					'a':a,
					'd':d,
					'deadline':frame_count/float(fps)}
				fbs_info.append(info)
				pkt_count += 1
			frame_type = 'P'
			if(frame_count % M==0):
				frame_type = 'I'
			frames.append(str(frame_count)+' '+frame_type)
			frame_count += 1
	cap.release()
	print('Video Loaded! Frame number: {}'.format((len(frames)-510)/6))

# Earliest Deadline First Algorithm
def edf_algo():
	print('EDF algirthm')
	for i,pkt in enumerate(frames):
		sock.sendto(pkt,(ip,port))
		if(len(pkt)<10):
			print('Sent {} '.format(pkt))
				#time.sleep(0.005)
	sock.sendto('FIN',(ip,port))
	print('Sent FIN')


# Frame based Scheduling algorithm
def fbs_algo():
	global display_head, start_time
	start_time = time.time()# start timer
	while True:
		print('display_head ',display_head)
		if(display_head>509):
			break
		# ------------first pass -----------
		candidate = 509
		for k in range(display_head+1,510):
			 # first pass candiate can only be unsent frame
			if(sent_list[k] == False):
				dl = fbs_info[k*6]['deadline'] -(time.time()-start_time)
				print(k,dl)
				if(dl > fbs_info[k*6]['d'] + 0 ):
					#print(dl)
					print('candidate',k)
					candidate = k
					break
		#if(candidate is None):
			#candidate = 510
		# ------------second pass---------------
		for k in range(display_head+1, candidate):
			if(ack_list[k] == False ):
				if(fbs_info[k*6]['d'] <= fbs_info[candidate*6]['d']):
					candidate = k
					print('woco {}',k)
					break
		# --------------------------------------
		for n in range(7):
			sock.sendto(frames[7*candidate+n],(ip,port))
			if(n==6):
				pkt = frames[7*candidate+n]
				sent_list[int(pkt.split()[0])] = True
				print('Sent {} '.format(pkt))
		# update display_head
		display_head = int((time.time()-start_time)/0.04)
		#print(display_head)

	sock.sendto('FIN',(ip,port))
	print('Sent FIN')


# separate socket for receiving ACK 
def rcv_ack():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
	s.bind(('',9999))
	while True:
		ack, addr = s.recvfrom(1024)
		if(ack=='FIN'):
			break
		ack_list[int(ack.split()[1])] = True
		print(ack)

	
	print(ack_list)
	
	print(sent_list)
		

def init_listener():
	t = threading.Thread(target=rcv_ack)
	t.start()
	print('ACK listener started')

def init_server():
	print('Starting Server...')
	sock.bind(('',port))
	print('Ready to stream'.format(port))
	while True:
		data, addr = sock.recvfrom(1024)
		print(data)
		if(data=='START'):
			edf_algo()
			break;
		elif(data=='FBS'):
			fbs_algo()


def main():
	load_video()
	#exit()
	init_listener()
	init_server()








if __name__ == '__main__':
	main()



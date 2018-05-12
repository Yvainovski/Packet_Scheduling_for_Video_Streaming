import numpy as np
import sys
import cv2
import socket
import threading
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
ip = '10.0.0.1' 
port = 8888
ack_port = 9999
sock.bind(('',port))
SEND_SIZE = 38400
#frame = np.zeros((240,320,3),np.uint8)
player_stat = True
rcv_buf = [None]*510



streaming_log = ''


def init_player():
	print('initing player')
	while(player_stat == True):
		player = cv2.imshow('Player', frame)
		key_in = cv2.waitKey(1)
		if (ord('q') == key_in):
			break	
	#cv2.destroyAllWindows()
	print('Player closed')


def play_video():
	global streaming_log
	while True:
		if(len(rcv_buf)>1):
		#if(rcv_buf[0] is not None):
			for i in range(510):
				frame = rcv_buf[i]
				if(frame is None):
					print('Lost {}'.format(i))
					streaming_log += 'Lost {}'.format(i)+'\n'
					cv2.imshow('Stream',np.zeros((240,320,3)))
				else:
					cv2.imshow('Stream',frame)
				key_in = cv2.waitKey(40) #25FPS
				if key_in == ord('q'):
					break	
			break
	
		cv2.destroyAllWindows()

	#---------------------Write Log---------------------_#
	with open('streaming_log.txt','w') as f:
		f.write(streaming_log)
		print('Log saved')
	#----------------------------------------------------#


def init_client():
	print('Starting client....')


def flush_rcv_data(data,i):
	global streaming_log

	if(len(data)!=SEND_SIZE*6):
		#print('Lost {}'.format(i))
		#rcv_buf.append(np.zeros((240,320,3)))
		#rcv_buf.append(None)
		#print(len(rcv_buf))
		return str()
	print('Received {} '.format(i))
	streaming_log += 'Received {} '.format(i) + '\n'
	frame = np.fromstring(data,np.uint8).reshape(240,320,3)
	rcv_buf[int(i.split()[0])]= (frame)
	sock.sendto('ACK '+i,(ip,ack_port))
	#cv2.imshow('Player',frame)
	#cv2.waitKey(1)
	return str()



def get_data():
	start_stream = False
	frame = str()
	while True:
		if(start_stream==False):
			#sock.sendto(bytes('START'),(ip,port))
			sock.sendto(bytes('FBS'),(ip,port))
			start_stream = True
		data, addr = sock.recvfrom(SEND_SIZE)
		if(data == 'FIN'):
			sock.sendto(bytes('FIN'),(ip,port))
			print('Sent FIN')
			break
		if(len(data) < SEND_SIZE ):
			frame = flush_rcv_data(frame,data)
			continue
			
		else:
			frame += data
		
	print('rv_buf len:',len(rcv_buf))
	
	


def main():
	#init_player()
	#play_video()
	
	t=threading.Thread(target=play_video)
	t.start()
	get_data()	
	
	


	

if __name__ == '__main__':
	main()


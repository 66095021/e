#!/bin/env python

import json 
import logging
import logging.handlers
import  datetime

'''
C2_Conn  is a dict 
{
orig_h:
resp_h:
resp_p:
proto:
ts_fist_time_seen:
ts_last_time_seen:
ts_last_time_calculated:
seq_len:
rank_cn:
rank_alex:

feature_group1:[]
feature_group2:[]
feature_group3:[]
feature_group4:[]
feature_group5:[]

}
'''

'''
obj_c2_conn: object of C2_Conn 
raw_datas:   list of ConnInfoJsonBB object
return: updated obj_c2_conn with feature_group*  calculates 
'''

#log to file and console 
logFormatter = logging.Formatter(
    '%(asctime)s %(filename)s[line:%(lineno)d] %(thread)s %(threadName)s %(levelname)s %(message)s'
)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.CRITICAL)
log_fileHandler = logging.handlers.RotatingFileHandler('/tmp/ConnMap.log',maxBytes=30*1024*1024, backupCount=5)
log_fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(log_fileHandler)

log_ConHandler = logging.StreamHandler()
log_ConHandler.setFormatter(logFormatter)
rootLogger.addHandler(log_ConHandler)



def conn_map(obj_c2_conn, raw_datas):
	#remove abnormal raw_datas row firstly 
	for i in raw_datas:
		if obj_c2_conn.orig_h !=  i.orig_h or   obj_c2_conn.resp_h != i.resp_h or  obj_c2_conn.resp_p != i.resp_p:
		
			logging.critical("remove abnormal row %s"%(i))
			del i

	
	#calucalte feature groups
	"""
	group1
	"""
	#avg pkt size 
	total_tcp_payload=0
	total_pkgt_number=0
	avg_pkg_size=0
	for i in raw_datas:
		total_tcp_payload=total_tcp_payload+i.orig_bytes+i.resp_bytes
		total_pkgt_number=total_pkgt_number+i.orig_pkts+i.resp_pkts
	if total_pkgt_number != 0:
		avg_pkg_size=total_tcp_payload/total_pkgt_number


	#avg pkg num
	avg_pkg_num=total_pkgt_number/len(raw_datas)
	
	#flow/connection numbers
	flow_num_accmulated=len(raw_datas)
	
	obj_c2_conn.feature_group1=[avg_pkg_size, avg_pkg_num, flow_num_accmulated]

	'''
	group2: map avg pkt size of each connection into 100 slots(16 bytes each slot unit)
	'''
	#bitmap of  100bits  string type, avg_conn_pkt_size means avg pkt size for one connection or stream
	init_bitmap_list=["0"]*100
	for i in raw_datas:
		avg_conn_pkt_size=(i.orig_bytes+i.resp_bytes)/(i.orig_pkts+i.resp_pkts)
		#only 100 slots, discard pkt too big (out of slots) of connection i 
		if avg_conn_pkt_size/16 >99:
			continue
		init_bitmap_list[avg_conn_pkt_size/16]="1"
	init_bitmap_list.reverse()
	bitmap="".join(init_bitmap_list)
	
	obj_c2_conn.feature_group2=bitmap

	
	'''
	group3: map  connections into different range by  avg pkg size  
	'''
	init_matrix=[[]]*20
	#[0,10],[11,20]...[191,200] 20 groups of 200 bytes
	for i in raw_datas:
		avg_conn_pkt_size=(i.orig_bytes+i.resp_bytes)/(i.orig_pkts+i.resp_pkts)
		if avg_conn_pkt_size/10 >20:
			continue
		init_matrix[avg_conn_pkt_size/10].append(i.ts)


	#sort it 

	for i in range(20):
		init_bitmap_list[i].sort()
	
	obj_c2_conn.feature_group3=init_bitmap_list



	"""
	groups4: numbers of no resp connections
	"""
	
	no_resp=0
	
	
	for i in raw_datas:
		if i.resp_bytes == 0:
			no_resp=no_resp+1

	obj_c2_conn.feature_group4=no_resp


	"""
	groups5: hour slots of begin time  for each connection
	"""

	init_hour_list=[0]*24

	for i in raw_datas:
		begin_time=raw_datas.ts
		#datetime.datetime.fromtimestamp(1473529000.97049).strftime('%Y-%m-%d %H:%M:%S')
		hour=datetime.datetime.fromtimestamp(1473529000.97049).strftime('%H')
		init_hour_list[int(hour)]=init_hour_list[int(hour)]+1


	obj_c2_conn.feature_group5=init_hour_list

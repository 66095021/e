#!/bin/env python

import json 
import logging
import logging.handlers
import  datetime
from operator import add

"""
merge features into first one
"""
def conn_reduce(obj_c2_conn_1, obj_c2_conn_2):
	#group 1
	avg_size=    (obj_c2_conn_1.feature_group1[0]+obj_c2_conn_2.feature_group1[0])/2
	avg_pkg_num= (obj_c2_conn_1.feature_group1[1]+obj_c2_conn_2.feature_group1[1])/2
	avg_flow=    (obj_c2_conn_1.feature_group1[2]+obj_c2_conn_2.feature_group1[2])/2
	obj_c2_conn_1.feature_group1=[avg_size, avg_pkg_num,avg_flow]

	#group 2: or on each string bit 
	o1=list(obj_c2_conn_1.feature_group2)
	o2r=list(obj_c2_conn_2.feature_group2)
	o3=[]
	for i in range(100):
		foo=int(o1[i])|int(o2[i])
		o3.append(str(foo))

	obj_c2_conn_1.feature_group2="".join(o3)

	#group3 add on each element 
	
	new_feature3=[]
	
	for i in range(20):
		new_element= obj_c2_conn_1.feature_group3[i]+obj_c2_conn_2.feature_group3[i]
		new_element.sort()
		new_feature3.append(new_element)

	obj_c2_conn_1.feature_group3=new_feature3

	#group4
	obj_c2_conn_1.feature_group4=obj_c2_conn_1.feature_group4+obj_c2_conn_2.feature_group4


	#group5
	new_list=map(add, obj_c2_conn_1.feature_group5, obj_c2_conn_2.feature_group5)
	obj_c2_conn_1.feature_group5=new_list

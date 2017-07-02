#coding=utf-8
import os
can_multi_N=3
can_add_N=3

str_num_map={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
num_str_map={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9'}

def main():	
	global Max
	Max=1
	for i in range( can_add_N ):
		Max = Max*10	
	# print add('-30','-0000')
	# print form_str('-00')
	# multi('0020','-00200')
	# half_num('13',3)
	# print multi_div( (('1334',0 ),('3662',0)) )
	# print multi_sub( '12323','234' )
	# print add( '264','3678000' )
	# print cal_input( '1223435 * 23242 - 28452543 - 3452345 * 245' )
	# print cmp_level('+','-')
	# a=[1,23,3,4]
	# a[2:3]=[]
	# print a
	# print type(4/10)
	
	
	
def cal_input( str ):
	items = str.split( ' ' )
	if len(items)==1:
		return form_str(str)
	i=1
	while i<len(items):
		if items[i]=='*':
			res_tmp = multi( items[i-1] , items[i+1] )
			items.insert(i-1,res_tmp)
			items[i:i+3]=[]
			i=i-1
		i=i+1
	print items
	while 1 < len(items):
		if items[1]=='+':
			res_tmp = add( items[0] , items[2] )
			items.insert(0,res_tmp)
			items[1:4]=[]
			
		elif items[1]=='-':
			res_tmp = minus( items[0] , items[2] )
			items.insert(0,res_tmp)
			items[1:4]=[]
	return items[0]
	
# "123456789" * "123456789"
def multi( str1 , str2 ):
	str1 = form_str( str1 )
	str2 = form_str( str2 )
	
	F1 = -1 if ('-' in str1 ) else 1
	F2 = -1 if ('-' in str2 ) else 1
	str1=str1[1:] if '-' in str1 else str1
	str2=str2[1:] if '-' in str2 else str2
	C='-' if F1*F2==-1 else ''
	return C + multi_sub( str1,str2 )
	
def mul_and_sum( cal_list ):
	add_list=[]
	for li in cal_list:
		num1 = str2num ( li[0][0] )
		num2 = str2num ( li[1][0] )
		res_num = num1*num2
		res_str = num2str( res_num )
		add_list.append( ( res_str , li[0][1]+li[1][1]) )
	SUM_str = '0'
	for li in add_list:
		SUM_str = add( SUM_str , li[0]+'0'*li[1] )
	return SUM_str
		
def multi_sub( str1 , str2 ):
	multi_list=[ ((str1,0),(str2,0)) ]
	cal_list=[]
	while multi_list!=[]:
		for li in multi_list:
			if len( li[0][0] )<=can_multi_N and len( li[1][0] )<=can_multi_N:
				cal_list.append( li )
				multi_list.remove( li )
			else:
				divs = multi_div( li )
				multi_list.remove( li )
				multi_list.extend( divs )
	return mul_and_sum( cal_list )	
	
def half_num( str , p ):
	headn = len(str)/2
	head = str[:headn]
	tail = str[headn:]
	return ( head,p+len(tail) ), ( tail,p )
	
def multi_div( li ):	#li = (( str1 , p1) , (str2 , p2 ))
	str1=li[0][0]
	str2=li[1][0]
	if len( str1 )<=can_multi_N and len( str2 )<=can_multi_N:
		return li
	if len( str1 )>can_multi_N and len( str2 )>can_multi_N:
		A , B = half_num( str1 , li[0][1] )
		C , D = half_num( str2 , li[1][1] )
		return [ (A , C),( A , D ),( B , C ),( B , D ) ]
	if len( str1 )> can_multi_N:
		A , B = half_num( str1 , li[0][1] )
		return ( ( A , li[1]) , (B , li[1]) )
	else:
		C , D = half_num( str2 , li[1][1] )
		return ( ( li[0] , C) , ( li[0] , D ) )
		
# just can_add_convert
def str2num( str ):	
	ifplus=1
	output=0
	if str[0]=='-':
		str=str[1:]
		ifplus=-1	
	for i in range( len(str) ):
		output=output*10+str_num_map[ str[i] ]
	return output*ifplus

def num2str_formed( num ):
	global Max
	flag=0
	if num<0:
		num = Max + num
		flag=-1
	if num>=Max:
		num=num-Max
		flag=1
	str = num2str( num )	
	return '0'*( can_add_N-len(str) )+str,flag
	
def form_str( str ):
	flag=''
	if str[0]=='-':
		flag='-'
		str=str[1:]
	str = str.lstrip('0')
	if str=='':
		return '0'
	else:
		return flag+str

def num2str( num ):
	flag=''
	if num==0:
		return '0'
	if num < 0:
		flag='-'
		num=-num
	outstr=''
	while( num > 0 ):
		outstr= num_str_map[ num%10 ]+outstr
		num=num/10
	return flag+outstr
# "123456789" + "123456789"

def get_res_flag( str1, F1 , str2 , F2 ):
	if( F1*F2 == 1 ):		#同号
		return F1
	if len( str1 )>len( str2 ):		#异号
		return F1
	if len( str2 ) > len( str1 ):
		return F2
	if str1 > str2:
		return F1	
	if str1 < str2:
		return F2	
	return 1
	
def add_sub( str1, F1 , str2 , F2):
	head,sum,C = add_step( str1, F1 , str2 , F2 )
	while( C != 0 ):		
		head,sum_tmp,C = add_step( head , 1, '1',C )
		sum = sum_tmp + sum
	if( head == '0' ):
		res = sum.lstrip('0')
		return res if res!='' else '0'
	else:
		res = (head+sum).lstrip('0')
		return res if res!='' else '0'
def minus(str1,str2):
	if str2[0]=='-':
		return add( str1 , str2[1:] )
	else:
		return add( str1 , '-'+str2 )
	
		
def add( str1,str2 ):
	str1 = form_str(str1)
	str2= form_str(str2)

	F1 = -1 if ('-' in str1 ) else 1
	F2 = -1 if ('-' in str2 ) else 1
	str1=str1[1:] if '-' in str1 else str1
	str2=str2[1:] if '-' in str2 else str2
		
	res_flag=get_res_flag( str1,F1,str2,F2 )
	if res_flag==1:
		return add_sub( str1,F1,str2,F2 )
	else:
		return '-'+add_sub( str1,-1*F1,str2,-1*F2 )

def add_step( str1, F1 , str2 , F2 ):		#运算结果为正数	
	C=0
	SUM_str=''
	if( str1==str2 and F1*F2==-1):
		return '0','0',0				# head body C
	while( len(str1)>0 and len(str2)>0 ):		#还有数未计算
		if( len(str1) )>= can_add_N:
			str1_out_str = str1[ -can_add_N: ]
			str1 = str1[:len(str1)-can_add_N]		
		else:
			str1_out_str = str1
			str1=''						#str1出数
		if( len(str2) )>= can_add_N:
			str2_out_str = str2[ -can_add_N: ]
			str2 = str2[:len(str2)-can_add_N]
		else:
			str2_out_str = str2
			str2=''						#str2出数
		str1_out_num=str2num(str1_out_str)*F1	#121
		str2_out_num=str2num(str2_out_str)*F2	#-41
		
		res_tmp_num=str1_out_num + str2_out_num + C  #运算结果num   
		res_tmp_str,C = num2str_formed(res_tmp_num)			 #运算结果str
		
		SUM_str=res_tmp_str + SUM_str		#整合运算结果
		
	if( len(str1)>0 ):	
		return str1,SUM_str,C		
	elif( len(str2)>0 ):
		return str2,SUM_str,C
	else:
		return '0',SUM_str,C


	
	
if __name__=='__main__':
	main()

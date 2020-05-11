
import csv
import gc
import os
from math import radians, cos, sin, asin, sqrt
import json
from collections import OrderedDict



def HaversineKM(latA, lonA, latB, lonB):
	R = 6371;
	
	#print("Point A is ", latA, lonA, "Point B is ", latB, lonB)
	lat1 = float(latA)
	lat2 = float(latB)
	lon1 = float(lonA)
	lon2 = float(lonB)
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	return c* R 

def HaversineMI(latA, lonA, latB, lonB):
	R = 3956;
	#print("Point A is ", latA, lonA, "Point B is ", latB, lonB)
	lat1 = float(latA)
	lat2 = float(latB)
	lon1 = float(lonA)
	lon2 = float(lonB)
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	return c* R 

def bin_search(data, target, low, high):
	#print("this is target ",target)
	if low > high:
		return False
	else:
		mid = (low + high) // 2
		#print("this is target ",mid)
		if target == data[mid]:
			return True
			
		elif target < data[mid]:
			return bin_search(data, target,low, mid -1)
		else:
			return bin_search(data, target, mid+1,high)

def mergeSort(arr):
	if len(arr) >1: 
		mid = len(arr)//2 #Finding the mid of the array 
		L = arr[:mid] # Dividing the array elements  
		R = arr[mid:] # into 2 halves 
		
		mergeSort(L) # Sorting the first half 
		mergeSort(R) # Sorting the second half 

		i = j = k = 0
		
		# Copy data to temp arrays L[] and R[] 
		while i < len(L) and j < len(R): 
			if L[i] < R[j]: 
				arr[k] = L[i] 
				i+=1
				
			else:
				arr[k] = R[j] 
				j+=1
			k+=1
		# Checking if any element was left 
		while i < len(L): 
			arr[k] = L[i] 
			i+=1
			k+=1

		while j < len(R): 
			arr[k] = R[j] 
			j+=1
			k+=1

def ZipsMechanic(var, Zips):
	print(" ")
	print(" -",var["Zipcode"], var["City"], ", ",var["State"])
	print(" ")
	if var['ZipCodeType'] != "MILITARY":
		CompleteZips= []
		for p in Zips:
			if p['ZipCodeType'] != "MILITARY":
				ChecNum =str(var['Zipcode']).zfill(5) + str(p['Zipcode']).zfill(5)
				ChecNum2 =str(p['Zipcode']).zfill(5) + str(var['Zipcode']).zfill(5)
				hgh = len(UsedCodes) -1
				#print("De la nada.")
				sdic={}
				sdic['ZipcodeA'] = var['Zipcode']
				sdic['ZipcodeB'] = p['Zipcode']
				sdic['KM']= HaversineKM(var['Lat'],var['Long'],p['Lat'],p['Long'])
				sdic['MI']= HaversineMI(var['Lat'],var['Long'],p['Lat'],p['Long'])
				#print("Que hacemos", ChecNum, ChecNum2)
				if sdic['MI'] <= 300:
					CompleteZips.append(sdic)
		print("Creating File file for ", var["Zipcode"])
		print("Size of Used Codes is ", len(UsedCodes))
		print("Size of Complete Zips Codes BEFORE is ", len(CompleteZips))
		#result = {frozenset(item.items()) : item for item in CompleteZips}.values()
		#CompleteZips = result
		print("Size of Complete Zips Codes AFTER is ", len(CompleteZips))
		jsString = json.dumps(CompleteZips)
		f= open("G:\Zips\\" + var['Zipcode'] +".json", "w+")
		f.write(jsString)
		f.close()
		gc.collect()
	
def ConZips(arr, RAW):
	
	
	if len(arr) > 1:

		mid = len(arr)//2
		print(mid)
		L = arr[:mid]
		R = arr[mid:]
		
		ConZips(L, RAW)
		ConZips(R, RAW)
		
		i = j = k = 0
		
		
		while i < len(L) and j < len(R):
			filepL = "G:\Zips\\" + L[i]['Zipcode'] +".json"
			if os.path.isfile(filepL) == False:
				ZipsMechanic(L[i], RAW)
				i+=1
			else:
				i+=1
			filepR = "G:\Zips\\" + R[j]['Zipcode'] +".json"
			if os.path.isfile(filepR) == False:
				ZipsMechanic(R[j], RAW)
				j+=1
			else:
				j+=1
			k+=1
		while i < len(L):
			filepL = "G:\Zips\\" + L[i]['Zipcode'] +".json"
			if os.path.isfile(filepL) == False:
				ZipsMechanic(L[i], RAW)
				i+=1
				k+=1
			else:
				i+=1
				k+=1
			
		while j < len(R):
			filepR = "G:\Zips\\" + R[j]['Zipcode'] +".json"
			if os.path.isfile(filepR) == False:
				ZipsMechanic(R[j], RAW)
				j+=1
				k+=1
			else:
				j+=1
				k+=1
	
	
	
i=0
Zips = []
#UsedZp= []
zp = {"ZIPCODES":[]}
codes = zp["ZIPCODES"]
csv.register_dialect('myDialect',
delimiter = ',',
skipinitialspace=True)
with open("/pythonscripts/pyzipcodes/assets/ZipCodes.csv", 'r') as csvfile:
	reader = csv.DictReader(csvfile, dialect='myDialect')
	for row in reader:
		#print(dict(row))
		#print(reader)
		info = dict(row)
		Zips.append(info)
		
		#print(info['City'])
		#print(info['Zipcode'])
		#print(i)
		i=i+1
csvfile.close()

length = len(Zips)
i= 0
last = length -1
UsedCodes= []
print("Size Before", len(Zips))
m = len(Zips) -1
for i in range(len(Zips)):
	if i > 0 and i < len(Zips):
		#print(i)
		if Zips[i]["Zipcode"] == Zips[i-1]["Zipcode"]:
			#print("Deleting ", Zips[i-1], " on ", i-1)
			del Zips[i-1]

print("Size After", len(Zips))

ConZips(Zips, Zips)
'''
while i < length:
	t= i+1
	v= i-1
	print(Zips[i]["Zipcode"])
	print(Zips[i]["City"])
	print(Zips[i]["State"])
	print(" ")
	if Zips[i]['ZipCodeType'] != "MILITARY":
		if (Zips[i]["Zipcode"] == Zips[t]["Zipcode"]) and (i < last):
			i=i+1
			continue
		CompleteZips= []
		for p in Zips:
			if p['ZipCodeType'] != "MILITARY":
				ChecNum =str(Zips[i]['Zipcode']).zfill(5) + str(p['Zipcode']).zfill(5)
				ChecNum2 =str(p['Zipcode']).zfill(5) + str(Zips[i]['Zipcode']).zfill(5)
				hgh = len(UsedCodes) -1
				if (len(UsedCodes) == 0):
						#print("De la nada.")
						sdic={}
						sdic['ZipcodeA'] = Zips[i]['Zipcode']
						sdic['ZipcodeB'] = p['Zipcode']
						sdic['KM']= HaversineKM(Zips[i]['Lat'],Zips[i]['Long'],p['Lat'],p['Long'])
						sdic['MI']= HaversineMI(Zips[i]['Lat'],Zips[i]['Long'],p['Lat'],p['Long'])
						#print("Que hacemos", ChecNum, ChecNum2)
						if sdic['MI'] <= 300:
							CompleteZips.append(sdic)
						#if ChecNum != ChecNum2:
							#print("Disme 1", ChecNum, ChecNum2)
							#UsedCodes.append(int(ChecNum))
							#UsedCodes.append(int(ChecNum2))
						#if ChecNum == ChecNum2:
							#print("Tu Supite 1", ChecNum, ChecNum2)
							#UsedCodes.append(int(ChecNum))
						#print("Used Size A ", len(UsedCodes))
				elif (len(UsedCodes) > 0):
					#if (bin_search(UsedCodes, int(ChecNum), 0, hgh) == False) and (bin_search(UsedCodes, int(ChecNum2), 0, hgh) == False):
					#print("Dime Bobby esta False.", UsedCodes, int(ChecNum))
					sdic={}
					sdic['ZipcodeA'] = Zips[i]['Zipcode']
					sdic['ZipcodeB'] = p['Zipcode']
					sdic['KM']= HaversineKM(Zips[i]['Lat'],Zips[i]['Long'],p['Lat'],p['Long'])
					sdic['MI']= HaversineMI(Zips[i]['Lat'],Zips[i]['Long'],p['Lat'],p['Long'])
					if sdic['MI'] <= 300:
						CompleteZips.append(sdic)
					#if ChecNum != ChecNum2:
						#print("OJO...", ChecNum)
						#UsedCodes.append(int(ChecNum))
						#UsedCodes.append(int(ChecNum2))
					#if ChecNum == ChecNum2:
						#UsedCodes.append(int(ChecNum))
					#print("List is...", len(UsedCodes))
		#mergeSort(UsedCodes)
		#list(OrderedDict.fromkeys(UsedCodes))
		print("Creating File file for ", Zips[i]["Zipcode"])
		print("Size of Used Codes is ", len(UsedCodes))
		print("Size of Complete Zips Codes BEFORE is ", len(CompleteZips))
		#result = {frozenset(item.items()) : item for item in CompleteZips}.values()
		#CompleteZips = result
		print("Size of Complete Zips Codes AFTER is ", len(CompleteZips))
		jsString = json.dumps(CompleteZips)
		f= open("G:\Zips\\" + Zips[i]['Zipcode'] +".json", "w+")
		f.write(jsString)
		f.close()
		gc.collect()
	i=i+1
'''




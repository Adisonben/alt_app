#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageOps, ImageDraw
from escpos import *
import json,sys

def imgFont(thai_text,font_size=23,line_height=5):
	font = ImageFont.truetype('resources/fonts/Loma.ttf', font_size)
	height_width = font.getsize(thai_text)
	image = Image.new('RGB', (height_width[0], line_height + height_width[1]))
	draw = ImageDraw.Draw(image)
	draw.text((0, 0), thai_text, font=font)
	#print "Print slip Width x Height= "+str(height_width[0])+"x"+str(line_height + height_width[1])
	return ImageOps.invert(image)

def PrintOut():
	Epson = printer.Usb(0x04b8,0x0e11)
	try:
		#print json.dumps(obj, indent=4, sort_keys=True)
		file = open("cache/db/"+sys.argv[1], "r")
		obj = json.loads(file.read())
		#print obj
		obj_status = 'OK'
		try:
			if obj['obj'] == 'OK':
				obj_status = 'OK'
			else:
				obj_status = 'FAIL'
		except Exception as e:
			#print e
			obj_status = 'FAIL'
		if obj_status == 'FAIL':
			sys.exit()
		else:
			departure_at = obj['departure_at']
			destination = obj['destination']
			full_date = obj['full_date']
			full_name = obj['full_name']
			id_card = obj['id_card']
			birthdate = obj['birthdate']
			license_exp  = obj['license_exp']
			license_number  = obj['license_number']

			alcohol_load  = obj['alcohol']
			alcohol_result  = obj['result']
			reaction_load  = obj['reaction_time']
			pulse_load  = obj['heart_rate']

			company = obj['company']+" "
			machine_code = obj['machine_code']
			machine_location = obj['machine_location']

		Epson.set(align='center')
		Epson.image('resources/images/slip_logo.jpg') # Logo

		#Epson.control('LF')

		Epson._convert_image(imgFont(u"ALCOHOL TESTER ID DRIVES",34,0))

		Epson.control('LF')
		#Epson.control('LF')
		Epson.set(align='left')

		Epson._convert_image(imgFont(u"วันที่ทดสอบ: "+full_date))
		Epson._convert_image(imgFont(u"ชื่อผู้ขับรถ: "+full_name+u" "))
		Epson._convert_image(imgFont(u"เลขประจำตัว: "+id_card))

		#Epson._convert_image(imgFont(u" วันเดือนปีเกิด: "+birthdate))
		#Epson._convert_image(imgFont(u" เดือนปีที่บัตรหมดอายุ: "+license_exp))
		#Epson._convert_image(imgFont(u" รหัสผู้ขับรถ: "+license_number))

		Epson._convert_image(imgFont(u"ชื่อบริษัท: "+company))
		Epson._convert_image(imgFont(u"เครื่องทดสอบ: "+machine_code))
		Epson._convert_image(imgFont(u"ที่ตั้งเครื่องทดสอบ: "+machine_location))

		Epson._convert_image(imgFont(u"ปริมาณแอลกอฮอล์: "+alcohol_load+u" mg/100ml"))
		#Epson._convert_image(imgFont(u" ผลทดสอบปฏิกิริยา: "+reaction_load))
		#Epson._convert_image(imgFont(u" ผลตรวจวัดชีพจร: "+pulse_load))
		Epson._convert_image(imgFont(u"สรุปผลการทดสอบ: "+alcohol_result))

		Epson.set(align='center')

		Epson._convert_image(imgFont(u"-----------------------------------------------------------"))
		Epson._convert_image(imgFont(u" เครื่องทดสอบปริมาณแอลกอฮอล์อิเล็กทรอนิกส์ "))
		Epson._convert_image(imgFont(u" Breath alcohol tester : IDAL-ONE "))
		Epson._convert_image(imgFont(u"-----------------------------------------------------------"))

		Epson.cut()
		print "#PRINT_SUCCESS#"
		#Epson.close()

	except Exception as e:
		#print e
		Epson.cut()
		print "#PRINT_FAIL#"

PrintOut()

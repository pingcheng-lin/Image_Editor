from tkinter import *
from PIL import Image, ImageTk, ImageFilter
from tkinter import filedialog
import cv2
import numpy
from matplotlib import pyplot as plt
import math

def open_file():
	global left_img, flag, window, copy, load, adjust_height, adjust_width, org_height, org_width

	#find location
	window.imgname = filedialog.askopenfilename(title = "Select A File", filetypes = (("tif files","*.tif"), ("all Files", "*.*")))

	#check if user celect a file
	if window.imgname:
		flag = 1
	else: return

	#use openCV read
	load = cv2.imread(window.imgname)
	load = cv2.cvtColor(load,cv2.COLOR_BGR2RGB)

	#adjust image's one side to 200 and other side has same magnification to show
	org_width, org_height = load.shape[:2]
	if org_height >= org_width:
		adjust = 200 / org_height
	else:
		adjust = 200 / org_width
	adjust_width = int(adjust * org_width)
	adjust_height = int(adjust * org_height)
	load = cv2.resize(load, (adjust_width, adjust_height), interpolation = cv2.INTER_LINEAR)
	left_img = ImageTk.PhotoImage(Image.fromarray(load))#tkinter store and display images using PhotoImage class
	current_left_img = Label(window, image = left_img, width = 300, height = 300)
	current_left_img.place(x = 100, y = 0)

	#avoid directly change the original image
	copy = load.copy()
	show_img()

def save_file():
	if flag:
		#change the size of original image
		finalw = int(slider_zoom.get()/100*org_width)
		finalh = int(slider_zoom.get()/100*org_height)
		final_copy = cv2.resize(copy, (finalw, finalh), interpolation = cv2.INTER_LINEAR)
		final_copy = cv2.cvtColor(final_copy,cv2.COLOR_RGB2BGR)
		#replace the original image with new one	
		cv2.imwrite(window.imgname,final_copy)

def reset_file():
	global copy
	if flag:
		current_img.destroy()
		copy = load.copy()
		slider_zoom.set(100)
		brighta.set(1)
		brightb.set(0)
		red.set(1)
		green.set(1)
		blue.set(1)
		show_img()

def zoom():
	global copy
	#check if user celect a file
	if flag:
		current_img.destroy()
		#adjust the size according to the slider
		tempw = int(slider_zoom.get()/100*adjust_width)
		temph = int(slider_zoom.get()/100*adjust_height)
		copy = cv2.resize(copy, (tempw, temph), interpolation = cv2.INTER_LINEAR)
		show_img()

def bright():
	global copy
	if flag:
		current_img.destroy()
		#get the property of image
		rows, cols, channels = copy.shape
		a = brighta.get()
		b = brightb.get()
		#linear operation 
		for i in range(rows):
			for j in range(cols):
				for c in range(3):
					color = (copy[i,j][c] * a + b)
					if color > 255:
						copy[i,j][c] = 255
					elif color < 0:
						copy[i,j][c] = 0
					else:
						copy[i,j][c] = color
		show_img()

def color():
	global copy
	if flag:
		current_img.destroy()
		#get the property of image
		rows, cols, channels = copy.shape
		rgb = [red.get(), green.get(), blue.get()]
		#linear operation 
		for i in range(rows):
			for j in range(cols):
				for c in range(3):
					color = copy[i,j][c] * rgb[c]
					if color > 255:
						copy[i,j][c] = 255
					elif color < 0:
						copy[i,j][c] = 0
					else:
						copy[i,j][c] = color
		show_img()

def complement():
	global copy
	if flag:
		current_img.destroy()
		copy[:, :, 0] = 256 - copy[:, :, 0]#256-red
		copy[:, :, 1] = 256 - copy[:, :, 1]#256-green
		copy[:, :, 2] = 256 - copy[:, :, 2]#256-blue
		tempw = int(slider_zoom.get()/100*adjust_width)
		temph = int(slider_zoom.get()/100*adjust_height)
		show_img()

def show_img():
	global new_img, current_img
	new_img = ImageTk.PhotoImage(Image.fromarray(copy))#tkinter store images
	current_img = Label(window, image = new_img, width = 300, height = 300)
	current_img.place(x = 450, y = 0)

if __name__ == '__main__':
	#create a new window
	window = Tk()
	#set the window title
	window.title('DIP')
	#avoid unnecessary warning
	numpy.seterr(over = 'ignore')

	#check whether open a file
	flag = 0

	#create label widgets
	label_ratio = Label(window, text = "ratio", font = 15, width = 10, height = 1)
	label_constant = Label(window, text = "constant", font = 15, width = 10, height = 1)
	label_red = Label(window, text = "r", font = 15, width = 10, height = 1)
	label_green = Label(window, text = "g", font = 15, width = 10, height = 1)
	label_blue = Label(window, text = "b", font = 15, width = 10, height = 1)
	#create button widgets
	button_open = Button(window, text = 'Open', command = open_file)
	button_save = Button(window, text = 'Save', command = save_file)
	button_reset = Button(window, text = 'Reset', command = reset_file)
	button_bright = Button(window, text = 'Brightness', command = bright)
	button_zoom = Button(window, text = "Zoom", command = zoom)
	button_color = Button(window, text = 'color', command = color)
	button_complement = Button(window, text = 'complement', command = complement)
	#create a slider widget
	brighta = Scale(window, from_ = 0, to = 2, length = 150, orient = HORIZONTAL, resolution = 0.1)
	brighta.set(1)
	brightb = Scale(window, from_ = -255, to = 255, length = 150, orient = HORIZONTAL)
	brightb.set(0)
	slider_zoom = Scale(window, from_ = 50, to = 150, length = 150, orient = HORIZONTAL)
	slider_zoom.set(100)
	red = Scale(window, from_ = 0, to = 2, length = 150, orient = HORIZONTAL, resolution = 0.1)
	red.set(1)
	green = Scale(window, from_ = 0, to = 2, length = 150, orient = HORIZONTAL, resolution = 0.1)
	green.set(1)
	blue = Scale(window, from_ = 0, to = 2, length = 150, orient = HORIZONTAL, resolution = 0.1)
	blue.set(1)

	#place labels
	label_ratio.place(x = 70, y = 315)
	label_constant.place(x = 65, y = 355)
	label_red.place(x = 375, y = 320)
	label_green.place(x = 375, y = 360)
	label_blue.place(x = 375, y = 400)
	#place buttons
	button_open.place(x = 0, y = 0)
	button_save.place(x = 0, y = 50)
	button_reset.place(x = 0, y = 100)
	button_bright.place(x = 0, y = 330)
	button_zoom.place(x = 50, y = 395)
	button_color.place(x = 350, y = 355)
	button_complement.place(x = 650, y = 355)
	#place sliders
	brighta.place(x = 150, y = 300)
	brightb.place(x = 150, y = 340)
	slider_zoom.place(x = 150, y = 380)
	red.place(x = 450, y = 300)
	green.place(x = 450, y = 340)
	blue.place(x = 450, y = 380)

	#draw the window
	window.geometry("800x500")
	#start the 'application'
	window.mainloop()

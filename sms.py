from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests
import bs4


# - - FUNCTIONS - - - - - - - - - -
def validate(rv, nv, mv):
	r = rv; n = nv; m = mv
	#print(r,n,m)
	if r == "":
		showerror('Error', 'Rno cannot be blank.')
		add_window_ent_rno.delete(0,END)
		update_window_ent_rno.delete(0,END)
		add_window_ent_rno.focus()
		update_window_ent_rno.focus()
		return(None,None,None)
	elif not r.isdigit():
		showerror('Error','Roll has to be numeric.')
		add_window_ent_rno.delete(0,END)
		update_window_ent_rno.delete(0,END)
		add_window_ent_rno.focus()
		update_window_ent_rno.focus()
		return(None,None,None)
	elif int(r) == 0:
		showerror('Error', 'Rno cannot be zero.')
		add_window_ent_rno.focus()
		update_window_ent_rno.focus()
		return(None,None,None)
	elif int(r) < 0:
		showerror('Error', 'Rno should be positive integers.')
		add_window_ent_rno.focus()
		update_window_ent_rno.focus()
		return(None,None,None)
	elif n == "":
		showerror('Error', 'Name cannot be blank.')
		add_window_ent_name.focus()
		update_window_ent_name.focus()
		return(None,None,None)
	elif not n.isalpha():
		showerror('Error', 'Name cannot be numeric')
		add_window_ent_name.delete(0,END)
		update_window_ent_name.delete(0,END)
		add_window_ent_name.focus()
		update_window_ent_name.focus()
		return(None,None,None)
	elif (len(n)) < 2:
		showerror('Error', 'Please enter a valid name.')
		add_window_ent_name.focus()
		update_window_ent_name.focus()
		return(None,None,None)
	elif m == "":
		showerror('Error', 'Marks cannot be blank.')
		add_window_ent_marks.focus()
		update_window_ent_marks.focus()
		return(None,None,None)
	elif not m.isdigit():
		showerror("Error","Marks has to be numeric.")
		add_window_ent_marks.delete(0,END)
		update_window_ent_marks.delete(0,END)
		add_window_ent_marks.focus()
		update_window_ent_marks.focus()
		return(None,None,None)
	elif int(m) < 0 or int(m) > 100: 
		showerror('Error', 'Marks should be in range 0-100.')
		add_window_ent_marks.focus()
		update_window_ent_marks.focus()
		return(None,None,None)
	else:
		vrno = int(r); vname = n; vmarks = int(m)
		return(vrno, vname, vmarks)

def f1():
	add_window.deiconify()
	main_window.withdraw()
	add_window_ent_rno.focus()

def f2():
	main_window.deiconify()
	add_window.withdraw()
	add_window_ent_rno.delete(0,END)
	add_window_ent_name.delete(0,END)
	add_window_ent_marks.delete(0,END)

def f3():
	view_window.deiconify()
	main_window.withdraw()
	view_window_st_data.delete(1.0, END)
	info = ""
	header = 'Rno.'+'\t'+'Names'+'\t'+' Marks' + '\n'
	con = None
	try:
		con = connect('kc.db')
		cursor = con.cursor()
		sql = "select * from student order by rno"
		cursor.execute(sql)
		data = cursor.fetchall()
		view_window_st_data.insert(INSERT,header)
		for d in data:
			info = info +str(d[0]) + '\t' + str(d[1]) + '\t  ' + str(d[2]) + '\n'
		view_window_st_data.insert(INSERT, info)
	except Exception as e:
		showerror('Failure', e)
	finally:
		if con is not None:
			con.close()

def f4():
	main_window.deiconify()
	view_window.withdraw()

def f5():
	rno = add_window_ent_rno.get()
	name = add_window_ent_name.get()
	marks = add_window_ent_marks.get()
	db_rno=[]
	vrno, vname, vmarks = validate(rno, name, marks)
	con = None
	if vrno != None:	
		try:
			con = connect('kc.db')
			cursor = con.cursor()
			get_rno = "select rno from student"
			cursor.execute(get_rno)
			data = cursor.fetchall()
			for d in data:
				db_rno.append(d[0])
			if vrno in db_rno:
				showwarning("Warning","Roll no. is already in use.")
				con.rollback()	
			else:
				sql = "insert into student values('%d', '%s', '%d')"
				cursor.execute(sql % (vrno, vname, vmarks))
				showinfo('Success', 'Record added')			
				con.commit()
			add_window_ent_rno.delete(0,END)
			add_window_ent_name.delete(0,END)
			add_window_ent_marks.delete(0,END)
		except Exception as e:
			showerror('Failure', e)
			#print(e)
		finally:
			if con is not None:
				con.close()

def f6():
	update_window.deiconify()
	main_window.withdraw()
	update_window_ent_rno.focus()

def f7():
	main_window.deiconify()
	update_window.withdraw()
	update_window_ent_rno.delete(0,END)
	update_window_ent_name.delete(0,END)
	update_window_ent_marks.delete(0,END)

def f8():
	con = None
	rno = update_window_ent_rno.get()
	name = update_window_ent_name.get()
	marks = update_window_ent_marks.get()
	vrno, vname, vmarks = validate(rno, name, marks)
	if vrno != None:
		try:
			con = connect('kc.db')
			cursor = con.cursor()
			sql = "update student set name='%s', marks='%d' where rno ='%d' "
			cursor.execute(sql % (vname, vmarks, vrno))
			if cursor.rowcount>0:
				showinfo('Success', 'Record updated')
				con.commit()
			else:
				showerror('Retry', 'Record doesnt exist')
			update_window_ent_rno.delete(0,END)
			update_window_ent_name.delete(0,END)
			update_window_ent_marks.delete(0,END)
		except Exception as e:
			showerror('Failure', e)
		finally:
			if con is not None:
				con.close()

def f9():
	delete_window.deiconify()
	main_window.withdraw()
	delete_window_ent_rno.focus()

def f10():
	main_window.deiconify()
	delete_window.withdraw()
	delete_window_ent_rno.delete(0,END)

def f11():
	con = None
	rno = delete_window_ent_rno.get()
	if rno == '':
		showwarning("Warning","Roll cannot be blank.")
		delete_window_ent_rno.focus()
	elif not rno.isdigit():
		showwarning("Warning","Roll has to be numeric.")
		delete_window_ent_rno.delete(0,END)
		delete_window_ent_rno.focus()
	else:
		try:
			con = connect('kc.db')
			cursor=con.cursor()
			sql="delete from student where rno='%d'" 
			rno = delete_window_ent_rno.get()
			cursor.execute(sql % int(rno))
			if cursor.rowcount>0:
				showinfo('Success', 'Record deleted')
				con.commit()
			else:	
				showwarning('Retry', 'Record doesnt exist')
			delete_window_ent_rno.delete(0,END)
		except Exception as e:
			showerror('Failure', e)
		finally:
			if con is not None:
				con.close()


def f12():					# - - Charts Window - - - - - - - - - - - -
	names=[]
	marks=[]
	con = None
	try:
		con = connect('kc.db')
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		#print(data)
		for d in data:
			names.append(d[1])
			marks.append(d[2])
			plt.bar(names,marks, linewidth=4, color = ['red', 'green', 'blue'])
		plt.title("Batch Information!")
		plt.xlabel("Names")
		plt.ylabel("Marks")

		plt.show()
	except Exception as e:
		showerror('Failure', e)
	finally:
		if con is not None:
			con.close()

def f13():
	if askokcancel("Quit","Click OK to Quit"):
		main_window.destroy()






# - - MAIN WINDOW - - - - - - - - - -
main_window = Tk()
main_window.title("S. M. S.")
main_window.geometry("600x500+400+100")

main_window_btn_add = Button(main_window, text="Add", font=('Times New Roman', 20, 'bold'), width=10, command=f1)
main_window_btn_view = Button(main_window, text="View", font=('Times New Roman', 20, 'bold'), width=10, command=f3)
main_window_btn_update = Button(main_window, text="Update", font=('Times New Roman', 20, 'bold'), width=10, command=f6)
main_window_btn_delete = Button(main_window, text="Delete", font=('Times New Roman', 20, 'bold'), width=10, command=f9)
main_window_btn_charts = Button(main_window, text="Charts", font=('Times New Roman', 20, 'bold'), width=10, command=f12)
res = requests.get("https://ipinfo.io/")
data = res.json()
city_name = data['city']
a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
a2 = "&q=" + city_name
a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
a = a1+a2+a3
res = requests.get(a)
data = res.json()
main = data['main']
avg = main['feels_like']
city_name = str(city_name)
avg = str(avg)
main_window_lbl_loct = Label(main_window, text=("Location: " + city_name + "\t\t\tTemp: " + avg + u'\u2103'),  font=('Times New Roman', 13, 'bold')) 
qt = requests.get("https://www.brainyquote.com/quote_of_the_day")
data = bs4.BeautifulSoup(qt.text,'html.parser')
info = data.find('img',{'class': 'p-qotd'})
main_window_lbl_qotd = Label(main_window, text=("QOTD: " +info['alt']), font=('Times New Roman', 11, 'italic'))
main_window_btn_add.pack(pady=10)
main_window_btn_view.pack(pady=10)
main_window_btn_update.pack(pady=10)
main_window_btn_delete.pack(pady=10)
main_window_btn_charts.pack(pady=10)
main_window_lbl_loct.pack(pady=10)
main_window_lbl_qotd.pack(pady=10)

#  - -  ADD WINDOW - - - - - - - - - -
add_window = Toplevel(main_window)
add_window.title("Add St.")
add_window.geometry("500x500+400+100")

add_window_lbl_rno = Label(add_window, text="Enter rno:", font=('Times New Roman', 20, 'bold'))
add_window_ent_rno = Entry(add_window, bd=5, font=('Times New Roman', 20, 'bold'))
add_window_lbl_name = Label(add_window, text="Enter name:", font=('Times New Roman', 20, 'bold'))
add_window_ent_name = Entry(add_window, bd=5, font=('Times New Roman', 20, 'bold'))
add_window_lbl_marks = Label(add_window, text="Enter marks:", font=('Times New Roman', 20, 'bold'))
add_window_ent_marks = Entry(add_window, bd=5, font=('Times New Roman', 20, 'bold'))
add_window_btn_save = Button(add_window, text="Save", font=('Times New Roman', 20, 'bold'), command=f5)
add_window_btn_back = Button(add_window, text="Back", font=('Times New Roman', 20, 'bold'), command=f2)

add_window_lbl_rno.pack(pady=10)
add_window_ent_rno.pack(pady=10)
add_window_lbl_name.pack(pady=10)
add_window_ent_name.pack(pady=10)
add_window_lbl_marks.pack(pady=10)
add_window_ent_marks.pack(pady=10)
add_window_btn_save.pack(pady=10)
add_window_btn_back.pack(pady=10)
add_window.withdraw()

#  - -  VIEW WINDOW - - - - - - - - - -
view_window = Toplevel(main_window)
view_window.title("View St.")
view_window.geometry("500x500+400+100")

view_window_st_data = ScrolledText(view_window, width=30, height=10, font=('Times New Roman', 20, 'bold'))
view_window_btn_back = Button(view_window, text="Back", font=('Times New Roman', 20, 'bold'), width=10, command=f4)
view_window_st_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()

#  - -  UPDATE WINDOW - - - - - - - - - -
update_window = Toplevel(main_window)
update_window.title("Update St.")
update_window.geometry("500x500+400+100")

update_window_lbl_rno = Label(update_window, text="Enter rno:", font=('Times New Roman', 20, 'bold'))
update_window_ent_rno = Entry(update_window, bd=5, font=('Times New Roman', 20, 'bold'))
update_window_lbl_name = Label(update_window, text="Enter name:", font=('Times New Roman', 20, 'bold'))
update_window_ent_name = Entry(update_window, bd=5, font=('Times New Roman', 20, 'bold'))
update_window_lbl_marks = Label(update_window, text="Enter marks:", font=('Times New Roman', 20, 'bold'))
update_window_ent_marks = Entry(update_window, bd=5, font=('Times New Roman', 20, 'bold'))
update_window_btn_save = Button(update_window, text="Save", font=('Times New Roman', 20, 'bold'), command=f8)
update_window_btn_back = Button(update_window, text="Back", font=('Times New Roman', 20, 'bold'), command=f7)
update_window_lbl_rno.pack(pady=10)
update_window_ent_rno.pack(pady=10)
update_window_lbl_name.pack(pady=10)
update_window_ent_name.pack(pady=10)
update_window_lbl_marks.pack(pady=10)
update_window_ent_marks.pack(pady=10)
update_window_btn_save.pack(pady=10)
update_window_btn_back.pack(pady=10)
update_window.withdraw()

#  - -  DELETE WINDOW - - - - - - - - - -
delete_window = Toplevel(main_window)
delete_window.title("Delete St.")
delete_window.geometry("500x500+400+100")

delete_window_lbl_rno = Label(delete_window, text="Enter rno:", font=('Times New Roman', 20, 'bold'))
delete_window_ent_rno = Entry(delete_window, bd=5, font=('Times New Roman', 20, 'bold'))
delete_window_btn_delete = Button(delete_window, text="Delete", font=('Times New Roman', 20, 'bold'), command=f11)
delete_window_btn_back = Button(delete_window, text="Back", font=('Times New Roman', 20, 'bold'), command=f10)
delete_window_lbl_rno.pack(pady=10)
delete_window_ent_rno.pack(pady=10)
delete_window_btn_delete.pack(pady=10)
delete_window_btn_back.pack(pady=10)
delete_window.withdraw()


	

main_window.protocol("WM_DELETE_WINDOW", f13)
main_window.mainloop()

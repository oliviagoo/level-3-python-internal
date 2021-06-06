#adding edit job option
#version 16
from tkinter import *

#setting constants for calculating the job cost
VIRUS_RATE = 0.8
WOF_RATE = 100
DIST_BASE_RATE = 10
DIST_RATE = 0.5
DIST_BASE_MIN = 5

#support class for individual jobs
class Job:
    def __init__(self, num, name, dist, virus, wof, minutes, charge):
        self.num = num
        self.name = name
        self.dist = dist
        self.virus = virus
        self.wof = wof
        self.minutes = minutes
        self.charge = charge

#a class containing all the GUI
class JobManagementGUI:
    def __init__(self, parent):
        #a list that keeps track of the Job objects
        self.job_list = []
        
        #suzy's logo
        self.logo_img = PhotoImage(file = "logo.gif")
        
        #variables for the entry frame
        self.next_id = len(self.job_list) + 1
        self.customer_name = StringVar()
        self.distance = IntVar()
        self.virus = IntVar()
        self.wof = IntVar()
        self.minutes = StringVar()
        self.minutes.set("0")

        self.mode = "s"
        #variable for the display frame
        self.position = 0

        #display frame GUI
        self.display_frame = Frame(parent)

        self.display_label = Label(self.display_frame, text = "")
        self.display_label.grid(row = 0, column = 0, pady = 10)

        self.add_but = Button(self.display_frame, text = "New Job", command = self.new_job)
        self.add_but.grid(row = 0, column = 1)

        self.disp_num_desc_label = Label(self.display_frame, text = "Job number:")
        self.disp_num_desc_label.grid(row = 1, column = 0, sticky = E, padx = 10)

        self.job_num_label = Label(self.display_frame, text = "")
        self.job_num_label.grid(row = 1, column = 1, sticky = W, padx = 10)

        self.disp_name_desc_label = Label(self.display_frame, text = "Customer name:")
        self.disp_name_desc_label.grid(row = 2, column = 0, sticky = E, padx = 10)
        

        self.name_label = Label(self.display_frame, text = "")
        self.name_label.grid(row = 2, column = 1, sticky = W, padx = 10)

        self.disp_charge_desc_label = Label(self.display_frame, text = "Job charge:")
        self.disp_charge_desc_label.grid(row = 3, column = 0, sticky = E, padx = 10)

        self.charge_label = Label(self.display_frame, text = "")
        self.charge_label.grid(row = 3, column = 1, sticky = W, padx = 10)

        self.back_but = Button(self.display_frame, text = "Back", command = self.back, state = DISABLED)
        self.back_but.grid(row = 4, column = 0, pady = 10, sticky = W, padx = 25)

        self.next_but = Button(self.display_frame, text = "Next", command = self.next, state = DISABLED)
        self.next_but.grid(row = 4, column = 1, pady = 10, sticky = E, padx = 25)

        self.no_job_label = Label(self.display_frame, text = "There are currently no jobs entered.\nPress New Job to enter a job!")

        self.edit_but = Button(self.display_frame, text = "Edit Job", command = self.edit)
        self.edit_but.grid(row = 5, column = 0, pady = 10)

        self.all_but = Button(self.display_frame, text = "View All")
        self.all_but.grid(row = 5, column = 1, pady = 10)

        logo = Label(self.display_frame, image = self.logo_img)
        logo.grid(row = 6, column = 0, columnspan = 2)

        self.display_frame.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.check_pos_update()

        #entry frame GUI

        self.entry_frame = Frame(parent)

        title_label = Label(self.entry_frame, text = "Enter Job Details:")
        title_label.grid(row = 0, column = 0, columnspan = 2, pady = 5)

        num_desc_label = Label(self.entry_frame, text = "Job number:")
        num_desc_label.grid(row = 1, column = 0, pady = 5)

        self.num_label = Label(self.entry_frame, text = self.next_id)
        self.num_label.grid(row = 1, column = 1)

        name_desc_label = Label(self.entry_frame, text = "Customer name:")
        name_desc_label.grid(row = 2, column = 0)

        self.name_entry = Entry(self.entry_frame, textvariable = self.customer_name)
        self.name_entry.grid(row = 2, column = 1, pady = 10)

        dist_desc_label = Label(self.entry_frame, text = "Distance travelled (in km):")
        dist_desc_label.grid(row = 3, column = 0)

        self.dist_entry = Entry(self.entry_frame, width = 3, textvariable = self.distance)
        self.dist_entry.grid(row = 3, column = 1, sticky = S)

        self.dist_slider = Scale(self.entry_frame, orient = HORIZONTAL, variable = self.distance, sliderlength = "15px", from_ = 1, to = 100, showvalue = 0)
        self.dist_slider.grid(row = 4, column = 1, sticky = N)

        self.virus_check = Checkbutton(self.entry_frame, text = "Virus Protection", variable = self.virus, onvalue = 1, offvalue = 0, command = self.toggle_min)
        self.virus_check.grid(row = 5, column = 0, pady = 10)

        self.wof_check = Checkbutton(self.entry_frame, text = "WOF and tune", variable = self.wof, onvalue = 1, offvalue = 0)
        self.wof_check.grid(row = 5, column = 1, pady = 10)

        self.min_desc_label = Label(self.entry_frame, text = "Minutes spent:", fg = "#949494")
        self.min_desc_label.grid(row = 6, column = 0)

        self.min_entry = Entry(self.entry_frame, textvariable = self.minutes, state = DISABLED, width = 5)
        self.min_entry.grid(row = 7, column = 0, pady = 5)

        self.cancel_but = Button(self.entry_frame, text = "Back to Menu", command = self.cancel_entry)
        self.cancel_but.grid(row = 8, column = 0, pady = 10)

        self.submit_but = Button(self.entry_frame, text = "Submit", command = self.check_job)
        self.submit_but.grid(row = 8, column = 1, pady = 10)

        self.update_but = Button(self.entry_frame, text = "Update Job", command = self.check_job)

        self.confirmation_label = Label(self.entry_frame, text = "", fg = "green")
        self.confirmation_label.grid(row = 9, column = 0, columnspan = 2)

    #this method opens the entry frame to submit a new job
    def new_job(self):
        self.display_frame.grid_remove()
        self.entry_frame.grid(row = 0, column = 0, padx = 10, pady = 5)
        self.update_but.grid_remove()
        self.submit_but.grid(row = 8, column = 1, pady = 10)
        self.num_label.configure(text = self.next_id)
        self.mode = "s"

    #empties the entries on the entry frame and unticks all checkboxes
    def clear_entry_fields(self):
        self.customer_name.set("")
        self.distance.set(0)
        self.virus.set(0)
        self.wof.set(0)
        self.minutes.set("0")
        self.min_entry.configure(state = DISABLED)
        self.confirmation_label.configure(text = "")

    #this method hides the entry frame and clears the entry fields
    def cancel_entry(self):
        self.entry_frame.grid_remove()
        self.display_frame.grid()
        self.clear_entry_fields()
        self.check_pos_update()

    #prevents error messages turning strings into ints
    #and makes sure that the int is above 0
    def check_int(self, number):
        try:
            valid_num = int(number)
            if valid_num > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    #this method creates a job object to "submit" the job
    #clears the entry fields, updates the confimation label
    def submit_job(self, min_number, virus_selected, wof_selected):
        min_number = int(self.minutes.get())
        charge = self.calc_charge(min_number, virus_selected, wof_selected, self.distance.get())
        self.job_list.append(Job(self.next_id, self.customer_name.get().title().strip(), self.distance.get(), virus_selected, wof_selected, min_number, charge))
        self.next_id = len(self.job_list) + 1
        self.num_label.configure(text = self.next_id)
        self.clear_entry_fields()
        self.confirmation_label.configure(text = "Job {} has been submitted!".format(self.next_id - 1), fg = "green")

    #this method makes sure all input is valid before submitting
    def check_job(self):
        if self.customer_name.get() != "":
            if self.wof.get() != 0 or self.virus.get() != 0:
                if self.virus.get() == 1:
                    virus_selected = True
                else:
                    virus_selected = False
                    
                if self.wof.get() == 1:
                    wof_selected = True
                else:
                    wof_selected = False

                if virus_selected == True:
                    valid_minutes = self.check_int(self.minutes.get())
                    if valid_minutes == True:
                        if self.mode == "s":
                            self.submit_job(self.minutes.get(), virus_selected, wof_selected)
                        else:
                            self.update_job(self.minutes.get(), virus_selected, wof_selected)
                    else:
                        self.confirmation_label.configure(text = "Please enter a whole number greater than 0\nfor minutes spent on Virus Protection", fg = "red")
                else:
                    if self.mode == "s":
                        self.submit_job(self.minutes.get(), virus_selected, wof_selected)
                    else:
                        self.update_job(self.minutes.get(), virus_selected, wof_selected)
            else:
                self.confirmation_label.configure(text = "Please tick either Virus Protection and/or WOF and tune", fg = "red")
        else:
            self.confirmation_label.configure(text = "Please enter a customer name!", fg = "red")

    #this method disables and enables the minutes entry
    def toggle_min(self):
        if self.virus.get() == 1:
            self.min_entry.configure(state = NORMAL)
            self.min_desc_label.configure(fg = "black")
        else:
            self.min_entry.configure(state = DISABLED)
            self.min_desc_label.configure(fg = "#949494")
            self.minutes.set("0")

    #this method calculates the charge for a job
    def calc_charge(self, minutes, virus, wof, dist):
        charge = 0
        if virus == True:
            charge += VIRUS_RATE * minutes
        if wof == True:
            charge += WOF_RATE

        charge += DIST_BASE_RATE
        if dist > DIST_BASE_MIN:
            dist -= DIST_BASE_MIN
            charge += DIST_RATE * dist

        return charge

    #this method scrolls to the next job in the display frame
    def next(self):
        self.position += 1
        self.check_pos_update()

    #this method scrolls to the previous job in the display frame
    def back(self):
        self.position -= 1
        self.check_pos_update()

    #this method allows the user to edit a specific job
    def edit(self):
        self.new_job()
        self.mode = "e"
        self.num_label.configure(text = self.position + 1)
        self.customer_name.set(self.job_list[self.position].name)
        self.distance.set(self.job_list[self.position].dist)
        if self.job_list[self.position].virus == True:
            self.virus.set(1)
            self.min_entry.configure(state = NORMAL)
        else:
            self.virus.set(0)
            self.min_entry.configure(state = DISABLED)
        if self.job_list[self.position].wof == True:
            self.wof.set(1)
        else:
            self.wof.set(0)
        self.minutes.set(self.job_list[self.position].minutes)
        
        self.confirmation_label.configure(text = "")
        self.submit_but.grid_remove()
        self.update_but.grid(row = 8, column = 1, pady = 10)
        

    #this method updates jobs after they have been edited
    def update_job(self, min_number, virus_selected, wof_selected):
        min_number = int(self.minutes.get())
        job_update = self.job_list[self.position]
        job_update.name = self.customer_name.get().title().strip()
        job_update.dist = self.distance.get()
        job_update.virus = virus_selected
        job_update.wof = wof_selected
        job_update.minutes = min_number
        job_update.charge = self.calc_charge(min_number, virus_selected, wof_selected, self.distance.get())
        self.confirmation_label.configure(text = "Job {} has been updated!".format(self.position + 1), fg = "green")

    #this method ensures that the user doesn't scroll too far, and
    #actually updates the labels to show another job
    def check_pos_update(self):
        #if there are jobs that have been inputted
        if len(self.job_list) > 0:
            #shows the necessary labels
            self.disp_num_desc_label.grid()
            self.disp_name_desc_label.grid()
            self.disp_charge_desc_label.grid()
            self.no_job_label.grid_remove()

            self.edit_but.configure(state = NORMAL)
            self.all_but.configure(state = NORMAL)

            #disabling and enabling buttons depending on the position
            if self.position == len(self.job_list) - 1:
                self.next_but.configure(state = DISABLED)
            else:
                self.next_but.configure(state = NORMAL)
                
            if self.position == 0:
                self.back_but.configure(state = DISABLED)
            else:
                self.back_but.configure(state = NORMAL)

            self.display_label.configure(text = "Displaying Job: {}/{}".format(self.position + 1, len(self.job_list)))
            self.job_num_label.configure(text = self.job_list[self.position].num)
            self.name_label.configure(text = self.job_list[self.position].name)
            self.charge_label.configure(text = "${:.2f}".format(self.job_list[self.position].charge))
        #if no jobs have been inputted, don't try and show jobs
        else:
            self.edit_but.configure(state = DISABLED)
            self.all_but.configure(state = DISABLED)
            self.disp_num_desc_label.grid_remove()
            self.disp_name_desc_label.grid_remove()
            self.disp_charge_desc_label.grid_remove()
            self.no_job_label.grid(row = 2, column = 0, columnspan = 2)


#main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Job Management Program")
    JobManager = JobManagementGUI(root)
    root.mainloop()

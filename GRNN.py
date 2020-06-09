# ======================================================================================================================

"""
Our gui implementation will be here
Tkinter will be use
"""

# ======================================================================================================================

import pandas as pd
import numpy as np
from grnn3_backend import GRNN
from utility import GET_PREDICTORS

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog     # for combobox, scrolledtext, message box, file dialog, input
from tkinter.ttk import Progressbar

# custom frame sizes
w_column1 = 555
h_column1 = 360


class DataOptions(tk.Frame):
    """
    Controls the data lists
    """

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, parent):
        # SET THE FRAME
        frame_File = tk.Frame(master=window, width=w_column1, height=h_column1, relief=tk.GROOVE, borderwidth=3)
        frame_File.grid(column=0, row=0, padx=10, pady=10)

        # set title
        label = tk.Label(master=window, text=' Data Options ', font=('Arial Bold', 10))
        label.place(x=30, y=0)

        # set listbox titles
        label = tk.Label(master=window, text='Train Sets')
        label.place(x=70, y=37)

        label = tk.Label(master=window, text='Test Sets')
        label.place(x=200, y=37)

        label = tk.Label(master=window, text='Predictors')
        label.place(x=320, y=37)

        label = tk.Label(master=window, text='Target')
        label.place(x=455, y=37)

        # set listboxes
        self.trainset_list = tk.Listbox(master=frame_File, width=20, height=13)
        self.trainset_list.place(x=25, y=45)

        self.testset_list = tk.Listbox(master=frame_File, width=20, height=13)
        self.testset_list.place(x=150, y=45)

        self.predictor_list = tk.Listbox(master=frame_File, width=20, height=13)
        self.predictor_list.place(x=275, y=45)

        self.target_list = tk.Listbox(master=frame_File, width=20, height=13)
        self.target_list.place(x=400, y=45)

        # store the path of the files
        self.PATHS = {}

        # set buttons
        trainset_button_add = tk.Button(master=frame_File, text='Add Train Set', activebackground='gray', command=self.ADD_TRAINSET)
        trainset_button_add.place(x=25, y=270, width=125)
        trainset_button_eject = tk.Button(master=frame_File, text='Eject Train Set', activebackground='gray', command=self.EJECT_TRAINSET)
        trainset_button_eject.place(x=25, y=300, width=125)

        testset_button_add = tk.Button(master=frame_File, text='Add Test Set', activebackground='gray', command=self.ADD_TESTSET)
        testset_button_add.place(x=150, y=270, width=125)
        testset_button_eject = tk.Button(master=frame_File, text='Eject Test Set', activebackground='gray', command=self.EJECT_TESTSET)
        testset_button_eject.place(x=150, y=300, width=125)

        predictor_button_add = tk.Button(master=frame_File, text='Add Predictor', activebackground='gray', command=self.ADD_PREDICTOR)
        predictor_button_add.place(x=275, y=270, width=125)
        predictor_button_eject = tk.Button(master=frame_File, text='Eject Predictor', activebackground='gray', command=self.EJECT_PREDICTOR)
        predictor_button_eject.place(x=275, y=300, width=125)

        target_button_add = tk.Button(master=frame_File, text='Add Target', activebackground='gray', command=self.ADD_TARGET)
        target_button_add.place(x=400, y=270, width=125)
        target_button_eject = tk.Button(master=frame_File, text='Eject Eject', activebackground='gray', command=self.EJECT_TARGET)
        target_button_eject.place(x=400, y=300, width=125)

    # ------------------------------------------------------------------------------------------------------------------

    def ADD_TRAINSET(self):
        # pick the file, add to listbox
        csv_dir = filedialog.askopenfilename(filetypes = (("Text files","*.csv"),("all files","*.*")))
        csv_name = csv_dir[csv_dir.rfind('/')+1:-4]

        # if already picked, return error window
        if csv_name in self.trainset_list.get(0, tk.END):
            messagebox.showerror('Duplicate', 'There is an item named {} already exist.'.format(csv_name))
            return
        self.trainset_list.insert(tk.END, csv_name)
        self.PATHS[csv_name] = csv_dir

    # ------------------------------------------------------------------------------------------------------------------

    def EJECT_TRAINSET(self):
        # remove the selection
        try:
            removed = self.trainset_list.curselection()[0]
            self.trainset_list.delete(removed)
            self.PATHS.pop(removed)
        except:
            IndexError()

    # ------------------------------------------------------------------------------------------------------------------

    def ADD_TESTSET(self):
        # pick the file, add to listbox
        csv_dir = filedialog.askopenfilename(filetypes=(("Text files", "*.csv"), ("all files", "*.*")))
        csv_name = csv_dir[csv_dir.rfind('/') + 1:-4]

        # if already picked, return error window
        if csv_name in self.testset_list.get(0, tk.END):
            messagebox.showerror('Duplicate', 'There is an item named {} already exist.'.format(csv_name))
            return
        self.testset_list.insert(tk.END, csv_name)
        self.PATHS[csv_name] = csv_dir

    # ------------------------------------------------------------------------------------------------------------------

    def EJECT_TESTSET(self):
        # remove the selection
        try:
            removed = self.testset_list.curselection()[0]
            self.testset_list.delete(removed)
            self.PATHS.pop(removed)
        except:
            IndexError()

    # ------------------------------------------------------------------------------------------------------------------

    def ADD_PREDICTOR(self):
        # add predictor manual
        predictor = simpledialog.askstring('Add Predictor', 'Predictor name: ')

        if predictor in self.predictor_list.get(0, tk.END):
            messagebox.showerror('Duplicate', 'There is an item named {} already exist.'.format(predictor))
            return
        self.predictor_list.insert(tk.END, predictor)

    # ------------------------------------------------------------------------------------------------------------------

    def EJECT_PREDICTOR(self):
        # remove predictor
        try:
            removed = self.predictor_list.curselection()[0]
            self.predictor_list.delete(removed)
        except:
            IndexError()

    # ------------------------------------------------------------------------------------------------------------------

    def ADD_TARGET(self):
        # add target manual
        target = simpledialog.askstring('Add Target','Target name: ')
        self.target_list.insert(tk.END, target)

    # ------------------------------------------------------------------------------------------------------------------

    def EJECT_TARGET(self):
        # remove the target
        try:
            removed = self.target_list.curselection()[0]
            self.target_list.delete(removed)
        except:
            IndexError()

    # ------------------------------------------------------------------------------------------------------------------

    def LOAD_PREDICTOR(self):
        # clear the list
        self.predictor_list.delete(0, tk.END)

        # get name of the selected file and read it
        selected = self.trainset_list.curselection()
        selected = self.trainset_list.get(selected)
        dataset = pd.read_csv(self.PATHS[selected])

        # add all features to the list
        for predictor in GET_PREDICTORS(dataset):
            self.predictor_list.insert(tk.END, predictor)

    # ------------------------------------------------------------------------------------------------------------------

    def LOAD_TARGET(self):
        # clear the list
        self.target_list.delete(0, tk.END)

        # get name of the selected file and read it
        selected = self.trainset_list.curselection()
        selected = self.trainset_list.get(selected)
        dataset = pd.read_csv(self.PATHS[selected])

        # add all features to the list
        for target in GET_PREDICTORS(dataset):
            self.target_list.insert(tk.END, target)

# ======================================================================================================================

class Preferences(tk.Frame):
    def __init__(self, parent):
        self.parentData = parent

        # SET THE Preferences FRAME
        frame_preferences = tk.Frame(master=window, width=w_column1, height=h_column1, relief=tk.GROOVE, borderwidth=3)
        frame_preferences.grid(column=0, row=1, padx=10, pady=10)

        # set the title
        label = tk.Label(master=window, text=' Preferences ', font=('Arial Bold', 10))
        label.place(x=30, y=380)

        # set loss function title
        label = tk.Label(master=window, text='Set Loss Function')
        label.place(x=30, y=420)

        # set loss functions
        self.mae_radiobtn = tk.Radiobutton(master=window, text='MAE', value='MAE')
        self.mae_radiobtn.place(x=30, y=440)

        self.mse_radiobtn = tk.Radiobutton(master=window, text='MSE', value='MSE')
        self.mse_radiobtn.place(x=180, y=440)

        self.rmse_radiobtn = tk.Radiobutton(master=window, text='RMSE', value='RMSE')
        self.rmse_radiobtn.place(x=330, y=440)

        # set sigma options
        label = tk.Label(master=window, text='Set Sigma Options')
        label.place(x=30, y=500)

        self.defaultsigma_checkstate = tk.BooleanVar()
        self.defaultsigma_checkstate.set(False)
        self.defaultsigma_checkbtn = tk.Checkbutton(master=window, text='default sigma\n(No training)', command=self.SET_SIGMA_ENTRIES)
        self.defaultsigma_checkbtn.place(x=30, y=520)

        # set labels before entries
        label = tk.Label(master=window, text='    set min σ:')
        label.place(x=183, y=520)

        label = tk.Label(master=window, text='    set max σ:')
        label.place(x=181, y=540)

        label = tk.Label(master=window, text='search steps:')
        label.place(x=180, y=560)

        # set entries
        # if defaultsigma is true, disable entries.
        self.minsigma_entry = tk.Entry(master=window)
        self.minsigma_entry.place(x=260, y=520)

        self.maxsigma_entry = tk.Entry(master=window)
        self.maxsigma_entry.place(x=260, y=540)

        self.searchsigma_entry = tk.Entry(master=window)
        self.searchsigma_entry.place(x=260, y=560)

        # save button
        self.sigmasave_button = tk.Button(master=window, text='SAVE\nSIGMA', font=('Arial Bold', 9), activebackground='gray', borderwidth=3)
        self.sigmasave_button.place(x=400, y= 520, width=120, height=60)

        # round the results
        self.roundresults_label = tk.Label(master=window, text='Rounding results: ')
        self.roundresults_label.place(x=30, y=620)

        self.roundresults_checkstate = tk.BooleanVar()
        self.roundresults_checkstate.set(False)
        self.roundresults_checkbox = tk.Checkbutton(master=window, text='round results', command=self.SET_ROUND_RESULTS)
        self.roundresults_checkbox.place(x=30, y=640)

    # ------------------------------------------------------------------------------------------------------------------

    def SET_SIGMA_ENTRIES(self):
        if not self.defaultsigma_checkstate:
            self.defaultsigma_checkstate = True
            state='normal'
        else:
            self.defaultsigma_checkstate = False
            state='disabled'

        self.minsigma_entry.configure(state=state)
        self.maxsigma_entry.configure(state=state)
        self.searchsigma_entry.configure(state=state)

    def SET_ROUND_RESULTS(self):
        if not self.roundresults_checkstate:
            self.roundresults_checkstate = True
        else:
            self.roundresults_checkstate = False

# ======================================================================================================================

# This class will also handle some multiple events in DataOptions
class Panel(tk.Frame):
    def __init__(self, parentData, parentPref):
        self.parentData = parentData
        self.parentPref = parentPref

        # SET THE Panel FRAME
        frame_panel = tk.Frame(master=window, width=w_column1+100, height=h_column1, relief=tk.GROOVE, borderwidth=3)
        frame_panel.grid(column=1,row=0, padx=10,pady=10)

        label = tk.Label(master=window, text=' Panel ', font=('Arial Bold', 10))
        label.place(x=605, y=0)

        # train set info
        trainset_label = tk.Label(master=window, text='Train Set     :')
        trainset_label.place(x=625, y=55)
        self.selected_trainset_info = tk.Label(master=window)
        self.selected_trainset_info.place(x=700, y=55)

        # test set info
        trainset_label = tk.Label(master=window, text='Test Set      :')
        trainset_label.place(x=625, y=95)
        self.selected_testset_info = tk.Label(master=window)
        self.selected_testset_info.place(x=700, y=95)

        # target info
        target_label = tk.Label(master=window, text='Target        :')
        target_label.place(x=625, y=135)
        self.selected_target_info = tk.Label(master=window)
        self.selected_target_info.place(x=700, y=135)

        # predictor list label
        chosen_predictor_label = tk.Label(master=window, text='Chosen Predictors :')
        chosen_predictor_label.place(x=850, y=35)

        # List of choosen predictors
        self.chosen_predictor_list = tk.Listbox(master=window, width=20, height=13)
        self.chosen_predictor_list.place(x=850, y=55)

        # loss function info
        lossfunc_label = tk.Label(master=window, text='Loss Function    :')
        lossfunc_label.place(x=1050, y=55)
        self.selected_lossfunc_info = tk.Label(master=window)
        self.selected_lossfunc_info.place(x=1150, y=55)

        # min sigma info
        minsigma_label = tk.Label(master=window, text='Min. Sigma        :')
        minsigma_label.place(x=1050, y=95)
        self.selected_minsigma_info = tk.Label(master=window)
        self.selected_minsigma_info.place(x=1150, y=95)

        # max sigma info
        maxsigma_label = tk.Label(master=window, text='Max. Sigma       :')
        maxsigma_label.place(x=1050, y=135)
        self.selected_maxsigma_info = tk.Label(master=window)
        self.selected_maxsigma_info.place(x=1150, y=135)

        # sigma searches info
        searchsigma_label = tk.Label(master=window, text='Search Sigma    :')
        searchsigma_label.place(x=1050, y=175)
        self.selected_searchsigma_info = tk.Label(master=window)
        self.selected_searchsigma_info.place(x=1150, y=175)

        # default sigma
        defaultsigma_label = tk.Label(master=window, text='Default Sigma   :')
        defaultsigma_label.place(x=1050, y=210)
        self.selected_defaultsigma_info = tk.Label(master=window)
        self.selected_defaultsigma_info.place(x=1150, y=210)

        # rounding results
        roundresults_label = tk.Label(master=window, text='Round Results    :')
        roundresults_label.place(x=1050, y=250)
        self.selected_roundresults_info = tk.Label(master=window)
        self.selected_roundresults_info.place(x=1150, y=250)


        # Data Options / if any train set is added, bind events to lists
        self.parentData.trainset_list.bind("<ButtonRelease-1>", self.BINDING_EVENTS_TRAINSET_LIST)
        self.parentData.testset_list.bind("<ButtonRelease-1>", self.BINDING_EVENTS_TESTSET_LIST)
        self.parentData.predictor_list.bind("<ButtonRelease-1>", self.BINDING_EVENTS_PREDICTOR_LIST)
        self.parentData.target_list.bind("<ButtonRelease-1>", self.BINDING_EVENTS_TARGET_LIST)

        # Preferences / whenever a sigma is written
        self.parentPref.mae_radiobtn.bind("<ButtonRelease-1>", self.BINDING_EVENTS_MAE_RADIOBTN)
        self.parentPref.mse_radiobtn.bind("<ButtonRelease-1>", self.BINDING_EVENTS_MSE_RADIOBTN)
        self.parentPref.rmse_radiobtn.bind("<ButtonRelease-1>", self.BINDING_EVENTS_RMSE_RADIOBTN)
        self.parentPref.sigmasave_button.bind("<ButtonRelease-1>", self.BINDING_EVENTS_SAVESIGMA_BUTTON)
        self.parentPref.defaultsigma_checkbtn.bind("<ButtonRelease-1>", self.BINDING_EVENTS_DEFAULTSIGMA_CHECKBOX)
        self.parentPref.roundresults_checkbox.bind("<ButtonRelease-1>", self.BINDING_EVENTS_ROUNDRESULTS_CHECKBOX)

        # Panel / double click to eject
        self.chosen_predictor_list.bind("<Double-Button-1>", self.BINDING_EVENTS_CHOSEN_PREDICTOR_LIST)

    # ------------------------------------------------------------------------------------------------------------------

    def BINDING_EVENTS_TRAINSET_LIST(self, event):
        # display trainset if selected
        selected = self.parentData.trainset_list.curselection()
        if selected:
            selected = self.parentData.trainset_list.get(selected)
            self.selected_trainset_info.configure(text=selected)

            # load predictor and target list in DataOp
            self.parentData.LOAD_PREDICTOR()
            self.parentData.LOAD_TARGET()

    # ------------------------------------------------------------------------------------------------------------------

    def BINDING_EVENTS_TESTSET_LIST(self, event):
        # display testset if selected
        selected = self.parentData.testset_list.curselection()
        if selected:
            selected = self.parentData.testset_list.get(selected)
            self.selected_testset_info.configure(text=selected)

    # ------------------------------------------------------------------------------------------------------------------

    def BINDING_EVENTS_PREDICTOR_LIST(self, event):
        # get the index of the selected
        selected = self.parentData.predictor_list.curselection()

        # then check if that element exist before adding to chosen predictor list
        if selected:
            selected = self.parentData.predictor_list.get(selected)
            if selected not in self.chosen_predictor_list.get(0,tk.END):
                self.chosen_predictor_list.insert(tk.END, selected)

    # ------------------------------------------------------------------------------------------------------------------

    def BINDING_EVENTS_CHOSEN_PREDICTOR_LIST(self, event):
        try:
            selected = self.chosen_predictor_list.curselection()[0]
            self.chosen_predictor_list.delete(selected)
        except:
            IndexError()

    # ------------------------------------------------------------------------------------------------------------------

    def BINDING_EVENTS_TARGET_LIST(self, event):
        # display predictor if selected/added
        selected = self.parentData.target_list.curselection()
        if selected:
            selected = self.parentData.target_list.get(selected)
            self.selected_target_info.configure(text=selected)

    # ------------------------------------------------------------------------------------------------------------------

    def BINDING_EVENTS_MAE_RADIOBTN(self, event):
        self.selected_lossfunc_info.configure(text='MAE')

    # ------------------------------------------------------------------------------------------------------------------

    def BINDING_EVENTS_MSE_RADIOBTN(self, event):
        self.selected_lossfunc_info.configure(text='MSE')

    # ------------------------------------------------------------------------------------------------------------------

    def BINDING_EVENTS_RMSE_RADIOBTN(self, event):
        self.selected_lossfunc_info.configure(text='RMSE')

    # ------------------------------------------------------------------------------------------------------------------

    def BINDING_EVENTS_SAVESIGMA_BUTTON(self, event):
        if not self.parentPref.defaultsigma_checkstate:
            minsigma_info = 'default'
            maxsigma_info = 'default'
            searchsigma_info = 'default'
        else:
            minsigma_info = self.parentPref.minsigma_entry.get()
            maxsigma_info = self.parentPref.maxsigma_entry.get()
            searchsigma_info = self.parentPref.searchsigma_entry.get()

        self.selected_minsigma_info.configure(text=minsigma_info)
        self.selected_maxsigma_info.configure(text=maxsigma_info)
        self.selected_searchsigma_info.configure(text=searchsigma_info)


    def BINDING_EVENTS_DEFAULTSIGMA_CHECKBOX(self, event):
        state = 'True' if self.parentPref.defaultsigma_checkstate else 'False'

        self.selected_defaultsigma_info.configure(text=state)

    def BINDING_EVENTS_ROUNDRESULTS_CHECKBOX(self, event):
        state = 'True' if self.parentPref.roundresults_checkstate else 'False'

        self.selected_roundresults_info.configure(text=state)

# ======================================================================================================================

class Model(tk.Frame):
    def __init__(self, parentPanel, parentData, parentPref):
        self.parentPanel = parentPanel
        self.parentData = parentData
        self.parentPref = parentPref

        # set frame
        frame_model = tk.Frame(master=window, width=w_column1+100, height=h_column1, relief=tk.GROOVE, borderwidth=3)
        frame_model.grid(column=1,row=1)

        # set scroll text label
        label = tk.Label(master=window, text='Output')
        label.place(x=600, y=415)

        # set the OUTPUT scrolled text
        self.output_scrlltext = scrolledtext.ScrolledText(master=window, width=45, height=18)
        self.output_scrlltext.place(x=600, y=440)

        # performence metrices. mae/mse/rmse
        performence_label = tk.Label(master=window, text='Performence Metrics')
        performence_label.place(x=980, y=450)

        mae_label = tk.Label(master=window, text='MAE :')
        mae_label.place(x=1000, y=480)
        self.mae_label_info = tk.Label(master=window)
        self.mae_label_info.place(x=1040, y= 480)

        mse_label = tk.Label(master=window, text='MSE :')
        mse_label.place(x=1000, y=520)
        self.mse_label_info = tk.Label(master=window)
        self.mse_label_info.place(x=1040, y=520)

        rmse_label = tk.Label(master=window, text='RMSE:')
        rmse_label.place(x=1000, y=560)
        self.rmse_label_info = tk.Label(master=window)
        self.rmse_label_info.place(x=1040, y=560)

        # model evaluation (IN THE PANEL)
        self.model_evaluate_button = tk.Button(master=window, text='Evaluate', activebackground='gray', borderwidth=3, command=self.EVALUATE)
        self.model_evaluate_button.place(x=650, y=250, width=120, height=60)

        # visualize dots
        self.model_visualize_button = tk.Button(master=window, text='Dot Graph\nVisualize', activebackground='gray', borderwidth=3, command=self.VISUALIZE)
        self.model_visualize_button.place(x=1000, y=600, width=80, height=40)

        # visualize dots / linear
        self.model_visualize2_button = tk.Button(master=window, text='Frequency\nVisualize', activebackground='gray', borderwidth=3, command=self.VISUALIZE2)
        self.model_visualize2_button.place(x=1100, y=600, width=80, height=40)

    # ------------------------------------------------------------------------------------------------------------------

    def EVALUATE(self, *args):
        # get required inputs from the gui
        self.trainset_dir = self.parentData.PATHS[self.parentPanel.selected_trainset_info.cget('text')]
        testset_dir = self.parentData.PATHS[self.parentPanel.selected_testset_info.cget('text')]
        predictors = list(self.parentPanel.chosen_predictor_list.get(0,tk.END))
        target = [self.parentPanel.selected_target_info.cget('text')]
        loss_function = self.parentPanel.selected_lossfunc_info.cget('text')
        default_sigma = self.parentPanel.selected_defaultsigma_info.cget('text')
        sigma_min = self.parentPanel.selected_minsigma_info.cget('text')
        sigma_max = self.parentPanel.selected_maxsigma_info.cget('text')
        sigma_search = self.parentPanel.selected_searchsigma_info.cget('text')
        round_results = self.parentPanel.selected_roundresults_info.cget('text')

        # check sigma if default
        if default_sigma == 'True':
            sigma_info = 'default'
        else:
            sigma_info = [float(sigma_min), float(sigma_max), int(sigma_search)]

        # check round_results if default
        round_results = True if round_results == 'True' else False

        # clear scrolledtext
        self.output_scrlltext.delete('1.0', tk.END)

        # read datasets
        trainset = pd.read_csv(self.trainset_dir)
        testset = pd.read_csv(testset_dir)

        # fill missing data
        trainset.fillna(0)
        testset.fillna(0)

        # create GRNN object
        self.grnn = GRNN(train_set=trainset, test_set=testset, predictors=predictors, target=target, sigma_info=sigma_info, rounded=round_results, loss_function=loss_function)

        # zip test inputs with corresponding outputs
        final_output = zip(self.grnn.test_set.transpose(), self.grnn.final_output)

        # print
        for i, j in final_output:
            # transpose the array to make the proccess easier for the next steps
            i = np.transpose(i)

            if round_results:
                j = round(j)
            self.output_scrlltext.insert(tk.INSERT, "Predicted: {}  Output: {}\n".format(i, j))


        self.mse_label_info.configure(text=self.grnn.mse)
        self.mae_label_info.configure(text=self.grnn.mae)
        self.rmse_label_info.configure(text=self.grnn.rmse)


    def VISUALIZE(self, *args):
        # TODO
        self.grnn.Visualize()

    def VISUALIZE2(self, *args):
        # TODO
        self.grnn.Visualize2()

# ======================================================================================================================

class Skeleton(tk.Frame):
    def __init__(self, parent):

        self.dataop = DataOptions(window)
        self.pref = Preferences(window)
        self.panel = Panel(self.dataop, self.pref)
        self.model = Model(self.panel, self.dataop, self.pref)

window = tk.Tk()

window.title('Regression by GRNN')
window.resizable(False, False)

Skeleton(window)

window.mainloop()

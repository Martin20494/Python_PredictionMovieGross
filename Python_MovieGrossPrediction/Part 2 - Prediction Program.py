"""Program name: Movie Gross Prediciton.

Student name: Thong Minh Nguyen (Martin)
Student ID: 68623131
Tutor: Liam Laing

Description: This program uses the training data gathered from the past to build 
             model that helps movie executive producers predict the gross
             of the movie with provided genre and budget, compare with other
             genres.
             
File: Movie Gross Prediction program

"""
import tkinter as tk
from tkinter.ttk import *
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
    
class MovieGui:
    '''Defines the Movie Interface'''
    
    def __init__(self, window, genres):
        '''Setup the label and button on given window'''
        
        # Delete 'Unknown' and sort the dictionary
        del genres['Unknown']        
        self.genres = dict(sorted(genres.items()))
        
        # Create some variables
        self.number = tk.StringVar()
        self.window = window
        self.scatter1 = None
        self.scatter = None
           
        # Head frame
        self.head_frame = tk.Frame(window, background='black', width=400, height=90)
        self.head_frame.grid(row=0, column=0, columnspan=2)
        
        # Foot frame
        self.foot_frame = tk.Frame(window, background='black', highlightbackground='black', highlightthickness=20, width=400, height=700)
        self.foot_frame.grid(row=1, column=1, rowspan=2)
        
        # Right frame
        self.canvas = tk.Frame(window, background='black', highlightbackground='black', highlightthickness=20, width=1000, height= 790)
        self.canvas.grid(row=0, rowspan=3, column=3)     
        
        # Configure head frame
        self.head_frame.grid_propagate(0)
        self.head_frame.grid_rowconfigure(0, weight=1)
        self.head_frame.grid_columnconfigure(1, weight=1)   
            
        # Configure foot frame
        self.foot_frame.grid_propagate(0)
        self.foot_frame.grid_rowconfigure(1, weight=1)
        self.foot_frame.grid_columnconfigure(1, weight=1) 
        
        # Configure right frame
        self.canvas.grid_propagate(0)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(1, weight=1) 
        
        # Title
        self.label_header_text_2 = tk.Label(self.head_frame, text='Movie Gross Prediction', background='black', fg='white', font=("Arial", 30))
        self.label_header_text_2.grid(row=0, column=1, columnspan=2)        
        
        # Adding canvas into right frame
        self.canvas1 = tk.Canvas(self.canvas, background='black', highlightbackground='black', width = 900, height = 350)
        self.canvas1.grid(row=0, rowspan=3, column=0)       
        
        # Create subframe in foot frame
        self.bottom_foot_frame = tk.Frame(self.foot_frame, background='black', width=370, height=650)    
        self.bottom_foot_frame.grid(row=1, sticky='n')
        self.bottom_foot_frame.grid_propagate(0)
        self.bottom_foot_frame.grid_rowconfigure(10, weight=1)
        self.bottom_foot_frame.grid_columnconfigure(1, weight=1)          
              
        # Create the widgets for the bottom_foot_frame
        # Label for genre
        self.genre_label = tk.Label(self.bottom_foot_frame, text='Genre: ', fg='white', background='black')
        self.genre_label.grid(row=0, column=0, pady=10)
        
        # Combo box for genre
        self.combobox = Combobox(self.bottom_foot_frame, values=list(self.genres.keys()), background='black')
        self.combobox.grid(row=0, column=1, pady=10)
        
        # Label for budget
        self.budget_label = tk.Label(self.bottom_foot_frame, text='Budget: ', fg='white', background='black')
        self.budget_label.grid(row=1, column=0, pady=10)
        
        # Entry for budget
        self.budget = tk.Entry(self.bottom_foot_frame, textvariable=self.number, width="20", highlightbackground='black')
        self.budget.grid(row=1, column=1, pady=10)
        
        # Information for budget
        self.budget_info = tk.Label(self.bottom_foot_frame, width='40', text='Please enter a positive number',fg='white', background='black')
        self.budget_info.grid(row=2, column=0, columnspan=2, pady=5)
        
        # View Button
        self.button_selected = tk.Button(self.bottom_foot_frame, text="View details", command=self.graphing, highlightbackground='black')
        self.button_selected.grid(row=3, column=0, columnspan=2, pady=10)
        
        #Label for information
        self.label_result = tk.Label(self.bottom_foot_frame, width='100', fg='white', text="Press 'View details'", background='black')
        self.label_result.grid(row=4, column=0, columnspan=2, pady=10)
        
        #Other predicted grosses
        self.button_compare = tk.Button(self.bottom_foot_frame, text='Compare', command=self.show_compare, highlightbackground = 'black')
        self.button_compare.grid(row=5, column=0, columnspan=2, pady=10)
        self.label_compare = tk.Label(self.bottom_foot_frame, fg='white', justify='left', background='black')
        self.label_compare.grid(row=6, column=0, columnspan=2, pady=10)
        
        #Button for second choice
        self.button_second = tk.Button(self.bottom_foot_frame, text='Second graph', command=self.compare_graph, highlightbackground = 'black')
        self.button_second.grid(row=7, column=0, columnspan=2, pady=10)
        
        #Reset
        self.button_reset = tk.Button(self.bottom_foot_frame, text="Reset", command=self.reset, highlightbackground='black')
        self.button_reset.grid(row=8, column=0, columnspan=2, pady=10)
        
        #Quit
        self.button_quit = tk.Button(self.bottom_foot_frame, text="Quit", command=self.destroy, highlightbackground='black')
        self.button_quit.grid(row=9, column=0, columnspan=2, pady=10)
        
        
    def selected_variable(self):
        '''Variable selected by user'''
        selected = self.genres[self.combobox.get()]
        self.combobox.selection_clear()
        return selected
        
    def variable_creator(self, variable):
        '''Create X and y ariable'''
        df = pd.DataFrame(variable, columns=['Budget', 'Gross'])
        X = df['Budget'].values.reshape(-1,1)
        y = df['Gross'].values.reshape(-1,1)
        return X, y    
    
    def test_and_train(self, variable):
        '''Splitting test and train data'''
        X, y = self.variable_creator(variable)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
        return X_train, X_test, y_train, y_test
    
    def linear_regression(self, variable):
        '''Linear regression'''
        X_train, X_test, y_train, y_test = self.test_and_train(variable)
        lm = LinearRegression()
        lm.fit(X_train, y_train)
        y_pred = lm.predict(X_test)
        slope = lm.coef_[0][0]
        intercept = lm.intercept_[0]
        return y_pred, slope, intercept
        
    def check_positive(self, num):
        '''Check positive'''
        if not num.isdigit():
            self.budget_info['text'] = "ERROR: Oops, this is not a positive number (*..*)"
            self.budget_info['text'] += "\n\nPlease try again"
        elif int(num) <= 0:
            self.budget_info['text'] = "ERROR: Please give me a positive number (T..T)"
        else:
            self.budget_info['text'] = ''
            return num
            
    def check_digit(self, budget):
        '''Check number'''
        budget = self.check_positive(budget)
        return budget    
        
    def gross_predict(self, variable):
        '''Predicted gross'''
        budget = self.check_digit(self.budget.get())
        if budget is not None:        
            y_pred, slope, intercept = self.linear_regression(variable)
            calculation = intercept + slope * float(budget)
            newgross = round(float(calculation), 2)
        return newgross
    
    def compare(self):
        '''Compare with other predicted grosses'''
        dict_grosses = {}
        for each_genre in list(self.genres.keys()):
            if each_genre != self.combobox.get():
                gross_info = self.genres[each_genre]
                X_train, X_test, y_train, y_test = self.test_and_train(gross_info)
                y_pred, slope, intercept = self.linear_regression(gross_info)
                newgross = self.gross_predict(gross_info)
                if slope > 0:
                    dict_grosses[newgross] = [each_genre, "Positive"]
                else:
                    dict_grosses[newgross] = [each_genre, "Negative"]
        return dict_grosses
                           
    def show_compare(self):
        '''Showing other predicted grosses to compare'''
        budget = self.check_digit(self.budget.get())
        if budget is not None:
            dict_grosses = dict(sorted(self.compare().items(), reverse=True))
            output = ''
            for gross, genre in dict_grosses.items():
                output += "({}) {}: {}\n".format(genre[1], genre[0], str(gross))
        self.label_compare['text'] = output
                
                
    def second_choice(self):
        '''Return the figures of second choice with the highest gross and the same budget'''
        budget = self.check_digit(self.budget.get())
        if budget is not None:
            dict_grosses = dict(sorted(self.compare().items(), reverse=True))
            other_genre = list(dict_grosses.values())[0][0]
            second = self.genres[other_genre]
            return other_genre, second
         
    def variable_for_graph(self, variable):
        '''Subgraphing'''
        newcounts = variable
        X_train, X_test, y_train, y_test = self.test_and_train(variable)
        y_pred, slope, intercept = self.linear_regression(variable)
        df = pd.DataFrame(newcounts, columns=['Budget', 'Gross'])
        df_test = pd.DataFrame({'X_test': X_test.flatten(), 'Predicted': y_pred.flatten()})
        return df['Budget'], df['Gross'], df_test['X_test'], df_test['Predicted']
    
    def compare_graph(self):
        '''Compare graph'''
        if self.scatter1 == None:
            budget = self.check_digit(self.budget.get())
            if budget is not None:
                other_genre, second = self.second_choice()
                df_budget, df_gross, df_xtest, df_predict = self.variable_for_graph(second)
                figure1 = plt.Figure(figsize=(4.5,7), dpi=100)
                ax1 = figure1.add_subplot(111)
                ax1.scatter(df_budget, df_gross, color = 'g')
                ax1.plot(df_xtest, df_predict, color='red', linewidth=2)
                self.scatter1 = FigureCanvasTkAgg(figure1, self.canvas1)
                self.scatter1.get_tk_widget().pack()
                ax1.set_ylabel('Gross')
                ax1.set_xlabel('Budget')
                ax1.set_title('Budget Vs. Gross - {}'.format(other_genre))      
        
    def graphing(self):
        '''Graphing'''
        if self.scatter == None and self.scatter1 == None:
            budget = self.check_digit(self.budget.get())
            if budget is not None:
                df_budget, df_gross, df_xtest, df_predict = self.variable_for_graph(self.selected_variable())
                figure = plt.Figure(figsize=(4.5,7), dpi=100)
                ax = figure.add_subplot(111)
                ax.scatter(df_budget, df_gross, color = 'g')
                ax.plot(df_xtest, df_predict, color='red', linewidth=2)
                self.scatter = FigureCanvasTkAgg(figure, self.canvas1)
                self.scatter.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                ax.set_ylabel('Gross')
                ax.set_xlabel('Budget')
                ax.set_title('Budget Vs. Gross - {}'.format(self.combobox.get()))
                newgross = self.gross_predict(self.selected_variable())
                self.label_result['text'] = "{}'s predicted gross is: {}".format(self.combobox.get(), str(newgross))
               
    def destroy(self):
        '''Destroy'''
        self.window.destroy()
             
    def reset(self):
        '''Reset button'''
        self.combobox.set("")
        self.number.set("")
        self.budget_info['text'] = ''
        self.label_compare['text'] = ''
        self.label_result['text'] = ''
        if self.scatter != None:
            self.scatter.get_tk_widget().destroy()
            self.scatter = None 
        else:
            self.scatter = None 
        if self.scatter1 != None:
            self.scatter1.get_tk_widget().destroy()
            self.scatter1 = None
        else:
            self.scatter1 = None
        self.budget_info['text'] = 'Please enter a positive number'
        self.label_result['text'] = "Press 'View details'"        

        
def read_file(filename):
    '''Read file'''
    infile = open(filename)
    lines = infile.read().splitlines()
    infile.close()
    newlist = [value for value in lines[1:] if value != ""] #Having each line in a list
    counts = {}
    for line in newlist:
        each = line.split(",")
        genres = each[4]
        counts[genres] = counts.get(genres)  
    genre_type = list(counts.keys())
    return newlist, genre_type

def filter_genre(newlist, genre_type):
    '''Categorising the movies'''
    movie = {}
    for eachs in genre_type:
        gross = []
        for lin in newlist:
            ea = lin.split(",")
            if ea[4] == eachs:
                year = int(ea[0])
                budget = int(ea[1])
                worldwide = int(ea[3])
                gross.append([budget, worldwide])
                movie[ea[4]] = gross       
    return movie
     
def main():
    '''Main'''
    file = "Data - COSC480 - Project - Thong Minh Nguyen (Martin) - 68623131.csv"
    newlist, genre_type = read_file(file)
    genres = filter_genre(newlist, genre_type) #Dictionary of movie
    window = tk.Tk()
    movie = MovieGui(window, genres)
    window.mainloop()

main()
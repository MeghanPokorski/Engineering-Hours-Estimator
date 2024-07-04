import math

import PySimpleGUI as sg
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Default estimator values. These will be updated with user input
d = {'sloc': [0], 'programming_language_C#': [0], 'programming_language_Simulink': [1]}
features = pd.DataFrame(data=d)

# Embedding the TKinter toolbar in the canvas
def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


# Main GUI
layout = [

    [sg.B('Plot'), sg.B('Exit'), sg.Text('SLOC'), sg.InputText(s=10, key='-SLOC-'),
    sg.Text('Language'), sg.Combo(['Simulink', 'C#', 'Ada'],
                                   default_value='Simulink', key='-LANGUAGE-', s=10),sg.Text('Hours: '),
    sg.Text("-", size=10, key='OUTPUT')],
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv')],
    [sg.T('Figure:')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       size=(400 * 2, 400)
                       )]
        ],
        pad=(0, 0)
    )]]

window = sg.Window('Engineering Hours Estimator', layout,use_custom_titlebar=True)

while True:
    event, values = window.read()
    # Updating the features dataframe with user input
    if values['-LANGUAGE-'] == 'Simulink':
        features.loc[0, 'programming_language_Simulink'] = 1
        features.loc[0, 'programming_language_C#'] = 0 
    elif values['-LANGUAGE-'] == 'C#':
        features.loc[0, 'programming_language_Simulink'] = 0
        features.loc[0, 'programming_language_C#'] = 1
    elif values['-LANGUAGE-'] == 'Ada':
        features.loc[0, 'programming_language_Simulink'] = 0
        features.loc[0, 'programming_language_C#'] = 0
    if 0 < float(values['-SLOC-']) < 1100:
        features.loc[0, 'sloc'] = int(values['-SLOC-'])
    else:
        sg.popup_error('Please enter a number between 1 and 1100.')
    
    if event in (sg.WIN_CLOSED, 'Exit'):  
        break          
    if event == 'Plot' and (0 < float(values['-SLOC-']) < 1100):
        # Plotting the prediction and the training data
        import pickle
        plt.style.use('ggplot')
        df = pd.read_csv('activities.csv')
        model_filename = 'overall_model.sav'
        # load the model from disk
        loaded_model = pickle.load(open(model_filename, 'rb'))
        prediction = loaded_model.predict(features)
        plt.figure(1)
        fig = plt.gcf()
        # Adjusting figure size to reduce the movement error when the mouse hovers over the figure
        DPI = fig.get_dpi()
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        fig, ax = plt.subplots()
        plt.gca()       
        for name, group in df.groupby('programming_language'):
            ax.scatter(
                group['sloc'], group['hours'], label=name)
        ax.scatter(features['sloc'], prediction, s=15, c='k', marker="o", label='Prediction')
        plt.legend(loc='upper left')
        plt.xlabel('SLOC')
        plt.ylabel('Hours')
        plt.suptitle('')
        plt.title('Hours Estimate')
        name = np.round(prediction, 2)
        # Displaying the hours estimate
        window['OUTPUT'].update(value=name)
        # Displaying the plot and toolbar
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

window.close()
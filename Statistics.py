import sys
import math
import pyperclip
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def RunPage1():
    # Create the Init Window
    window1 = sg.Window("GAC Helper", InitPage.layout)

    while True:
        event, values = window1.read()
        blacklist = [" ", ",", "\"\"", "\'\'", "-", ":", "."]
        # Load Tokens into Lists
        if event == "-FILE1-":
            f1 = open(values["-FILE1-"], "r")
            lines = f1.read()
            tempToken = ""
            for letter in lines:
                if letter not in blacklist:
                    tempToken += letter
                else:
                    acaTokens.append(tempToken)
                    tempToken = ""
            f1.close()
        if event == "-FILE2-":
            f2 = open(values["-FILE2-"], "r")
            lines = f2.read()
            tempToken = ""
            for letter in lines:
                if letter not in blacklist:
                    tempToken += letter
                else:
                    creTokens.append(tempToken)
                    tempToken = ""
            f2.close()

        if event == "Continue":
            if acaTokens == [] or creTokens == []:
                sys.exit(0)
            break
        if event == sg.WIN_CLOSED:
            sys.exit(0)
    window1.close()


def ProcessData():
    len_list_aca = []
    len_list_cre = []
    len_unique_aca = {}
    len_unique_cre = {}

    # TODO: Fix Counting Error (+1)
    # Data Processing -> {token length: count} * 2
    for tokens in acaTokens:
        len_list_aca.append(len(tokens))
    for tokens in creTokens:
        len_list_cre.append(len(tokens))
    for tok_len in len_list_aca:
        if tok_len in len_unique_aca:
            len_unique_aca[tok_len] += 1
        elif tok_len not in len_unique_aca:
            len_unique_aca[tok_len] = 1
    for tok_len in len_list_cre:
        if tok_len in len_unique_cre:
            len_unique_cre[tok_len] += 1
        elif tok_len not in len_unique_cre:
            len_unique_cre[tok_len] = 1
    # Sorted() has a implicit conversion from {token length: count} -> [(token length, count)]
    len_unique_cre = sorted(len_unique_cre.items())
    len_unique_aca = sorted(len_unique_aca.items())
    len_list_aca = sorted(len_list_aca)
    len_list_cre = sorted(len_list_cre)
    return [len_unique_aca, len_unique_cre, len_list_aca, len_list_cre]


def LoadGraphs(len_unique_aca, len_unique_cre, len_list_aca, len_list_cre):
    # Load Bar Graphs
    x_values_1, y_values_1, x_values_2, y_values_2 = [], [], [], []
    for token_len, freq in len_unique_aca:
        x_values_1.append(token_len)
        y_values_1.append(freq)
    for token_len, freq in len_unique_cre:
        x_values_2.append(token_len)
        y_values_2.append(freq)
    plt.figure(0)
    plt.bar(x_values_1, y_values_1)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel("Token Length")
    plt.ylabel("Frequency")
    plt.title("Column Graph of Size of Tokens in Academic Writing Source")
    plt.figure(1)
    plt.bar(x_values_2, y_values_2)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel("Token Length")
    plt.ylabel("Frequency")
    plt.title("Column Graph of Size of Tokens in Creative Writing Source")

    # Load Cumulative Frequency Graph
    cumulative_freq_1, cumulative_freq_2 = [], []
    for index, freq in enumerate(y_values_1):
        if index == 0:
            cumulative_freq_1.append(freq)
        else:
            cumulative_freq_1.append(cumulative_freq_1[index - 1] + freq)
    for index, freq in enumerate(y_values_2):
        if index == 0:
            cumulative_freq_2.append(freq)
        else:
            cumulative_freq_2.append(cumulative_freq_1[index - 1] + freq)
    plt.figure(2)
    plt.plot(x_values_1, cumulative_freq_1)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel("Token Length")
    plt.ylabel("Frequency")
    plt.title("Cumulative Frequency of Size of Tokens in Academic Writing Source")
    plt.figure(3)
    plt.plot(x_values_2, cumulative_freq_2)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel("Token Length")
    plt.ylabel("Frequency")
    plt.title("Cumulative Frequency Graph of Size of Tokens in Creative Writing Source")

    # Load Box and Whisker Diagram
    plt.figure(4)
    plt.boxplot(len_list_aca)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title("The Box Plot for the Academic Writing Sample.")
    plt.figure(5)
    plt.boxplot(len_list_cre)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title("The Box Plot for the Creative Writing Sample.")

    # DEBUG USE ONLY
    print(len_list_aca)
    print(len_list_cre)
    print(len_unique_aca)
    print(len_unique_cre)
    print(y_values_1)
    print(y_values_2)
    print(cumulative_freq_1)
    print(cumulative_freq_2)
    plt.show()

    # Calculate mean sd median Q1 Q3 IQR
    Xf_1, fsq_1 = [], []
    Xf_2, fsq_2 = [], []
    mean_1, sd_1, median_1, Q1_1, Q3_1, IQR_1 = 0, 0, 0, 0, 0, 0
    mean_2, sd_2, median_2, Q1_2, Q3_2, IQR_2 = 0, 0, 0, 0, 0, 0
    for token_len, freq in len_unique_aca:
        Xf_1.append(token_len * freq)
    mean_1 = sum(Xf_1) / sum(y_values_1)
    for token_len, freq in len_unique_aca:
        fsq_1.append(freq * (token_len - mean_1) ** 2)
    sd_1 = math.sqrt(sum(fsq_1) / sum(y_values_1))
    for token_len, freq in len_unique_cre:
        Xf_2.append(token_len * freq)
    mean_2 = sum(Xf_2) / sum(y_values_2)
    for token_len, freq in len_unique_aca:
        fsq_2.append(freq * (token_len - mean_2) ** 2)
    sd_2 = math.sqrt(sum(fsq_2) / sum(y_values_2))
    if len(len_list_aca) % 2 == 0:  # if even
        median_1 = (len_list_aca[int(len(len_list_aca) / 2 - 1) - 1] + len_list_aca[
                    int(len(len_list_aca) / 2 + 1) - 1]) / 2
    else:  # if odd
        median_1 = len_list_aca[int(len(len_list_aca) / 2) - 1]
    if len(len_list_cre) % 2 == 0:  # if even
        median_2 = (len_list_cre[int(len(len_list_cre) / 2 - 1) - 1] + len_list_cre[
                    int(len(len_list_cre) / 2 + 1) - 1]) / 2
    else:  # if odd
        median_2 = len_list_cre[int(len(len_list_cre) / 2) - 1]
    # Copy the results to the clipboard
    pyperclip.copy("Academic Source Data:" + "\nMean = " + str(mean_1) + "\nStandard Deviation = " + str(sd_1) +
                   "\nMedian = " + str(median_1) + "\nQ1 = " + str(Q1_1) +
                   "\nQ3 = " + str(Q3_1) + "\nIQR = " + str(IQR_1) + "\n\n"
                                                                     "Creative Writing Source Data:" + "\nMean = " + str(
        mean_2) +
                   "\nStandard Deviation = " + str(sd_2) +
                   "\nMedian = " + str(median_2) + "\nQ1 = " + str(Q1_2) +
                   "\nQ3 = " + str(Q3_2) + "\nIQR = " + str(IQR_2)
                   )

    # Create Output Window
    column1 = [
        [sg.Text("Academic Source Data:")],
        [sg.Text("Mean = " + str(mean_1) + "\nStandard Deviation = " + str(sd_1) +
                 "\nMedian = " + str(median_1) + "\nQ1 = " + str(Q1_1) +
                 "\nQ3 = " + str(Q3_1) + "\nIQR = " + str(IQR_1))]
    ]
    column2 = [
        [sg.Text("Creative Writing Source Data:")],
        [sg.Text("Mean = " + str(mean_2) + "\nStandard Deviation = " + str(sd_2) +
                 "\nMedian = " + str(median_2) + "\nQ1 = " + str(Q1_2) +
                 "\nQ3 = " + str(Q3_2) + "\nIQR = " + str(IQR_2))]
    ]
    layout = [
        [sg.Column(column1), sg.VSeperator(), sg.Column(column2)],
        [sg.Text("Result Copied to Clipboard!", text_color="yellow")],
    ]

    window2 = sg.Window("GAC Helper", layout)
    while True:
        event, values = window2.read()
        if event == sg.WIN_CLOSED:
            break
    window2.close()


class InitPage:
    academicSourceUI = [
        [sg.Text("Academic Writing Source"), sg.In(size=(25, 1), enable_events=True, key="-FILE1-"), sg.FileBrowse()],
        [sg.Text("*Note: ONLY Supports .txt", text_color="red")]
    ]

    creativeSourceUI = [
        [sg.Text("Creative Writing Source"), sg.In(size=(25, 1), enable_events=True, key="-FILE2-"), sg.FileBrowse()],
        [sg.Text("")]
    ]

    layout = [
        [sg.Column(academicSourceUI), sg.VSeperator(), sg.Column(creativeSourceUI)],
        [sg.Button("Continue")]
    ]


acaTokens = []
creTokens = []

if __name__ == '__main__':
    RunPage1()
    data = ProcessData()
    LoadGraphs(data[0], data[1], data[2], data[3])

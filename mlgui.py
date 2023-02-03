import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo
from classification import fit_predict_evaluate_classification
from EDA import create_descriptives
from report_templates import classification_report_template
from multiprocessing import freeze_support
freeze_support()

def make_report(filename: str, export_name="report.html", outcome=None):
    """make a report from a csv file"""
    df = pd.read_csv(filename)
    if any([x == "Unnamed: 0" for x in df.columns.tolist()]):
        _ = df.drop(columns="Unnamed: 0", inplace=True)
    EDA_results_dict = create_descriptives(
        data=df, cli_output=False, outcome=outcome)

    classification_results_dict = fit_predict_evaluate_classification(
        data=df.dropna(), outcome=outcome)

    _ = classification_report_template(filename=export_name,
                                       dataframe_head_insert=EDA_results_dict["head_df"].to_html(
                                       ),
                                       dataframe_descriptives_insert=EDA_results_dict["desc_df"].to_html(
                                       ),
                                       plot_descriptives_insert=EDA_results_dict["desc_plot"],
                                       plot_outcomes_insert=EDA_results_dict["outcome_count_plot"],
                                       plot_corrs_insert=EDA_results_dict["corr_plot"],
                                       dataframe_missingness_insert=EDA_results_dict["miss_df"].to_html(
                                       ),
                                       dataframe_optimized_model_insert=classification_results_dict["model_summary_df"].to_html(
                                       ),
                                       plot_cross_validation_insert=classification_results_dict[
                                           "cross_val_plot"],
                                       plot_confusion_insert=classification_results_dict["confusion_plot"],
                                       dataframe_filename=filename)

def report_save_location():
    """callback when the select save location button clicked
    """
    global save_location
    save_location = filedialog.askdirectory()
    msg = f'You have the following location to save the report: {save_location}'
    showinfo(
        title='Information',
        message=msg
    )
    

def upload_action(event=None):
    filename = filedialog.askopenfilename()
    print(f'Selected file: {filename}')
    print(f'Selected outcome variable: {outcome.get()}')
    print(f'Selected save location: {save_location}')
    _ = make_report(filename=filename, export_name=f"{save_location}/report.html", outcome=outcome.get())

    
def outcome_clicked():
    """callback when the outcome button clicked
    """
    msg = f'You have chosen outcome: {outcome.get()}'
    showinfo(
        title='Information',
        message=msg
    )


root = tk.Tk()
root.geometry("800x500")
root.title("Machine Learning Report Creation")
# root.iconbitmap("./assets/favicon.ico")
# root.iconbitmap('./assets/test.ico')
# root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./assets/logo.png'))

# store outcome_string
outcome = tk.StringVar()

# Upload frame
upload_report_frame = ttk.Frame(root)
upload_report_frame.pack(padx=30, fill='x', expand=True)

introduction = ttk.Label(upload_report_frame, 
                         text="Upload a .csv file and specify the outcome variable to create a Machine Learning Report",
                         font=("Arial", 30), 
                         wraplength=800, justify="center")
introduction.pack(pady=20)

outcome_label = ttk.Label(upload_report_frame, text="Type in the outcome variable you are interested in:", anchor="w", font=("Arial", 20))
outcome_label.pack(pady=10, fill="both")
outcome_entry = ttk.Entry(upload_report_frame, textvariable=outcome)
outcome_entry.pack(fill="both", expand=False)
outcome_button = ttk.Button(upload_report_frame, text='Choose Outcome', command=outcome_clicked)
outcome_button.pack(fill="both")

save_loc_label = ttk.Label(upload_report_frame, text="Choose a directory to save the report.html to:", anchor="w", font=("Arial", 20))
save_loc_label.pack(pady=10, fill="both")
save_loc_button = ttk.Button(upload_report_frame, text='Choose Directory', command=report_save_location)
save_loc_button.pack(fill="both")

upload_label = ttk.Label(upload_report_frame, text="Choose a csv file to base the machine learning analysis on:", anchor="w", font=("Arial", 20))
upload_label.pack(pady=10, fill="both")
upload_button = ttk.Button(upload_report_frame, text='Choose File', command=upload_action)
upload_button.pack(fill="both")

# Create a progressbar widget
progress_bar = ttk.Progressbar(upload_report_frame, orient="horizontal",
                              mode="determinate", maximum=100, value=0)
progress_bar.start()
progress_bar.step(10)

root.mainloop()
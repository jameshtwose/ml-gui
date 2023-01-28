import pandas as pd
from datetime import datetime
# import pdfkit

def create_date_html():
    """
    Create a string formatted correctly to be inserted in the report.html consisting
    of the current date and time that it was run
    Parameters
    ----------
    None
    Returns
    -------
    str
        The correctly formatted date and time that the function was run
    """

    return f"<p>This report was created on {pd.to_datetime(datetime.now()).round('1s')}</p>"


def classification_report_template(
    filename=None,
    dataframe_head_insert=None,
    dataframe_descriptives_insert=None,
    plot_descriptives_insert=None,
    plot_outcomes_insert=None,
    plot_corrs_insert=None,
    dataframe_missingness_insert=None,
    dataframe_optimized_model_insert=None,
    plot_cross_validation_insert=None,
    plot_confusion_insert=None,
    pictures_folder="insert_files",
    dataframe_filename=None,
    export_as_pdf=False
):
    """
    Create a html report of ML classification.
    Parameters
    ----------
    filename: str
        A string indicating the name of the created file
    Returns
    -------
    None
    """

    if filename is None:
        filename = "report.html"

    style_insert = """
    body {
        font-family: 'Raleway', sans-serif;
        --darkgrey: grey;
        --yellow: #fcdd14;
        --yellowgradient: #fcdd1462;
        --white: #ffffff;
        --purple: #43125d;
        --purplegradient: #43125dce;
        color: var(--purple);
    }
    #mainbody {
        padding-top: 50px;
        padding-left: 5%;
        padding-bottom: 50px;
        padding-right: 300px;
        text-align: left;
    }
    #row {
        padding-top: 20px;
        padding-bottom: 20px;
    }
    p {
        font-family: 'Raleway', sans-serif;
    }
    p.top-summary {
        color: var(--grey);
        border: 2px solid var(--yellowgradient);
        padding: 1em 5em 1em 1em;
        display: inline-block;
    }
    p.exception {
        color: red
    }
    p span {
        color: var(--grey)
    }
    p.explanation {
        font-style: italic;
    }
    p:hover {
        background: var(--yellowgradient);
        cursor: pointer;
    }
    h1 {
        color: var(--grey);
        padding-bottom: 10px;
    }
    h1 span {
        font-size:20px;
        color: var(--purple);
    }
    h2 {
        color: var(--purple);
        padding-bottom: 10px;
        font-size: 26px;
    }
    h3 {
        color: var(--purple);
        font-size: 20px;
        padding-top: 50px;
    }
    h3::before{content: "-"}
    ul li a {
        color: var(--purple);
    }
    li {
        color: var(--purple);
        padding: 0.2%;
    }
    .dataframe {
        color: var(--grey) !important;
        background-color: white;
        border-collapse: collapse;
        border: none;
        width: 90%;
        display: block;
        max-width: fit-content;
        margin: 5px;
        overflow-x: auto;
    }
    .dataframe th, .dataframe td {
        border-left: 50px solid transparent;
    }
    .dataframe tr>td:first-child {
        border:0px;
    }
    tbody tr:hover {
        background: var(--yellowgradient);
        cursor: pointer;
    }
    .singlecolumn {
        width: 25%
    }
    .singlecolumnwide {
        width: 100%
    }
    .verticalindex thead tr th.index_name {
        text-align: right;
        writing-mode: vertical-lr;
        rotate: 180deg;
    }
    .blank {
        background-color: transparent !important;
    }
    .index_name {
        background-color: transparent !important;
    }
    """

    html_str = f"""<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title></title>
            <meta name="description" content="">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link
                href="https://fonts.googleapis.com/css2?family=Raleway:wght@350&display=swap"
                rel="stylesheet">
            <link
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
                rel="stylesheet"
                integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD"
                crossorigin="anonymous">
            <style>
                {style_insert}
            </style>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script> 
        </head>
        <body>
            <section id="mainbody">
                <h1>Machine Learning Classification Report</h1>
                <section>{create_date_html()}</section>
                <h2 id="steps-">The steps done in running this classification:</h2>
                <ul>
                    <li>read in the data frame: <code>{dataframe_filename}</code></li>
                    <li>run a small exploratory data analysis (EDA)</li>
                    <ul>
                        <li>show the head of the data frame</li>
                        <li>show some descriptives</li>
                        <li>plot a scatter matrix between all columns</li>
                        <li>plot the countplot in the outcome</li>
                        <li>plot the correlations between all features</li>
                        <li>show the amount of missing values per column</li>
                    </ul>
                    <li>show the optimized model summary</li>
                    <li>plot the metrics from cross validating the model</li>
                    <li>plot the confusion matrix of the classification</li>
                </ul>
                <section id="row">
                <h2>Dataframe head:</h2>
                    <section>{dataframe_head_insert}</section>
                </section>
                <section id="row">
                <h2>Dataframe descriptives:</h2>
                    <section>{dataframe_descriptives_insert}</section>
                    <section>{plot_descriptives_insert}</section>
                    <section>{plot_outcomes_insert}</section>
                </section>
                <section id="row">
                <h2>Correlations between possible features:</h2>
                    <section>{plot_corrs_insert}</section>
                </section>
                <section id="row">
                <h2>Dataframe missingness summary:</h2>
                    <section>{dataframe_missingness_insert}</section>
                </section>
                <section id="row">
                <h2>Optimized model summary:</h2>
                    <section>{dataframe_optimized_model_insert}</section>
                </section>
                <section id="row">
                <h2>Cross Validation Plot</h2>
                    <section>{plot_cross_validation_insert}</section>
                </section>
                <section id="row">
                <h2>Plot Confusion Matrix</h2>
                    <section>{plot_confusion_insert}</section>
                </section>            
            </section>
            <script src="" async defer></script>
        </body>
    </html>
    """

    with open(filename, "w") as f:
        f.write(html_str)
        
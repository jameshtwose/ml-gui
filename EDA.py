import plotly
import plotly.express as px


def create_descriptives(data, cli_output=True, outcome=None):
    if cli_output:
        print("Data Frame head:")
        print(data.head())
        print("\nData Frame Descriptives:")
        print(data.describe().round(2))
        print("\nAmount of missings per column")
        print(data.isna().sum())
    
    if outcome is None:
        desc_fig = px.scatter_matrix(data, height=1000)
        outcome_count_fig = None
        outcome_count_plot = None
    else:
        desc_fig = px.scatter_matrix(data, color=outcome, height=1000)
        count_df = data[outcome].value_counts().to_frame(
            name="count").reset_index().rename(columns={"index": "outcome"})
        outcome_count_fig = px.bar(
            data_frame=count_df, x="outcome", y="count", color="outcome", title=f"Balance in outcome ({outcome})")
        outcome_count_plot = plotly.offline.plot(
            outcome_count_fig, include_plotlyjs=False, output_type='div')
    desc_fig.update_traces(diagonal_visible=False)

    corr_fig = px.imshow(data.corr(numeric_only=True).round(3), text_auto=True)

    return {"head_df": data.head(),
            "desc_df": data.describe().round(2),
            "miss_df": data.isna().sum().to_frame(name="Missings").T,
            "desc_plot": plotly.offline.plot(desc_fig, include_plotlyjs=False, output_type='div'),
            "outcome_count_plot": outcome_count_plot,
            "corr_plot": plotly.offline.plot(corr_fig, include_plotlyjs=False, output_type='div'), }
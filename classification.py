import pandas as pd
import plotly.express as px
import plotly
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate, RepeatedStratifiedKFold
from sklearn.metrics import confusion_matrix, make_scorer, f1_score, accuracy_score, balanced_accuracy_score, recall_score, precision_score

from jmspack.ml_utils import optimize_model


def fit_predict_evaluate_classification(data, outcome):
    features_list = data.select_dtypes("number").columns.tolist()
    X = data[features_list]
    y = data[outcome]

    (optimized_estimator,
     feature_ranking,
     feature_selected,
     feature_importance,
     optimized_params_df,
     ) = optimize_model(X=X, y=y, estimator=RandomForestClassifier(),
                        grid_params_dict={
         "max_depth": [1, 2, 3, 4, 5, 10],
         "n_estimators": [10, 20, 30, 40, 50],
         "max_features": ["log2", "sqrt"],
         "criterion": ["gini", "entropy"],
     },
        gridsearch_kwargs={"scoring": "accuracy", "cv": 3, "n_jobs": -2},
        rfe_kwargs={"n_features_to_select": 2, "verbose": 1})

    model_summary_df = optimized_params_df.assign(**{"selected_features": str(feature_selected)}).T
    
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=10, random_state=1)
    if data[outcome].nunique() > 2:
        scorers = {'accuracy': make_scorer(accuracy_score),
                   'balanced_accuracy': make_scorer(balanced_accuracy_score),
                   'f1': make_scorer(f1_score, average='weighted'),
                   'precision': make_scorer(precision_score, average='weighted'),
                   'recall': make_scorer(recall_score, average='weighted')}
    else:
        scorers = ('accuracy',
                   'balanced_accuracy',
                   'f1',
                   'f1_weighted',
                   'precision',
                   'precision_weighted',
                   'recall',
                   'recall_weighted',
                   'roc_auc',
                   )

    cross_val_out = cross_validate(estimator=optimized_estimator, X=X[feature_selected], y=y.astype(
        "category").cat.codes, groups=None, scoring=scorers, cv=cv, n_jobs=-1)

    cv_metrics_df = pd.DataFrame(cross_val_out).drop(
        ["fit_time", "score_time"], axis=1).melt(var_name="Metric")

    cross_val_fig = px.box(data_frame=cv_metrics_df, x="Metric", y="value", color="Metric", points="all",
                           title=f"All performance metrics {optimized_estimator.__class__.__name__} with cross validation")

    conf_mat = confusion_matrix(
        y_true=y, y_pred=optimized_estimator.predict(X))

    confusion_df = pd.DataFrame(
        conf_mat, index=data[outcome].unique(), columns=data[outcome].unique())

    confusion_fig = px.imshow(confusion_df, text_auto=True)

    return {"model_summary_df": model_summary_df,
            "cross_val_plot": plotly.offline.plot(cross_val_fig, include_plotlyjs=False, output_type='div'),
            "confusion_plot": plotly.offline.plot(confusion_fig, include_plotlyjs=False, output_type='div')}
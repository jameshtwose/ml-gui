import pandas as pd
import plotly.express as px
import plotly
import numpy as np
import sklearn
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate, RepeatedStratifiedKFold, train_test_split, GridSearchCV
from sklearn.feature_selection import RFE
from sklearn.metrics import confusion_matrix, make_scorer, f1_score, accuracy_score, balanced_accuracy_score, recall_score, precision_score


def optimize_model(
    X: pd.DataFrame,
    y: pd.Series,
    estimator: BaseEstimator = sklearn.ensemble.RandomForestClassifier(),
    grid_params_dict: dict = {
        "max_depth": [1, 2, 3, 4, 5, 10],
        "n_estimators": [10, 20, 30, 40, 50],
        "max_features": ["log2", "auto", "sqrt"],
        "criterion": ["gini", "entropy"],
    },
    gridsearch_kwargs: dict = {"scoring": "roc_auc", "cv": 3, "n_jobs": -2},
    rfe_kwargs: dict = {"n_features_to_select": 2, "verbose": 1},
):
    
    """tmp

    Parameters
    ----------
    tmp: 
        TODO
 
    Returns
    -------
    TODO

    Examples
    --------
    >>> #TODO
    
    """
    # Perform a 75% training and 25% test data split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3,
        # stratify=y,
        random_state=42
    )

    # Instantiate grid_dt
    grid_dt = GridSearchCV(
        estimator=estimator, param_grid=grid_params_dict, **gridsearch_kwargs,
    )

    # Optimize hyperparameter
    _ = grid_dt.fit(X_train, y_train)

    # Extract the best estimator
    optimized_estimator = grid_dt.best_estimator_

    # Create the RFE with a optimized random forest
    rfe = RFE(estimator=optimized_estimator, **rfe_kwargs)

    # Fit the eliminator to the data
    _ = rfe.fit(X_train, y_train)

    # create dataframe with features ranking (high = dropped early on)
    feature_ranking = pd.DataFrame(
        data=dict(zip(X.columns, rfe.ranking_)), index=np.arange(0, len(X.columns))
    )
    feature_ranking = feature_ranking.loc[0, :].sort_values()

    # create dataframe with feature selected
    feature_selected = X.columns[rfe.support_].to_list()

    # create dataframe with importances per feature
    feature_importance = pd.Series(
        dict(zip(X.columns, optimized_estimator.feature_importances_.round(2)))
    )

    return (
        optimized_estimator,
        feature_ranking,
        feature_selected,
        feature_importance,
        pd.DataFrame(optimized_estimator.get_params(), index=["optimal_parameters"]),
    )


def fit_predict_evaluate_classification(data, outcome):
    features_list = data.select_dtypes("number").columns.tolist()
    X = data[features_list]
    y = data[outcome]

    (optimized_estimator,
     feature_ranking,
     feature_selected,
     feature_importance,
     optimized_params_df,
     ) = optimize_model(X=X, y=y, estimator=RandomForestClassifier(n_jobs=1, random_state=42),
                        grid_params_dict={
         "max_depth": [1, 2, 3, 4, 5, 10],
         "n_estimators": [10, 20, 30, 40, 50],
         "max_features": ["log2", "sqrt"],
         "criterion": ["gini", "entropy"],
     },
        gridsearch_kwargs={"scoring": "accuracy", "cv": 3, "n_jobs": 1},
        rfe_kwargs={"n_features_to_select": 2, "verbose": 1})

    model_summary_df = optimized_params_df.assign(**{"selected_features": str(feature_selected)}).T
    
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=1)
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
        "category").cat.codes, groups=None, scoring=scorers, cv=cv, n_jobs=1)

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
            # "cross_val_plot": None,
            "cross_val_plot": plotly.offline.plot(cross_val_fig, include_plotlyjs=False, output_type='div'),
            "confusion_plot": plotly.offline.plot(confusion_fig, include_plotlyjs=False, output_type='div')}
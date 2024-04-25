import os

import catboost
import pandas as pd
from sklearn import metrics

import mlops_ods.utils.utils_etl as ut_etl
import mlops_ods.utils.utils_model as ut_models
from mlops_ods.config import load_config_yaml
from mlops_ods.utils import utils_etl

PATH_TO_DATA = os.path.join(os.path.dirname(os.getcwd()), "mlops_ods", "dataset")
PATH_TO_MODEL = os.path.join(os.path.dirname(os.getcwd()), "resources", "model.bin")
logger = utils_etl.get_logger(__name__)
logger.propagate = False


def main(train: bool = True):
    """
    Train or predict data with model

    :param train: if true - train, if false - predict
    :return:
    """
    mode = "train" if train else "predict"
    logger.info("Start job in mode %s", mode)
    config = load_config_yaml()

    logger.info("Get data")
    file_name = "2015-street-tree-census-tree-data.csv"
    ut_etl.download_kaggle_dataset_if_not_exist(PATH_TO_DATA, file_name)

    df = pd.read_csv(f"{PATH_TO_DATA}/{file_name}")
    df = df[~df["health"].isna()]

    logger.info("Preprocess data")
    ut_models.drop_columns(df)
    ut_models.preprocess_data(df)

    num_cols = config["features"]["numerical"]
    cat_cols = config["features"]["categorical"]
    total_cols = num_cols + cat_cols

    if train:
        logger.info("Fit model")
        clf = catboost.CatBoostClassifier(
            iterations=config["model_params"]["iterations"],
            verbose=config["model_params"]["verbose"],
            random_seed=config["model_params"]["random_seed"],
            cat_features=cat_cols,
        )
        clf.fit(df[total_cols], df["health"])
        predictions = clf.predict_proba(df[total_cols])
        roc_auc = metrics.roc_auc_score(df["health"], predictions, multi_class="ovr")
        logger.info("Roc auc score: %s", roc_auc)

        logger.info("Save model")
        ut_etl.save_model(model_path=PATH_TO_MODEL, model=clf)

    else:
        logger.info("Predict")
        clf = ut_etl.load_model(PATH_TO_MODEL)
        predictions = clf.predict_proba(df[total_cols])
        logger.info("Number of predictions: %s", len(predictions))


if __name__ == "__main__":
    main(train=True)

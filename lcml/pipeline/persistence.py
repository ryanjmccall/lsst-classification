import json
import os
import platform

import sklearn
from sklearn.externals import joblib

from lcml.utils.basic_logging import BasicLogging


logger = BasicLogging.getLogger(__name__)


def saveModel(model, modelPath, params=None, metrics=None):
    """If 'modelPath' is specified, the model and its metadata, including
    'trainParams' and 'cvScore' are saved to disk.

    :param model: a trained ML model, could be any Python object
    :param modelPath: save path
    :param params: all experiment params including hyperparameters
    :param metrics: metric values obtained from running model on test data
    """
    joblib.dump(model, modelPath)
    logger.info("Dumped model to: %s", modelPath)
    metadataPath = _metadataPath(modelPath)
    archBits = platform.architecture()[0]
    metadata = {"archBits": archBits, "sklearnVersion": sklearn.__version__,
                "pythonSource": __name__, "params": params,
                "metrics": metrics}
    with open(metadataPath, "w") as f:
        json.dump(metadata, f)


def loadModel(modelPath):
    try:
        model = joblib.load(modelPath)
    except IOError:
        logger.warning("Failed to load model from: %s", modelPath)
        return None, None

    logger.info("Loaded model from: %s", modelPath)
    metadataPath = _metadataPath(modelPath)
    try:
        with open(metadataPath) as mFile:
            metadata = json.load(mFile)
    except IOError:
        logger.warning("Metadata file doesn't exist: %s", metadataPath)
        return None, None

    if metadata["archBits"] != platform.architecture()[0]:
        logger.critical("Model created on arch: %s but current arch is %s",
                        metadata["archBits"], platform.architecture()[0])
        raise ValueError("Unusable model")

    return model, metadata


def _metadataPath(modelPath):
    finalDirLoc = modelPath.rfind(os.sep)
    return os.path.join(modelPath[:finalDirLoc], "metadata.json")

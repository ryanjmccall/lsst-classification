from multiprocessing import cpu_count, Pool

from lcml.utils.basic_logging import BasicLogging


logger = BasicLogging.getLogger(__name__)


def multiprocessMapGenerator(func, jobArgs, reportFrequency=100):
    """Executes a function on a batch of inputs using multiprocessing in an
    unordered fashion (`multiprocessing.Pool.imap_unordered`). Reports progress
    periodically as jobs complete

    :param func: function to execute
    :param jobArgs: iterable of tuples where each tuple is the arguments to
    `func` for a single job
    :param reportFrequency: After a batch of jobs having this size completes,
    log simple status report
    :return list of job results
    """
    p = Pool(processes=cpu_count())
    i = -1
    for i, result in enumerate(p.imap_unordered(func, jobArgs), 1):
        yield result
        if i % reportFrequency == 0:
            logger.info("multiprocessing completed: %s", i)

    logger.info("multiprocessing: total completed: %s", i)


def feetsExtract(args):
    """Wrapper function conforming to Python multiprocessing API performing the
    `feets` library's feature extraction.
    """
    return _feetsExtract(*args)


def _feetsExtract(featureSpace, uid, label, times, mags, errors):
    """
    :param featureSpace: feets.FeatureSpace object
    :param uid: light curve uid
    :param label: class label
    :param times: lc times
    :param mags: lc mags
    :param errors: lc errors
    :return: lc uid, lc class label, feature names, feature values
    """
    return (uid, label) + featureSpace.extract(times, mags, errors)

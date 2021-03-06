import numpy as np
import pytest

import autokeras as ak
from tests import common


@pytest.fixture(scope='module')
def tmp_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('task_api')


def test_image_classifier(tmp_dir):
    train_x = common.generate_data(num_instances=100, shape=(32, 32, 3))
    train_y = common.generate_one_hot_labels(num_instances=100, num_classes=10)
    clf = ak.ImageClassifier(directory=tmp_dir, max_trials=2, seed=common.SEED)
    clf.fit(train_x, train_y, epochs=1, validation_split=0.2)
    assert clf.predict(train_x).shape == (len(train_x), 10)


def test_image_regressor(tmp_dir):
    train_x = common.generate_data(num_instances=100, shape=(32, 32, 3))
    train_y = common.generate_data(num_instances=100, shape=(1,))
    clf = ak.ImageRegressor(directory=tmp_dir, max_trials=2, seed=common.SEED)
    clf.fit(train_x, train_y, epochs=1, validation_split=0.2)
    assert clf.predict(train_x).shape == (len(train_x), 1)


def test_text_classifier(tmp_dir):
    (train_x, train_y), (test_x, test_y) = common.imdb_raw()
    clf = ak.TextClassifier(directory=tmp_dir, max_trials=2, seed=common.SEED)
    clf.fit(train_x, train_y, epochs=1, validation_data=(test_x, test_y))
    assert clf.predict(test_x).shape == (len(test_x), 1)


def test_text_regressor(tmp_dir):
    (train_x, train_y), (test_x, test_y) = common.imdb_raw()
    train_y = common.generate_data(num_instances=train_y.shape[0], shape=(1,))
    test_y = common.generate_data(num_instances=test_y.shape[0], shape=(1,))
    clf = ak.TextRegressor(directory=tmp_dir, max_trials=2, seed=common.SEED)
    clf.fit(train_x, train_y, epochs=1, validation_data=(test_x, test_y))
    assert clf.predict(test_x).shape == (len(test_x), 1)


def test_structured_data_from_numpy_regressor(tmp_dir):
    num_data = 500
    num_train = 400
    data = common.generate_structured_data(num_data)
    x_train, x_test = data[:num_train], data[num_train:]
    y = common.generate_data(num_instances=num_data, shape=(1,))
    y_train, y_test = y[:num_train], y[num_train:]
    clf = ak.StructuredDataRegressor(directory=tmp_dir,
                                     max_trials=1,
                                     seed=common.SEED)
    clf.fit(x_train, y_train, epochs=2, validation_data=(x_train, y_train))
    assert clf.predict(x_test).shape == (len(y_test), 1)


def test_structured_data_from_numpy_classifier(tmp_dir):
    num_data = 500
    num_train = 400
    data = common.generate_structured_data(num_data)
    x_train, x_test = data[:num_train], data[num_train:]
    y = common.generate_one_hot_labels(num_instances=num_data, num_classes=3)
    y_train, y_test = y[:num_train], y[num_train:]
    clf = ak.StructuredDataClassifier(directory=tmp_dir,
                                      max_trials=1,
                                      seed=common.SEED)
    clf.fit(x_train, y_train, epochs=2, validation_data=(x_train, y_train))
    assert clf.predict(x_test).shape == (len(y_test), 3)

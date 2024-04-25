# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Thomas Hartmann
#
# This file is part of the obob_mne Project, see:
# https://gitlab.com/obob/obob_mne
#
#    obob_mne is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    obob_mne is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with obob_subjectdb. If not, see <http://www.gnu.org/licenses/>.

import mne
import copy
import numpy
import logging

from .helpers import _get_Y_from_metadata


class TemporalArray(mne.EvokedArray):
    """Base class for temporal decoding.

    Parameters
    ----------
    raw_scores : :class:`numpy.ndarray` shape (n_times) or (n_folds, n_times)
        The scores of the classification
    weights : :class:`numpy.ndarray` shape (n_channels, n_times)
        Classifier weights
    n_classes : int
        The number of classes
    info : dict
        Info dict
    tmin : float
        Time of the first sample in seconds
    scoring_name : str
        Name of the scoring function (i.e. Accuracy...)
    c_factors_training : str
        Name of the factors over which was collapsed in the training set
    nave : int, optional
        Number of epochs in the training set.
    nave_testing : int or None
        Number of epochs in the testing set. If ``None``, it is copied
        from nave.
    c_factors_testing : None or str
        Name of the factors over which was collapsed in the testing set.
        If ``None``, it is copied from c_factors_training.

    """

    def __init__(self, raw_scores, weights, n_classes, info, tmin,
                 scoring_name,
                 c_factors_training, nave=1, nave_testing=None,
                 c_factors_testing=None):
        self._scores_raw = raw_scores
        self._nclasses = n_classes
        self._scoring_name = scoring_name
        self._c_factors_training = c_factors_training
        if c_factors_testing is None:
            self._c_factors_testing = self._c_factors_training
        else:
            self._c_factors_testing = c_factors_testing

        if nave_testing is None:
            nave_testing = nave

        self.nave_testing = nave_testing
        self.nave = nave

        super(TemporalArray, self).__init__(weights, info, tmin, nave=nave)

    @property
    def scores(self):
        """:class:`numpy.ndarray`: The scores of the classification"""
        if self._scores_raw.ndim == 1:
            return self._scores_raw
        else:
            return numpy.average(self._scores_raw, axis=0)

    @property
    def nclasses(self):
        return self._nclasses

    @property
    def chance_level(self):
        """float: The chance level of the classifier."""
        return 1.0 / self._nclasses

    def plot_scores(self, axes=None, show=True):
        """Plot the scores as a line plot.

        Parameters
        ----------
        axes : :class:`matplotlib.axes.Axes` or None, optional
            The axes where to draw the plot. If ``None``, a new figure is
            created.
        show : bool, optional
            True to actually show the plot.
        """
        import matplotlib.pyplot as plt

        if not isinstance(axes, plt.Axes):
            fig, axes = plt.subplots(1, 1)
        else:
            fig = axes.get_figure()

        axes.plot(self.times, self.scores, label='score')
        axes.axhline(self.chance_level, color='k', linestyle='--',
                     label='chance')
        axes.set_xlabel('Times')
        axes.set_ylabel(self._scoring_name)
        axes.legend()
        axes.axvline(.0, color='k', linestyle='-')
        axes.set_title('Sensor space decoding')
        if show:
            plt.show()

        return fig


class Temporal(TemporalArray):
    """Apply a decoding pipeline to every sample.

    Use this class to perform Temporal decoding. This means that a classifier
    is trained on every sample and tested on that very sample.

    The minimum requirements are the data as :class:`mne.Epochs` and
    the pipeline as :class:`sklearn.pipeline.Pipeline`, which is most
    commonly generated using :func:`sklearn.pipeline.make_pipeline`.

    This class treats every individual ``event_id`` as an individual target.
    If you want to combine multiple ``events_id`` into one target, you can
    use :func:`epochs.collapse_conditions`.

    If you want the training and testing data to be different, you can supply
    the training data to ``epochs`` and the testing data to ``epochs_test``.

    Cross validation will be run only if training and testing data are equal
    (i.e., when ``epochs_test=None``).

    Parameters
    ----------
    epochs : :class:`mne.Epochs`
        The epochs to apply the classifier pipeline to.
    pipeline : :class:`sklearn.pipeline.Pipeline`
        The classifier pipeline to use. Most likely created with
        :func:`sklearn.pipeline.make_pipeline`
    epochs_test : :class:`mne.Epochs` or None, optional
        If set, the classifier gets tested on this data. The event_ids must
        be equal. No crossvalidation will be run in this case.
    cv : int, optional
        The amount of folds for cross validation
    scoring : str or callable, optional
        The scoring function to use.
    n_jobs : int, optional
        Number of CPU cores to use
    """

    def __init__(self, epochs, pipeline, epochs_test=None, cv=2,
                 scoring='accuracy', n_jobs=-1, metadata_querylist=None,
                 metadata_querylist_test=None):

        new_info = mne.create_info(epochs.info['ch_names'],
                                   epochs.info['sfreq'])
        new_info['chs'] = copy.deepcopy(epochs.info['chs'])
        self._decoder = mne.decoding.SlidingEstimator(pipeline, n_jobs=n_jobs,
                                                      scoring=scoring)
        X = epochs.get_data()
        if metadata_querylist is None:
            y = epochs.events[:, 2]
        else:
            y = _get_Y_from_metadata(epochs, metadata_querylist)
            if metadata_querylist_test is None:
                metadata_querylist_test = metadata_querylist

        nave = len(epochs)
        nave_testing = None

        n_classes = numpy.unique(y).size

        c_factors_training = ''
        if 'collapsed_factors' in epochs.info:
            c_factors_training = epochs.info['collapsed_factors']

        c_factors_testing = None

        if isinstance(epochs_test, mne.BaseEpochs):
            logging.info('Using epochs argument for training and epochs_test '
                         'argument for testing')
            X_test = epochs_test.get_data()
            if metadata_querylist is None:
                y_test = epochs_test.events[:, 2]
            else:
                y_test = _get_Y_from_metadata(epochs_test,
                                              metadata_querylist_test)
            nave_testing = len(epochs_test)

            if 'collapsed_factors' in epochs_test.info:
                c_factors_testing = epochs_test.info['collapsed_factors']

            if numpy.setdiff1d(y, y_test).size != 0:
                raise ValueError(
                    'Training and testing set must have the same targets!')

            if X.shape[1:] != X_test.shape[1:]:
                raise ValueError(
                    'Training and testing set must have the same number '
                    'of channels and samples!')

            self._decoder.fit(X, y)
            scores_raw = self._decoder.score(X_test, y_test)
        else:
            scores_raw = mne.decoding.cross_val_multiscore(self._decoder, X, y,
                                                           cv=cv)
            self._decoder.fit(X, y)

        weights = mne.decoding.get_coef(self._decoder, 'patterns_',
                                        inverse_transform=True)
        if weights.ndim == 3:
            weights = numpy.average(weights, axis=1)

        super(Temporal, self).__init__(raw_scores=scores_raw,
                                       weights=weights,
                                       n_classes=n_classes,
                                       info=new_info,
                                       tmin=epochs.times[0],
                                       scoring_name=scoring,
                                       nave=nave,
                                       nave_testing=nave_testing,
                                       c_factors_testing=c_factors_testing,
                                       c_factors_training=c_factors_training)

    @property
    def decoder(self):
        """The decoder."""
        return self._decoder

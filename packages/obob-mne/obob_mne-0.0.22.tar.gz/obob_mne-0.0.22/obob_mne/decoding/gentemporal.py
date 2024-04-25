# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Thomas Hartmann
#
# This file is part of the obob_mne Project, see:
# https://gitlab.com/obob/obob_mne
#
# obob_mne is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# obob_mne is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with obob_mne. If not, see <http://www.gnu.org/licenses/>.

import mne
import numpy
import copy
import logging
import collections
import scipy.stats

from .temporal import TemporalArray
from .helpers import _get_Y_from_metadata


class GeneralizedTemporalArray(mne.utils.SizeMixin):
    """Base class for Temporal Generalization Decoding.

    Parameters
    ----------
    scores_raw : :class:`numpy.ndarray` shape (n_times, n_times) or \
                (n_folds, n_times, n_times)
        Classifier accuracies.
    scoring_name : str
        Name of the scoring function (i.e. Accuracy...)
    n_classes : int
        Number of classes of the classification
    c_factors_training : str
        Name of the factors over which was collapsed in the training set
    weights : :class:`numpy.ndarray` shape (n_channels, n_times)
        Classifier weights
    info : dict
        Info dict
    times_training : :class:`numpy.ndarray` shape (n_times)
        Array of times in seconds of the training data
    tmin : int
        ???
    times_testing : None or :class:`numpy.ndarray` shape (n_times)
        Array of times in seconds of the testing data. If ``None``,
        it is copied from times_training.
    c_factors_testing : None or str
        Name of the factors over which was collapsed in the testing set.
        If ``None``, it is copied from c_factors_training.
    nave : int
        Number of epochs in the training set.
    nave_testing : int or None
        Number of epochs in the testing set. If ``None``, it is copied
        from nave.
    """

    def __init__(self, scores_raw, scoring_name, n_classes, c_factors_training,
                 weights, info, times_training, tmin,
                 times_testing=None, c_factors_testing=None, nave=1,
                 nave_testing=None):
        self._scores_raw = scores_raw
        self._scoring_name = scoring_name
        self._nclasses = n_classes
        self._c_factors_training = c_factors_training
        self._weights = weights
        if c_factors_testing is None:
            self._c_factors_testing = self._c_factors_training
        else:
            self._c_factors_testing = c_factors_testing

        self._times_training = times_training
        if times_testing is None:
            self._times_testing = self._times_training
        else:
            self._times_testing = times_testing

        self._info = info
        self._tmin = tmin
        self._nave = nave

        if nave_testing is None:
            nave_testing = nave

        self._nave_testing = nave_testing

    @property
    def info(self):
        """:class:`Measurement info <mne.Info>`"""
        return self._info

    @property
    def tmin(self):
        """float: tmin"""
        return self._tmin

    @property
    def nave(self):
        """int: Number of epochs in the training set."""
        return self._nave

    @property
    def nave_testing(self):
        """int: Number of epochs in the testing set."""
        return self._nave_testing

    @property
    def scores(self):
        """:class:`numpy.ndarray`: The scores of the classification"""
        if self._scores_raw.ndim <= 2:
            return self._scores_raw
        else:
            return numpy.average(self._scores_raw, axis=0)

    @property
    def weights(self):
        """:class:`numpy.ndarray`:The classifier weights"""
        return self._weights

    @property
    def chance_level(self):
        """float: The chance level of the classifier."""
        return 1.0 / self._nclasses

    def diagonal_as_temporal(self):
        """Return the non-generalized results."""
        if len(self._times_training) != len(self._times_testing):
            raise RuntimeError('Cannot show diagonal for non uniform '
                               'dimensions!')
        if self._scores_raw.ndim == 2:
            raw_scores = numpy.diagonal(self._scores_raw)
        else:
            raw_scores = numpy.diagonal(self._scores_raw, axis1=1, axis2=2)

        return TemporalArray(raw_scores=raw_scores,
                             weights=self.weights,
                             n_classes=self._nclasses,
                             info=self.info,
                             tmin=self.tmin,
                             scoring_name=self._scoring_name,
                             nave=self.nave,
                             nave_testing=self.nave_testing,
                             c_factors_training=self._c_factors_training,
                             c_factors_testing=self._c_factors_testing
                             )

    def get_temporal_from_training_interval(self, tmin, tmax):
        """Average the scores of a training interval.

        Parameters
        ----------
        tmin : int
            Start time in seconds of the training interval to average.
        tmax : int
            End time in seconds of the training interval to average.

        Returns
        -------
        data : instance of :class:`TemporalArray`
            The :class:`TemporalArray` with the averaged scores.
        """
        time_idx = numpy.where(
            numpy.logical_and(
                self._times_training >= tmin,
                self._times_training <= tmax))[0]
        if self._scores_raw.ndim == 2:
            raw_scores = numpy.mean(self._scores_raw[time_idx, :], axis=0)
        else:
            raw_scores = numpy.mean(self._scores_raw[:, time_idx, :], axis=1)

        return TemporalArray(raw_scores=raw_scores,
                             weights=self.weights,
                             n_classes=self._nclasses,
                             info=self.info,
                             tmin=self.tmin,
                             scoring_name=self._scoring_name,
                             nave=self.nave,
                             nave_testing=self.nave_testing,
                             c_factors_training=self._c_factors_training,
                             c_factors_testing=self._c_factors_testing
                             )

    def _plot_image(self, values, axes=None, show=True, cmap='Reds',
                    colorbar=True,
                    interpolation='bessel', alpha=None):
        import matplotlib.pyplot as plt

        if not isinstance(axes, plt.Axes):
            fig, axes = plt.subplots(1, 1)
        else:
            fig = axes.get_figure()

        im = axes.imshow(values, interpolation=interpolation, origin='lower',
                         cmap=cmap,
                         extent=numpy.append(self._times_testing[[0, -1]],
                                             self._times_training[[0, -1]]),
                         aspect='auto',
                         alpha=alpha)

        xlabel = 'Testing time (s)'
        ylabel = 'Training time (s)'

        if self._c_factors_testing:
            xlabel = '\n'.join([self._c_factors_testing, xlabel])

        if self._c_factors_training:
            ylabel = '\n'.join([self._c_factors_training, ylabel])

        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        axes.set_title('Temporal Generalization')
        axes.axvline(0, color='k')
        axes.axhline(0, color='k')
        old_xlim = axes.get_xlim()
        old_ylim = axes.get_ylim()
        diag = (min(self._times_testing[0], self._times_training[0]),
                max(self._times_testing[-1], self._times_training[-1]))
        axes.plot(diag, diag, color='k')
        axes.set_xlim(old_xlim)
        axes.set_ylim(old_ylim)
        if colorbar:
            plt.colorbar(im, ax=axes)

        if show:
            plt.show()

        return fig

    def plot_scores(self, axes=None, show=True, cmap='Reds', colorbar=True,
                    mask_below_chance=False, interpolation='bessel',
                    insignificant_alpha=0.3):
        """Plot the scores as a Matrix.

        Parameters
        ----------
        axes : :class:`matplotlib.axes.Axes` or None, optional
            The axes where to draw the plot. If ``None``, a new figure is
            created.
        show : bool, optional
            True to actually show the plot.
        cmap : str or :class:`matplotlib.colors.Colormap`, optional
            The colormap.
        colorbar : bool, optional
            Whether to draw the colorbar.
        mask_below_chance : bool, optional
            If True, values below chance level get masked.
        interpolation : str, optional
            The interpolation method used.
        """
        scores = self.scores

        alpha = numpy.ones_like(scores)

        if mask_below_chance:
            mask = scores < self.chance_level
            alpha[mask] = insignificant_alpha

        return self._plot_image(values=scores, axes=axes, show=show, cmap=cmap,
                                colorbar=colorbar, interpolation=interpolation,
                                alpha=alpha)

    def drop_channels(self, chs):
        """Drop the channels from the weights.

        Parameters
        ----------
        chs : list of str
            The names of the channels to drop.
        """
        good_channels_idx = mne.pick_channels(self.info['ch_names'],
                                              include=[],
                                              exclude=chs)

        self._info = mne.pick_info(self.info, good_channels_idx)
        self._weights = self._weights[good_channels_idx, :]

    def crop(self, tmin_training=None, tmax_training=None,
             tmin_testing=None, tmax_testing=None):
        """Crop to times

        """
        if tmin_training is None:
            tmin_training = self._times_training[0]
        if tmax_training is None:
            tmax_training = self._times_training[-1]

        if tmin_testing is None:
            tmin_testing = self._times_testing[0]
        if tmax_testing is None:
            tmax_testing = self._times_testing[-1]

        time_idx_training = numpy.where(
            numpy.logical_and(
                self._times_training >= tmin_training,
                self._times_training <= tmax_training))[0]

        time_idx_testing = numpy.where(
            numpy.logical_and(
                self._times_testing >= tmin_testing,
                self._times_testing <= tmax_testing))[0]

        if self._scores_raw.ndim == 2:
            self._scores_raw = self._scores_raw[time_idx_training, :]
            self._scores_raw = self._scores_raw[:, time_idx_testing]
            if self._weights is not None:
                self._weights = self._weights[time_idx_training, :]
                self._weights = self._weights[:, time_idx_testing]
        else:
            self._scores_raw = self._scores_raw[:, time_idx_training, :]
            self._scores_raw = self._scores_raw[:, :, time_idx_testing]
            if self._weights is not None:
                self._weights = self._weights[:, time_idx_training, :]
                self._weights = self._weights[:, :, time_idx_testing]

        self._times_testing = self._times_testing[time_idx_testing]
        self._times_training = self._times_training[time_idx_training]

        return self


class GeneralizedTemporalFromCollection(GeneralizedTemporalArray):
    """Base class for Temporal Generalization data from multiple subjects.

    The individual elements must match in number of classes, times etc.

    Parameters
    ----------
    data_list : iterable of :class:`GeneralizedTemporalArray`
        A list (or any other iterable) of :class:`GeneralizedTemporalArray`
    raw_scores : :class:`numpy.ndarray` shape (n_channels, n_times) or \
                (n_folds, n_channels, n_times)
        The already processed (i.e., averaged, statistically tested) scores.
    weights : :class:`numpy.ndarray` shape (n_channels, n_times)
        The already processed (i.e., averaged, statistically tested) weights.
    """

    must_be_equal = ['_scoring_name', '_nclasses', '_c_factors_training',
                     '_times_training', 'tmin', '_times_testing',
                     '_c_factors_testing']

    def __init__(self, data_list, raw_scores, weights):
        if not all(isinstance(item, GeneralizedTemporalArray) for item in
                   data_list):
            raise TypeError('Only GeneralizedTemporal instances allowed!')

        self._check_same(data_list)

        first_item = data_list[0]

        nave = first_item.nave
        n_classes = first_item._nclasses
        scoring_name = first_item._scoring_name
        c_factors_training = first_item._c_factors_training
        info = first_item.info
        times_training = first_item._times_training
        tmin = first_item.tmin
        times_testing = first_item._times_testing
        c_factors_testing = first_item._c_factors_testing

        super(GeneralizedTemporalFromCollection, self).__init__(
            scores_raw=raw_scores,
            scoring_name=scoring_name, n_classes=n_classes,
            c_factors_training=c_factors_training, weights=weights, info=info,
            times_training=times_training, tmin=tmin,
            times_testing=times_testing,
            c_factors_testing=c_factors_testing, nave=nave)

    def _check_same(self, data_list):
        first_item = data_list[0]
        for cur_item in data_list:
            for cur_parameter in self.must_be_equal:
                first = getattr(first_item, cur_parameter)
                cur = getattr(cur_item, cur_parameter)
                cmp = first == cur
                if not isinstance(cmp, collections.abc.Iterable):
                    cmp = [cmp]
                if not all(cmp):
                    # raise ValueError('All items must come
                    # from the same contrast!')
                    pass

    def _equalize_channels(self, data_list):
        chan_max_idx = numpy.argmax([c.info['nchan'] for c in data_list])
        chan_template = data_list[chan_max_idx].info['ch_names']

        channels = [set(c.info['ch_names']) for c in data_list]
        common_channels = set(chan_template).intersection(*channels)

        for c in data_list:
            drop_them = list(set(c.info['ch_names']) - common_channels)
            if drop_them:
                c.drop_channels(drop_them)


class GeneralizedTemporalAverage(GeneralizedTemporalFromCollection):
    """Create average instance of Temporal Generalization results.

    Given a list of Temporal Generalization Results, this class computes the
    average of their weights and returns an instance of
    :class:`GeneralizedTemporalArray` so you can plot the average scores
    and weights.

    Parameters
    ----------
    data_list : iterable of :class:`GeneralizedTemporalArray`
        A list (or any other iterable) of :class:`GeneralizedTemporalArray`

    """

    def __init__(self, data_list):
        self._equalize_channels(data_list)

        if None not in [x._weights for x in data_list]:
            weights = numpy.average(numpy.stack([x._weights for x in data_list]),  # noqa
                                    axis=0)
        else:
            weights = None

        scores_raw = numpy.average(
            numpy.stack([x._scores_raw for x in data_list]), axis=0)

        super(GeneralizedTemporalAverage, self).__init__(data_list,
                                                         raw_scores=scores_raw,
                                                         weights=weights)


class GeneralizedTemporalStatistics(GeneralizedTemporalAverage):
    """Run statistics on Temporal Generalization results.

    Given a list of Temporal Generalization Results, this class calculates
    a statistic on the weights and returns an instance of
    :class:`GeneralizedTemporalArray`.
    """

    def __init__(self, data_list, stat_function=scipy.stats.ttest_1samp,
                 popmean=None, **kwargs):
        super(GeneralizedTemporalStatistics, self).__init__(data_list)

        if popmean is None:
            popmean = self.chance_level

        scores_for_stats = numpy.stack(x.scores for x in data_list)

        self.stat_values, self.p = stat_function(scores_for_stats,
                                                 popmean=popmean, **kwargs)
        self.p = self.p / 2.0

    def plot_scores(self, axes=None, show=True, cmap='Reds', colorbar=True,
                    mask_below_chance=False, interpolation='bessel',
                    mask_p=None, insignificant_alpha=0.3):
        """Plot the scores as a Matrix.

        Parameters
        ----------
        axes : :class:`matplotlib.axes.Axes` or None, optional
            The axes where to draw the plot. If ``None``, a new figure is
            created.
        show : bool, optional
            True to actually show the plot.
        cmap : str or :class:`matplotlib.colors.Colormap`, optional
            The colormap.
        colorbar : bool, optional
            Whether to draw the colorbar.
        mask_below_chance : bool, optional
            If True, values below chance level get masked.
        interpolation : str, optional
            The interpolation method used.
        mask_p : float or None, optional
            If set, the plot is masked for the given p-value.
        """
        scores = self.scores

        alpha = numpy.ones_like(scores)

        if mask_below_chance:
            mask = scores < self.chance_level
            alpha[mask] = insignificant_alpha

        if mask_p is not None:
            mask = self.p > mask_p
            alpha[mask] = insignificant_alpha

        return self._plot_image(values=scores, axes=axes, show=show, cmap=cmap,
                                colorbar=colorbar, interpolation=interpolation,
                                alpha=alpha)

    def get_temporal_from_training_interval(self, tmin, tmax):
        """Average the scores of a training interval.

        Parameters
        ----------
        tmin : int
            Start time in seconds of the training interval to average.
        tmax : int
            End time in seconds of the training interval to average.

        Returns
        -------
        data : instance of :class:`TemporalArray`
            The :class:`TemporalArray` with the averaged scores.
        """
        temporal = super(GeneralizedTemporalStatistics,
                         self).get_temporal_from_training_interval(tmin=tmin,
                                                                   tmax=tmax)

        time_idx = numpy.where(
            numpy.logical_and(self._times_training >= tmin,
                              self._times_training <= tmax))[0]

        stats = numpy.mean(self.stat_values[time_idx, :], axis=0)
        temporal.stat_values = stats

        return temporal


class GeneralizedTemporal(GeneralizedTemporalArray):
    """Apply a decoding pipeline using Temporal Generalization.

    Use this class to perform Temporal Generalization decoding. This means
    that a classifier is trained on every sample and then tested on all
    samples. So, if you supply epochs with 100 samples, a classifier gets
    trained on the data data of the first sample. This classifier is then
    tested on the data of the first sample, then the second sample and so on.
    The process is then repeated by training on the second sample and testing
    on all samples and so forth.

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
                 metadata_querylist_test=None, verbose=True):
        times_training = epochs.times
        times_testing = None
        nave = len(epochs)
        nave_testing = None

        new_info = mne.create_info(epochs.info['ch_names'],
                                   epochs.info['sfreq'])

        with new_info._unlock():
            new_info['chs'] = copy.deepcopy(epochs.info['chs'])

        self._decoder = mne.decoding.GeneralizingEstimator(pipeline,
                                                           n_jobs=n_jobs,
                                                           scoring=scoring,
                                                           verbose=verbose)
        X = epochs.get_data()
        if metadata_querylist is None:
            y = epochs.events[:, 2]
        else:
            y = _get_Y_from_metadata(epochs, metadata_querylist)
            if metadata_querylist_test is None:
                metadata_querylist_test = metadata_querylist

        n_classes = numpy.unique(y).size

        c_factors_training = ''
        if 'collapsed_factors' in epochs.info:
            c_factors_training = epochs.info['collapsed_factors']

        c_factors_testing = None

        if isinstance(epochs_test, mne.BaseEpochs):
            logging.info(
                'Using epochs argument for training and epochs_test argument '
                'for testing')

            X_test = epochs_test.get_data()
            if metadata_querylist_test is None:
                y_test = epochs_test.events[:, 2]
            else:
                y_test = _get_Y_from_metadata(epochs_test,
                                              metadata_querylist_test)
            nave_testing = len(epochs_test)

            if 'collapsed_factors' in epochs_test.info:
                c_factors_testing = epochs_test.info['collapsed_factors']

            times_testing = epochs_test.times

            if numpy.setdiff1d(y, y_test).size != 0:
                raise ValueError(
                    'Training and testing set must have the same targets!')

            if X.shape[1] != X_test.shape[1]:
                raise ValueError('Training and testing set must have the '
                                 'same number of channels!')

            self._decoder.fit(X, y)
            scores_raw = self._decoder.score(X_test, y_test)

        else:
            scores_raw = mne.decoding.cross_val_multiscore(self._decoder, X, y,
                                                           cv=cv)

        try:
            self._decoder.fit(X, y)
            weights = mne.decoding.get_coef(self._decoder, 'patterns_',
                                            inverse_transform=True)
            if weights.ndim == 3:
                weights = numpy.average(weights, axis=1)
        except ValueError:
            weights = None

        super(GeneralizedTemporal, self).__init__(scores_raw=scores_raw,
                                                  scoring_name=scoring,
                                                  n_classes=n_classes,
                                                  c_factors_training=c_factors_training,  # noqa
                                                  c_factors_testing=c_factors_testing,  # noqa
                                                  times_training=times_training,  # noqa
                                                  times_testing=times_testing,
                                                  weights=weights,
                                                  tmin=epochs.times[0],
                                                  info=new_info,
                                                  nave=nave,
                                                  nave_testing=nave_testing)

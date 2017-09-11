import pandas as pd
import numpy as np
import masseval


def main():

    # masseval side
    masseval.config.mus_base_path = '/vol/vssp/maruss/data2/MUS2017'
    masseval.config.dsd_base_path = '/vol/vssp/maruss/data2/DSD100'

    exclude_tracks = experiment_stimuli()

    training(exclude_tracks)


def experiment_stimuli():

    audio_dir = './site/sounds'

    # config for selection
    only_these_algos = None
    targets = ['vocals']
    metrics = ['SAR', 'SIR']
    num_algos = 5
    num_tracks_per_metric = [8, 8]
    target_loudness = -23
    segment_duration = 7
    remove_outliers = False
    trim_factor_distorted = 0.4

    df = masseval.data.get_sisec_df(False)

    # Main processing
    full_test = pd.DataFrame()
    for target in targets:
        exclude_tracks = [3]  # Song 3 has strange vocals
        for metric, num_tracks in zip(metrics, num_tracks_per_metric):

            sample = masseval.data.get_sample(
                df,
                num_tracks=num_tracks,
                num_algos=num_algos,
                metric=metric,
                target=target,
                only_these_algos=only_these_algos,
                exclude_tracks=exclude_tracks,
                remove_outliers=remove_outliers,
                selection_plot=False,
            )

            tracks = sample['track_id'].values
            exclude_tracks = np.append(exclude_tracks, np.unique(tracks))
            full_test = pd.concat([full_test, sample])

            # Store the test wav files
            masseval.audio.write_target_from_sample(
                sample,
                target=target,
                directory=audio_dir,
                force_mono=True,
                target_loudness=target_loudness,
                segment_duration=segment_duration,
                trim_factor_distorted=trim_factor_distorted,
                include_background_in_quality_anchor=False,
                loudness_normalise_interferer=False,
                )

    full_test.to_csv('./data/experiment_stimul.csv', index=None)

    return exclude_tracks


def training(exclude_tracks):

    # masseval side
    masseval.config.mus_base_path = '/vol/vssp/maruss/data2/MUS2017'
    masseval.config.dsd_base_path = '/vol/vssp/maruss/data2/DSD100'
    audio_dir = './site/sounds_training'

    # config for selection
    only_these_algos = ['GRA3', 'KON', 'OZE', 'UHL3', 'NUG3']
    # only_these_algos = None
    target = 'vocals'
    metric = 'SAR'
    num_algos = 5
    num_tracks = 1
    target_loudness = -30
    segment_duration = 7
    remove_outliers = False
    trim_factor_distorted = 0.4

    df = masseval.data.get_sisec_df(False)

    sample = masseval.data.get_sample(
        df,
        num_tracks=num_tracks,
        num_algos=num_algos,
        metric=metric,
        target=target,
        only_these_algos=only_these_algos,
        exclude_tracks=exclude_tracks,
        remove_outliers=remove_outliers,
        selection_plot=False,
    )

    # Store the test wav files
    masseval.audio.write_target_from_sample(
        sample,
        target=target,
        directory=audio_dir,
        force_mono=True,
        target_loudness=target_loudness,
        segment_duration=segment_duration,
        trim_factor_distorted=trim_factor_distorted,
        include_background_in_quality_anchor=False,
        loudness_normalise_interferer=False,
        )

    sample.to_csv('./data/training_stimul.csv', index=None)


if __name__ == '__main__':

    main()

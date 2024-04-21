#!python3
""" CLI to refine template matching candidates.

    Copyright (c) 2023-2024 European Molecular Biology Laboratory

    Author: Valentin Maurer <valentin.maurer@embl-hamburg.de>
"""
import argparse
from time import time

import numpy as np
from numpy.typing import NDArray

from tme.backends import backend
from tme import Density, Structure
from tme.matching_data import MatchingData
from tme.analyzer import MaxScoreOverRotations, MaxScoreOverTranslations
from tme.matching_utils import (
    load_pickle,
    get_rotation_matrices,
    compute_parallelization_schedule,
)
from tme.matching_exhaustive import scan_subsets, MATCHING_EXHAUSTIVE_REGISTER

from postprocess import Orientations
from match_template import load_and_validate_mask

def parse_args():
    parser = argparse.ArgumentParser(
        description="Refine Template Matching Orientations."
    )
    parser.add_argument(
        "--input_file",
        required=True,
        type=str,
        help="Path to the output of match_template.py.",
    )
    parser.add_argument(
        "--orientations",
        required=True,
        type=str,
        help="Path to orientations from postprocess.py.",
    )
    parser.add_argument(
        "--output_file",
        required=True,
        help="Path to the refined output orientations.",
    )
    parser.add_argument(
        "-n",
        dest="cores",
        required=False,
        type=int,
        default=4,
        help="Number of cores used for template matching.",
    )

    args = parser.parse_args()

    return args


def load_template(filepath: str, sampling_rate: NDArray) -> "Density":
    try:
        template = Density.from_file(filepath)
    except ValueError:
        template = Structure.from_file(filepath)
        template = Density.from_structure(template, sampling_rate=sampling_rate)

    return template


def main():
    args = parse_args()
    meta = load_pickle(args.input_file)[-1]
    target_origin, _, sampling_rate, cli_args = meta

    orientations = Orientations.from_file(
        filename=args.orientations, file_format="text"
    )

    template = load_template(cli_args.template, sampling_rate)
    template_mask = load_and_validate_mask(
        mask_target=template, mask_path=cli_args.template_mask
    )

    if not cli_args.no_centering:
        template, translation = template.centered(0)

    if template_mask is None:
        template_mask = template.empty
        if not cli_args.no_centering:
            enclosing_box = template.minimum_enclosing_box(
                0, use_geometric_center=False
            )
            template_mask.adjust_box(enclosing_box)

        template_mask.data[:] = 1
        translation = np.zeros_like(translation)

    template_mask.pad(template.shape, center=False)
    origin_translation = np.divide(
        np.subtract(template.origin, template_mask.origin), template.sampling_rate
    )
    translation = np.add(translation, origin_translation)

    template_mask = template_mask.rigid_transform(
        rotation_matrix=np.eye(template_mask.data.ndim),
        translation=-translation,
        order=1,
    )
    template_mask.origin = template.origin.copy()

    target = Density.from_file(cli_args.target)
    peaks = orientations.translations.astype(int)
    half_shape = np.divide(template.shape, 2).astype(int)
    observation_starts = np.subtract(peaks, half_shape)
    observation_stops = np.add(peaks, half_shape) + np.mod(template.shape, 2).astype(
        int
    )

    pruned_starts = np.maximum(observation_starts, 0)
    pruned_stops = np.minimum(observation_stops, target.shape)

    keep_peaks = (
        np.sum(
            np.multiply(
                observation_starts == pruned_starts, observation_stops == pruned_stops
            ),
            axis=1,
        )
        == observation_starts.shape[1]
    )
    observation_starts = observation_starts[keep_peaks]
    observation_stops = observation_stops[keep_peaks]

    observation_slices = [
        tuple(slice(s, e) for s, e in zip(start_row, stop_row))
        for start_row, stop_row in zip(observation_starts, observation_stops)
    ]

    matching_data = MatchingData(target=target, template=template)
    matching_data.rotations = np.eye(template.data.ndim).reshape(1, 3, 3)

    target_pad = matching_data.target_padding(pad_target=True)
    out_shape = np.add(target_pad, template.shape).astype(int)

    observations = np.zeros((len(observation_slices), *out_shape))


    for idx, obs_slice in enumerate(observation_slices):
        subset = matching_data.subset_by_slice(
            target_slice=obs_slice,
            target_pad=target_pad,
            invert_target=cli_args.invert_target_contrast,
        )
        xd = template.copy()
        xd.pad(subset.target.shape, center = True)
        # observations[idx] = subset.target
        observations[idx] = xd.data


    matching_data = MatchingData(target=observations, template=template)
    matching_data._set_batch_dimension(target_dims=0, template_dims=None)
    matching_data.rotations = get_rotation_matrices(15)
    if template_mask is not None:
        matching_data.template_mask = template_mask.data

    template_box = np.ones(len(matching_data._output_template_shape), dtype=int)
    target_padding = np.zeros_like(matching_data._output_target_shape)

    scoring_method = "FLC"
    callback_class = MaxScoreOverRotations
    splits, schedule = compute_parallelization_schedule(
        shape1=matching_data._output_target_shape,
        shape2=template_box,
        shape1_padding=target_padding,
        max_cores=args.cores,
        max_ram=backend.get_available_memory(),
        split_only_outer=False,
        matching_method=scoring_method,
        analyzer_method=callback_class.__name__,
        backend=backend._backend_name,
        float_nbytes=backend.datatype_bytes(backend._default_dtype),
        complex_nbytes=backend.datatype_bytes(backend._complex_dtype),
        integer_nbytes=backend.datatype_bytes(backend._default_dtype_int),
    )

    matching_setup, matching_score = MATCHING_EXHAUSTIVE_REGISTER[scoring_method]

    start = time()
    candidates = scan_subsets(
        matching_data=matching_data,
        matching_score=matching_score,
        matching_setup=matching_setup,
        callback_class=callback_class,
        callback_class_args={
            # "score_space_shape" : (
                # matching_data.rotations.shape[0], observations.shape[0]
            # ),
            # "score_space_dtype" : backend._default_dtype,
            # "template_shape" : (matching_data.rotations.shape[0], *matching_data._template.shape)
        },
        target_splits=splits,
        job_schedule=schedule,
        pad_target_edges=False,
        pad_fourier=False,
        interpolation_order=cli_args.interpolation_order,
    )
    print(candidates[0].max())
    Density(candidates[0][0]).to_file("scores.mrc")

    runtime = time() - start
    print(f"\nRuntime real: {runtime:.3f}s user: {(runtime * args.cores):.3f}s.")


if __name__ == "__main__":
    main()

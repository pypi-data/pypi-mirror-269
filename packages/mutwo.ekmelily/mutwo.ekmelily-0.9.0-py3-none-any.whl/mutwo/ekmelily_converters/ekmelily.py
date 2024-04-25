"""Build tuning files for `Lilypond <https://lilypond.org/>`_ extension `Ekmelily <http://www.ekmelic-music.org/en/extra/ekmelily.htm>`_.

By default the smallest step which Lilypond supports is one quartertone. With
the help of Ekmelily it is easily possible to add more complex micro- or
macrotonal tunings to Lilypond. The converter in this module aims to make it easier
to build tuning files to be used with the 'ekmel-main.ily' script from Thomas Richter.

**Disclaimer:**

For now the converters only support making notation tables for English note names.
"""

import dataclasses
import itertools
import typing
import warnings

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import core_converters
from mutwo import core_constants
from mutwo import ekmelily_converters
from mutwo import music_parameters

__all__ = (
    "EkmelilyAccidental",
    "EkmelilyTuningFileConverter",
    "HEJIEkmelilyTuningFileConverter",
)


@dataclasses.dataclass(frozen=True)
class EkmelilyAccidental(object):
    """Representation of an Ekmelily accidental.

    :param accidental_name: The name of the accidental that
        follows after the diatonic pitch name (e.g. 's' or 'qf')
    :type accidental_name: str
    :param accidental_glyph_tuple: The name of accidental glyphs that should
        appear before the notehead. For
        a list of available glyphs, check the documentation of
        `Ekmelos <http://www.ekmelic-music.org/en/extra/ekmelos.htm>`_.
        Furthermore one can find mappings from mutwo data to Ekmelos glyph
        names in :const:`~mutwo.ekmelily_converters.constants.PRIME_AND_EXPONENT_AND_TRADITIONAL_ACCIDENTAL_TO_ACCIDENTAL_GLYPH_DICT`
        and :const:`~mutwo.ekmelily_converters.constants.TEMPERED_ACCIDENTAL_TO_ACCIDENTAL_GLYPH_DICT`.
    :type accidental_glyph_tuple: tuple[str, ...]
    :param deviation_in_cents: How many cents shall an altered pitch differ from
        its diatonic / natural counterpart.
    :type deviation_in_cents: float
    :param available_diatonic_pitch_index_tuple: Sometimes one
        may want to define accidentals which are only available for certain
        diatonic music_parameters. For this case, one can use this argument
        and specify all diatonic music_parameters which should know this
        accidental. If this argument keeps undefined, the accidental
        will be added to all seven diatonic music_parameters.
    :type available_diatonic_pitch_index_tuple: typing.Optional[tuple[int, ...]], optional

    **Example:**

    >>> from mutwo import ekmelily_converters
    >>> natural = ekmelily_converters.EkmelilyAccidental('', ("#xE261",), 0)
    >>> sharp = ekmelily_converters.EkmelilyAccidental('s', ("#xE262",), 100)
    >>> flat = ekmelily_converters.EkmelilyAccidental('f', ("#xE260",), -100)
    """

    accidental_name: str
    accidental_glyph_tuple: tuple[str, ...]
    deviation_in_cents: float
    available_diatonic_pitch_index_tuple: typing.Optional[tuple[int, ...]] = None

    def __hash__(self) -> int:
        return hash(
            (
                self.accidental_name,
                self.accidental_glyph_tuple,
                self.deviation_in_cents,
                self.available_diatonic_pitch_index_tuple,
            )
        )


class EkmelilyTuningFileConverter(core_converters.abc.Converter):
    """Build Ekmelily tuning files from Ekmelily accidentals.

    :param path: Path where the new Ekmelily tuning file shall be written.
        The suffix '.ily' is recommended, but not necessary.
    :type path: str
    :param ekmelily_accidental_sequence: A sequence which contains all
        :class:`EkmelilyAccidental` that shall be written to the tuning file,
    :type ekmelily_accidental_sequence: typing.Sequence[EkmelilyAccidental]
    :param global_scale: From the `Lilypond documentation <https://lilypond.org/doc/v2.20/Documentation/notation/scheme-functions>`_:
        "This determines the tuning of music_parameters with no accidentals or key signatures.
        The first pitch is c. Alterations are calculated relative to this scale.
        The number of music_parameters in this scale determines the number of scale steps
        that make up an octave. Usually the 7-note major scale."
    :type global_scale: tuple[fractions.Fraction, ...], optional

    **Example:**

    >>> from mutwo import ekmelily_converters
    >>> natural = ekmelily_converters.EkmelilyAccidental('', ("#xE261",), 0)
    >>> sharp = ekmelily_converters.EkmelilyAccidental('s', ("#xE262",), 100)
    >>> flat = ekmelily_converters.EkmelilyAccidental('f', ("#xE260",), -100)
    >>> eigth_tone_sharp = ekmelily_converters.EkmelilyAccidental('es', ("#xE2C7",), 25)
    >>> eigth_tone_flat = ekmelily_converters.EkmelilyAccidental('ef', ("#xE2C2",), -25)
    >>> converter = ekmelily_converters.EkmelilyTuningFileConverter(
    >>>     'ekme-test.ily', (natural, sharp, flat, eigth_tone_sharp, eigth_tone_flat)
    >>> )
    >>> converter.convert()
    """

    def __init__(
        self,
        path: str,
        ekmelily_accidental_sequence: typing.Sequence[EkmelilyAccidental],
        # should have exactly 7 fractions (one for each diatonic pitch)
        global_scale: typing.Optional[tuple[fractions.Fraction, ...]] = None,
    ):
        if global_scale is None:
            # set to default 12 EDO, a' = 440 Hertz
            global_scale = ekmelily_converters.configurations.DEFAULT_GLOBAL_SCALE

        global_scale = EkmelilyTuningFileConverter._correct_global_scale(global_scale)

        self._path = path
        self._global_scale = global_scale
        self._ekmelily_accidental_sequence = ekmelily_accidental_sequence
        (
            self._accidental_to_alteration_code_mapping,
            self._alteration_code_to_alteration_fraction_mapping,
        ) = EkmelilyTuningFileConverter._make_accidental_to_alteration_code_mapping_and_alteration_code_to_alteration_fraction_mapping(
            self._ekmelily_accidental_sequence
        )

    # ###################################################################### #
    #                          static methods                                #
    # ###################################################################### #

    @staticmethod
    def _correct_global_scale(
        global_scale: tuple[fractions.Fraction, ...]
    ) -> tuple[fractions.Fraction, ...]:
        # Lilypond doesn't allow negative values for first item in global scale.
        # Therefore Mutwo makes sure that the first item isn't a negative number.
        corrected_global_scale = list(global_scale)
        if corrected_global_scale[0] != 0:
            message = (
                "Found value '{}' for first scale degree in global scale. Autoset value"
                " to 0 (Lilypond doesn't allow values != 0 for the first scale degree)".format(
                    corrected_global_scale[0]
                )
            )
            warnings.warn(message)
            corrected_global_scale[0] = fractions.Fraction(0, 1)
        return tuple(corrected_global_scale)

    @staticmethod
    def _deviation_in_cents_to_alteration_fraction(
        deviation_in_cents: core_constants.Real, max_denominator: int = 1000
    ) -> fractions.Fraction:
        # simplify fraction to avoid too complex calculations during Lilyponds midi
        # render (otherwise Lilypond won't be able to render Midi / it will take
        # too long)
        return fractions.Fraction(deviation_in_cents / 200).limit_denominator(
            max_denominator
        )

    @staticmethod
    def _alteration_fraction_to_deviation_in_cents(
        alteration_fraction: fractions.Fraction,
    ) -> float:
        return float(alteration_fraction * 200)

    @staticmethod
    def _accidental_index_to_alteration_code(accidental_index: int) -> str:
        # convert index of accidental to hex code in a format that is
        # readable by Lilypond
        return "#x{}".format(str(hex(accidental_index))[2:].upper())

    @staticmethod
    def _find_and_group_accidentals_by_specific_deviation_in_cents(
        ekmelily_accidental_sequence: typing.Sequence[EkmelilyAccidental],
        deviation_in_cents: float,
    ) -> tuple[tuple[EkmelilyAccidental, ...], tuple[EkmelilyAccidental, ...]]:
        positive_list, negative_list = [], []
        for accidental in ekmelily_accidental_sequence:
            if accidental.deviation_in_cents == deviation_in_cents:
                positive_list.append(accidental)
            elif (
                accidental.deviation_in_cents == -deviation_in_cents
                and deviation_in_cents != 0
            ):
                negative_list.append(accidental)

        return tuple(positive_list), tuple(negative_list)

    @staticmethod
    def _group_accidentals_by_deviations_in_cents(
        ekmelily_accidental_sequence: typing.Sequence[EkmelilyAccidental],
    ) -> tuple[tuple[float, tuple[tuple[EkmelilyAccidental, ...], ...]], ...,]:
        """Put all accidentals with the same absolute deviation to the same tuple.

        The first element of each tuple is the absolute deviation in cents,
        the second element is tuple with two elements where the first element
        contains all positive accidentals and the second tuple all negative
        accidentals.
        """

        available_deviations_in_cents = sorted(
            set(
                map(
                    lambda accidental: abs(accidental.deviation_in_cents),
                    ekmelily_accidental_sequence,
                )
            )
        )
        accidentals_grouped_by_deviations_in_cents = tuple(
            (
                deviation_in_cents,
                EkmelilyTuningFileConverter._find_and_group_accidentals_by_specific_deviation_in_cents(
                    ekmelily_accidental_sequence, deviation_in_cents
                ),
            )
            for deviation_in_cents in available_deviations_in_cents
        )

        return accidentals_grouped_by_deviations_in_cents

    @staticmethod
    def _process_single_accidental(
        accidental_to_alteration_code_mapping: dict[EkmelilyAccidental, str],
        alteration_code_to_alteration_fraction_mapping: dict[str, fractions.Fraction],
        accidental: typing.Optional[EkmelilyAccidental],
        accidental_index: int,
        is_positive: bool,
        absolute_deviation_in_cents: float,
    ):
        alteration_code = (
            EkmelilyTuningFileConverter._accidental_index_to_alteration_code(
                accidental_index
            )
        )

        if accidental:
            accidental_to_alteration_code_mapping.update({accidental: alteration_code})

        if is_positive:
            alteration_fraction = (
                EkmelilyTuningFileConverter._deviation_in_cents_to_alteration_fraction(
                    absolute_deviation_in_cents
                )
            )
            alteration_code_to_alteration_fraction_mapping.update(
                {alteration_code: alteration_fraction}
            )

    @staticmethod
    def _process_accidental_pair(
        accidental_to_alteration_code_mapping: dict[EkmelilyAccidental, str],
        alteration_code_to_alteration_fraction_mapping: dict[str, fractions.Fraction],
        positive_accidental: typing.Optional[EkmelilyAccidental],
        positive_alteration_index: int,
        negative_accidental: typing.Optional[EkmelilyAccidental],
        negative_alteration_index: int,
        absolute_deviation_in_cents: float,
    ) -> None:
        # Add accidental data to accidental_to_alteration_code_mapping
        # and alteration_code_to_alteration_fraction_mapping.

        for is_positive, accidental, accidental_index in (
            (True, positive_accidental, positive_alteration_index),
            (False, negative_accidental, negative_alteration_index),
        ):
            EkmelilyTuningFileConverter._process_single_accidental(
                accidental_to_alteration_code_mapping,
                alteration_code_to_alteration_fraction_mapping,
                accidental,
                accidental_index,
                is_positive,
                absolute_deviation_in_cents,
            )

    @staticmethod
    def _get_accidental_from_accidental_iterator(
        accidental_iterator: typing.Iterator,
    ) -> typing.Optional[EkmelilyAccidental]:
        try:
            accidental = next(accidental_iterator)
        except StopIteration:
            accidental = None

        return accidental

    @staticmethod
    def _process_accidental_group(
        accidental_to_alteration_code_mapping: dict[EkmelilyAccidental, str],
        alteration_code_to_alteration_fraction_mapping: dict[str, fractions.Fraction],
        nth_alteration: int,
        accidental_group: tuple[tuple[EkmelilyAccidental, ...], ...],
        absolute_deviation_in_cents: float,
    ) -> int:
        # Define alteration codes and alteration fractions for accidentals
        # in one accidental group and add the calculated data to both mappings.

        positive_accidentals, negative_accidentals = accidental_group
        positive_accidentals_iterator = iter(positive_accidentals)
        negative_accidentals_iterator = iter(negative_accidentals)
        for _ in range(max((len(positive_accidentals), len(negative_accidentals)))):
            positive_alteration_index, negative_alteration_index = (
                nth_alteration,
                nth_alteration + 1,
            )
            positive_accidental = (
                EkmelilyTuningFileConverter._get_accidental_from_accidental_iterator(
                    positive_accidentals_iterator
                )
            )
            negative_accidental = (
                EkmelilyTuningFileConverter._get_accidental_from_accidental_iterator(
                    negative_accidentals_iterator
                )
            )

            EkmelilyTuningFileConverter._process_accidental_pair(
                accidental_to_alteration_code_mapping,
                alteration_code_to_alteration_fraction_mapping,
                positive_accidental,
                positive_alteration_index,
                negative_accidental,
                negative_alteration_index,
                absolute_deviation_in_cents,
            )
            nth_alteration += 2

        return nth_alteration

    @staticmethod
    def _make_accidental_to_alteration_code_mapping_and_alteration_code_to_alteration_fraction_mapping(
        ekmelily_accidental_sequence: typing.Sequence[EkmelilyAccidental],
    ) -> tuple[dict[EkmelilyAccidental, str], dict[str, fractions.Fraction]]:
        accidentals_grouped_by_deviations_in_cents = (
            EkmelilyTuningFileConverter._group_accidentals_by_deviations_in_cents(
                ekmelily_accidental_sequence
            )
        )
        accidental_to_alteration_code_mapping: dict[EkmelilyAccidental, str] = {}
        alteration_code_to_alteration_fraction_mapping: dict[
            str, fractions.Fraction
        ] = {}

        nth_alteration = 0
        for (
            absolute_deviation_in_cents,
            accidental_group,
        ) in accidentals_grouped_by_deviations_in_cents:
            nth_alteration = EkmelilyTuningFileConverter._process_accidental_group(
                accidental_to_alteration_code_mapping,
                alteration_code_to_alteration_fraction_mapping,
                nth_alteration,
                accidental_group,
                absolute_deviation_in_cents,
            )

        return (
            accidental_to_alteration_code_mapping,
            alteration_code_to_alteration_fraction_mapping,
        )

    # ###################################################################### #
    #                          private methods                               #
    # ###################################################################### #

    def _make_tuning_table(self) -> str:
        tuning_table_entries = [
            "  (-1 {})".format(" ".join((str(ratio) for ratio in self._global_scale)))
        ]
        for (
            alteration_code,
            alteration_fraction,
        ) in self._alteration_code_to_alteration_fraction_mapping.items():
            alteration = "({} . {})".format(alteration_code, alteration_fraction)
            tuning_table_entries.append(alteration)

        tuning_table = "ekmTuning = #'(\n{})".format("\n  ".join(tuning_table_entries))
        return tuning_table

    def _get_pitch_entry_from_accidental_and_diatonic_pitch(
        self,
        accidental: EkmelilyAccidental,
        nth_diatonic_pitch: int,
        diatonic_pitch: str,
    ) -> typing.Optional[str]:
        is_addable = True
        if accidental.available_diatonic_pitch_index_tuple is not None:
            is_addable = (
                nth_diatonic_pitch in accidental.available_diatonic_pitch_index_tuple
            )
        if is_addable:
            pitch_name = "{}{}".format(diatonic_pitch, accidental.accidental_name)
            alteration_code = self._accidental_to_alteration_code_mapping[accidental]
            pitch_entry = "({} {} . {})".format(
                pitch_name, nth_diatonic_pitch, alteration_code
            )
            return pitch_entry

        return None

    def _make_languages_table(self) -> str:
        language_table_entries = []

        for accidental in self._ekmelily_accidental_sequence:
            for nth_diatonic_pitch, diatonic_pitch in enumerate(
                music_parameters.constants.DIATONIC_PITCH_CLASS_CONTAINER
            ):
                pitch_entry = self._get_pitch_entry_from_accidental_and_diatonic_pitch(
                    accidental, nth_diatonic_pitch, diatonic_pitch
                )
                if pitch_entry is not None:
                    language_table_entries.append(pitch_entry)

        # for now: only support english language
        languages_table = "ekmLanguages = #'(\n(english . (\n  {})))".format(
            "\n  ".join(language_table_entries)
        )
        return languages_table

    def _make_notations_table(self) -> str:
        notations_table_entries: list[str] = []

        for accidental in self._ekmelily_accidental_sequence:
            alteration_code = self._accidental_to_alteration_code_mapping[accidental]
            accidental_notation = "({} {})".format(
                alteration_code, " ".join(accidental.accidental_glyph_tuple)
            )
            notations_table_entries.append(accidental_notation)

        notations_table = "ekmNotations = #'(\n(default .(\n  {})))".format(
            "\n  ".join(notations_table_entries)
        )
        return notations_table

    # ###################################################################### #
    #                          public api                                    #
    # ###################################################################### #

    def convert(self):
        """Render tuning file to :attr:`path`."""

        ekmelily_tuning_file = (
            self._make_tuning_table(),
            self._make_languages_table(),
            self._make_notations_table(),
            r'\include "ekmel-main.ily"',
        )

        ekmelily_tuning_file = "\n\n".join(ekmelily_tuning_file)

        with open(self._path, "w") as f:
            f.write(ekmelily_tuning_file)


class HEJIEkmelilyTuningFileConverter(EkmelilyTuningFileConverter):
    """Build Ekmelily tuning files for `Helmholtz-Ellis JI Pitch Notation <https://marsbat.space/pdfs/notation.pdf>`_.

    :param path: Path where the new Ekmelily tuning file shall be written.
        The suffix '.ily' is recommended, but not necessary.
    :type path: str
    :param prime_to_highest_allowed_exponent: Mapping of prime number to
        highest exponent that should occur. Take care not to add
        higher exponents than the HEJI Notation supports. See
        :const:`~mutwo.ekmelily_converters.configurations.DEFAULT_PRIME_TO_HIGHEST_ALLOWED_EXPONENT_DICT`
        for the default mapping.
    :type prime_to_highest_allowed_exponent: dict[int, int], optional
    :param reference_pitch: The reference pitch (1/1). Should be a diatonic
        pitch name (see
        :const:`~mutwo.parameters.music_parameters.constants.DIATONIC_PITCH_CLASS_CONTAINER`)
        in English nomenclature. For any other reference pitch than 'c', Lilyponds
        midi rendering for music_parameters with the diatonic pitch 'c' will be slightly
        out of tune (because the first value of `global_scale`
        always have to be 0).
    :type reference_pitch: str, optional
    :param prime_to_heji_accidental_name: Mapping of a prime number
        to a string which indicates the respective prime number in the resulting
        accidental name. See
        :const:`~mutwo.ekmelily_converters.configurations.DEFAULT_PRIME_TO_HEJI_ACCIDENTAL_NAME_DICT`
        for the default mapping.
    :type prime_to_heji_accidental_name: dict[int, str], optional
    :param otonality_indicator: String which indicates that the
        respective prime alteration is otonal. See
        :const:`~mutwo.ekmelily_converters.configurations.DEFAULT_OTONALITY_INDICATOR`
        for the default value.
    :type otonality_indicator: str, optional
    :param utonality_indicator: String which indicates that the
        respective prime alteration is utonal. See
        :const:`~mutwo.ekmelily_converters.configurations.DEFAULT_UTONALITY_INDICATOR`
        for the default value.
    :type utonality_indicator: str, optional
    :param exponent_to_exponent_indicator: Function to convert the
        exponent of a prime number to string which indicates the respective
        exponent. See
        :func:`~mutwo.ekmelily_converters.configurations.DEFAULT_EXPONENT_TO_EXPONENT_INDICATOR`
        for the default function.
    :type exponent_to_exponent_indicator: typing.Callable[[int], str], optional
    :param tempered_pitch_indicator: String which indicates that the
        respective accidental is tempered (12 EDO). See
        :const:`~mutwo.ekmelily_converters.configurations.DEFAULT_TEMPERED_PITCH_INDICATOR`
        for the default value.
    :type tempered_pitch_indicator: str, optional
    :param set_microtonal_tuning: If set to ``False`` the converter won't apply any
        microtonal pitches. In this case all chromatic pitches will return normal
        12EDO pitches. Default to ``True``.
    :type set_microtonal_tuning: bool
    """

    def __init__(
        self,
        path: str = None,
        prime_to_highest_allowed_exponent: typing.Optional[dict[int, int]] = None,
        reference_pitch: str = "c",
        prime_to_heji_accidental_name: typing.Optional[dict[int, str]] = None,
        otonality_indicator: str = None,
        utonality_indicator: str = None,
        exponent_to_exponent_indicator: typing.Callable[[int], str] = None,
        tempered_pitch_indicator: str = None,
        set_microtonal_tuning: bool = True,
    ):
        # set default values
        if path is None:
            path = "ekme-heji-ref-{}".format(reference_pitch)
            if not set_microtonal_tuning:
                path += "-not-tuned"
            path += ".ily"

        if prime_to_highest_allowed_exponent is None:
            prime_to_highest_allowed_exponent = (
                ekmelily_converters.configurations.DEFAULT_PRIME_TO_HIGHEST_ALLOWED_EXPONENT_DICT
            )

        if prime_to_heji_accidental_name is None:
            prime_to_heji_accidental_name = (
                ekmelily_converters.configurations.DEFAULT_PRIME_TO_HEJI_ACCIDENTAL_NAME_DICT
            )

        if otonality_indicator is None:
            otonality_indicator = (
                ekmelily_converters.configurations.DEFAULT_OTONALITY_INDICATOR
            )

        if utonality_indicator is None:
            utonality_indicator = (
                ekmelily_converters.configurations.DEFAULT_UTONALITY_INDICATOR
            )

        if exponent_to_exponent_indicator is None:
            exponent_to_exponent_indicator = (
                ekmelily_converters.configurations.DEFAULT_EXPONENT_TO_EXPONENT_INDICATOR
            )

        if tempered_pitch_indicator is None:
            tempered_pitch_indicator = (
                ekmelily_converters.configurations.DEFAULT_TEMPERED_PITCH_INDICATOR
            )

        difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches = HEJIEkmelilyTuningFileConverter._find_difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches(
            reference_pitch
        )
        if set_microtonal_tuning:
            global_scale = HEJIEkmelilyTuningFileConverter._make_global_scale(
                difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches
            )
        else:
            global_scale = None
        ekmelily_accidental_sequence = (
            HEJIEkmelilyTuningFileConverter._make_ekmelily_accidental_sequence(
                difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches,
                prime_to_highest_allowed_exponent,
                prime_to_heji_accidental_name,
                otonality_indicator,
                utonality_indicator,
                exponent_to_exponent_indicator,
                tempered_pitch_indicator,
                set_microtonal_tuning,
            )
        )
        super().__init__(path, ekmelily_accidental_sequence, global_scale=global_scale)

    # ###################################################################### #
    #                          static methods                                #
    # ###################################################################### #

    @staticmethod
    def _find_difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches(
        reference_pitch: str,
    ) -> tuple[float, ...]:
        difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches = []
        reference_pitch_index = (
            music_parameters.constants.DIATONIC_PITCH_NAME_CYCLE_OF_FIFTH_TUPLE.index(
                reference_pitch
            )
        )
        for (
            diatonic_pitch_name
        ) in music_parameters.constants.DIATONIC_PITCH_CLASS_CONTAINER:
            pitch_index = music_parameters.constants.DIATONIC_PITCH_NAME_CYCLE_OF_FIFTH_TUPLE.index(
                diatonic_pitch_name
            )
            n_exponents_difference_from_reference = pitch_index - reference_pitch_index
            difference_from_tempered_diatonic_pitch = (
                ekmelily_converters.constants.DIFFERENCE_BETWEEN_PYTHAGOREAN_AND_TEMPERED_FIFTH
                * n_exponents_difference_from_reference
            )
            difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches.append(
                difference_from_tempered_diatonic_pitch
            )

        return tuple(difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches)

    @staticmethod
    def _make_global_scale(
        difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches: tuple[
            float, ...
        ],
    ) -> tuple[fractions.Fraction, ...]:
        new_global_scale = []

        for (
            nth_diatonic_pitch,
            difference_in_cents_from_tempered_pitch_class,
        ) in enumerate(
            difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches
        ):
            default_cents_for_diatonic_pitch = (
                EkmelilyTuningFileConverter._alteration_fraction_to_deviation_in_cents(
                    ekmelily_converters.configurations.DEFAULT_GLOBAL_SCALE[
                        nth_diatonic_pitch
                    ]
                )
            )
            n_cents = (
                default_cents_for_diatonic_pitch
                + difference_in_cents_from_tempered_pitch_class
            )
            alteration_fraction = (
                EkmelilyTuningFileConverter._deviation_in_cents_to_alteration_fraction(
                    n_cents, max_denominator=1000
                )
            )
            new_global_scale.append(alteration_fraction)

        return tuple(new_global_scale)

    @staticmethod
    def _make_pythagorean_accidentals(
        set_microtonal_tuning: bool,
    ) -> tuple[EkmelilyAccidental, ...]:
        accidentals = []
        for (
            alteration_name
        ) in (
            ekmelily_converters.constants.PYTHAGOREAN_ACCIDENTAL_TO_CENT_DEVIATION_DICT.keys()
        ):
            glyph = ekmelily_converters.constants.PRIME_AND_EXPONENT_AND_TRADITIONAL_ACCIDENTAL_TO_ACCIDENTAL_GLYPH_DICT[
                None, None, alteration_name
            ]
            if set_microtonal_tuning:
                cents_deviation = ekmelily_converters.constants.PYTHAGOREAN_ACCIDENTAL_TO_CENT_DEVIATION_DICT[
                    alteration_name
                ]
            else:
                cents_deviation = int(
                    music_parameters.constants.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT[
                        alteration_name
                    ]
                    * 200
                )
            accidental = EkmelilyAccidental(alteration_name, (glyph,), cents_deviation)
            accidentals.append(accidental)

        return tuple(accidentals)

    @staticmethod
    def _process_prime(
        prime_to_heji_accidental_name: dict[int, str],
        pythagorean_accidental: str,
        prime: int,
        exponent: int,
        otonality_indicator: str,
        utonality_indicator: str,
        exponent_to_exponent_indicator: typing.Callable[[int], str],
    ) -> tuple[str, str, float]:
        glyph_key = (
            (prime, exponent, pythagorean_accidental)
            if prime == 5
            else (prime, exponent, None)
        )
        glyph = ekmelily_converters.constants.PRIME_AND_EXPONENT_AND_TRADITIONAL_ACCIDENTAL_TO_ACCIDENTAL_GLYPH_DICT[
            glyph_key
        ]

        accidental_name = "{}{}{}".format(
            (otonality_indicator, utonality_indicator)[exponent < 0],
            prime_to_heji_accidental_name[prime],
            exponent_to_exponent_indicator(abs(exponent) - 1),
        )

        cents_deviation = music_parameters.JustIntonationPitch(
            music_parameters.configurations.DEFAULT_PRIME_TO_COMMA_DICT[prime].ratio
            ** exponent
        ).cents
        return accidental_name, glyph, cents_deviation

    @staticmethod
    def _make_higher_prime_accidental(
        pythagorean_accidental: str,
        pythagorean_accidental_cents_deviation: float,
        exponents: tuple[int, ...],
        prime_to_highest_allowed_exponent: dict[int, int],
        prime_to_heji_accidental_name: dict[int, str],
        otonality_indicator: str,
        utonality_indicator: str,
        exponent_to_exponent_indicator: typing.Callable[[int], str],
        set_microtonal_tuning: bool,
    ) -> EkmelilyAccidental:
        accidental_parts = ["{}".format(pythagorean_accidental)]
        cents_deviation = float(pythagorean_accidental_cents_deviation)
        glyphs = []
        for prime, exponent in zip(
            prime_to_highest_allowed_exponent.keys(),
            exponents,
        ):
            if exponent != 0:
                (
                    accidental_change,
                    glyph,
                    cents_deviation_change,
                ) = HEJIEkmelilyTuningFileConverter._process_prime(
                    prime_to_heji_accidental_name,
                    pythagorean_accidental,
                    prime,
                    exponent,
                    otonality_indicator,
                    utonality_indicator,
                    exponent_to_exponent_indicator,
                )
                accidental_parts.append(accidental_change)
                glyphs.append(glyph)
                cents_deviation += cents_deviation_change

        # add traditional accidentals (sharp, flat, etc.) if no syntonic
        # comma is available (if there is any syntonic comma there is
        # already the necessary pythagorean accidental)
        if exponents[0] == 0:
            glyphs.insert(
                0,
                ekmelily_converters.constants.PRIME_AND_EXPONENT_AND_TRADITIONAL_ACCIDENTAL_TO_ACCIDENTAL_GLYPH_DICT[
                    (None, None, pythagorean_accidental)
                ],
            )

        # start with highest primes
        glyphs.reverse()

        accidental_name = "".join(accidental_parts)

        cents_deviation = round(cents_deviation, 4)

        new_accidental = EkmelilyAccidental(
            accidental_name, tuple(glyphs), cents_deviation
        )
        return new_accidental

    @staticmethod
    def _make_accidentals_for_higher_primes(
        prime_to_highest_allowed_exponent: dict[int, int],
        prime_to_heji_accidental_name: dict[int, str],
        otonality_indicator: str,
        utonality_indicator: str,
        exponent_to_exponent_indicator: typing.Callable[[int], str],
        set_microtonal_tuning: bool,
    ) -> tuple[EkmelilyAccidental, ...]:
        allowed_exponents = tuple(
            tuple(range(-maxima_exponent, maxima_exponent + 1))
            for _, maxima_exponent in sorted(
                prime_to_highest_allowed_exponent.items(),
                key=lambda prime_to_maxima_exponent: prime_to_maxima_exponent[0],
            )
        )
        accidentals = []

        for exponents in itertools.product(*allowed_exponents):
            if any(tuple(exp != 0 for exp in exponents)):
                for (
                    pythagorean_accidental,
                    pythagorean_accidental_cents_deviation,
                ) in (
                    ekmelily_converters.constants.PYTHAGOREAN_ACCIDENTAL_TO_CENT_DEVIATION_DICT.items()
                ):
                    accidental = (
                        HEJIEkmelilyTuningFileConverter._make_higher_prime_accidental(
                            pythagorean_accidental,
                            pythagorean_accidental_cents_deviation,
                            exponents,
                            prime_to_highest_allowed_exponent,
                            prime_to_heji_accidental_name,
                            otonality_indicator,
                            utonality_indicator,
                            exponent_to_exponent_indicator,
                            set_microtonal_tuning,
                        )
                    )
                    accidentals.append(accidental)

        return tuple(accidentals)

    @staticmethod
    def _make_tempered_accidentals(
        difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches: tuple[
            float, ...
        ],
        tempered_pitch_indicator: str,
    ) -> tuple[EkmelilyAccidental, ...]:
        accidentals = []

        for (
            nth_diatonic_pitch,
            difference_in_cents_from_tempered_pitch_class,
        ) in enumerate(
            difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches,
        ):
            for (
                tempered_accidental,
                accidental_glyph,
            ) in (
                ekmelily_converters.constants.TEMPERED_ACCIDENTAL_TO_ACCIDENTAL_GLYPH_DICT.items()
            ):

                accidental_name = "{}{}".format(
                    tempered_accidental, tempered_pitch_indicator
                )
                deviation_in_cents = (
                    ekmelily_converters.constants.TEMPERED_ACCIDENTAL_TO_CENT_DEVIATION_DICT[
                        tempered_accidental
                    ]
                    - difference_in_cents_from_tempered_pitch_class
                )

                accidental = EkmelilyAccidental(
                    accidental_name,
                    (accidental_glyph,),
                    deviation_in_cents,
                    available_diatonic_pitch_index_tuple=(nth_diatonic_pitch,),
                )
                accidentals.append(accidental)

        return tuple(accidentals)

    @staticmethod
    def _make_ekmelily_accidental_sequence(
        difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches: tuple[
            float, ...
        ],
        prime_to_highest_allowed_exponent: dict[int, int],
        prime_to_heji_accidental_name: dict[int, str],
        otonality_indicator: str,
        utonality_indicator: str,
        exponent_to_exponent_indicator: typing.Callable[[int], str],
        tempered_pitch_indicator: str,
        set_microtonal_tuning: bool,
    ) -> tuple[EkmelilyAccidental, ...]:

        pythagorean_accidentals = (
            HEJIEkmelilyTuningFileConverter._make_pythagorean_accidentals(
                set_microtonal_tuning
            )
        )

        accidentals_for_higher_primes = (
            HEJIEkmelilyTuningFileConverter._make_accidentals_for_higher_primes(
                prime_to_highest_allowed_exponent,
                prime_to_heji_accidental_name,
                otonality_indicator,
                utonality_indicator,
                exponent_to_exponent_indicator,
                set_microtonal_tuning,
            )
        )

        tempered_accidentals = (
            HEJIEkmelilyTuningFileConverter._make_tempered_accidentals(
                difference_in_cents_from_tempered_pitch_class_for_diatonic_pitches,
                tempered_pitch_indicator,
            )
        )

        return (
            pythagorean_accidentals
            + accidentals_for_higher_primes
            + tempered_accidentals
        )

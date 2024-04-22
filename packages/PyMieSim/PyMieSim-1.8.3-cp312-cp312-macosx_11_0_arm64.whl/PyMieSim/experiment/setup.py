#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import NoReturn
    from PyMieSim.experiment.scatterer import Sphere, Cylinder, CoreShell
    from PyMieSim.experiment.detector import Photodiode, LPMode
    from PyMieSim.experiment.source import Gaussian, PlaneWave

import numpy
from dataclasses import dataclass

from DataVisual import Array, Table
from PyMieSim.binary.Experiment import CppExperiment


@dataclass
class Setup(object):
    """
    Orchestrates the setup and execution of light scattering experiments using PyMieSim.

    Attributes:
        scatterer_set (Union[Sphere, Cylinder, CoreShell]): Configuration for the scatterer in the experiment.
            Defines the physical properties of the particle being studied.
        source_set (Union[Gaussian, PlaneWave]): Configuration for the light source. Specifies the characteristics
            of the light (e.g., wavelength, polarization) illuminating the scatterer.
        detector_set (Union[Photodiode, LPMode, None], optional): Configuration for the detector, if any. Details the
            method of detection for scattered light, including positional and analytical parameters. Defaults to None.

    Methods provide functionality for initializing bindings, generating parameter tables for visualization,
    and executing the simulation to compute and retrieve specified measures.
    """
    scatterer_set: Sphere | Cylinder | CoreShell
    source_set: Gaussian | PlaneWave
    detector_set: Photodiode | LPMode | None = None

    def __post_init__(self):
        """
        Initializes the experiment by setting the source for the scatterer and establishing bindings
        between the components and the simulation environment.
        """
        self.initialize_experiment()
        self.bind_components()

    def initialize_experiment(self) -> NoReturn:
        """
        Initializes the experiment with necessary bindings.
        """
        self.scatterer_set.source_set = self.source_set

        self.binding = CppExperiment()

    def bind_components(self):
        """Binds the experiment components to the CppExperiment instance."""
        for component in [self.source_set, self.scatterer_set, self.detector_set]:
            if component:
                component.bind_to_experiment(experiment=self)

    def generate_datavisual_table(self) -> NoReturn:
        """
        Generates and populates the 'x_table' with parameters from the source, scatterer, and detector sets.
        This table is instrumental for data visualization and analysis.

        Returns:
            NoReturn
        """
        self.x_table = []
        self.x_table.extend(self.source_set.get_datavisual_table())
        self.x_table.extend(self.scatterer_set.get_datavisual_table())

        if self.detector_set:
            self.x_table.extend(self.detector_set.get_datavisual_table())

    def get(self, measure: Table, export_as_numpy: bool = False) -> numpy.ndarray | Array:
        """
        Executes the simulation to compute and retrieve the specified measure.

        Parameters:
            measure (Table): The measure to be computed by the simulation, defined by the user.
            export_as_numpy (bool): Determines the format of the returned data. If True, returns a numpy array,
                                    otherwise returns a Array object for enhanced visualization capabilities.

        Returns:
            Union[numpy.ndarray, Array]: The computed data in the specified format, either as raw numerical
                                              values in a numpy array or structured for visualization with Array.
        """
        if measure.short_label not in self.scatterer_set.available_measure_list:
            raise ValueError(f"Cannot compute {measure.short_label} for {self.scatterer_set.name}")

        measure_string = f'get_{self.scatterer_set.name}_{measure.short_label}'

        array = getattr(self.binding, measure_string)()

        if export_as_numpy:
            return self._export_as_numpy(array)

        return self._export_as_data_visual(measure, array)

    def _export_as_numpy(self, array):
        for k, v in self.source_set.binding_kwargs.items():
            setattr(self, k, v)
        for k, v in self.scatterer_set.binding_kwargs.items():
            setattr(self, k, v)
        if self.detector_set is not None:
            for k, v in self.detector_set.binding_kwargs.items():
                setattr(self, k, v)

        return array

    def _export_as_data_visual(self, measure, array):
        self.generate_datavisual_table()
        measure.set_base_values(array)

        for k, v in self.source_set.mapping.items():
            setattr(self, k, v)
        for k, v in self.scatterer_set.mapping.items():
            setattr(self, k, v)
        if self.detector_set is not None:
            for k, v in self.detector_set.mapping.items():
                setattr(self, k, v)

        return Array(x_table=Table(self.x_table), y=measure)

# -

"""
    turgorgrowth.postprocessing
    ~~~~~~~~~~~~~~~~~~~~~~

    The module :mod:`turgorgrowth.postprocessing` defines post-processing to apply
    on Turgor-Wheat outputs, and provides a front-end to automatize the generation of graphs
    for validation of the outputs.

    Please use front-ends :func:`postprocessing` and :func:`generate_graphs`.

    :license: CeCILL-C, see LICENSE for details.
"""

from __future__ import division  # use "//" to do integer division
import os

import pandas as pd

from turgorgrowth import simulation as turgorgrowth_simulation
from turgorgrowth import tools as turgorgrowth_tools

#: the time index
T_INDEX = turgorgrowth_simulation.Simulation.T_INDEX

#: the indexes to locate the hidden zones in the modeled system
HIDDENZONE_INDEXES = turgorgrowth_simulation.Simulation.HIDDENZONE_INDEXES
#: concatenation of :attr:`T_INDEX` and :attr:`HIDDENZONE_INDEXES`
HIDDENZONE_T_INDEXES = turgorgrowth_simulation.Simulation.HIDDENZONE_T_INDEXES
#: hidden zones post-processing variables
HIDDENZONE_POSTPROCESSING_VARIABLES = []
HIDDENZONE_RUN_VARIABLES_ADDITIONAL = []
#: concatenation of :attr:`HIDDENZONE_T_INDEXES`, :attr:`HIDDENZONE_RUN_VARIABLES <turgorgrowth.simulation.Simulation.HIDDENZONE_RUN_VARIABLES>` and :attr:`HIDDENZONE_POSTPROCESSING_VARIABLES`
HIDDENZONE_RUN_POSTPROCESSING_VARIABLES = HIDDENZONE_T_INDEXES + turgorgrowth_simulation.Simulation.HIDDENZONE_RUN_VARIABLES + HIDDENZONE_RUN_VARIABLES_ADDITIONAL + HIDDENZONE_POSTPROCESSING_VARIABLES

#: the indexes to locate the elements in the modeled system
ELEMENTS_INDEXES = turgorgrowth_simulation.Simulation.ELEMENTS_INDEXES
#: concatenation of :attr:`T_INDEX` and :attr:`ELEMENTS_INDEXES`
ELEMENTS_T_INDEXES = turgorgrowth_simulation.Simulation.ELEMENTS_T_INDEXES
#: elements post-processing variables
ELEMENTS_POSTPROCESSING_VARIABLES = []
ELEMENTS_RUN_VARIABLES_ADDITIONAL = []
#: concatenation of :attr:`ELEMENTS_T_INDEXES`, :attr:`ELEMENTS_RUN_VARIABLES <turgorgrowth.simulation.Simulation.ELEMENTS_RUN_VARIABLES>` and :attr:`ELEMENTS_POSTPROCESSING_VARIABLES`
ELEMENTS_RUN_POSTPROCESSING_VARIABLES = ELEMENTS_T_INDEXES + turgorgrowth_simulation.Simulation.ELEMENTS_RUN_VARIABLES + ELEMENTS_RUN_VARIABLES_ADDITIONAL + ELEMENTS_POSTPROCESSING_VARIABLES

# ---------------------------------------------------
#           POST-PROCESSING FUNCTIONS               -
#           DO NOT USE THEM DIRECTLY                -
# ---------------------------------------------------


class HiddenZone:
    """
    Post-processing to apply on HiddenZone outputs.
    """
    pass


class Element:
    """
    Post-processing to apply on Element outputs.
    """
    pass

# ------------------------------------------------------------------------------------------------
#                                   POST-PROCESSING FRONT-END                                    -
#           PLEASE USE THIS FUNCTION TO APPLY POST-PROCESSING ON THE OUTPUT OF TURGOR-GROWTH     -
# ------------------------------------------------------------------------------------------------


def postprocessing(hiddenzones_df=None, elements_df=None):
    """
    Compute post-processing from Turgor-Growth outputs, and format the post-processing to :class:`dataframes <pandas.DataFrame>`.

    For each post-processing output dataframe:

        * compute post-processing from Turgor-Growth outputs,
        * concatenate Turgor-Growth outputs and post-processing and place the results in a jointed dataframe,
        * reorder the columns of the dataframes according to
          :attr:`HIDDENZONE_RUN_POSTPROCESSING_VARIABLES`, :attr:`ELEMENTS_RUN_POSTPROCESSING_VARIABLES`,
        * and convert the indexes of plants and metamers to integers (if relevant).

    :param pandas.DataFrame hiddenzones_df: Turgor-Growth outputs at hidden zone scale (see :attr:`simulation.Simulation.HIDDENZONE_RUN_VARIABLES`)
    :param pandas.DataFrame elements_df: Turgor-Growth outputs at element scale (see :attr:`simulation.Simulation.ELEMENTS_RUN_VARIABLES`)

    :return: :class:`dataframes <pandas.DataFrame>` of post-processing for each scale:
            * hidden zone (see :attr:`HIDDENZONE_RUN_POSTPROCESSING_VARIABLES`)
            * element (see :attr:`ELEMENTS_RUN_POSTPROCESSING_VARIABLES`)

    :rtype (pandas.DataFrame, pandas.DataFrame)
    """

    returned_dataframes = []

    # hidden zones
    if hiddenzones_df is not None:
        pp_hiddenzones_df = pd.concat([hiddenzones_df, pd.DataFrame(columns=HIDDENZONE_POSTPROCESSING_VARIABLES)], sort=True)
        pp_hiddenzones_df = pp_hiddenzones_df.reindex(columns=HIDDENZONE_RUN_POSTPROCESSING_VARIABLES, copy=False)
        pp_hiddenzones_df[['plant', 'metamer']] = pp_hiddenzones_df[['plant', 'metamer']].astype(int)
        returned_dataframes.append(pp_hiddenzones_df)

    # elements
    if elements_df is not None:
        pp_elements_df = pd.concat([elements_df, pd.DataFrame(columns=ELEMENTS_POSTPROCESSING_VARIABLES)], sort=True)
        pp_elements_df = pp_elements_df.reindex(columns=ELEMENTS_RUN_POSTPROCESSING_VARIABLES, copy=False)
        pp_elements_df[['plant', 'metamer']] = pp_elements_df[['plant', 'metamer']].astype(int)
        returned_dataframes.append(pp_elements_df)

    return tuple(returned_dataframes)


# ---------------------------------------------------------------------
#                       GRAPHS GENERATION FRONT-END                   -
#           PLEASE USE THIS FUNCTION FOR THE GENERATION OF GRAPHS     -
# ---------------------------------------------------------------------

def generate_graphs(hiddenzones_df=None, elements_df=None, graphs_dirpath='.'):
    """
    Generate graphs to validate the outputs of Turgor-Growth, and save them in directory `graphs_dirpath`.

    :param pandas.DataFrame hiddenzones_df: Turgor-Growth outputs at hidden zone scale (see :attr:`HIDDENZONE_RUN_POSTPROCESSING_VARIABLES`)
    :param pandas.DataFrame elements_df: Turgor-Growth outputs at element scale (see :attr:`ELEMENTS_RUN_POSTPROCESSING_VARIABLES`)
    :param str graphs_dirpath: the path of the directory to save the generated graphs
    """

    x_name = 't'
    x_label = 'Time (Hour)'

    # 1) Photosynthetic organs
    if elements_df is not None:
        graph_variables_ph_elements = {'length': 'Length (m)',
                                       'osmotic_water_potential': u'Osmotic water potential (MPa)', 'thickness': u'Thickness (m)', 'total_water_potential': u'Total water potential (MPa)',
                                       'turgor_water_potential': u'Turgor water potential (MPa)', 'water_content': u'Water content (g)', 'width': u'Width (m)',
                                       'water_influx': u'Water_influx (g)', 'resistance': u'Resistance (MPa s g$^{-1}$)'}
    
        for org_ph in (['blade'], ['sheath'], ['internode']):
            for variable_name, variable_label in graph_variables_ph_elements.items():
                graph_name = variable_name + '_' + '_'.join(org_ph) + '.PNG'
                turgorgrowth_tools.plot_turgorgrowth_ouputs(elements_df,
                                                            x_name=x_name,
                                                            y_name=variable_name,
                                                            x_label=x_label,
                                                            y_label=variable_label,
                                                            filters={'organ': org_ph},
                                                            plot_filepath=os.path.join(graphs_dirpath, graph_name),
                                                            explicit_label=False)

    # 2) Hidden zones
    if hiddenzones_df is not None:
        graph_variables_hiddenzones = {'leaf_L': 'Leaf length in hz (m)',
                                       'osmotic_water_potential': u'Osmotic water potential (MPa)', 'width': u'Width (m)', 'total_water_potential': u'Total water potential (MPa)',
                                       'turgor_water_potential': u'Turgor water potential (MPa)', 'water_content': u'Water content (g)', 'water_influx': u'Water_influx (g)',
                                       'resistance': u'Resistance (MPa s g$^{-1}$)', 'thickness': u'Thickness (m)'}
    
        for variable_name, variable_label in graph_variables_hiddenzones.items():
            graph_name = variable_name + '_hz' + '.PNG'
            turgorgrowth_tools.plot_turgorgrowth_ouputs(hiddenzones_df,
                                                        x_name=x_name,
                                                        y_name=variable_name,
                                                        x_label=x_label,
                                                        y_label=variable_label,
                                                        filters={'plant': 1, 'axis': 'MS'},
                                                        plot_filepath=os.path.join(graphs_dirpath, graph_name),
                                                        explicit_label=False)

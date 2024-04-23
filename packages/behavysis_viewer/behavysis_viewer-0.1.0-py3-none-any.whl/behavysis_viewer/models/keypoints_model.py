import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from behavysis_core.mixins.df_io_mixin import DFIOMixin
from behavysis_core.mixins.keypoints_mixin import KeypointsMixin
from behavysis_core.utils.constants import PROCESS_COL
from behavysis_viewer.pydantic_models.experiment_configs import ExperimentConfigs


class KeypointsModel:

    raw_dlc_df: pd.DataFrame
    annot_dlc_df: pd.DataFrame
    indivs_bpts_ls: pd.MultiIndex
    colours_ls = np.ndarray
    pcutoff: float
    radius: int
    colour_level: str
    cmap: str

    def __init__(self):
        self.raw_dlc_df = None
        self.annot_dlc_df = None
        self.indivs_bpts_ls = None
        self.colours_ls = None
        self.pcutoff = None
        self.radius = None
        self.colour_level = None
        self.cmap = None

    def load(self, fp: str, configs: ExperimentConfigs):
        self.raw_dlc_df = DFIOMixin.read_feather(fp)
        self.set_configs(configs)
        self.dlc_2_annot()

    def set_configs(self, configs: ExperimentConfigs):
        configs_filt = configs.user.evaluate.eval_vid
        self.colour_level = configs_filt.colour_level
        self.pcutoff = configs_filt.pcutoff
        self.radius = configs_filt.radius
        self.cmap = configs_filt.cmap

    def dlc_2_annot(self):
        dlc_df = self.raw_dlc_df.copy()
        dlc_df = KeypointsMixin.clean_headings(dlc_df)
        # Modifying dlc_df and making list of how to select dlc_df components to optimise processing
        # Filtering out PROCESS_COL columns
        if PROCESS_COL in dlc_df.columns.unique("individuals"):
            dlc_df.drop(columns=PROCESS_COL, level="individuals")
        # Getting (indivs, bpts) MultiIndex
        indivs_bpts_ls = dlc_df.columns.droplevel("coords").unique()
        # Rounding and casting to correct dtypes - "x" and "y" values are ints
        dlc_df = dlc_df.fillna(0)
        columns = dlc_df.columns[
            dlc_df.columns.get_level_values("coords").isin(["x", "y"])
        ]
        dlc_df[columns] = dlc_df[columns].round(0).astype(int)
        # Changing the columns MultiIndex to a single-level index. For speedup
        dlc_df.columns = [
            f"{indiv}_{bpt}_{coord}" for indiv, bpt, coord in dlc_df.columns
        ]
        # Making the corresponding colours list for each bodypart instance (colours depend on indiv/bpt)
        colours_i, _ = pd.factorize(indivs_bpts_ls.get_level_values(self.colour_level))
        colours_ls = plt.get_cmap(self.cmap)(colours_i / colours_i.max()) * 255
        colours_ls = colours_ls[:, [2, 1, 0, 3]]
        # Saving data to instance
        self.annot_dlc_df = dlc_df
        self.indivs_bpts_ls = indivs_bpts_ls
        self.colours_ls = colours_ls

    def annot_keypoints(self, frame: np.ndarray, frame_num: int) -> np.ndarray:
        """
        Adding the keypoints (given in frame number) to the frame and returning the annotated frame.

        Parameters
        ----------
        frame : np.ndarray
            cv2 frame array.
        frame_num : int
            index (i.e. frame number) in DLC dataframe.

        Returns
        -------
        np.ndarray
            cv2 frame array.
        """
        # Checking that frame_num is in the DLC dataframe
        if frame_num not in self.annot_dlc_df.index:
            return frame
        # Getting the corresponding row in the DLC dataframe
        row = self.annot_dlc_df.loc[frame_num]
        # For each indiv-bpt, if likelihood is above pcutoff, draw the keypoint
        for i, (indiv, bpt) in enumerate(self.indivs_bpts_ls):
            if row[f"{indiv}_{bpt}_likelihood"] >= self.pcutoff:
                cv2.circle(
                    frame,
                    (int(row[f"{indiv}_{bpt}_x"]), int(row[f"{indiv}_{bpt}_y"])),
                    radius=self.radius,
                    color=self.colours_ls[i],
                    thickness=-1,
                )
        return frame

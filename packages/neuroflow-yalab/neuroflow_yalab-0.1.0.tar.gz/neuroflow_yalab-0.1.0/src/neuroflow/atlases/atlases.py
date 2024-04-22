"""
Registrations of atlases to subject's diffusion space.
"""

import copy
from pathlib import Path
from typing import ClassVar, Optional, Union

from nipype.interfaces import fsl

from neuroflow.atlases.available_atlases.available_atlases import AVAILABLE_ATLASES
from neuroflow.atlases.utils import generate_gm_mask_from_5tt, qc_atlas_registration
from neuroflow.files_mapper.files_mapper import FilesMapper


class Atlases:
    """
    Registrations of atlases to subject's diffusion space.
    """

    ATLASES: ClassVar = AVAILABLE_ATLASES
    OUTPUT_TEMPLATE: ClassVar = (
        "sub-{subject}_ses-{session}_space-{space}_label-{label}_{atlas}"
    )

    DIRECTORY_NAME: ClassVar = "atlases"

    def __init__(
        self,
        mapper: FilesMapper,
        output_directory: Union[str, Path],
        atlases: Optional[Union[str, list]] = None,
        crop_to_gm: Optional[bool] = True,
    ):
        """
        Initialize the Atlases class.

        Parameters
        ----------
        mapper : FilesMapper
            An instance of FilesMapper class.
        out_dir : Union[str, Path]
            Path to the output directory.
        atlases : Optional[Union[str, list]]
            Atlases to register.

        """
        self.mapper = mapper
        self.output_directory = self._gen_output_directory(output_directory)
        self.atlases = self._validate_atlas(atlases)
        self.crop_to_gm = crop_to_gm
        self.label = "GM" if self.crop_to_gm else "WholeBrain"

    def _gen_output_directory(self, output_directory: Optional[str] = None) -> Path:
        """
        Generate output directory for QC measures.

        Parameters
        ----------
        output_directory : Optional[str], optional
            Path to the output directory, by default None

        Returns
        -------
        Path
            Path to the output directory
        """
        if output_directory is None:
            return None
        output_directory = Path(output_directory)
        flags = [
            output_directory.parent.name == f"ses-{self.mapper.session}",
            output_directory.parent.parent.name == f"sub-{self.mapper.subject}",
        ]
        if all(flags):
            output_directory = output_directory / self.DIRECTORY_NAME
        else:
            output_directory = (
                Path(output_directory)
                / f"sub-{self.mapper.subject}"
                / f"ses-{self.mapper.session}"
                / self.DIRECTORY_NAME
            )
        output_directory.mkdir(parents=True, exist_ok=True)
        return output_directory

    def _validate_atlas(self, atlases: Union[str, list]):
        """
        Validate that the provided atlas is included in the available atlases.
        """
        if atlases is None:
            return self.ATLASES
        if isinstance(atlases, str):
            atlases = [atlases]
        for atlas in atlases:
            if atlas not in self.ATLASES:
                raise ValueError(f"Atlas {atlas} is not available.")
        return {atlas: self.ATLASES[atlas] for atlas in atlases}

    def generate_gm_mask(self):
        """
        Generate a grey matter mask.
        """
        gm_mask = (
            self.output_directory
            / f"sub-{self.mapper.subject}_ses-{self.mapper.session}_space-T1w_label-GM_mask.nii.gz"  # noqa: E501
        )
        if not gm_mask.exists():
            generate_gm_mask_from_5tt(self.mapper.files.get("t1w_5tt"), gm_mask)
        return gm_mask

    def register_atlas_to_t1w(self, force: bool = False):
        """
        Register an atlas to the subject's T1w space.
        """
        t1w_atlases = copy.deepcopy(self.atlases)
        for atlas, atlas_entities in self.atlases.items():
            nifti = atlas_entities["nifti"]
            atlas_base = Path(nifti).name.replace("space-MNI152_", "")
            out_file = self.output_directory / self.OUTPUT_TEMPLATE.format(
                subject=self.mapper.subject,
                session=self.mapper.session,
                space="T1w",
                atlas=atlas_base,
                label=self.label,
            )
            t1w_atlases[atlas]["nifti"] = str(out_file)
            if force:
                out_file.unlink(missing_ok=True)
            if out_file.exists():
                continue
            aw = fsl.ApplyWarp(datatype="int", interp="nn", out_file=str(out_file))
            aw.inputs.in_file = nifti
            aw.inputs.ref_file = self.mapper.files.get("t1w_brain")
            aw.inputs.mask_file = (
                self.mapper.files.get("t1w_brain_mask")
                if not self.crop_to_gm
                else self.generate_gm_mask()
            )
            aw.inputs.field_file = self.mapper.files.get("template_to_t1w_warp")
            aw.run()
            qc_atlas_registration(
                out_file, self.mapper.files.get("t1w_brain"), atlas, "T1w", force=force
            )
        return t1w_atlases

    def register_atlas_to_dwi(self, force: bool = False):
        """
        Register an atlas to the subject's diffusion space.
        """
        dwi_atlases = copy.deepcopy(self.atlases)
        for atlas, atlas_entities in self.atlases.items():
            nifti = atlas_entities["nifti"]
            in_file = self.t1w_atlases[atlas]["nifti"]
            atlas_base = Path(nifti).name.replace("space-MNI152_", "")
            out_file = self.output_directory / self.OUTPUT_TEMPLATE.format(
                subject=self.mapper.subject,
                session=self.mapper.session,
                space="dwi",
                atlas=atlas_base,
                label=self.label,
            )
            dwi_atlases[atlas]["nifti"] = str(out_file)
            if force:
                out_file.unlink(missing_ok=True)
            if out_file.exists():
                continue
            apply_xfm = fsl.ApplyXFM(
                datatype="int", interp="nearestneighbour", out_file=str(out_file)
            )
            apply_xfm.inputs.in_file = in_file
            apply_xfm.inputs.reference = self.mapper.files.get("b0_brain")
            apply_xfm.inputs.in_matrix_file = self.mapper.files.get("t1w_to_dwi_mat")
            apply_xfm.inputs.apply_xfm = True
            res = apply_xfm.run()
            # clean up the intermediate file
            Path(res.outputs.out_matrix_file).unlink()

            qc_atlas_registration(
                out_file, self.mapper.files.get("b0_brain"), atlas, "DWI", force=force
            )
        return dwi_atlases

    @property
    def t1w_atlases(self):
        """
        Register the atlases to the T1w space.
        """
        return self.register_atlas_to_t1w()

    @property
    def dwi_atlases(self):
        """
        Register the atlases to the diffusion space.
        """
        return self.register_atlas_to_dwi()

from typing import Union
from .event_collection import Event

try:
    from func_adl_servicex.ServiceX import ServiceXSourceCPPBase
    from servicex.servicex import ServiceXDataset
    from servicex.utils import DatasetType


    class SXDSAtlasxAODR22(ServiceXSourceCPPBase[Event]):
        def __init__(self, sx: Union[ServiceXDataset, DatasetType], backend="atlasr22"):
            """
            Create a servicex dataset sequence from a servicex dataset.
            """
            super().__init__(sx, backend, item_type=Event)


    class SXDSAtlasxAODR22PHYS(ServiceXSourceCPPBase[Event]):
        def __init__(self, sx: Union[ServiceXDataset, DatasetType], backend="atlasr22"):
            """
            Create a servicex dataset sequence from a servicex dataset.
            """
            super().__init__(sx, backend, item_type=Event)
            # Do update-in-place to configure the calibration
            from .calibration_support import calib_tools
            new_sx = calib_tools.query_update(self, calib_tools.default_config("PHYS"))
            self._q_ast = new_sx._q_ast


    class SXDSAtlasxAODR22PHYSLITE(ServiceXSourceCPPBase[Event]):
        def __init__(self, sx: Union[ServiceXDataset, DatasetType], backend="atlasr22"):
            """
            Create a servicex dataset sequence from a servicex dataset.
            """
            super().__init__(sx, backend, item_type=Event)
            # Do update-in-place to configure the calibration
            from .calibration_support import calib_tools
            new_sx = calib_tools.query_update(self, calib_tools.default_config("PHYSLITE"))
            self._q_ast = new_sx._q_ast

except ImportError:
        pass

try:
    from servicex import FuncADLQuery as sxFuncADLQuery


    class FuncADLQuery(sxFuncADLQuery[Event]):
        def __init__(self, **kwargs):
            '''Builds a `FuncADLQuery` object to work with 
            datasets. Pass any argument to this function that you would normally
            pass to `FuncADLQuery`.

            Args:
            * `item_type` - The type of this object. Will default to `Event`.
            * `codegen` - This backend code-generator. Defaults to `atlasr22`.

            Note:
            * The current front-end ignores the `codegen` argument.
            '''
            if "item_type" not in kwargs:
                kwargs["item_type"] = Event
            if "codegen" not in kwargs:
                kwargs["codegen"] = "atlasr22"

            super().__init__(**kwargs)


    class FuncADLQueryPHYS(sxFuncADLQuery[Event]):
        def __init__(self, **kwargs):
            '''Builds a `FuncADLQuery` object to work with PHYS
            datasets. Pass any argument to this function that you would normally
            pass to `FuncADLQuery`.

            Args:
            * `item_type` - The type of this object. Will default to `Event`.
            * `codegen` - This backend code-generator. Defaults to `atlasr22`.

            Note:
            * The current front-end ignores the `codegen` argument.
            '''
            if "item_type" not in kwargs:
                kwargs["item_type"] = Event
            if "codegen" not in kwargs:
                kwargs["codegen"] = "atlasr22"

            super().__init__(**kwargs)
            # Hack to subvert the replace-in-place.
            from .calibration_support import calib_tools
            ds = calib_tools.query_update(self, calib_tools.default_config("PHYS"))
            self._q_ast = ds._q_ast


    class FuncADLQueryPHYSLITE(sxFuncADLQuery[Event]):
        def __init__(self, **kwargs):
            '''Builds a `FuncADLQuery` object to work with PHYSLITE
            datasets. Pass any argument to this function that you would normally
            pass to `FuncADLQuery`.

            Args:
            * `item_type` - The type of this object. Will default to `Event`.
            * `codegen` - This backend code-generator. Defaults to `atlasr22`.

            Note:
            * The current front-end ignores the `codegen` argument.
            '''
            if "item_type" not in kwargs:
                kwargs["item_type"] = Event
            if "codegen" not in kwargs:
                kwargs["codegen"] = "atlasr22"

            super().__init__(**kwargs)
            # Hack to subvert the replace-in-place.
            from .calibration_support import calib_tools
            ds = calib_tools.query_update(self, calib_tools.default_config("PHYSLITE"))
            self._q_ast = ds._q_ast

except ImportError:
        pass

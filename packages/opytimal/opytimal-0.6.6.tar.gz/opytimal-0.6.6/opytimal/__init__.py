'''
Opytimal module
'''

from dolfin import *

from .numeric import getPow10
from .profiler import ProgressBar
from .tests import testLoop
from .parallel import parallel
from .types import Tuple, Union
from .files import createFolder
from .profiler import tic, toc, ticRAM, tocRAM
from .mathFunctions import sin, cos, tan, exp, log, ln
from .symbols import x, y, z, t, symbols
from .analytical import (AnalyticalFunction, AnalyticalVectorFunction)
from .arrays import (identity, zeros, getComplement, array, concatenate,
                     ravel, hstack, vstack, arange, norm as arrNorm,
                     flatten)
from .strings import (showInfo, splitPathFile, replaceProgressive,
                      basename, showErrors)
from .meshes import (readXDMFMesh, getInnerNodes, getSubMeshes,
                     getCoordinates, getNormal, getBoundaryDofsWithout,
                     getBoundaryDofs)
from .plots import (plotMesh, plotComparison, adjustFiguresInScreen,
                    show, figure, dynamicComparison, imageTypes,
                    setPltStyle, plt)
from .fenics import (setExpression, extractElements, calculeNnz,
                     mySolve, appendErrorsByTime, getInputExactData,
                     setSolver, getErrorFormula, gradJ, copySolver,
                     getFormTerm, emptyForm, gradientDescent, showError,
                     getDomainLabels, replaceBoundNameByMark,
                     getMeasure, evaluateErrors, Zero, getAdjointSystem,
                     getOptimalConditionsSystem, evaluateCost,
                     getLocal, setLocal, showProblemData,
                     getFunctionExpressions)

__version__ = "0.6.6"

def __getattr__(attr):
    # Warn for expired attributes
    import warnings

    if attr == "demos":
        import opytimal.demos as demos
        return demos

    raise AttributeError("module {!r} has no attribute "
                            "{!r}".format(__name__, attr))

def __dir__():
    public_symbols = (
        {'demos', 'dolfin'}
    )
    return list(public_symbols)

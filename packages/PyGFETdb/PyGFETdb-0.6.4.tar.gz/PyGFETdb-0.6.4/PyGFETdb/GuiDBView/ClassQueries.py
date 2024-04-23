import numpy as np
import quantities as pq

# Default Units
OutUnits = {'Ids': 'uA',
            'GM': 'mS',
            'GMabs': 'mS',
            'GMV': 'mS/V',
            'Irms': 'uA',
            'Vrms': 'uV',
            'NoA': 'A**2',
            'NoC': 'A**2',
            'GmFcut': 'Hz',
            'GmF0': 'mS',
            'GmErr': '',
            }

# Default Scalar parameters
FixQueries = {'CNP': {'Param': 'Ud0',
                      'Units': 'mV'},
              'IgMax': {'Param': 'IgMax',
                        'Units': 'nA'
                        },
              'RdsCNP': {'Param': 'Rds',
                         'Vgs': 0 * pq.V,
                         'Ud0Norm': True,
                         'Units': 'kOhm'
                         },
              }


def GenQueries(Pars, Vgs=-0.1 * pq.V, Ud0Norm=True, KeySufix='01'):
    Out = {}
    for par in Pars:
        d = {'Param': par,
             'Vgs': Vgs,
             'Ud0Norm': Ud0Norm}
        if par in OutUnits:
            d['Units'] = OutUnits[par]
        Out[par + KeySufix] = d
    return Out


def GenpdAttrs(ClassQueries):
    Vgs = []
    VgsNorm = []
    ScalarCols = []
    ArrayCols = []
    ArrayColsNorm = []
    for k, q in ClassQueries.items():
        if 'Vgs' in q:
            if q['Vgs'].size == 1:
                ScalarCols.append(k)
            else:
                ArrayCols.append(k)
                if q['Ud0Norm']:
                    ArrayColsNorm.append(k)
                    VgsNorm.append(q['Vgs'])
                else:
                    Vgs.append(q['Vgs'])
        else:
            ScalarCols.append(k)

    for v in Vgs:
        if not (v == Vgs[0]).all():
            print('Error in Vgs')

    for v in VgsNorm:
        if not (v == VgsNorm[0]).all():
            print('Error in VgsNorm')

    return {'Vgs': Vgs[0],
            'VgsNorm': VgsNorm[0],
            'ScalarCols': ScalarCols,
            'ArrayCols': ArrayCols,
            'ArrayColsNorm': ArrayColsNorm

            }

def UpdateVgs(ClassQueries, Vgs, Ud0Norm):
    pdAttr = GenpdAttrs(ClassQueries)
    for k, q in ClassQueries.items():
        if k in pdAttr['ScalarCols']:
            if 'Vgs' in q:
                q['Vgs'] = Vgs
            if 'Ud0Norm' in q:
                q['Ud0Norm'] = Ud0Norm

    return ClassQueries

########################################################################################################################
## Define default scalar parameters
########################################################################################################################
ScalarSimpleQueriesDC = GenQueries(Pars=('Ids', 'GMabs'))
ScalarSimpleQueriesDC.update(FixQueries)

ScalarQueriesDC = GenQueries(Pars=('Ids', 'GM', 'GMV', 'GMabs'))
ScalarQueriesDC.update(FixQueries)

ScalarQueriesAC = GenQueries(Pars=('Irms', 'Vrms', 'NoA', 'NoB', 'NoC', 'GmFcut', 'GmF0', 'GmErr'))
ScalarQueriesAC.update(FixQueries)

ScalarSimpleQueriesAC = GenQueries(Pars=('Irms', 'Vrms', 'GmFcut', 'GmF0'))
ScalarSimpleQueriesDC.update(FixQueries)

########################################################################################################################
## Define default Array parameters
########################################################################################################################
Vgs = np.linspace(-0.6, 0.6, 200) * pq.V
VgsNorm = np.linspace(-0.4, 0.4, 200) * pq.V

ArraySimpleQueriesDC = GenQueries(Pars=('Ids', 'GMabs'),
                                  Vgs=Vgs,
                                  Ud0Norm=False,
                                  KeySufix='')
ArraySimpleQueriesDC.update(GenQueries(Pars=('Ids', 'GMabs'),
                                       Vgs=VgsNorm,
                                       Ud0Norm=True,
                                       KeySufix='Norm'))

ArrayQueriesDC = GenQueries(Pars=('Ids', 'GM', 'GMV', 'GMabs'),
                            Vgs=Vgs,
                            Ud0Norm=False,
                            KeySufix='')
ArrayQueriesDC.update(GenQueries(Pars=('Ids', 'GM', 'GMV', 'GMabs'),
                                 Vgs=VgsNorm,
                                 Ud0Norm=True,
                                 KeySufix='Norm'))

ArrayQueriesAC = GenQueries(Pars=('Irms', 'Vrms', 'NoA', 'NoB', 'NoC', 'GmFcut', 'GmF0', 'GmErr'),
                            Vgs=Vgs,
                            Ud0Norm=False,
                            KeySufix='')
ArrayQueriesAC.update(GenQueries(Pars=('Irms', 'Vrms', 'NoA', 'NoB', 'NoC', 'GmFcut', 'GmF0', 'GmErr'),
                                 Vgs=VgsNorm,
                                 Ud0Norm=True,
                                 KeySufix='Norm'))

ArraySimpleQueriesAC = GenQueries(Pars=('Irms', 'Vrms', 'GmFcut', 'GmF0',),
                                  Vgs=Vgs,
                                  Ud0Norm=False,
                                  KeySufix='')
ArraySimpleQueriesAC.update(GenQueries(Pars=('Irms', 'Vrms', 'GmFcut', 'GmF0',),
                                       Vgs=VgsNorm,
                                       Ud0Norm=True,
                                       KeySufix='Norm'))

#######################################################################################################################
## Define Class Queries
########################################################################################################################

ClassQueries = ScalarQueriesDC.copy()
ClassQueries.update(ScalarQueriesAC)
ClassQueries.update(ArrayQueriesDC)
ClassQueries.update(ArrayQueriesAC)

ClassQueriesSimple = ScalarSimpleQueriesDC.copy()
ClassQueriesSimple.update(ScalarSimpleQueriesAC)
ClassQueriesSimple.update(ArraySimpleQueriesDC)
ClassQueriesSimple.update(ArraySimpleQueriesAC)

ClassQueriesDC = ScalarQueriesDC.copy()
ClassQueriesDC.update(ArrayQueriesDC)
ClassQueriesDCSimple = ScalarSimpleQueriesDC.copy()
ClassQueriesDCSimple.update(ArraySimpleQueriesDC)



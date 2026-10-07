_alt_packs = []
_circle=np.linspace(0,2*np.pi,12,endpoint=False)
_small_ring=make_pca_case(np.column_stack([np.cos(_circle),np.sin(_circle)])*3,False)
for _source in [pca_lab['covCases'], [pca_lab['edgeCases'][1],_small_ring,pca_lab['nuisance']]]:
    _alt_list=[]
    for _old in _source:
        _case=make_pca_case(_old['raw'])
        for _frame in _case['frames']:
            for _key in ['terms','residual','turn','eigen','lengths','kept','lost']:
                _frame.pop(_key,None)
        _alt_list.append(_case)
    _alt_packs.append(_alt_list)
pca_cov_v2=_alt_packs[0]
# Base-case triangles need the three squared lengths. Other examples do not.
pca_cov_v2[0]=pca_lab['base']
pca_edges_v2=_alt_packs[1]
pca_model_v2={'challenge':pca_lab['challenge']}
pca_scales_v2=[]
for _scale in pca_lab['scales']:
    _pack={}
    for _kind in ['raw','standard']:
        _case=make_pca_case(_scale[_kind]['raw'],False)
        _w=np.asarray(_case['axes'][0])
        _pts=np.asarray(_case['points'])
        _z=_pts@_w
        _pr=np.outer(_z,_w)
        _kept=_z**2
        _lost=((_pts-_pr)**2).sum(1)
        _case['frames']=[dict(w=_w.tolist(),sw=(np.asarray(_case['cov'])@_w).tolist(),z=_z.tolist(),projected=_pr.tolist(),kept=_kept.tolist(),lost=_lost.tolist(),lengths=(_pts**2).sum(1).tolist(),variance=_case['values'][0],loss=_case['values'][1],ratio=_case['ratio'],slope=0,sumSquares=float(_kept.sum()))]
        _pack[_kind]=_case
    pca_scales_v2.append(_pack)
None

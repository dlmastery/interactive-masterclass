_base = np.array([[8,7],[7,8],[5,4],[4,5]],dtype=float)
_centered = _base - _base.mean(0)
_cases = [make_pca_case(_base), make_pca_case(_centered * [1,-1],False),
          make_pca_case(np.column_stack((_centered[:,0],[1,-2,2,-1])),False)]
_centers = []
for _i in range(21):
    _fraction = _i/20
    _shifted = _base - _fraction*_base.mean(0)
    _centers.append(dict(points=_shifted.tolist(),mean=_shifted.mean(0).tolist(),
                         fraction=_fraction))
_scales = []
for _factor in range(1,11):
    _scaled = _centered * [1,_factor]
    _scales.append(dict(raw=make_pca_case(_scaled,False),
        standard=make_pca_case(_scaled/_scaled.std(0,ddof=1),False),factor=_factor))
_ruler = []
for _length in range(1,7):
    _w = np.array([1.,1.])/np.sqrt(2)*_length
    _z = _centered@_w
    _ruler.append(dict(length=_length,w=_w.tolist(),z=_z.tolist(),
        norm2=float(_w@_w),variance=float(_z@_z/3)))
_mix = []
for _i in range(101):
    _p = _i/100
    _v = _p*6+(1-_p)*2/3
    _mix.append(dict(p=_p,a=float(np.sqrt(_p)),b=float(np.sqrt(1-_p)),
        variance=_v,first=_p*6,second=(1-_p)*2/3))
_rotation = np.array([[np.cos(.41),-np.sin(.41)],[np.sin(.41),np.cos(.41)]])
_challenge = make_pca_case(_centered@_rotation.T)
_theta = np.linspace(0,2*np.pi,24,endpoint=False)
_ring = make_pca_case(np.column_stack([np.cos(_theta),np.sin(_theta)])*3,False)
_nuisance = make_pca_case([[x,y] for y in [-.5,.5] for x in [-3,-1,1,3]],False)
_outlier = make_pca_case(np.vstack([_centered,[0,10]]),False)
pca_lab = dict(base=_cases[0],covCases=_cases,centers=_centers,scales=_scales,
               ruler=_ruler,mixtures=_mix,challenge=_challenge,
               edgeCases=[make_pca_case(_centered,False),_outlier,_ring],
               nuisance=_nuisance,people=['A','B','C','D'])
None

def provider_usgs_base(pos, type, **kwargs):
    x, y, z = pos
    url = f'https://basemap.nationalmap.gov/arcgis/rest/services/{type}/MapServer/tile/{z}/{y}/{x}'
    return url


def provider_usgs_hydro(pos, **kwargs):
    return provider_usgs_base(pos, type='USGSHydroCached', **kwargs)


def provider_usgs_imagery(pos, **kwargs):
    return provider_usgs_base(pos, type='USGSImageryOnly', **kwargs)


def provider_usgs_imagery_topo(pos, **kwargs):
    return provider_usgs_base(pos, type='USGSImageryTopo', **kwargs)


def provider_usgs_shaded_relief(pos, **kwargs):
    return provider_usgs_base(pos, type='USGSShadedReliefOnly', **kwargs)


def provider_usgs_tnm_blank(pos, **kwargs):
    return provider_usgs_base(pos, type='USGSTNMBlank', **kwargs)


def provider_usgs_topo(pos, **kwargs):
    return provider_usgs_base(pos, type='USGSTopo', **kwargs)


def provider_strm(pos, **kwargs):
    x, y, z = pos
    url = f'https://s3.amazonaws.com/elevation-tiles-prod/  {z}/{x}/{y}.png'
    return url


providers = {
    'usgs_hydro': provider_usgs_hydro,
    'usgs_imagery': provider_usgs_imagery,
    'usgs_imagery_topo': provider_usgs_imagery_topo,
    'usgs_shaded_relief': provider_usgs_shaded_relief,
    'usgs_tnm_blank': provider_usgs_tnm_blank,
    'usgs_topo': provider_usgs_topo,
    'strm': provider_strm,
}

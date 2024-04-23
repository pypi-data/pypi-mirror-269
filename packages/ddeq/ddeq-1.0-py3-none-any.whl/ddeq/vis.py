
import copy
import os
import textwrap
import warnings

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.colors import LinearSegmentedColormap, LogNorm

import matplotlib as mpl
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import cartopy.feature as cfeature
import numpy as np
import pandas
import scipy.stats
import ucat
import xarray as xr

import ddeq


LON_EQ_TO_LETTER = {
    0: 'a',  401: 'b', 805: 'c', 1207: 'd', 1610: 'e', 2012: 'f'
}


def sub_numbers(s):
    return s.translate(str.maketrans("xX0123456789", "ₓₓ₀₁₂₃₄₅₆₇₈₉"))


def add_gridlines(ax, dlon=1.0, dlat=1.0):
    """
    Add grid lines to ax.
    """
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0.5, color='k', alpha=0.5, linestyle='-',
                      x_inline=False, y_inline=False, #zorder=6,
    )
    gl.top_labels = False
    gl.bottom_labels = True
    gl.right_labels = False

    gl.xlocator = mticker.FixedLocator(np.arange(-180,180,dlon))
    gl.ylocator = mticker.FixedLocator(np.arange(-90,90,dlat))

    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 9, 'color': 'black'}
    gl.ylabel_style = {'size': 9, 'color': 'black'}


def corners2grid(lon, lat):
    """
    Create lon, lat grid from four corners of pixel (n,m,4).
    """
    lonc = np.zeros((lon.shape[0]+1, lon.shape[1]+1))
    lonc[:-1,:-1] = lon[:,:,0]
    lonc[-1,:-1] = lon[-1,:,3]
    lonc[:-1,-1] = lon[:,-1,1]
    lonc[-1,-1] = lon[-1,-1,2]

    latc = np.zeros((lat.shape[0]+1, lat.shape[1]+1))
    latc[:-1,:-1] = lat[:,:,0]
    latc[-1,:-1] = lat[-1,:,3]
    latc[:-1,-1] = lat[:,-1,1]
    latc[-1,-1] = lat[-1,-1,2]

    return lonc, latc


def create_map(domain, add_colorbar=False, edgecolor='black',
               admin_level=1, fig_size=6.0, dright=0.0, ax=None):
    """
    Make a map for given domain (ddeq.misc.Domain).
    """

    dx = (domain.stoplon - domain.startlon)
    dy = (domain.stoplat - domain.startlat)

    if add_colorbar:
        dc = 1.0
        ll, rr = 0.017, 0.8-dright
    else:
        dc = 0.0
        ll, rr = 0.02, 0.96

    if ax is None:
        fig = plt.figure(figsize=(fig_size+dc, fig_size*dy/dx))
        ax = fig.add_axes([ll,0.02,rr,0.96], projection=domain.proj)

    else:
        fig = ax.get_figure()

    ax.set_aspect('equal', adjustable='box')

    ax.set_xlim(domain.startlon, domain.stoplon)
    ax.set_ylim(domain.startlat, domain.stoplat)

    if add_colorbar:
        cax = fig.add_axes([2*ll+rr,0.02,0.04,0.96])
    else:
        cax = None

    ax.coastlines(resolution='10m', color=edgecolor, linewidth=1.0)
    lines = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_boundary_lines_land',
        scale='10m',
    )
    ax.add_feature(lines, edgecolor=edgecolor, facecolor='none', linewidth=1.0)

    if admin_level > 0:
        lines = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='10m',
        )
        ax.add_feature(lines, edgecolor=edgecolor, facecolor='none', linewidth=0.5)

    return fig, ax, cax


def make_field_map(data, trace_gas, domain=None, vmin=None, vmax=None,
                   cmap='viridis', border=0.00, label='',
                   fig=None, alpha=None, xlim=None, ylim=None,
                   edgecolor='black', add_colorbar=True,
                   fig_size=6.0, dright=0.0, admin_level=1,
                   origin='lower'):
    """
    Make a map of 2D field.
    """
    rlon, rlat = data['rlon'], data['rlat']
    field = data[trace_gas]

    dlon = rlon[1] - rlon[0]
    left = rlon[0] - dlon / 2.0
    right = rlon[-1] + dlon / 2.0

    dlat = rlat[1] - rlat[0]
    bottom = rlat[0] - dlat / 2.0
    top = rlat[-1] + dlat / 2.0

    if fig is None:
        fig,ax,cax = create_map(domain, add_colorbar, edgecolor=edgecolor,
                                fig_size=fig_size, dright=dright,
                                admin_level=admin_level)
    else:
        ax, cax = fig.get_axes()
        cax.cla()

        # remove cosmo data
        ax.axes.get_images()[0].remove()

    c = ax.imshow(field, norm=None, vmin=vmin, vmax=vmax, cmap=cmap, zorder=-1,
                  aspect=ax.get_aspect(), origin=origin, 
                  extent=(left, right, bottom, top), transform=domain.proj)

    if add_colorbar:
        cb = plt.colorbar(c, cax=cax)
        cb.set_label(label)

    if alpha is not None:
        cm = LinearSegmentedColormap.from_list('alpha', [(1,1,1,0),(1,1,1,1)], 256)
        ax.imshow(alpha, vmin=0, vmax=1, cmap=cm, zorder=-1,
                  aspect=ax.get_aspect(), origin=origin,
                  extent=(left, right, bottom, top), transform=domain.proj)


    ax.set_xlim(left + border * dlon, right - border * dlon)
    ax.set_ylim(bottom + border * dlat, top - border * dlat)


    if xlim is not None:
        ax.set_xlim(*xlim)

    if ylim is not None:
        ax.set_ylim(*ylim)


    return fig


def make_level2_map(lon, lat, values, domain=None, fig=None,
                    vmin=None, vmax=None, label='', alpha=1.0,
                    cmap='viridis', clct=None, xlim=None, ylim=None,
                    edgecolor='black', is_discrete=False,
                    cb_labels=None, cb_labelsize='small',
                    truncate_cmap=False, do_zoom=False, zoom_area=None,
                    fig_size=6.0, dright=0.0, bg_color='silver',
                    admin_level=1, add_colorbar=True):
    """\
    Make a map of Level-2 satellite data.

    lon, lat :: longitude and latitude of pixel corners
    values   :: 2d field of level-2 data

    is_discrete :: bool (default False)
        if True uses colormap with discrete levels with one colour per values
        in fields
    """
    lon = np.asarray(lon)
    lat = np.asarray(lat)
    values = np.asarray(values)

    # Mask invalid lon/lat towards the nearest pole because pcolormesh cannot
    # handle nans in the coordinates, which can happen with the TROPOMI product.
    if np.any(np.isnan(lon)) or np.any(np.isnan(lat)):
        lon = xr.where(np.isnan(lon), 0, lon)
        if np.nanmean(lat) < 0:
             lat = xr.where( np.isnan(lat), -90, lat)
        else:
             lat = xr.where( np.isnan(lat), +90, lat)

    if values.dtype == bool:
        is_discrete = True

    if fig is None:
        fig,ax,cax = create_map(domain, add_colorbar=add_colorbar,
                                edgecolor=edgecolor,
                                fig_size=fig_size, dright=dright,
                                admin_level=admin_level)
    else:
        if isinstance(fig, plt.Figure):
            ax, cax = fig.get_axes()
        else:
            ax, cax = fig
            fig = ax.get_figure()

    # draw background
    if bg_color is not None:
        bg_color = 255 * np.array(mpl.colors.to_rgb(bg_color))
        bg = np.tile(np.array(bg_color, dtype=np.uint8), [2,2,1])
        ax.imshow(bg, origin='upper', aspect=ax.get_aspect(),
                transform=ccrs.PlateCarree(),
                extent=[-180, 180, -180, 180]
        )

    if is_discrete:
        if hasattr(values, 'mask'):
            v = values[~values.mask].flatten()
        else:
            v = values.flatten()

        if cb_labels is None:
            n = len(set(v))
        else:
            n = len(cb_labels)

        if isinstance(cmap, list):
            cmap = LinearSegmentedColormap.from_list('list', cmap)
        else:
            try:
                cmap = mpl.colormaps.get_cmap(cmap)
            except AttributeError:
                cmap = plt.cm.get_cmap(cmap)

        bounplrange(-0.5,n+0.5)
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    else:
        try:
            cmap = mpl.colormaps.get_cmap(cmap)
        except AttributeError:
            cmap = plt.cm.get_cmap(cmap)

        cmap = copy.copy(cmap)
        cmap.set_bad('#a0a0a0')

        norm = None

    if truncate_cmap:
        cmap = LinearSegmentedColormap.from_list(
                'new', cmap(np.linspace(0.25, 1.0, 101))
        )

    # create tiled grid
    if np.ndim(lon) == 3 and np.ndim(lat) == 3:
        lonc, latc = corners2grid(lon,lat)

        # FIXME: pcolormesh causes crash if calling ax.legend
        c = ax.pcolormesh(lonc, latc, values, vmin=vmin, vmax=vmax, cmap=cmap,
                          norm=norm, alpha=alpha, transform=ccrs.PlateCarree(),
                          shading='flat', edgecolors='None')
        c.set_rasterized(True)

        if clct is not None:
            cm = LinearSegmentedColormap.from_list('alpha', [(1,1,1,0),(1,1,1,1)], 256)
            c2 = ax.pcolormesh(lonc, latc, clct, vmin=0, vmax=1, cmap=cm,
                               shading='flat', transform=ccrs.PlateCarree())
            c2.set_rasterized(True)

    else:
        c = ax.scatter(lon, lat, c=values, vmin=vmin, vmax=vmax, cmap=cmap,
                       alpha=alpha, transform=ccrs.PlateCarree())


    if xlim is not None and np.all(np.isfinite(xlim)):
        ax.set_xlim(*xlim)
    if ylim is not None and np.all(np.isfinite(ylim)):
        ax.set_ylim(*ylim)

    if add_colorbar:
        cb = plt.colorbar(c, cax=cax)
        cb.set_label(label)

        if is_discrete:
            cb.set_ticks(np.arange(0,n+1))

        if cb_labels is not None:
            cb.set_ticklabels(cb_labels)
            cb.ax.tick_params(labelsize=cb_labelsize)

    if do_zoom:
        if zoom_area is None:
            zoom_area = np.isfinite(values)

        xmin, xmax = np.min(lon[zoom_area]), np.max(lon[zoom_area])
        ymin, ymax = np.min(lat[zoom_area]), np.max(lat[zoom_area])

        xmin, ymin = domain.proj.transform_point(xmin, ymin, ccrs.PlateCarree())
        xmax, ymax = domain.proj.transform_point(xmax, ymax, ccrs.PlateCarree())

        ax.set_xlim(xmin - 0.1, xmax + 0.1)
        ax.set_ylim(ymin - 0.1, ymax + 0.1)

    return fig




def _iter_contours(x, y, binary, nmax=4, tolerance=1.0):
    """
    Iter over contours.
    """
    x = np.array(x)
    y = np.array(y)
    binary = np.array(binary)

    for contour in skimage.measure.find_contours(binary, 0.5):
        coords = skimage.measure.approximate_polygon(contour, tolerance=tolerance)

        n,_ = np.shape(coords)
        if n <= nmax:
            continue

        i,j = coords[:,0].astype(int), coords[:,1].astype(int)
        yield x[i,j], y[i,j]


def draw_contours(ax, x, y, binary, ls='-', color='k', label=None,
                  tolerance=1.0, transform=ccrs.PlateCarree()):
    """
    Draw contours for given x and y coords to axis used for example for
    drawing outer border of CO2 plume.
    """
    line = []
    for x,y in _iter_contours(x, y, binary, tolerance=tolerance):
        line = ax.plot(x,y, color=color, ls=ls, transform=ccrs.PlateCarree(),
                       label=label)

        label = '_none_'

    return line


def add_hot_spots(ax, color='black', size='medium', suffixes=None, sources=None,
                  va='center', ha=None, fontdict=None, bbox=None, ms=None,
                  do_path_effect=False, mec=None, add_labels=True,
                  winds=None, domain=None, time=None):
    """
    Add marker and name of hot spots to map.
    """
    if domain is not None:
        if domain.proj is None:
            lon_o = sources.lon_o.values
            lat_o = sources.lat_o.values
        else:
            lon_o, lat_o, _ = domain.proj.transform_points(ccrs.PlateCarree(),
                                                           sources.lon_o,
                                                           sources.lat_o).T
        in_domain = xr.DataArray(
            (lat_o >= domain.startlat) &
            (lat_o <= domain.stoplat)  &
            (lon_o >= domain.startlon) &
            (lon_o <= domain.stoplon),
            dims='source'
        )
        sources = sources.where(in_domain, drop=True)

    if add_labels:
        if winds is not None:
            ax.plot(0, -90, '>', color=color, transform=ccrs.PlateCarree(),
                    mec=mec, ms=ms, label='point source (with wind direction)',
                    zorder=0)
        else:
            ax.plot(0, -90, 'D', color=color, transform=ccrs.PlateCarree(),
                    mec=mec, ms=ms, label='city', zorder=0)
            ax.plot(0, -90, 'o', color=color, transform=ccrs.PlateCarree(),
                    mec=mec, ms=ms, label='power plant', zorder=0)

    for i, key in enumerate(sources['source'].values, 1):

        source = sources.sel(source=key)

        lon = float(source['lon_o'])
        lat = float(source['lat_o'])
        text = str(source['label'].values)
        type_ = str(source['type'].values)

        if winds is not None:
            delta=0.044

            # use rotated pole coords to avoid distortion
            rlon, rlat = ddeq.misc.transform_coords(lon, lat,
                                                    ccrs.PlateCarree(),
                                                    domain.proj,
                                                    use_xarray=False)

            u = float(winds.sel(source=key)['U'])
            v = float(winds.sel(source=key)['V'])

            scaling = np.sqrt(u**2 + v**2)
            u = u / scaling
            v = v / scaling

            if np.isnan(scaling) or np.isclose(scaling, 0.0):
                ax.plot(lon, lat, 'o', color=color, transform=ccrs.PlateCarree(),
                        mec=mec, ms=ms, label='_none_', zorder=2)
            else:
                ax.arrow(rlon, rlat, delta * u, delta * v, shape='full',
                         head_width=2.0 * delta, head_length= 2.0 * delta,
                         length_includes_head=True, fc='k', ec='w',
                         lw=1, transform=domain.proj, zorder=2
                )
        else:
            marker = 'D' if type_ == 'city' else 'o'
            ax.plot(lon, lat, marker, color=color, transform=ccrs.PlateCarree(),
                    mec=mec, ms=ms, label='_none_', zorder=2)

        if ha is None:
            if winds is not None:
                align = 'left' if u < 0 else 'right'
            else:
                align = 'left'
        else:
            align = ha if isinstance(ha, str) else ha[i]

        t = ax.text(lon, lat, f'   {text}   ', va=va, ha=align, fontsize=size,
                    transform=ccrs.PlateCarree(), color=color, clip_on=True,
                    fontdict=fontdict, bbox=bbox)
        t.set_clip_on(True)

        if do_path_effect:
            t.set_path_effects([PathEffects.withStroke(linewidth=2.5,
                                                       foreground='w')])


def add_area(ax, data, curve, xa, xb, ya, yb, color='yellow',
             add_label=True, extra_width=5e3, lw=None,
             do_middle_lines=True, lds=None, crs=None):

    # polygon (outside) 
    x_left = []
    x_right = []
    y_left = []
    y_right = []

    for i in range(xa.size):

        # interpolate distance from arc(t)
        xmin = curve.arc2parameter(xa[i])
        xmax = curve.arc2parameter(xb[i])
        y = np.array([ya[i], yb[i]])

        # compute normals
        (x0, x1), (y0, y1) = curve.compute_normal(xmin, t=y)
        (x3, x2), (y3, y2) = curve.compute_normal(xmax, t=y)

        if i == 0:
            x_right.extend([x0, x1, x2])
            x_left.append(x0)
            y_right.extend([y0, y1, y2])
            y_left.append(y0)
        else:
            x_right.append(x2)
            x_left.append(x3)
            y_right.append(y2)
            y_left.append(y3)

        # plot box
        if do_middle_lines and i > 0:
            xx,yy = np.array([x0, x1]), np.array([y0, y1])
            add_curve(ax, xx, yy, ls='-', lw=lw,
                      color=color, label=None, alpha=0.5,
                     crs=crs)

    if len(xa) == 1:
        x_left.append(x3)
        y_left.append(y3)

    label = 'Plume polygons' if add_label else None
    xx = np.array(x_right + list(reversed(x_left)))
    yy = np.array(y_right + list(reversed(y_left)))
    add_curve(ax, xx, yy, ls='-', lw=lw,
              color=color, label=label, crs=crs)


def update_legend(legend, new_lines=None, new_labels=None):

    if new_lines is None or new_labels is None:
        new_lines = []
        new_labels = []

    ax = legend.axes
    handles, labels = ax.get_legend_handles_labels()

    handles += new_lines
    labels += new_labels

    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())

    legend.get_figure().canvas.draw()


def visualize(data, values, do_zoom=True, winds=None, show_clouds=True,
              alpha=None, vlim=(-2,2),
              legend_loc='upper right', simple_legend=True,
              add_multiple_sources=True, gas=None, scaling=None, 
              sources=None, names=None, names_align=None, figwidth=6.97,
              vmin=None, vmax=None, zoom_on=None,
              min_height=None, ax=None, cax=None, cmap=None, marker='+',
              markersize=3, domain=None, label=None, units=None,
              draw_gridlines=False,
             ):
    """
    Visualize detected plume. Image is "trace_gas"/"variable"

    Parameter
    ---------
    names : list of hot spot names that will added to the map
    names_align : horizontal alignment of name labels (default: 'left')

    Zoom on detected plumes
    -----------------------
    If `do_zoom` is True, zoom on detected plume(s) instead of showing full
    domain. If `zoom_on` is not None, only zoom on detected plume for given
    source name.


    show_clouds :: if true overlay cloudy pixels
    """
    if isinstance(data.time, str):
        time = pandas.Timestamp(data.time)
    else:
        time = pandas.Timestamp(data.time.values)

    if ax is None and cax is None:
        fig = None
    else:
        fig = ax, cax

    if isinstance(values, str):
        values = data[values]

    if scaling is not None:
        with xr.set_options(keep_attrs=True):
            values = scaling * values

    if winds is not None and "time" in winds.dims and winds.time.size > 1:
        winds = winds.sel(time=data.time, method="nearest")

    # show clouds?
    if show_clouds and 'clouds' in data:
        cloud_threshold = values.attrs.get('cloud_threshold', 1.0)
        clouds = data.clouds > cloud_threshold
        clouds.attrs['threshold'] = cloud_threshold
    else:
        clouds = None

    if gas is not None:
        if vmin is None and vmax is None:
            if gas == 'CO2':
                mean_bg = np.nanmean(values)

                if np.isnan(mean_bg):
                    mean_bg = 400

                vmin = round(mean_bg + vlim[0])
                vmax = round(mean_bg + vlim[1])

            elif gas == 'NO2':
                vmin = -2.5e15
                vmax = 10.0e15

        if units is None:
            units = values.attrs.get('units', 'a.u.')
            units = units.replace('-2', '$^{-2}$')

        if label is None:
            label = {
                'CO2': f'XCO$_2$ [{units}]',
                'NO2': f'NO$_2$ columns [{units}]' 
            }.get(gas, f'{gas} [{units}]')

    if domain is None:
        domain = ddeq.misc.Domain(
            name='',
            startlat=float(data.lat.min() - 0.5),
            stoplat=float(data.lat.max() + 0.5),
            startlon=float(data.lon.min() - 0.5),
            stoplon=float(data.lon.max() + 0.5)
        )

    lonc = data['lonc'] if 'lonc' in data else data['longitude_bounds']
    latc = data['latc'] if 'latc' in data else data['latitude_bounds']

    fig = make_level2_map(
        lonc, latc, values, vmin=vmin, vmax=vmax, truncate_cmap=False,
        label=label, clct=clouds, alpha=alpha,
        domain=domain, fig_size=figwidth, fig=fig, cmap=cmap
    )

    if ax is None:
        ax, cax = fig.get_axes()

    # if sources not provided use source array from dataset instead
    if sources is None and 'source' in data:
        sources = data.copy()

    if sources.source.ndim == 0:
        pass

    if names is not None:
        sources = sources.sel(source=names)

    if sources is not None:
        add_hot_spots(ax, color='black', mec='white', ms=5, ha=names_align,
                      size='small', sources=sources, do_path_effect=True,
                      winds=winds, domain=domain, time=time)

    # lines and labels
    if show_clouds and clouds is not None:
        label = 'Cloud fraction > %d%%' % (100*clouds.threshold)
        ax.plot(domain.startlon - 1, domain.startlat - 1, marker='s', mec='k',
                mfc='w', ls='', transform=ccrs.PlateCarree(), label=label)

    # detected plumes
    if ('detected_plume' in data and data.detected_plume is not None and
        np.sum(data.detected_plume) > 0):

        if np.ndim(data.detected_plume) == 3:
            plume = data.detected_plume.values.astype(bool)
        else:
            plume = data.detected_plume.values[:,:,np.newaxis].astype(bool)

        # plot multiple detections
        multiple_sources = plume.sum(2) > 1

        if add_multiple_sources:
            lon0 = data.lon.values[multiple_sources]
            lat0 = data.lat.values[multiple_sources]
            n_pixels = np.sum(multiple_sources)

            if n_pixels and markersize > 0:
                ax.plot(lon0, lat0, marker=marker, color='r', alpha=0.5,
                        ms=markersize, ls='', transform=ccrs.PlateCarree(),
                        label='Multiple sources (%d px)' % n_pixels)

        # plot other plumes
        if zoom_on is not None:
            if 'other_sources' in data:
                other_sources = data['other_sources'].values
            else:
                other_sources = data.detected_plume.any('source') \
                                & ~data.detected_plume.sel(source=zoom_on)

            if np.any(other_sources) and markersize > 0:
                lon0 = data.lon.values[other_sources]
                lat0 = data.lat.values[other_sources]

                ax.plot(lon0, lat0, marker=marker, color='r', alpha=0.5,
                        ms=markersize, ls='', transform=ccrs.PlateCarree(),
                        label='Other sources')

        # zoom on detected or specific plume detection
        for source in sources['source'].values:

            if zoom_on is not None and zoom_on != source:
                continue

            try:
                name = str(sources.sel(source=source)['label'].values)
                this = data.sel(source=source)
            except KeyError:
                continue

            lon0 = data.lon.values[this.detected_plume & ~multiple_sources]
            lat0 = data.lat.values[this.detected_plume & ~multiple_sources]
            n_pixels = lon0.size

            if sources is None and n_pixels == 0:
                continue

            if simple_legend:
                label = '%s (%d px)' % (name, n_pixels)
            else:
                label = 'detected plume (q = %.3f, n = %d)\nwith %d pixels' 
                label %= (
                    data.attrs['probability for z-value'],
                    data.attrs['size of neighborhood'],
                    n_pixels
                )

            if lon0.size > 0 and markersize > 0:
                ax.plot(lon0, lat0, marker=marker, mec='k',
                        ms=markersize, mfc='k', ls='',
                        transform=ccrs.PlateCarree(), label=label,
                        alpha=0.5 if zoom_on is None else 1.0)

    if do_zoom and ('detected_plume' in data or zoom_on is not None):
        if 'detected_plume' in data:
            if zoom_on is not None and 'source' in data.dims:
                data = data.sel(source=zoom_on)

            if np.ndim(data['detected_plume']) == 3:
                lon_o = data['lon_o'].values
                lat_o = data['lat_o'].values

                lon = np.concatenate([
                    lon_o,
                    data.lon.values[data['detected_plume'].any('source')].flatten()
                ])
                lat = np.concatenate([
                    lat_o,
                    data.lat.values[data['detected_plume'].any('source')].flatten()
                ])
            else:
                if 'lon_o' in data:
                    lon_o = data['lon_o'].values
                    lat_o = data['lat_o'].values
                else:
                    lon_o, lat_o, _ = misc.get_source_origin(source[0])

                lon = np.concatenate([
                    [lon_o - 0.5, lon_o + 0.5],
                    data.lon.values[data['detected_plume']].flatten()
                ])
                lat = np.concatenate([
                    [lat_o - 0.5, lat_o + 0.5],
                    data.lat.values[data['detected_plume']].flatten()
                ])

            rlon_0, rlat_0 = ddeq.misc.transform_coords(
                lon, lat, ccrs.PlateCarree(), domain.proj, use_xarray=False
            )

            xmin, xmax = np.nanmin(rlon_0), np.nanmax(rlon_0)
            ymin, ymax = np.nanmin(rlat_0), np.nanmax(rlat_0)

        else:
            source = sources.sel(source=zoom_on)
            lon_source, lat_source = ddeq.misc.get_source_location(source)
            offset_lat_lon=0.5
            res = domain.proj.transform_points(
                ccrs.PlateCarree(),
                np.array([lon_source - offset_lat_lon,
                          lon_source + offset_lat_lon]),
                np.array([lat_source - offset_lat_lon,
                          lat_source + offset_lat_lon])
            )
            xmin, xmax = res[:,0]
            ymin, ymax = res[:,1]


        # make figure at least 200 km high
        if min_height is None:
            min_height = 2.0 if zoom_on is None else 1.0

        if ymax - ymin < min_height:
            ymid = ymin + 0.5 * (ymax - ymin)
            ymin = ymid - 0.5 * min_height
            ymax = ymid + 0.5 * min_height

        # make figure have same aspect ratio as model domain
        aspect = domain.width / domain.height
        width = aspect * (ymax - ymin)
        height = aspect * (xmax - xmin)

        if width > (xmax - xmin):
            delta = (width - (xmax - xmin)) / 2.0
            xmin -= delta
            xmax += delta
        else:
            delta = (height - (ymax - ymin)) / 2.0
            ymin -= delta
            ymax += delta

        # shift limits when outside of domain boundary
        if xmin < domain.startlon:
            shift = domain.startlon - xmin
            xmin += shift
            xmax += shift

        if xmax > domain.stoplon:
            shift = xmax - domain.stoplon
            xmin -= shift
            xmax -= shift

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

    legend = ax.legend(loc=legend_loc, numpoints=1, markerscale=1.5,
                       fontsize='small')

    if draw_gridlines:
        add_gridlines(ax)

    return fig


def add_curve(ax, x, y, crs, label=None,
              color=None, ls='-', lw=None, marker='', mec=None, ms=None,
              alpha=None, zorder=None):
    """\
    Add a curve to map.
    """
    if crs is None:
        warnings.warn("To plot the polygons, a coordinate reference system (crs) must be provided.")

    lines = ax.plot(x, y, ms=ms, ls=ls, lw=lw, color=color, transform=crs,
                    label=label, marker=marker, mec=mec, alpha=alpha, zorder=zorder)
    return lines


def show_detected_plumes(data, curves, values, ld=None, add_polygons=True,
                         zoom_on=None, figwidth=6.97, ax=None, cax=None,
                         cmap=None, alpha=None, min_height=None,
                         add_multiple_sources=True, vmin=None, vmax=None,
                         show_clouds=True, winds=None, domain=None,
                         add_origin=False, marker='+', markersize=3,
                         label=None, do_zoom=True,
                         crs=None, gas=None, dmin=None, delta=None,
                         legend_loc='upper left', add_upstream_box=None,
                         polygon_color='yellow', do_middle_lines=True):
    """
    Show detected plumes in swath and add curves and control polygons if available.
    """
    #FIXME: plot polygons does not work if crs is not defined

    first = True # first time adding polygons

    fig = visualize(
        data, values, do_zoom=do_zoom, show_clouds=show_clouds,
        legend_loc=legend_loc, gas=gas, zoom_on=zoom_on, figwidth=figwidth,
        ax=ax, cax=cax, cmap=cmap, alpha=alpha, min_height=min_height,
        vmin=vmin, vmax=vmax, add_multiple_sources=add_multiple_sources,
        winds=winds, domain=domain, marker=marker, markersize=markersize,
        label=label, draw_gridlines=True
    )

    if ax is None:
        ax, cax = fig.get_axes()

    for i, source in enumerate(data.source.values):

        if zoom_on is not None and source != zoom_on:
            continue

        d = data.sel(source=source)

        if source in curves and curves[source] is not None:

            plume = d['detected_plume']

            pixel_size = np.sqrt(np.mean(data['pixel_area']))
            pixel_size = int(round(float(pixel_size), -2)) # round to next 100m

            if ld is None:
                source_type = str(d['type'].values)
                xa, xb, ya, yb = ddeq.misc.compute_polygons(
                    d, source_type=source_type, dmin=dmin, delta=delta,
                    add_upstream_box=add_upstream_box,
                    pixel_size=pixel_size
                )
            else:
                xa, xb = ld[source].xa, ld[source].xb
                ya, yb = ld[source].ya, ld[source].yb

            # don't draw curves for overlapping plumes
            if ddeq.misc.has_multiple_sources(data, source):
                continue

            x = d['x'].values[plume]
            y = d['y'].values[plume]
            curve = curves[source]

            try:
                tmax = curve.arc2parameter(xb[-1])
            except IndexError:
                tmax = curve.t_o + 10e3

            t = np.linspace(curve.t_o, tmax)

            add_curve(ax, *curve(t=t), zorder=10, crs=crs,
                      color='black', label='Center lines' if first else None)

            if add_polygons:

                # polygon upstream
                add_area(ax, d, curve, xa[:1], xb[:1], ya[:1], yb[:1],
                         add_label=first, lw=1, crs=crs,
                         do_middle_lines=do_middle_lines,
                         color=polygon_color)

                # polygons downstream
                add_area(ax, d, curve, xa[1:], xb[1:], ya[1:], yb[1:],
                         add_label=False, lw=1, crs=crs,
                         do_middle_lines=do_middle_lines, color=polygon_color)

            if add_origin:
                add_curve(ax, curve.x0, curve.y0, marker='D', crs=crs,
                          ls='', color=polygon_color, mec='k', ms=5,
                          label='Origin ($x_o$, $y_o$)' if first else None)
            first = False

    return fig


def add_text(gases, data, result, title=None):
    """
    this - xr.Dataset with remote sensing image data
    result - xr.Dataset with result from CSF method
    """
    time = pandas.Timestamp(data.time.values)
    plume_age, plume_length = ddeq.misc.compute_plume_age_and_length(result)
    plume_size = np.nansum(data.detected_plume)

    text = []
    detection_gas = data.attrs['trace_gas']

    if title is not None:
        text.append(title)

    text.append('\nInstrument:')
    text.append(f'• Time: {time.round(freq="s")}')

    for gas in gases:
        noise = data[gas].attrs['noise_level']
        units = data[gas].attrs['units']
        text.append(f'• {sub_numbers(gas)} noise: {noise:g} {units}')

    text.append('')
    text.append('Plume detection:')
    text.append(f'• Trace gas: {sub_numbers(detection_gas)}')
    text.append(f'• Plume size: {plume_size:d} px')
    text.append(f'• Plume length: {plume_length:.1f} km')
    text.append(f'• Plume maximum age: {plume_age:.1f} h')

    text.append('\nWind:')
    text.append(f'• Mean wind: {np.mean(result.wind_speed):.1f} m s$^{{-1}}$, '
                f'{scipy.stats.circmean(result.wind_direction, high=360):.0f}°')

    angle = scipy.stats.circmean(result['angle_between_curve_and_wind'], high=360)
    text.append(f'• Angle between curve and wind: {angle:.0f}°')

    text.append('\nEstimated emissions:')
    for gas in gases:
        if gas == 'NO2':
            gas = 'NOx'
        q = ddeq.misc.kgs_to_Mtyr(result[f'{gas}_emissions'])
        text.append(f'• {sub_numbers(gas)} emissions: {q:.3g} Mt/a')

        if f'{gas}_decay_time' in result:
            tau = result[f'{gas}_decay_time'] / 3600
            text.append(f'• {sub_numbers(gas)} decay time: {tau:.1f} h')

    # TODO true emissions

    return '\n'.join(text)


def add_lines(ax, edgecolor='k'):
    ax.coastlines(resolution='10m', color=edgecolor, linewidth=1.0)
    lines = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_boundary_lines_land',
        scale='10m',
    )
    ax.add_feature(lines, edgecolor=edgecolor, facecolor='none', linewidth=1.0)

    lines = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='10m',
    )
    ax.add_feature(lines, edgecolor=edgecolor, facecolor='none', linewidth=0.5)


def plot_along_plume(ax, gas, ld, figwidth=6.97):
    """
    Plot along plume fluxes from CSF results `ld`/
    """
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(figwidth, 4))
    else:
        fig = ax.get_figure()

    if gas in ['NO2', 'NOx', 'NOX']:
        factor = ddeq.misc.kgs_to_Mtyr(1.0) * 1e3
        units = 'kt/a'
    else:
        factor = ddeq.misc.kgs_to_Mtyr(1.0)
        units = 'Mt/a'

    if gas == 'NO2' and 'NOx_flux' in ld:
        ax.errorbar(ld['along'] / 1e3, factor * ld[f'NOx_flux'],
                    factor * ld[f'NOx_flux_precision'],
                    marker='o', ms=4, color='tab:blue', capsize=2,
                    ls='', mfc='none', label='NO$_x$ estimates')

        ax.errorbar(ld['along'] / 1e3, factor * ld[f'NOx_flux'] / ld['f'],
                    factor * ld[f'NOx_flux_precision'] / ld['f'],
                    marker='s', ms=4, color='tab:red', capsize=2,
                    ls='', mfc='none', label='NO$_2$ estimates')
    else:
        ax.errorbar(ld['along'] / 1e3, factor * ld[f'{gas}_flux'],
                    factor * ld[f'{gas}_flux_precision'],
                    marker='o', ms=4, color='tab:blue', capsize=2,
                    ls='', mfc='none', label=f'{sub_numbers(gas)} estimates')

    # TODO: NO2 and NOx
    if gas == 'NO2':
        Q = ld[f'NOx_emissions']
        Q_std = ld[f'NOx_emissions_precision']
        tau = ld.get(f'NOx_decay_time', np.nan)
        tau_std = ld.get(f'NOx_decay_time_precision', np.nan)
    else:
        Q = ld[f'{gas}_emissions']
        Q_std = ld[f'{gas}_emissions_precision']
        tau = ld.get(f'{gas}_decay_time', np.nan)
        tau_std = ld.get(f'{gas}_decay_time_precision', np.nan)

    u = ld['wind_speed']
    u_std = ld['wind_speed_precision']

    x = ld['along_hr']

    if gas == 'NO2':
        y = factor * ld[f'NOx_flux_fit']
    else:
        y = factor * ld[f'{gas}_flux_fit']

    label = 'Flux fit'
    ax.plot(x / 1e3, y, label=label, color='tab:blue', ls='-')

    # labels
    if gas == 'NO2':
        gas = 'NO$_x$'
    else:
        for l in '1234Xx':
            gas = gas.replace(l, f'$_{l}$')

    ax.set_ylabel(f'{sub_numbers(gas)} flux [{units}]')
    ax.set_xlabel('Along-plume distance [km]')
    ax.grid(True)
    ax.legend(fontsize='small', ncol=1)

    right = ld['along'].max() / 1e3 + 5.0
    xticks = np.array( sorted(set(list(ld.xa.values) 
                                  + list(ld.xb.values))) ) / 1e3

    ax.set_xticks(np.round(xticks))
    ax.set_xlim(xticks[0], xticks[-1])

    # prevent crowded xaxis in case of long plume
    if len(xticks) >= 20:
        for text in ax.get_xticklabels()[1::2]:
            text.set_visible(False)

    return fig


def plot_across_section(polygon, gases, method='sub-areas',
                        show_true=False, add_errors=True, ax=None,
                        legend='standard', max_values=None):
    """
    Plot across plume concentrations and line densities from means of
    sub-polygons or curve fits.
    """
    exponent2mass = {
        +0: 'k',
        -3: '',
        -6: 'm',
        -9: 'µ',
        -12: 'n',
    }

    axes = []
    lines = []

    if ax is None:
        figsize = plt.rcParams['figure.figsize']
        figsize = [figsize[0], figsize[1] * 2 / 3]
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()

    if max_values is None:
        max_values = [np.abs(np.nanmax(polygon[gas])) for gas in gases]

    for i, gas in enumerate(gases):

        if i == 1:
            ax = ax.twinx()

        axes.append(ax)

        exponent = np.ceil(np.log10(max_values[i]))
        exponent = exponent - exponent % 3
        scaling = 10 ** np.negative(exponent)

        suffix = exponent2mass.get(exponent, 'k')
        fmt = f'%.0f$\\pm$%.0f$\\,${suffix}g$\\,$m$^{-1}$'

        figsize = plt.rcParams['figure.figsize']
        figsize = [figsize[0], figsize[1] * 2 / 3]

        y = polygon['y']
        detection = polygon['is_plume'].values

        c1 = polygon[gas]
        c1_std = polygon[f'{gas}_std']

        label = sub_numbers(gas)

        color = ['tab:blue', 'tab:red'][i]
        marker = ['o', 's'][i]

        if add_errors:
            lines.append(ax.errorbar(y/1e3, scaling  * c1, scaling * c1_std,
                                     color=color, mfc='none',
                                     marker=marker, ms=5, ls='',
                                     label=label)
                        )
        else:
            lines += ax.plot(y/1e3, scaling * c1, marker=marker, color=color,
                              mfc='none', ms=5, label=label)

        if method == 'sub-areas':
            ss = polygon['subpolygons']
            area_means = scaling * polygon[f'{gas}_sub']
            area_means_std = scaling * polygon[f'{gas}_std_sub']

            mass_means = polygon[f'{gas}_line_density']
            mass_means_std = polygon[f'{gas}_line_density_precision']

            lines +=ax.plot(ss/1e3, area_means, lw=2,
                            ds='steps-mid', color='black',
                            ls=['-', '--'][i],
                            label='Sub-area means (%s)' % fmt % (mass_means,
                                                                 mass_means_std))
        else:
            s, co2 = ddeq.misc.calculate_gaussian_curve(gas, polygon)

            ls = ['-', '--'][i]
            lines += ax.plot(s/1e3, scaling * co2, 'k', ls=ls, lw=2, label=label)

        gas_latex = gas.replace('2', '$_2$').replace('4', '$_4$')
        ax.set_ylabel(f'{gas_latex} [{suffix}g m$^{{-2}}$]', color=color)
        ax.grid(False)
        ax.set_xlabel('Across-plume direction [km]')
        ax.tick_params(axis='y', colors=color)

    ncol = 1 if legend == 'simple' else 2
    loc = 'upper right' if legend == 'simple' else 0

    axes[0].legend(lines, [l.get_label() for l in lines], fontsize='small',
                   ncol=ncol, loc=loc)

    # align zeros on both y-axis
    if len(axes) == 2:
        y0 = axes[0].get_ylim()
        y1 = axes[1].get_ylim()    

        l_top = y0[1] / (y0[1] - y0[0])
        l_bottom = y0[0] / (y0[1] - y0[0])

        r_top = y1[1] / (y1[1] - y1[0])
        r_bottom = y1[0] / (y1[1] - y1[0])

        top = max(l_top, r_top)
        bottom = min(l_bottom, r_bottom)

        axes[0].set_ylim(bottom * (y0[1] - y0[0]), top * (y0[1] - y0[0]))
        axes[1].set_ylim(bottom * (y1[1] - y1[0]), top * (y1[1] - y1[0]))

    return fig, axes



def plot_gauss_result(data, results, sources, gas, curves, domain=None,
                      crs=None, vmin=None, vmax=None):
    """
    Plot results from Gaussian plume inversion.

    Parameters
    ----------
    data : xr.Dataset
        Remote sensing dataset

    results : xr.Dataset
        Results from Gaussian plume inversion.

    sources : list
        List of names of sources in `data` and `results`.

    gas : str
        Name of gas (e.g., "CO2" or "NO2").

    curves : dict
        Dictionary with center curves.

    domain : ddeq.misc.Domain
        The plotting region. If given as None, domain expand will be created
        from `lon` and `lat` variable in `data`.

    crs : cartopy.crs
        The coordinate reference system used for the center curves.

    vmin : float
        Minimum value on colorbar (in kg m-2).

    vmax : float
        Maximum value on colorbar (in kg m-2).

    Returns
    -------
    plt.figure
    """

    if domain is None:
        domain = ddeq.misc.Domain(
                name='',
                startlat=data.lat.min() - 0.2,
                stoplat=data.lat.max() + 0.2,
                startlon=data.lon.min() - 0.2,
                stoplon=data.lon.max() + 0.2,
        )

    if isinstance(sources, str):
        sources = [sources]

    these = data.sel(source=sources)
    results = results.sel(source=sources)

    fig = plt.figure(figsize=(11,3))
    ax1 = fig.add_axes([0.01, 0.02, 0.285, 0.90], projection=domain.proj)
    ax2 = fig.add_axes([0.30, 0.02, 0.285, 0.90], projection=domain.proj)
    ax3 = fig.add_axes([0.59, 0.02, 0.285, 0.90], projection=domain.proj)
    cax = fig.add_axes([0.88, 0.048,0.03, 0.906])

    # --- Subplot 1
    ddeq.vis.visualize(these, f'{gas}_minus_estimated_background_mass', gas=gas,
                       domain=domain, winds=None, do_zoom=True, zoom_on=sources[0],
                       show_clouds=True,
                       vmin=vmin, vmax=vmax, markersize=0,
                       label='column density [kg m$^{-2}$]', ax=ax1, cax=cax)
    ax1.set_title('Data')

    # --- Subplot 2
    model_values = these[f'{gas}_plume_model_mass'].sum('source')

    ddeq.vis.visualize(these, model_values, gas=gas, domain=domain,
                       winds=None, do_zoom=True, zoom_on=sources[0],
                       show_clouds=True,
                       vmin=vmin, vmax=vmax, markersize=0,
                       label='column density [kg m$^{-2}$]', ax=ax2, cax=cax, names=sources);

    Q = results.sel(source=sources[0]).get(f'{gas}_estimated_emissions', np.nan)
    tau = results.sel(source=sources[0]).get(f'{gas}_decay_time', np.nan)
    ax2.set_title(f'Model (Q = {float(Q):.3g} kg/s, $\\tau$ = {float(tau/3600):.1f} h)')

    # --- Subplot 3
    diff = these[f'{gas}_minus_estimated_background_mass'] - model_values
    ddeq.vis.visualize(data, diff, gas=gas, domain=domain, winds=None, do_zoom=True,
                       zoom_on=sources[0], show_clouds=True, markersize=0,
                       vmin=vmin, vmax=vmax,
                       label='column density [kg m$^{-2}$]', ax=ax3, cax=cax, names=sources);
    ax3.set_title('Data-Model mismatch')

    for source in sources:

        # old curve
        curve = curves[source]
        xp, yp = curve(t=np.linspace(curve.t_o, curve.tmax, 100)) 
        x, y = ddeq.misc.transform_coords(xp, yp, crs, ccrs.PlateCarree(), use_xarray=False)
        ax1.plot(x, y, 'k', transform=ccrs.PlateCarree())

        # new curve
        for ax in [ax1, ax2, ax3]:
            xp, yp = results[f'{gas}_curve'].sel(source=source).T
            x, y = ddeq.misc.transform_coords(xp, yp, crs, ccrs.PlateCarree(), use_xarray=False)
            ax.plot(x, y, 'r', transform=ccrs.PlateCarree())

    return fig


def plot_csf_result(gases, data, winds, line_densities, curves,
                    source, domain=None, crs=None,
                    scalings=None, vmins=None, vmaxs=None):
    """
    Plot results from cross sectional flux method.

    Parameters
    ----------
    gases : list of str
        List of maximum two gases.

    data : xr.Dataset
        Remote sensing dataset.

    winds : xr.Dataset
        Wind dataset at each source.

    line_densities : xr.Dataset
        Results from cross sectional flux method.

    curves : dict
        Dictionary with center curves.

    source : str
        Name of sources in `data` and `results`.

    domain : ddeq.misc.Domain
        The plotting region. If given as None, domain expand will be created
        from `lon` and `lat` variable in `data`.

    crs : cartopy.crs
        The coordinate reference system used for the center curves.

    scalings : list of floats
        Scaling applied to `data[gas]` for plotting.

    vmins : list of floats
        Minimum values on colorbar for given gases.

    vmaxs : list of floats
        Maximum values on colorbar for given gases.

    Returns
    -------
    plt.figure
    """

    if 'NOx' in gases or 'NOX' in gases:
        print('Note: provide "NO2" instead of "NOx".')
    time = pandas.Timestamp(data.time.values)

    if domain is None:
        domain = ddeq.misc.Domain(
                name='',
                startlat=data.lat.min() - 0.2,
                stoplat=data.lat.max() + 0.2,
                startlon=data.lon.min() - 0.2,
                stoplon=data.lon.max() + 0.2,
        )

    # define margins for the subplots
    ax_left = 0.07
    ax_right = 0.95
    ax_bottom = 0.12
    ax_top = 0.93

    with plt.style.context({'font.size': 10}):
        fig_scaling = 1.0
        figsize= (13.94 * fig_scaling, 7.45 * fig_scaling)
        aspect = figsize[0] / figsize[1] # used to ensure eq spacing in h and v direction

        # create canvas for the subfigures
        fig = plt.figure(figsize=figsize)
        subfigs = fig.subfigures(2, 2, width_ratios=[2, 3], height_ratios=[1,1])

        # create subfigure for along plume
        axs_lower_right = subfigs[1,1].subplots(len(gases), 1, sharex=True)
        axs_lower_right = np.atleast_1d(axs_lower_right)

        for g, gas in enumerate(gases):

            vmin = None if vmins is None else vmins[g]
            vmax = None if vmaxs is None else vmaxs[g]
            scaling = 1.0 if scalings is None else scalings[g]

            # set titles
            subfigs[g, 0].suptitle('(%s)' % 'ab'[g])
            subfigs[0, 1].suptitle('(%s)' % 'bc'[g])
            subfigs[1, 1].suptitle('(%s)' % 'cd'[g])

            # plot satellite image(s)
            axs_left = subfigs[g,0].add_subplot(111, projection=domain.proj)

            axs_left.set_aspect('equal', adjustable='box')
            axs_left.set_xlim(domain.startlon, domain.stoplon)
            axs_left.set_ylim(domain.startlat, domain.stoplat)
            add_lines(axs_left)

            with xr.set_options(keep_attrs=True):
                scaled_data = scaling * data[gas]

            sat = show_detected_plumes(data, curves, scaled_data,
                                       gas=gas,
                                       ld=line_densities,
                                       add_polygons=True,
                                       winds=winds,
                                       domain=domain,
                                       zoom_on=source,
                                       ax=axs_left, cax=None,
                                       vmin=vmin, vmax=vmax,
                                       crs=crs)

            # adjust margins
            subfigs[g, 0].subplots_adjust(left=0.0,
                                          right=0.93,
                                          bottom=ax_bottom,
                                          top=ax_top)

        # plot across plume
        axs_upper_right = subfigs[0, 1].subplots(2, 3, sharex=True)

        n = line_densities[source].along.size

        if n <= 6:
            alongs = np.arange(n)
        else:
            alongs = [0, 1, 2, 3, n-2, n-1]

        across_axes = dict((gas, []) for gas in gases)
        max_values = [np.abs(np.nanmax(line_densities[source][gas]))
                      for gas in gases]

        for j, (i, ax) in enumerate(zip(alongs, axs_upper_right.flat)):
            if 0 <= i < line_densities[source].along.size:
                polygon = line_densities[source].isel(along=i)


                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore',
                                            r'All-NaN (slice|axis) encountered')

                    _, axes2 = plot_across_section(polygon, gases=gases, ax=ax,
                                                   max_values=max_values,
                                                   method=polygon.method,
                                                   show_true=False,
                                                   add_errors=True,
                                                   legend='simple')

                    for gas, ax2 in zip(gases, axes2):
                        across_axes[gas].append(ax2)

                    # modify axis labels and ticks
                    if len(axes2) == 2:
                        if j not in [2,5]:
                            axes2[1].set_ylabel('')
                            axes2[1].set_yticks([])

                ax.text(0.01, 0.98, '%d-%d km' % (polygon.xa/1e3, polygon.xb/1e3),
                            va='top', ha='left', transform=ax.transAxes)

                if j in [0,1,2]:
                    ax.set_xlabel('')

                if j not in [0,3]:
                    ax.set_yticklabels([])
                    ax.set_ylabel('')

                if j != 5:
                    legend = ax.get_legend()

                    if legend is not None:
                        legend.remove()

        for gas in gases:
            bottom = min(ax.get_ylim()[0] for ax in across_axes[gas])
            top = max(ax.get_ylim()[1] for ax in across_axes[gas])

            for ax in across_axes[gas]:
                ax.set_ylim(bottom, top)

        # adjust margins
        right = 0.65 if len(gases) == 2 else ax_right
        subfigs[0, 1].subplots_adjust(left=ax_left,
                                      right=ax_right,
                                      bottom=ax_bottom,
                                      top=ax_top,
                                      wspace=0.05, hspace=0.05*aspect)

        subfigs[1, 1].subplots_adjust(left=ax_left,
                                      right=right,
                                      wspace=0.15, hspace=0.15)

        # plot along plume
        for a, ax in enumerate(axs_lower_right):
            plot_along_plume(ax, gases[a], line_densities[source])

            if len(gases) == 2 and a == 0:
                    ax.set_xlabel('')

        # add retrieval information
        text = add_text(gases, data.sel(source=source), line_densities[source])

        if len(gases) == 2:
            subfigs[1, 1].text(0.67, 0.97, text, va='top', linespacing=1.1)
        else:
            subfigs[1, 0].text(0.12, 0.97, text, va='top', linespacing=1.1)

        return fig


def visualize_lcsf_plume(data, results, gas, sources, source_name,
                         domain=None, ax=None, cax=None, line_color='b',
                         do_zoom=True, vmin=None, vmax=None):
    """\
    Make a map showing `gas` image around `source_name`. Draw line used for
    computing the line densities with the LCSF method. This requires that
    `all_diags` was set to True for `ddeq.lcsf.estimate_emissions`.
    """

    fig = visualize(data, data[gas], gas=gas, domain=domain,
                    sources=sources, winds=None,
                    do_zoom=do_zoom, zoom_on=source_name,
                    ax=ax, cax=cax, draw_gridlines=True,
                    vmin=vmin, vmax=vmax,
                   )

    if ax is None and cax is None:
        ax, cax = fig.axes

    if f'{gas}_alongw_line_pts' not in results:
        raise ValueError(
            '`ddeq.lcsf.estimate_emissions` needs `all_diags = True` to '
            'include fields in results required for this functions.'
        )

    if results.source.ndim > 0:
        results = results.sel(source=source_name)

    llat = results[f'{gas}_alongw_line_pts'][:,0]
    llon = results[f'{gas}_alongw_line_pts'][:,1]

    ax.plot(llon, llat, c=line_color, transform=ccrs.PlateCarree())

    orth_llat = results[f'{gas}_acrossw_line_pts'][:,:,0]
    orth_llon = results[f'{gas}_acrossw_line_pts'][:,:,1]

    for iedge in range(2):
        ax.plot(orth_llon[iedge,:], orth_llat[iedge,:], c=line_color,
                transform=ccrs.PlateCarree())

    #Plotting fit pts
    tmp_lat_arr = results[f'{gas}_lat_lon_fit_pts'][:,0]
    tmp_lon_arr = results[f'{gas}_lat_lon_fit_pts'][:,1]

    for iopt in range(len(tmp_lat_arr)):
        hh, = ax.plot(tmp_lon_arr[iopt], tmp_lat_arr[iopt], ls='',
                      transform=ccrs.PlateCarree(), ms=3, marker='+',
                      color='k')

    return fig



def plot_lcsf_result(source_name, results, data, sources, gases,
                     true_emis=None, domain=None, vmin=None, vmax=None):
    '''\
    Plot results from the light cross-sectional method (LCSF) method for a
    given source.

    Parameters
    ----------
    source_name : str
        Name of the source whose results are shown

    results : xr.Dataset
        Result dataset from the LCSF method.

    data : xr.Dataset
        Remote sensing data

    gases : str or list of str
        List of trace gases.

    true_emis : dict, optional
        If not None should be a dictionary with true emissions for given gases.

    domain : ddeq.misc.Domain, optional
        The plotting region. If given as None, domain will be created from `lat`
        and `lat` variable in `data`.

    vmin : float, optional
        Minimum value for colorbar.

    vmax : float, optional
        Maximum value for colorbar.

    Returns
    -------
    plt.figure
    '''
    if isinstance(gases, str):
        gases = [gases]

    if domain is None:
        domain = ddeq.misc.Domain(
                name='',
                startlat=data.lat.min() - 0.2,
                stoplat=data.lat.max() + 0.2,
                startlon=data.lon.min() - 0.2,
                stoplon=data.lon.max() + 0.2,
        )

    if source_name not in results.source:
        print(f'Source {source_name} has not been estimated')

    results = results.sel(source=source_name)

    if f'{gases[0]}_alongw_line_pts' not in results:
        print('Information on line densities required for plotting. '
              'Set all_diags=True in `ddeq.lcs.estimate_emissions`.')

    nrows = len(gases) # number of subplots
    ncol = 3

    #Dimensions of the subplots
    height_gap = 0.05
    width_gap = 0.07
    bottom_offset = 0.1
    top_offset = 0.08
    left_offset = 0.03
    right_offset = 0.03
    cb_width = 0.01
    cb_gap = 0.01

    rel_width = (1.-left_offset-right_offset-ncol*(cb_gap+cb_width)-(ncol-1)*width_gap)/ncol
    rel_height = (1.-top_offset-bottom_offset-(nrows-1)*height_gap)/nrows

    #Plotting options
    fs_label = 19
    fs_ax_label = 14
    fs_title = 14
    fs_leg = 10
    fs_suptitle = 18
    fs_cb = 1

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b",
              "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

    n_colors = len(colors)

    figw = 17
    figh = {1: 5, 2: 9}[nrows]

    fig = plt.figure(num=1, figsize=(figw,figh), facecolor='w', edgecolor='k',
                     frameon=False)

    for i, gas in enumerate(gases):

        #  Plotting l2 data maps
        icol = 1

        bottom = bottom_offset + (nrows - i - 1 ) * (rel_height + height_gap)
        left = left_offset + (icol - 1) * (rel_width + width_gap + cb_width + cb_gap)

        ax = fig.add_axes([
            left, bottom, rel_width, rel_height],
            projection=domain.proj
        )
        ax.set_aspect('equal', adjustable='box')
        cax = fig.add_axes([left + rel_width + cb_gap, bottom,
                            cb_width, rel_height])

        visualize_lcsf_plume(data, results, gas, sources, source_name,
                             domain=domain, ax=ax, cax=cax, line_color='b',
                             do_zoom=True, vmin=vmin, vmax=vmax)

        #  Plotting line densities
        icol=2

        bottom = bottom_offset + (nrows - i - 1) * (rel_height + height_gap)
        left = left_offset + (icol - 1) * (rel_width + width_gap + cb_width + cb_gap)

        ax = fig.add_axes([left, bottom, rel_width, rel_height])

        centered_dists = results[f'{gas}_centered_distances'].data
        popts = results[f'{gas}_popts'].data
        slice_fit_pts_index = results[f'{gas}_slice_fit_pts_index'].data
        n_lds = popts.shape[0]

        # We plot only one line density
        i_ld = 0
        tmp_centered_dists = centered_dists[i_ld][np.isfinite(centered_dists[i_ld])]

        if len(tmp_centered_dists) == 0:
            ax.axis('off')
            ax.text(0.5, 0.5,f'NO {gas} ESTIMATES', ha='center', va='top',
                    transform=ax.transAxes, fontsize=22, color='k')
            continue

        ij_slice = slice_fit_pts_index[i_ld,:]
        tmp_data_slice = data[gas].data[ij_slice]
        tmp_data_slice = tmp_data_slice[np.isfinite(tmp_data_slice)]

        ax.plot(tmp_centered_dists, tmp_data_slice, ls='none', marker='o',
                markersize=5, mfc='none', mec=colors[i_ld % n_colors])

        # fitted function
        xx = np.sort(tmp_centered_dists)
        popt = popts[i_ld]
        fit_obs = ddeq.functions.gauss(xx, *popt)

        tmp_hh = ax.plot(xx, fit_obs, color=colors[i_ld % n_colors], lw=2)[0]

        # Quality of the fit
        R2 = np.corrcoef(fit_obs,
                         tmp_data_slice[np.argsort(tmp_centered_dists)])[0,1]**2

        tmp_emis = np.round(float(
            results[f'{gas}_estimated_emissions'][i_ld].data), 1)
        tmp_std_emis = np.round(float(
            results[f'{gas}_estimated_emissions_precision'][i_ld].data), 1)

        tmp_dist = float(results[f'{gas}_dist_from_src'].data[i_ld])
        units = results[f'{gas}_estimated_emissions'][i_ld].unit

        text = '\n'.join([
            f'Distance from source {tmp_dist:.1f} km',
            f'R2 = {R2:.2f}',
            f'Estimated Emissions: {tmp_emis} $\\pm$ {tmp_std_emis} {units}',
            '' if true_emis is None else f'True emissions: {true_emis[gas]:.1f} {units}'
        ])

        ax.text(0.03, 0.98, text, ha='left', va='top',
                transform=ax.transAxes, fontsize=10, color='k')

        xmax = +25
        xmin = -25

        ax.set_xlim([xmin, xmax])
        xticks = np.arange(xmin, xmax + 5, 5)
        ax.set_xticks(xticks, xticks)

        fs_ax_label = 12

        if i == nrows - 1:
            ax.set_xlabel('Centered Distances (km)', fontsize=fs_ax_label)
        ax.tick_params(axis='both', labelsize=10)

        scale_fctr = 0.3

        ymin = np.min(tmp_data_slice)
        ymax = np.max(tmp_data_slice)

        ax.set_ylim([ymin, ymax + scale_fctr * (ymax - ymin)])
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")

        if gas == 'NO2':
            ylab_str = 'NO$_2$ column [10$^{15}$ molecules per cm$^2$]'

        if gas =='CO2':
            ylab_str = 'XCO$_2$ [ppm]'

        ax.set_ylabel(ylab_str, fontsize=fs_ax_label)

        #  Plotting Emission estimates depending on their along-wind distance from the source
        icol=3

        bottom = bottom_offset + (nrows - i - 1) * (rel_height + height_gap)
        left = left_offset + (icol - 1) * (rel_width + width_gap + cb_width + cb_gap)

        ax = fig.add_axes([left, bottom, rel_width, rel_height])

        emis_estim = results[f'{gas}_estimated_emissions']
        std_emis_estim = results[f'{gas}_estimated_emissions_precision']
        dist_from_src = results[f'{gas}_dist_from_src']

        emis_estim = emis_estim[np.isfinite(emis_estim)]
        n_estim = len(emis_estim)
        std_emis_estim = std_emis_estim[:n_estim]

        xx = dist_from_src[:n_estim]
        hh = ax.errorbar(xx, emis_estim, std_emis_estim, color=colors[0],
                         ls='none', marker='o', label='Along-plume estimates')
        xmin = 0
        xmax = np.max(xx) + 1
        ymax = np.max(emis_estim + std_emis_estim)

        hh = ax.plot([xmin,100], 2 * [np.median(emis_estim)], lw=2,
                     color=colors[0], label='Median estimate')[0]

        if true_emis is not None:
            hh = ax.plot([xmin,xmax], 2 * [true_emis[gas]], lw=2,
                         color='k', label='True emission')
            ymax = max([ymax, true_emis[gas]])

        #Legend
        ll = ax.legend(prop=dict(size=fs_leg), framealpha=0.5,
                       labelspacing=0.9, loc=0)
        #Axis set-up
        if gas == 'NO2':
            gas_str = 'NO$_x$'
        if gas=='CO2':
            gas_str = 'CO$_2$'

        text_str = f'{gas_str} Emissions [{units}]'
        ax.set_ylabel(text_str, fontsize=fs_ax_label)
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
        ax.set_ylim(top=ymax+10)

        ax.set_xlim([xmin, xmax])
        if i == nrows-1:
            ax.set_xlabel('Along-plume distance [km]', fontsize=fs_ax_label)

    #  Suptitle
    date = pandas.Timestamp(data.time.values)
    plt.suptitle(date.strftime(f'{source_name} %Y-%m-%d'),
                 fontsize=fs_suptitle)


    return fig




def visualize_integrated_wind(fig, winds, threshold, domain):
    """
    Visualize integrated winds in figure.
    """
    ax, cax = fig.get_axes()

    if winds.direction.size==1:
        return fig
    else:
        for i in range(winds.direction.size):

            u = float(winds.U.values[i])
            v = float(winds.V.values[i])

            scaling = np.sqrt(u**2 + v**2)
            u = u / scaling
            v = v / scaling
            delta = 0.02

            ec = "r" if abs(winds.angle_between_curve_and_wind.values[i]) > threshold else "w"

            ax.arrow(winds.lon.values[i], winds.lat.values[i],
                     delta * u, delta * v, shape='full',
                     head_width=2.0 * delta, head_length= 2.0 * delta,
                     length_includes_head=True, fc='k', ec=ec,
                     lw=1, transform=domain.proj, zorder=10)

    return fig



def plot_divergence_maps(NOx_div, CO2_div, center_lon, center_lat, lon_km=50.0,
                         lat_km=50.0, grid_reso=50.0, sources=None, ms=5,
                         fontsize='x-large', cbar_fraction=0.051):
    """
    Plot results from divergence method.

    Parameters
    ----------
    NOx_div : np.array
        NOx divergence map (in g/m2/s)

    CO2_div : np.array
        CO2 divergence map (in g/m2/s).

    center_lon : float
        Longitude of source.

    center_lat : float
        Latitude of source.

    lon_km : float, optional
        The east-west extension of the grid around a source in kilometers.

    lat_km : float, optional
        The south-north extension of the grid around a source in kilometers.

    grid_reso : float, optional
        The resolution of the grid in kilometers.

    sources : xr.Dataset
        Dataset with source locations.

    ms : int
        Size of point source markers.

    fontsize : str, optional
        Font size in plot.

    cbar_fraction : float, optional
        Fraction of colorbar.

    Returns
    -------
    plt.Figure
    """
    longrid, latgrid, _, _ = ddeq.misc.generate_grids(center_lon, center_lat,
                                                      lon_km+grid_reso/2,
                                                      lat_km+grid_reso/2,
                                                      grid_reso)

    request = cimgt.OSM()
    #request = cimgt.QuadtreeTiles()
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(16, 10),
                                   subplot_kw=dict(projection=request.crs))
    # plot NOx divergence
    extent = [np.min(longrid)-0.2, np.max(longrid)+0.2,
              np.min(latgrid)-0.2, np.max(latgrid)+0.2]
    ax1.set_extent(extent)
    ax1.add_image(request, 6)

    if sources is not None:
        ddeq.vis.add_hot_spots(ax1, sources=sources, size=fontsize, ms=ms)
    c1 = ax1.pcolormesh(longrid, latgrid, NOx_div,
                        shading='auto',
                        cmap=plt.cm.jet,
                        transform=ccrs.PlateCarree(),
                        alpha=0.3,
                        vmin=-2,
                        vmax=+4
                       )

    ax1.set_title("NO$_x$ divergence")
    ax1.set_xlabel('longitude (°)')
    ax1.set_ylabel('latitude (°)')
    cbar1 = plt.colorbar(mappable=c1, ax=ax1, fraction=cbar_fraction)
    cbar1.ax.set_title('g/m$^2$/s')

    # plot CO2 divergence
    ax2.set_extent(extent)
    ax2.add_image(request, 6)
    if sources is not None:
        ddeq.vis.add_hot_spots(ax2, sources=sources, size=fontsize, ms=ms)
    c2 = ax2.pcolormesh(longrid, latgrid, CO2_div/1e3,
                        shading='auto',
                        cmap=plt.cm.jet,
                        transform=ccrs.PlateCarree(),
                        alpha=0.3,
                        vmin=-2,
                        vmax=+4
                       )
    ax2.set_title("CO$_2$ divergence")
    ax2.set_xlabel('longitude (°)')
    ax2.set_ylabel('latitude (°)')
    cbar2 = plt.colorbar(mappable=c2, ax=ax2, fraction=cbar_fraction)
    cbar2.ax.set_title('kg/m$^2$/s')

    return fig


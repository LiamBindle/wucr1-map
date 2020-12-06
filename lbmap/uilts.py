import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from lbmap.colors import draw_cax, make_axes_empty
from lbmap.styles import dark_stylesheet
import matplotlib
import skimage.transform

stylesheet = dark_stylesheet

matplotlib.rc('font', **stylesheet.font)

def new_single_panel(resolution=[1920, 1080], dpi=300, **kwargs):
    width_in = resolution[0] / dpi
    height_in = resolution[1] / dpi
    figsize = (width_in, height_in)
    return plt.figure(figsize=figsize, dpi=dpi)


def savefig(fig: plt.Figure, fname='figure.png'):
    fig.savefig(fname, facecolor=stylesheet.background, pad_inches=0, transparent=True)

def basemap(fig: plt.Figure):
    ax = fig.add_axes(stylesheet.map_frame, projection=ccrs.EqualEarth())
    ax.set_global()
    img = plt.imread(r'/GRAY_LR_SR_W.tif')
    img = skimage.transform.resize(img, (img.shape[0] // 8, img.shape[1] // 8),
                           anti_aliasing=True)
    img_extent=(-180, 180, -90, 90)
    ax.imshow(img, origin='upper', extent=img_extent, vmin=0, vmax=1, transform=ccrs.PlateCarree(), cmap='Greys_r', interpolation='antialiased')

    # ax.coastlines(                                                  # coastline styling
    #     resolution='110m',
    #     color=stylesheet.primary,
    #     linewidth=stylesheet.primary_linewidth,
    # )
    #
    # lakes = cfeature.NaturalEarthFeature(
    #     'physical', 'lakes', '110m',
    #     edgecolor=stylesheet.primary,
    #     linewidth=stylesheet.primary_linewidth,
    #     facecolor='none',
    # )
    # ax.add_feature(lakes)


    ax.patch.set_fill(False)                                        # transparent map
    ax.spines['geo'].set_edgecolor('#7E7E7E') #stylesheet.primary)              # map outline color
    ax.spines['geo'].set_linewidth(0.5) #stylesheet.primary_linewidth)    # map outline linewidth
    return ax

def single_cbar(fig):
    cax = fig.add_axes(stylesheet.cbar_frame)
    cax.set_facecolor(stylesheet.background)
    cb = draw_cax(cax, cmap=stylesheet.cmap, norm=stylesheet.norm, ticks=stylesheet.cbar_ticks, extend='max',
                  extendfrac=0.02)
    # cb.set_label('colorbar label', color=stylesheet.text2)
    cb.ax.xaxis.set_tick_params(color=stylesheet.text1, width=stylesheet.thicker_primary_linewidth)
    cb.outline.set_edgecolor(None)
    # cb.outline.set_linewidth(stylesheet.primary_linewidth)
    plt.setp(plt.getp(cb.ax.axes, 'xticklabels'), color=stylesheet.text1)

def multi_cbar(fig):
    for i in range(len(stylesheet.multi_cbar_frame)):
        cax = fig.add_axes(stylesheet.multi_cbar_frame[i])
        cax.set_facecolor(stylesheet.background)
        if stylesheet.multi_cbar_label[i]:
            ticks = stylesheet.multi_cbar_ticks
        else:
            ticks = []
        cb = draw_cax(cax, cmap=stylesheet.multi_cbar_cmap[i], norm=stylesheet.norm, ticks=ticks, extend='max',
                      extendfrac=0.02)
        # cb.set_label('colorbar label', color=stylesheet.text2)
        cb.ax.xaxis.set_tick_params(color=stylesheet.text1, width=stylesheet.thicker_primary_linewidth, labelsize='x-small')
        cb.outline.set_edgecolor(None)
        cb.patch.set_facecolor(stylesheet.background)
        cb.patch.set_alpha(0.5)
        # cb.outline.set_linewidth(stylesheet.primary_linewidth)
        plt.setp(plt.getp(cb.ax.axes, 'xticklabels'), color=stylesheet.text1)


def legend(fig):
    ax = fig.add_axes(stylesheet.legend_frame)
    make_axes_empty(ax)
    ax.text(
        0, 0,
        '2018-06-04 08:00:00z\nAerosol Optical Depth, 550 nm\nWUCR1 (GCHP 13.0.0, C360)', # 25 km, GCHP 13.0.0, WUCR1, CPU time: XXX hours
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes,
        color=stylesheet.text1,
        fontsize='small',
        linespacing=1.5,
    )

    ax = fig.add_axes([0.35, 0.075, 0.3, 0.2])
    make_axes_empty(ax)
    ax.text(
        0, 0,
        'OC\nSS\nDust', # 25 km, GCHP 13.0.0, WUCR1, CPU time: XXX hours
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes,
        color=stylesheet.text1,
        fontsize='x-small',
        linespacing=1.1,
    )

    ax = fig.add_axes([0.33+0.3, 0.075, 0.3, 0.2])
    make_axes_empty(ax)
    ax.text(
        0, 0,
        '\nBC\nSO4', # 25 km, GCHP 13.0.0, WUCR1, CPU time: XXX hours
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes,
        color=stylesheet.text1,
        fontsize='x-small',
        linespacing=1.1,
    )



if __name__ == '__main__':
    import xarray as xr
    ds = xr.open_dataset(r'test.nc4')
    from palettable.colorbrewer.sequential import BuPu_8
    import matplotlib.colors
    cmaplist = np.array(BuPu_8.colors)
    cmaplist = np.concatenate([cmaplist.transpose()/255, np.linspace(0, 1, cmaplist.shape[0])[:, np.newaxis].transpose()**2]).transpose()
    cmap = matplotlib.colors.ListedColormap(cmaplist.tolist(), name='foo')
    print(ds)
    fig = new_single_panel()
    ax = basemap(fig)
    #single_cbar(fig)
    for nf in range(6):
        norm = stylesheet.norm
        x = ds.corner_lons.isel(nf=nf).values
        x = x %360 # x[x >180] -= 360
        y = ds.corner_lats.isel(nf=nf)
        dust_cm = stylesheet.multi_cbar_cmap[0]
        ss_cm = stylesheet.multi_cbar_cmap[1]
        oc_cm = stylesheet.multi_cbar_cmap[2]
        so4_cm = stylesheet.multi_cbar_cmap[3]
        bc_cm = stylesheet.multi_cbar_cmap[4]
        da = ds['AODDust'].isel(nf=nf).sum('lev').squeeze()
        ax.pcolormesh(x, y.values, da.values, transform=ccrs.PlateCarree(),
                      cmap=dust_cm, norm=norm, antialiased=True, zorder=10)
        da = (ds['AODHygWL1_SALA'] + ds['AODHygWL1_SALC']).isel(nf=nf).sum('lev').squeeze()
        ax.pcolormesh(x, y.values, da.values, transform=ccrs.PlateCarree(),
                      cmap=ss_cm, norm=norm, antialiased=True, zorder=10)
        da = ds['AODHygWL1_OCPI'] .isel(nf=nf).sum('lev').squeeze()
        ax.pcolormesh(x, y.values, da.values, transform=ccrs.PlateCarree(),
                      cmap=oc_cm, norm=norm, antialiased=True, zorder=10)

        da = ds['AODHygWL1_SO4'] .isel(nf=nf).sum('lev').squeeze()
        ax.pcolormesh(x, y.values, da.values, transform=ccrs.PlateCarree(),
                      cmap=so4_cm, norm=norm, antialiased=True, zorder=10)
        da = ds['AODHygWL1_BCPI'] .isel(nf=nf).sum('lev').squeeze()
        ax.pcolormesh(x, y.values, da.values, transform=ccrs.PlateCarree(),
                      cmap=bc_cm, norm=norm, antialiased=True, zorder=10)
    multi_cbar(fig)
    legend(fig)
    savefig(fig)

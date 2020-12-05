import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np

import palettable.colorbrewer.sequential

def get_rect(anchor_x, anchor_y, width, height, anchor='center'):
    if anchor =='center':
        x0 = anchor_x - width / 2
        y0 = anchor_y - height / 2
    elif anchor == 'bottom-left':
        x0 = anchor_x
        y0 = anchor_y
    else:
        raise NotImplemented(f'anchor: "{anchor}" is not implemented')
    return [x0, y0, width, height]

def make_cmap_transparent(cm):
    cmaplist = np.array(cm.colors)
    cmaplist = np.concatenate(
        [cmaplist.transpose() / 255, np.linspace(0, 0.8, cmaplist.shape[0])[:, np.newaxis].transpose()]).transpose()
    cmaplist[:3, -1] = 0
    #cmaplist[3:, -1] = 1
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('foo', cmaplist.tolist(), N=256)
    return cmap

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

dark_palette_1 = dotdict(
    background='#0e0e0e',
    text1='#919191',
    text2='#9b9b9b',
    cmap='Oranges', #sns.color_palette("YlOrBr", as_cmap=True),
    primary='#919191',

)

dark_stylesheet = dotdict(
    primary=dark_palette_1.primary,
    primary_linewidth=0.1,
    thicker_primary_linewidth=0.3,

    background=dark_palette_1.background,

    # 1920x1080
    map_frame=get_rect(0.5, 0.56, 0.9, 0.85, anchor='center'),
    cbar_frame=get_rect(0.6, 0.1, 0.5, 0.02, anchor='center'),
    legend_frame=get_rect(0.12, 0.045, 0.3, 0.1, anchor='bottom-left'),

    cmap=dark_palette_1.cmap,
    norm=plt.Normalize(0, 0.25),
    cbar_ticks=[0, 0.5, 1],

    text1=dark_palette_1.text1,
    text2=dark_palette_1.primary,

    font=dict(
        family='Open Sans',
        weight='light',
        size=7,
    ),

    multi_cbar_frame=[
        get_rect(0.39, 0.08, 0.2, 0.015, anchor='bottom-left'),
        get_rect(0.39, 0.08+0.02, 0.2, 0.015, anchor='bottom-left'),
        get_rect(0.39, 0.08+0.02+0.02, 0.2, 0.015, anchor='bottom-left'),

        get_rect(0.37+0.3, 0.08, 0.2, 0.015, anchor='bottom-left'),
        get_rect(0.37+0.3, 0.08+0.02, 0.2, 0.015, anchor='bottom-left'),
    ],
    multi_cbar_label=[
        True, False, False, True, False
    ],
    multi_cbar_cmap=[
        make_cmap_transparent(palettable.colorbrewer.sequential.Oranges_9),
        make_cmap_transparent(palettable.colorbrewer.sequential.PuBu_9),
        make_cmap_transparent(palettable.colorbrewer.sequential.Greens_9),
        make_cmap_transparent(palettable.colorbrewer.sequential.Reds_9),
        make_cmap_transparent(palettable.colorbrewer.sequential.Purples_9),
    ],
    multi_cbar_ticks=[0, 0.125, 0.25],
)
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm

def draw_cax(cax, cmap='viridis', norm=None, **colorbar_kwargs):
    colorbar_kwargs.setdefault('orientation', 'horizontal')
    if norm is None:
        norm = plt.Normalize(0, 1)
        colorbar_kwargs.setdefault('ticks', [])
    cb = plt.colorbar(
        mappable=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),
        cax=cax,
        **colorbar_kwargs
    )
    cb.solids.set_edgecolor("face")
    return cb

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

def make_axes_empty(ax):
    ax.set_frame_on(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


def dummy_panel(palette):
    fig = plt.figure()
    rect = get_rect(0, 0, 1, 1, anchor='bottom-left')
    ax = fig.add_axes(rect, anchor='SW')
    ax.set_facecolor(palette.background)
    rect = get_rect(0.5, 0.25, 0.9, 0.4, anchor='center')
    cax = fig.add_axes(rect)
    cb = draw_cax(cax, cmap=palette.cmap)
    cb.outline.set_visible(False)

    rect = get_rect(0.5, 0.75, 0.9, 0.3, anchor='center')
    ax = fig.add_axes(rect)
    make_axes_empty(ax)
    ax.text(
        0.1, 0.66,
        'Lorem ipsum dolor sit amet.',
        horizontalalignment='left',
        verticalalignment='center',
        transform=ax.transAxes,
        color=palette.text1
    )
    ax.text(
        0.1, 0.33,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non.',
        horizontalalignment='left',
        verticalalignment='center',
        transform=ax.transAxes,
        color=palette.text1,
        size='small'
    )




if __name__ == '__main__':
    import matplotlib.cm

    dummy_panel(dark_palette_1)
    plt.show()

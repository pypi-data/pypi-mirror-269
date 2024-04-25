import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy import array, floor, ones_like
from Bio import Seq
import openpyxl

from ..external.plot_eteTree import plot_tree
from ete3 import NodeStyle

python_ver, mpl_ver, mpl_minor = mpl.__version__.split('.')


def _convert_to_num(sequence: Seq) -> Seq:
    """
        Converts letter-code to numeric-code of a nt sequence
        for plotting purposes.

        A: 1, T: 2, G: 3, C: 4, N: 5, X: 6, gap (-): 0.
    """
    return sequence.replace('A', '1').replace('T', '2').replace('G',
           '3').replace('C', '4').replace('N', '5').replace('X',
           '6').replace('-', '0')


def _format_tree_label(leaf, XLS_DB: str) -> str:
    """
        Manipulate the name of each leaf from the phylogenetic tree to
        add metadata from XLS_DB.
    """
    ASSEMBLY_NAME_POS = 0
    ASSEMBLY_TYPE_POS = 6

    # Load (and set active worksheet) excel file with metadata
    DB = openpyxl.load_workbook(XLS_DB).active
    for asmbl in DB:
        if asmbl[ASSEMBLY_NAME_POS].value is not None:
            if leaf.name.split('__')[0].split('_L')[0] == \
                    asmbl[ASSEMBLY_NAME_POS].value.removesuffix('.fasta'):
                return str(asmbl[ASSEMBLY_TYPE_POS].value)
            elif leaf.name.split('__')[0].split('_L')[0].split('_')[1] in \
                    asmbl[ASSEMBLY_NAME_POS].value.removesuffix('.fasta'):
                return str(asmbl[ASSEMBLY_TYPE_POS].value)


def _index_phylogeny(phylogeny) -> dict:
    """
        Find index of each assembly within the phylogeny to aid
        representation of mutations.
    """
    return dict((leaf.name.split('__')[0], id) for id,
                leaf in enumerate(phylogeny.get_leaves()[::-1]))


def plot_alignment(alignment: Seq, FIG_FNAME: str, coverage_data: list,
                   phylogeny: str, consensus_seq: Seq, conserved_seq: Seq,
                   mutations: dict, LABELS: str, SEQ_CUTOFF: int,
                   reference_regions: list, custom_cmap: array = None,
                   PROMOTER_ONLY: bool = False, show_plot: bool = True):
    """
        Plot alignment as a grid, highlighting deviations form consensus
        and conserved sequences. If 'promoter_regions' given, it will also
        highlight specific sections of the alignment.
    """
    # Convert sequence data into numeric data for plotting
    num_aln = array([_convert_to_num(i.seq) for i in alignment], dtype='int')
    asmbl_indexes = _index_phylogeny(phylogeny)

    # Calculate overall distance between root and closest leaves (for plotting)
    tree_distance = phylogeny.get_distance(phylogeny.get_farthest_leaf()[0],
                                           phylogeny.get_closest_leaf()[0])

    # This avoids copy/pasting function to test different colours in terminal
    if custom_cmap is not None:
        my_cmap = custom_cmap
    else:
        if mpl_ver >= '7' and mpl_minor >= '0':
            my_cmap = mpl.colormaps['Purples'].resampled(10)
        else:
            my_cmap = mpl.cm.get_cmap('Purples', 10)

    # Figure width, font sizes
    if len(phylogeny) < 75:
        fig_width = 6
        PHY_F_SIZE = 3
    else:
        fig_width = 10
        PHY_F_SIZE = 4
    fig_height = int(0.085 * len(alignment))

    F_SIZE = 8
    LBL_SIZE = 18
    TK_SIZE = 12
    AN_WIDTH = 2
    AN_OFFSET = 0.01 if len(alignment) <= 10 else 0.125

    if coverage_data is not None:
        fig, ax = plt.subplot_mosaic('122223', figsize=(fig_width, fig_height))
    else:
        fig, ax = plt.subplot_mosaic('12222', figsize=(fig_width, fig_height))

    # Set figure size
    # fig.set_figwidth(fig_width)
    # fig.set_figheight(fig.get_figheight() + fig.get_figheight() * fig_height)

    # Plot phylogeny
    tree_dims = ax['1'].get_position()  # left, bottom, width, height
    tree_dims.x0 = tree_dims.x0 * 0.5  # Account for annotations
    ax['1'].set_position(tree_dims)
    ax['1'].autoscale(tight=True)
    ax['1'].axis('off')
    ax['1'].set_zorder(ax['2'].get_zorder() + 0.1)
    # Shift -5% to avoid overlap of labels with alignment plot
    box = ax['1'].get_position()
    offset = box.x1 * 0.05
    box.x0 = box.x0 - offset
    box.x1 = box.x1 - offset
    ax['1'].set_position(box)

    nstyle = NodeStyle()
    nstyle['fgcolor'] = 'black'
    nstyle['shape'] = 'circle'

    nstyle['size'] = 0.5
    nstyle['hz_line_width'] = 0  # eteTree adds 1 to this amount

    nstyle2 = NodeStyle()
    nstyle2['size'] = 0
    nstyle2['shape'] = 'square'
    nstyle2['fgcolor'] = 'none'
    nstyle2['hz_line_width'] = 0  # eteTree adds 1 to this amount
    nstyle2['vt_line_width'] = 0  # eteTree adds 1 to this amount

    for n in phylogeny.iter_descendants():
        if n.is_leaf():  # Style for leafs / terminal branches
            n.set_style(nstyle)
        else:  # Style for internal branches
            n.set_style(nstyle2)
    phylogeny.set_style(nstyle2)

    asmbl_colors = dict()
    for leaf in phylogeny.iter_leaves():
        if LABELS is not None:
            asmbl_type = _format_tree_label(leaf, LABELS)
        else:
            asmbl_type = None

        if mutations is not None:
            # Highlight genes based on source and mutations. Black default.
            if len(mutations[leaf.name.split('__')[0]]) > 0:
                asmbl_colour = 'darkorange' if asmbl_type == 'UTI' else 'indianred'
            else:
                asmbl_colour = 'black'
        else:
            asmbl_colour = 'black'

        if asmbl_type is None:  # 'region' column not detected in XLSX?
            leaf.add_feature('name', leaf.name.split('__')[0])
        else:
            if len(leaf.name.split('__')[0].split('_')) < 3:
                leaf_name = leaf.name.split('__')[0].split('_')[0]
            else:
                leaf_name = '_'.join(leaf.name.split('__')[0].split('_')[0::2])
            # Re-format leaf name to avoid asmbl_type NoneType and error
            leaf.add_feature('name', leaf_name + ' (' + asmbl_type + ')')
        # Assign colours
        asmbl_colors[leaf.name] = asmbl_colour

    N_OFFSET = 0.005  # Phylogeny leaf label gap with tree
    if tree_distance < 0.1 and len(tree_distance.__repr__().split('.')) > 1:
        exponent = tree_distance.__repr__().split('.')[1].count('0') + 3
        N_OFFSET = 10 ** int(-exponent)

    coords = plot_tree(phylogeny, name_offset=N_OFFSET,
                       name_colors=asmbl_colors, font_size=PHY_F_SIZE,
                       ms=0, axe=ax['1'])

    # Plot
    ax['2'].pcolormesh(num_aln, cmap=my_cmap, zorder=-5, vmin=num_aln.min(),
                       vmax=num_aln.max())
    ax['2'].scatter(0, ax['1'].get_ylim()[0], color='white')
    ax['2'].autoscale(tight=True)  # Do not move from here

    # Add SNPs
    if mutations is not None:
        for asmbl in mutations:
            if len(mutations[asmbl]) > 0:
                snps = mutations[asmbl]
                asmbl_pos = asmbl_indexes[asmbl]
                for nt in snps:
                    ax['2'].scatter(array(nt) + 0.5,
                                    ones_like(nt) * asmbl_pos + 0.5,
                                    s=0.25, color='black', marker='.')

    ax['2'].set(xlabel='Position (nt)')

    # Hack for legend
    ax_ylim = ax['2'].get_ylim()
    ax_xlim = ax['2'].get_xlim()
    ax['2'].scatter(-100, 10, s=520, color=my_cmap(2), marker='s', label='A',
                    zorder=-10)
    ax['2'].scatter(-100, 10, s=520, color=my_cmap(4), marker='s', label='T',
                    zorder=-10)
    ax['2'].scatter(-100, 10, s=520, color=my_cmap(6), marker='s', label='G',
                    zorder=-10)
    ax['2'].scatter(-100, 10, s=520, color=my_cmap(8), marker='s', label='C',
                    zorder=-10)

    if PROMOTER_ONLY is True:
        ax['2'].set_xlim(0, SEQ_CUTOFF * 1.75)
    else:
        ax['2'].set_xlim(ax_xlim)

    # Highlight promoter regions, if any
    if reference_regions[0] is not None and PROMOTER_ONLY is True:
        ref_label, ref_location = reference_regions
        for label, location in zip(ref_label, ref_location):
            if label != 'ATG' and label.lower() != 'promoter' and location[1] != -1:
                ax['2'].plot([location[0]+1, location[1]-1], [ax_ylim[1]+AN_OFFSET,
                             ax_ylim[1]+AN_OFFSET], 'black', linewidth=AN_WIDTH)
                ax['2'].text(location[0] + int((location[1] - location[0])/2),
                             ax_ylim[1]+0.75, label.replace('\\n', '\n'),
                             horizontalalignment='center', fontsize=F_SIZE)
            elif label == 'ATG':
                atg_pos = location[0]

    # Highlight ATG init translation
    if PROMOTER_ONLY is False:
        atg_pos = consensus_seq.find('ATG')
    atg_col = 'dimgrey' if atg_pos > -1 else 'tomato'
    ax['2'].plot([atg_pos+1, atg_pos + 2], [ax_ylim[1]+AN_OFFSET,
                                            ax_ylim[1]+AN_OFFSET], atg_col,
                 linewidth=AN_WIDTH)
    # Additional bar to thicken highlight without extending to neighbouring NT
    ax['2'].plot([atg_pos+1, atg_pos + 2], [ax_ylim[1]+AN_OFFSET*2,
                                            ax_ylim[1]+AN_OFFSET*2], atg_col,
                 linewidth=AN_WIDTH)
    ax['2'].text(atg_pos+2, ax_ylim[1]+0.75, 'ATG',
                 horizontalalignment='center', fontsize=F_SIZE, color=atg_col)

    # Get rid of plot frame, but preserve labels (so can't use axis('off'))
    ax['2'].spines['top'].set_visible(False)
    ax['2'].spines['bottom'].set_visible(False)
    ax['2'].spines['left'].set_visible(False)
    ax['2'].spines['right'].set_visible(False)
    ax['2'].spines['bottom'].set_position(('data', 0))  # Keep ticks at base of data 

    # Adjust fontsize
    ax['2'].xaxis.label.set_size(LBL_SIZE)
    ax['2'].yaxis.label.set_size(LBL_SIZE)
    ax['2'].tick_params(direction='out', labelsize=TK_SIZE)
    xtick_labels = ax['2'].get_xticks()
    xtick_labels[0] = 1
    ax['2'].set_xticks(xtick_labels[:-1])  # It adds tick at 300? Get rid of it
    ax['2'].set_yticks([])

    # Add legend (adaptive)
    if len(alignment) < 50:
        lower_anchor = -0.3
    elif len(alignment) < 300:
        lower_anchor = -0.15
    elif len(alignment) < 550:
        lower_anchor = -0.05
    elif len(alignment) < 900:
        lower_anchor = -0.03
    else:
        lower_anchor = -0.0175

    ax['2'].legend(loc='lower center', ncol=4, frameon=False,
                   bbox_to_anchor=(0.5, lower_anchor), fontsize=LBL_SIZE,
                   columnspacing=0.75, labelspacing=0, borderpad=0)

    # Plot coverage data
    if coverage_data is not None:
        coverage_data.reverse()

        ax['3'].barh([d+0.5 for d in range(len(coverage_data))], coverage_data,
                     height=1, align='center', color='black', zorder=10)
        ax['3'].plot([2, 2], [0, len(coverage_data)], linewidth=0.75,
                     color='red', zorder=11)
        ax['3'].autoscale(tight=True)
        ax['3'].set(xlabel='RCN')
        ax['3'].grid(axis='x', linestyle=':', alpha=0.5, linewidth=0.5,
                     color='darkgrey')

        # Get rid of plot frame, but preserve labels (so can't use axis('off'))
        ax['3'].spines['left'].set_visible(False)
        ax['3'].spines['right'].set_visible(False)
        ax['3'].spines['bottom'].set_position(('data', 0))  # Keep ticks at base of data 

        # Adjust fontsize
        ax['3'].xaxis.label.set_size(LBL_SIZE)
        ax['3'].yaxis.label.set_size(LBL_SIZE)
        ax['3'].tick_params(direction='out', labelsize=TK_SIZE, top=True,
                            labeltop=True)
        ax['3'].set_yticks([])
        ax_lims = ax['3'].get_xlim()
        ax['3'].set_xlim(0, ax_lims[1].__ceil__())

    # Balance y-axes
    ax['1'].set_ylim(ax['2'].get_ylim())
    if coverage_data is not None:
        ax['3'].set_ylim(ax['2'].get_ylim())

    # Save figure
    FIG_EXT = FIG_FNAME.split('.')[1]
    fig.savefig(FIG_FNAME, format=FIG_EXT, bbox_inches='tight')

    if show_plot is True:
        plt.show()
    plt.close('all')
    return coords


def plot_depth_stats(depth_stats: dict, FIG_FNAME: str):
    """
        Plots the average depth of all housekeeping, with std,
        for completeness.
    """
    assemblies = depth_stats.keys()
    stats = depth_stats.values()

    mean_depth = [i[0] for i in stats]
    std_depth = [i[1] for i in stats]
    labels = [i.removesuffix('_assembly.fa') for i in assemblies]

    # Plot
    fig = plt.figure(1, figsize=(16, 7))
    ax = fig.add_subplot(111)
    ax.errorbar(range(0, len(stats)), mean_depth, yerr=std_depth,
                linestyle='none', color='k', ecolor='k', linewidth=0.25,
                capsize=2)
    ax.plot(range(0, len(stats)), mean_depth, linestyle='none', color='k',
            linewidth=0.25, marker='o', markersize=4, markerfacecolor='white')

    # Format axes
    ylims = ax.get_ylim()
    ax.set_ylim(0, ylims[1]*1.005)
    ax.set_xlim(-0.5, len(labels)+0.5)
    ax.set_xticks(range(len(assemblies)), labels)
    ax.tick_params(axis='x', labelsize=7, rotation=-45)
    ax.tick_params(axis='y', labelsize=7)
    for tick in ax.xaxis.get_majorticklabels():  # Re-align labels for readability
        tick.set_horizontalalignment('left')
    ax.set_ylabel('Coverage depth (mean $\pm$ standard deviation)', fontsize=8)

    # Save figure
    FIG_EXT = FIG_FNAME.split('.')[1]
    FIG_NAME = FIG_FNAME.split('.')[0] + str('_stats') + str('.') + FIG_EXT
    fig.savefig(FIG_NAME, format=FIG_EXT, bbox_inches='tight')
    plt.close('all')
    return


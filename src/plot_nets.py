#!/usr/bin/python3
import matplotlib, os, sys, math
matplotlib.use('Agg') # This must be done before importing matplotlib.pyplot
import matplotlib.pyplot as plt, matplotlib.patches as mpatches
import numpy as np, networkx as nx
import math, re, pickle


################## ORGANIZER FUNCTIONS ##################
def single_run_plots (dirr):
    #plots features_over_time and degree_distrib
    #only uses most fit indiv in population
    if not os.path.exists(dirr):
        print("ERROR plot_nets(): given directory not found: " + str(dirr))
        return

    net_info, titles = parse_info(dirr)

    if not os.path.exists(dirr + "/images_by_size/"): os.makedirs(dirr + "/images_by_size/")
    if not os.path.exists(dirr + "/images_by_time/"): os.makedirs(dirr + "/images_by_time/")

    mins, maxs = 0,0
    features_over_size(dirr, net_info, titles, mins, maxs, False)
    features_over_time(dirr, net_info, titles, mins, maxs, False)

    print("Generating directed degree distribution plots.")
    degree_distrib(dirr)

    print("Generating undirected degree distribution plots.")
    plot_undir(dirr, False, None) #last two args for Biased and bias on, which haven't really been implemented

    print("Generating degree change plot.\n")
    degree_distrib_change(dirr) #may require debugging


def plot_undir(output_dir, biased, bias_on):
    dirs = ["/undirected_degree_distribution/", "/undirected_degree_distribution/loglog/", "/undirected_degree_distribution/loglog%/"] #"/undirected_degree_distribution/scatter/", "/undirected_degree_distribution/scatter%/"]
    for dirr in dirs:
        if not os.path.exists(output_dir + dirr):
            os.makedirs(output_dir + dirr)

    for root, dirs, files in os.walk(output_dir + "/nets_nx/"):
        for f in files:
            undir_deg_distrib(root + "/" + f, output_dir + "/undirected_degree_distribution/", f, biased, bias_on)



################## IMAGE GENERATION FUNCTIONS ##################
def undir_deg_distrib(net_file, destin_path, title, biased, bias_on):

    if (re.match(re.compile("[a-zA-Z0-9]*pickle"), net_file)):
        with open(net_file, 'rb') as file:
            net = pickle.load(file)
            file.close()
    else:
        net = nx.read_edgelist(net_file, nodetype=int, create_using=nx.DiGraph())

    colors = ['#0099cc','#ff5050', '#6699ff']
    color_choice = colors[0]

    for type in ['loglog', 'loglog%']: #can also use ['scatter', 'scatter%']
        H = []
        #loglog
        degrees = list(net.degree().values())
        degs, freqs = np.unique(degrees, return_counts=True)
        tot = float(sum(freqs))
        if (type=='loglog%' or type=='scatter%'): freqs = [(f/tot)*100 for f in freqs]

        #derive vals from conservation scores
        bias_vals, ngh_bias_vals = [], []
        if (biased == True or biased == 'True'):
            for deg in degs: #deg bias is normalized by num nodes
                avg_bias, ngh_bias, num_nodes = 0,0,0
                for node in net.nodes():
                    if (net.degree(node) == deg):
                        if (bias_on == 'nodes'):
                            avg_bias += abs(.5-net.node[node]['bias'])

                            avg_ngh_bias = 0
                            for ngh in net.neighbors(node):
                                avg_ngh_bias += net.node[ngh]['bias']
                            avg_ngh_bias /= len(net.neighbors(node))
                            ngh_bias += abs(.5-avg_ngh_bias)

                        elif (bias_on == 'edges'): #node bias is normalized by num edges
                            node_bias, num_edges = 0, 0
                            for edge in net.edges(node):
                                node_bias += net[edge[0]][edge[1]]['bias']
                                num_edges += 1
                            if (num_edges != 0): node_bias /= num_edges
                        num_nodes += 1
                avg_bias /= num_nodes
                ngh_bias /= num_nodes
                bias_vals.append(avg_bias)
                ngh_bias_vals.append(ngh_bias)
            assert(len(bias_vals) == len(degs))

            with open(destin_path + "/degs_freqs_bias_nghBias",'wb') as file:
                pickle.dump(file, [degs, freqs, bias_vals, ngh_bias_vals])


            cmap = plt.get_cmap('plasma')
            bias_colors = cmap(bias_vals)

            if (type == 'loglog' or type=='loglog%'): plt.loglog(degs, freqs, basex=10, basey=10, linestyle='',  linewidth=2, c = bias_colors, alpha=1, markersize=8, marker='D', markeredgecolor='None')
            elif (type == 'scatter' or type=='scatter%'):
                sizes = [10 for i in range(len(degs))]
                plt.scatter(degs, freqs, c = bias_colors, alpha=1, s=sizes, marker='D')

        else:
            if (type == 'loglog' or type=='loglog%'): 
                plt.loglog(degs, freqs, basex=10, basey=10, linestyle='',  linewidth=2, color = color_choice, alpha=1, markersize=8, marker='D', markeredgecolor='None')
            elif (type == 'scatter' or type=='scatter%'):
                sizes = [10 for i in range(len(degs))]
                plt.scatter(degs, freqs, color = color_choice, alpha=1, s=sizes, marker='D')
        patch =  mpatches.Patch(color=color_choice, label=title + "_" + type)
        H = H + [patch]

        #FORMAT PLOT
        ax = plt.gca() # gca = get current axes instance

        if (type == 'loglog%' or type=='scatter%'):
            ax.set_xlim([0,100])
            ax.set_ylim([0,100])
        elif (type == 'loglog' or type == 'scatter'):
            max_x = max(1,math.floor(max(degs)/10))
            max_x = max_x*10+10

            max_y = max(1,math.floor(max(freqs)/10))
            max_y = max_y*10+100

            upper_lim = max(max_x, max_y)

            ax.set_xlim([0, upper_lim])
            ax.set_ylim([0, upper_lim])

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tick_params(axis='both', which='both', right='off', top='off') #http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.tick_params
        plt.legend(loc='upper right', handles=H, frameon=False,fontsize= 11)
        plt.xlabel('Degree')
        if (type=='loglog%'): plt.ylabel('Percent of Nodes with Given Degree')
        else: plt.ylabel('Number of Nodes with Given Degree')
        #plt.title('Degree Distribution of ' + str(title) + ' vs Simulation')

        plt.tight_layout()
        plt.savefig(destin_path + "/" + type + "/" + title + ".png", dpi=300,bbox='tight') # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
        plt.clf()
        plt.cla()
        plt.close()



def degree_distrib(dirr):
        deg_file_name = dirr + "/degree_distrib.csv"

        if not os.path.exists(dirr + "/directed_degree_distribution/"):
            os.makedirs(dirr + "/directed_degree_distribution/")

        all_lines = [Line.strip() for Line in (open(deg_file_name,'r')).readlines()]
        titles = all_lines[0]
        img_index = 0
        for line in all_lines[1:]:
            line = line.replace('[', '').replace(']','').replace("\n", '')
            line = line.split(',')
            gen = line[0]
            in_deg = line[2].split(" ")
            in_deg_freq = line[3].split(" ")
            out_deg = line[4].split(" ")
            out_deg_freq = line[5].split(" ")

            in_deg = list(filter(None, in_deg))
            in_deg_freq = list(filter(None, in_deg_freq))
            out_deg = list(filter(None, out_deg))
            out_deg_freq = list(filter(None, out_deg_freq))

            # plot in degrees
            plt.loglog(in_deg, in_deg_freq, basex=10, basey=10, linestyle='', color='blue', alpha=0.7, markersize=7, marker='o', markeredgecolor='blue')

            #plot out degrees on same figure
            plt.loglog(out_deg, out_deg_freq, basex=10, basey=10, linestyle='', color='green', alpha=0.7, markersize=7, marker='D', markeredgecolor='green')

            #way to not do every time?
            ax = matplotlib.pyplot.gca()
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            plt.tick_params(  # http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.tick_params
                axis='both',  # changes apply to the x-axis
                which='both',  # both major and minor ticks are affected
                right='off',  # ticks along the right edge are off
                top='off',  # ticks along the top edge are off
            )
            in_patch = mpatches.Patch(color='blue', label='In-degree')
            out_patch = mpatches.Patch(color='green', label='Out-degree')
            plt.legend(loc='upper right', handles=[in_patch, out_patch], frameon=False)
            plt.xlabel('Degree (log) ')
            plt.ylabel('Number of nodes with that degree (log)')
            plt.title('Degree Distribution of Fittest Net at Generation ' + str(gen))
            plt.xlim(1,1000)
            plt.ylim(1,1000)
            plt.savefig(dirr + "/directed_degree_distribution/" + str(gen) + ".png", dpi=300)
            plt.clf()
            img_index += 1


def features_over_size(dirr, net_info, titles, mins, maxs, use_lims):
    #size is 2nd col of net info

    img_dirr = dirr + "/images_by_size/"
    for i in range(len(titles)):
        num_outputs = len(net_info)
        ydata = []
        xdata = []
        for j in range(num_outputs):
            ydata.append(net_info[j,i])
            xdata.append(net_info[j,1])
        x_ticks = []
        max_net_size = max(xdata)
        for j in range(0,11):
            x_ticks.append((max_net_size/10)*j)
        plt.plot(xdata, ydata)
        plt.ylabel(titles[i] + " of most fit Individual")
        plt.title(titles[i])
        if (use_lims==True): plt.ylim(mins[i], maxs[i])
        plt.xlabel("Net Size")
        plt.xticks(x_ticks, x_ticks)
        plt.savefig(img_dirr + str(titles[i]) + ".png")
        plt.clf()
    return


def degree_distrib_change(dirr):
    deg_file_name = dirr + "/degree_distrib.csv"

    if not os.path.exists(dirr + "/degree_distribution_change/"):
        os.makedirs(dirr + "/degree_distribution_change/")

    all_lines = [Line.strip() for Line in (open(deg_file_name, 'r')).readlines()]
    titles = all_lines[0]

    # Get starting degree distribution
    line = all_lines[1]
    line = line.replace('[', '').replace(']', '').replace("\n", '')
    line = line.split(',')
    deg = line[6].split(" ")
    deg_freq = line[7].split(" ")
    start_deg = list(filter(None, deg))
    start_freq = list(filter(None, deg_freq))

    # Get ending degree distribution
    line = all_lines[-1]
    line = line.replace('[', '').replace(']', '').replace("\n", '')
    line = line.split(',')
    deg = line[6].split(" ")
    deg_freq = line[7].split(" ")
    end_deg = list(filter(None, deg))
    end_freq = list(filter(None, deg_freq))

    start_col = '#ff5050'
    end_col = '#0099cc'

    plt.loglog(start_deg, start_freq, basex=10, basey=10, linestyle = '', c=start_col, alpha=0.8, markersize=7, marker='o')
    plt.loglog(end_deg, end_freq, basex=10, basey=10, linestyle='', c=end_col, alpha=0.8, markersize=7, marker='o')
    #plt.scatter(end_deg, end_freq, c=end_col, alpha=0.8, s=40, marker='o')

    ax = matplotlib.pyplot.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim([1,1000])
    ax.set_ylim([1,1000])
    #ax.set_yticks([0,50,100,150,200])
    #ax.set_xticks([0,2,4,6,8,10,12,14,16])

    plt.tick_params(  # http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.tick_params
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        right='off',  # ticks along the right edge are off
        top='off',  # ticks along the top edge are off
    )
    in_patch = mpatches.Patch(color=start_col, label='Initial Degree Frequency')
    out_patch = mpatches.Patch(color=end_col, label='Final Degree Frequency')
    plt.legend(loc='upper right', handles=[in_patch, out_patch], frameon=False)
    plt.xlabel('Degree')
    plt.ylabel('Number of Nodes with Given Degree')
    plt.title('Change in Degree Distribution')
    plt.savefig(dirr + "/degree_distribution_change/in_degree_change.png", dpi=300)
    plt.clf()



def features_over_time(dirr, net_info, titles, mins, maxs, use_lims):
    img_dirr = dirr + "/images_by_time/"
    for i in range(len(titles)):
        num_outputs = len(net_info)
        ydata = []
        xdata = []
        for j in range(num_outputs):
            ydata.append(net_info[j, i])
            xdata.append(net_info[j, 0])

        x_ticks = []
        max_gen = xdata[-1]
        for j in range(0, 11):
            x_ticks.append(int((max_gen / 10) * j))
        plt.plot(xdata, ydata)

        #EX OF EXTRA SPECIFICATIONS
        '''
        ax = plt.gca() 

        if(titles[i] == ' Leaf Measure'):
            plt.ylabel("Leaf Fitness")
            ax.set_ylim([0,.3])
            ax.set_xlim([0,2000])
            plt.title("Network Leaf Fitness")
            ticks = [0, .1, .2, .3, .4]
            ax.set_yticks(ticks)
            ticks = [0, 400, 800, 1200, 1600, 2000]
            ax.set_xticks(ticks)
        elif(titles[i] == '  Hub Measure'):
            plt.ylabel("Hub Fitness")
            ax.set_ylim([0,.1])
            ax.set_xlim([0,2000])
            plt.title("Network Hub Fitness")
            ticks = [0, .02, .04, .06, .08]
            ax.set_yticks(ticks)
            ticks = [0, 400, 800, 1200, 1600, 2000]
            ax.set_xticks(ticks)
        elif(titles[i] == ' Fitness'):
            plt.ylabel("Fitness")
            ax.set_ylim([0,.025])
            ax.set_xlim([0,2000])
            plt.title("Network Fitness")
            ticks = [0, .005, .01, .015, .02, .025]
            ax.set_yticks(ticks)
            ticks = [0, 400, 800, 1200, 1600, 2000]
            ax.set_xticks(ticks)
                
        else: 
            plt.ylabel(titles[i])
            plt.title(titles[i])
        '''
        plt.ylabel(titles[i])
        plt.title(titles[i])
        if (use_lims == True): plt.ylim(mins[i], maxs[i])
        plt.xlabel("Generation")
        plt.xticks(x_ticks, x_ticks)
        plt.savefig(img_dirr + str(titles[i]) + ".png")
        plt.clf()

        if (titles[i] == ' Fitness'): #redo, this time log-scaled
            num_outputs = len(net_info)
            ydata = []
            xdata = []
            for j in range(num_outputs):
                ydata.append(net_info[j, i])
                xdata.append(net_info[j, 0])

            ydata2 = []
            for y in ydata:
                if (y==0): ydata2.append(0)
                elif(y<0): ydata2.append(-100)
                else: ydata2.append(math.log(y,10))
            ydata = ydata2
            titles[i] += ' Log-Scaled'

            x_ticks = []
            max_gen = xdata[-1]
            for j in range(0, 11):
                x_ticks.append(int((max_gen / 10) * j))
            plt.plot(xdata, ydata)

            plt.ylabel(titles[i])
            plt.title(titles[i])
            if (use_lims == True): plt.ylim(mins[i], maxs[i])
            plt.xlabel("Generation")
            plt.xticks(x_ticks, x_ticks)
            plt.savefig(img_dirr + str(titles[i]) + ".png")
            plt.clf()

    return

def solver_time(dirr):
    img_dirr = dirr + "/images_by_size/"
    with open(dirr + "/timing.csv", 'r') as timing_csv:
        lines = timing_csv.readlines()
        title = lines[0]
        net_size=[]
        time=[]
        for line in lines[1:]:
            line = line.split(",")
            line[-1].replace("\n",'')
            net_size.append(line[0])
            time.append(line[1])
        max_net_line = lines[-1].split(",")
        max_net_size = int(max_net_line[0])
    x_ticks = []
    for j in range(0, 11):
        x_ticks.append(int((max_net_size / 10) * j))
    plt.plot(net_size,time)
    plt.xlabel("Net Size")
    plt.ylabel("Seconds to Pressurize")
    plt.title("Pressurize Time as Networks Grow")
    plt.xticks(x_ticks, x_ticks)
    plt.savefig(img_dirr + "pressurize_time")
    plt.clf()


################## HELPER FUNCTIONS ##################
def parse_info(dirr):
    #returns 2d array of outputs by features
    #note that feature[0] is the net size

    with open(dirr + "/net_data.csv", 'r') as info_csv:
        lines = info_csv.readlines()
        titles = lines[0].split(",")
        piece = titles[-1].split("\n")
        titles[-1] = piece[0]
        num_features = len(titles)
        num_output = len(lines)-1
        master_info = np.empty((num_output, num_features))

        for i in range(0,num_output):
            row = lines[i+1].split(",", num_features) 
            piece = row[-1].split("\n")
            row[-1] = piece[0]
            master_info[i] = row

    return master_info, titles 


if __name__ == "__main__":
    #first bash arg should be parent directory, then each child directory
    base_dir = "/home/2014/choppe1/Documents/EvoNet/virt_workspace/data/output/"

    if sys.argv[1] == 'comparison': #poss needs to be updated
        net1_path = sys.argv[2]
        net2_path = sys.argv[3]
        biased = False  # sys.argv[2]
        bias_on = None  # sys.argv[3]

        dirs = ["/undirected_degree_distribution/", "/undirected_degree_distribution/loglog/",
                "/undirected_degree_distribution/loglog%/", "/undirected_degree_distribution/scatter/",
                "/undirected_degree_distribution/scatter%/"]
        for dirr in dirs:
            if not os.path.exists(net1_path + dirr):
                os.makedirs(net1_path + dirr)

    elif sys.argv[1] == 'undir':
        biased = None
        bias_on = None

        parent_dir = sys.argv[1]

        for dirr in sys.argv[2:]:
            print("plotting " + base_dir + parent_dir + dirr)
            plot_undir(base_dir + parent_dir + dirr, biased, bias_on)

    else: #default
        dirr_parent = sys.argv[1]
        base_dir += dirr_parent

        for arg in sys.argv[2:]:
            print("Plotting dirr " + str(arg))
            dirr_addon = arg
            dirr= base_dir + dirr_addon
            single_run_plots(dirr)

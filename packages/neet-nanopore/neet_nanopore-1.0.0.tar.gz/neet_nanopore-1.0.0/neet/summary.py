import os, datetime
from collections import defaultdict
from typing import List, Tuple, Dict, Any
from statistics import mean
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.io import to_html
import numpy as np
from tqdm import tqdm

try: # when invoked from the package
    from neet import helper_functions as hs
except ImportError: # when invoked directly
    import helper_functions as hs

class SummaryCreator:
    input_path: str
    output_path: str
    n_bins: int | None
    perc_mis_col: str
    data: Dict[str, List[Any]] # can be of type str, int, float
    export_svg: bool

    def __init__(self, in_path: str, out_path: str | None = None, n_bins: int|None = 5000, use_perc_mismatch_alt: bool = False, export_svg: bool = False) -> None:
        self.process_paths(in_path, out_path)
        self.n_bins = n_bins if n_bins != -1 else None
        self.perc_mis_col = "mismatch_rate_alt" if use_perc_mismatch_alt else "mismatch_rate"
        self.export_svg = export_svg
        
    #################################################################################################################
    #                                   Functions called during initialization                                      #
    #################################################################################################################

    def process_paths(self, in_path: str, out_dir: str|None) -> None:
        """
        Process the input and output path for the SummaryCreator instance. If no output path is given, uses the
        input path with the added suffix "_summary.html" as output path.

        Parameters:
        - in_path (str): The input file path.
        - out_path (str|None): The output file path or directory.

        Raises:
        - FileNotFoundError: If the specified input file path does not exist or if the specified output directory does not exist.
        - Warning: If the output file has an extension other than '.html'. A warning is issued, but the function continues execution.
        """
        # process input path
        hs.check_input_path(in_path, [".tsv"])
        self.input_path = os.path.abspath(in_path)

        # process output path
        if out_dir:
            out_dir = os.path.abspath(out_dir)
            ext = os.path.splitext(out_dir)[1]
            if ext:
                hs.print_update(f"Warning: Extension {ext} was found. Make sure to provide a single output directory.")
            hs.check_create_dir(out_dir)
            filename = f"{os.path.splitext(os.path.basename(in_path))[0]}_summary.html"
            self.output_path = os.path.join(out_dir, filename)
        else:
            self.output_path = f"{os.path.splitext(in_path)[0]}_summary.html"

    def load_data(self) -> None:
        """
        Load data from the specified input file into the SummaryCreator instance.

        Reads the data from a tab-separated values (tsv) file as created by the PileupExtractor module
        and stores it in the 'data' attribute of the class.
        """
        cols = ["chr", "n_reads", "ref_base", "majority_base", "deletion_rate", "insertion_rate", "refskip_rate", "mismatch_rate", "q_mean", "motif"]

        col_idx = {'chr': 0, 'site': 1, 'n_reads': 2, 'ref_base': 3, 'majority_base': 4, 'n_a': 5, 'n_c': 6, 'n_g': 7, 'n_t': 8, 'n_del': 9, 'n_ins': 10, 'n_ref_skip': 11, 'a_rate': 12, 'c_rate': 13, 'g_rate': 14, 'u_rate': 15, 'deletion_rate': 16, 'insertion_rate': 17, 'refskip_rate': 18, 'mismatch_rate': 19, 'mismatch_rate_alt': 20, 'motif': 21, 'q_mean': 22, 'q_std': 23, 'neighbour_error_pos': 24}
        dtypes = {'chr': str, 'site': int, 'n_reads': int, 'ref_base': str, 'majority_base': str, 'n_a': int, 'n_c': int, 'n_g': int, 'n_t': int, 'n_del': int, 'n_ins': int, 'n_ref_skip': int, 'a_rate': float, 'c_rate': float, 'g_rate': float, 'u_rate': float, 'deletion_rate': float, 'insertion_rate': float, 'refskip_rate': float, 'mismatch_rate': float, 'mismatch_rate_alt': float, 'motif': str, 'q_mean': float, 'q_std': float, 'neighbour_error_pos': str}
        
        with open(self.input_path, "r") as file:
            next(file)
            data = dict(zip(cols, [[] for _ in cols]))
            for line in file:
                line = line.strip().split("\t")
                for col in cols: 
                    data[col].append(dtypes[col](line[col_idx[col]]))
            self.data = data

    ######################################################################################################################
    #                                               Main processing method                                               #
    ######################################################################################################################
    def main(self) -> None:
        """
        Orchestrates the creation of a summary report from the input data file.

        This function performs the following steps:
        1. Loads data from the input file.
        2. Creates various summary plots including general statistics, chromosome-wise information,
        general mismatch statistics, specific mismatch type summaries, and motif summaries.
        3. Writes an HTML summary file containing the generated plots.

        Note: The function includes print statements to provide updates on the progress of each step.

        Raises:
            Exception: If any error occurs during the execution, an exception is raised with an
                    accompanying error message.
        """
        time = hs.get_time()

        hs.print_update(f"Starting creation of summary from file '{self.input_path}'.")

        with tqdm(desc=f"{time} | Loading data", total=6) as progress:
            self.load_data()
            n_positions = len(self.data["chr"])
            n_chromosomes = len(set(self.data["chr"]))

            plots = []
    
            progress.update()
            progress.set_description(f"{time} | General summary")
            plots.append(self.create_general_plot())

            progress.update()
            progress.set_description(f"{time} | General mismatch summary")
            plots.append(self.create_mism_general_plot())

            progress.update()
            progress.set_description(f"{time} | Specific mismatch summary")
            plots += self.create_mism_types_plots()

            progress.update()
            progress.set_description(f"{time} | Motif summary")
            plots += self.create_motif_plot()

            progress.update()
            progress.set_description(f"{time} | Writing to HTML")
            self.write_to_html(n_positions, n_chromosomes, plots)

            progress.update()

        hs.print_update(f"Finished. Wrote output to {self.output_path}")
    

    ################################################################################################################
    #                                                Helper methods                                                #
    ################################################################################################################

    def update_plot(self, fig, title: str|None = None, xlab: str|None = None, ylab: str|None = None, height: int = 500, width: int = 800):
        """
        Update the layout of the given Plotly figure.

        Parameters:
        - fig (plotly.graph_objs.Figure): The Plotly figure to be updated.
        - title (str|None): Title for the plot.
        - xlab (str|None): Label for the x-axis.
        - ylab (str|None): Label for the y-axis.
        - height (int): Height of the figure.
        - width (int): Width of the figure.

        Returns:
        - plotly.graph_objs.Figure: The updated Plotly figure.
        """
        fig.update_layout(template="seaborn",
                    title = title,
                    xaxis_title = xlab,
                    yaxis_title = ylab,
                    font=dict(family="Open sans, sans-serif", size=20),
                    plot_bgcolor="white",
                    margin=dict(l=50, r=50, t=50, b=50),
                    height=height,  # Set the height to a constant value
                    width=width)
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, showticklabels=True, ticks='outside', showgrid=False, tickwidth=2)
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True, showticklabels=True, ticks='outside', showgrid=False, tickwidth=2)

        return fig

    def bin_data(self, data: List[int|float]) -> List[int|float]:
        """
        Bin the input data into segments and return the mean value of each segment.

        Parameters:
        - data (List[int|str|float]): The input data to be binned.

        Raises:
        - Exception: If the number of bins is larger than the length of the data.

        Returns:
        - List[int|float]: List of mean values for each bin.
        """
        total_length = len(data)
        num_segments = self.n_bins

        if num_segments: # added to stop pylance from complaining 
            if total_length == num_segments:
                return data
            elif total_length < num_segments:
                return data
            segment_length = segment_length = total_length // num_segments
            remainder = total_length % num_segments
            
            start_index = 0
            end_index = 0
            segments = []
            for i in range(num_segments):
                end_index = start_index + segment_length + (1 if i < remainder else 0)
                segments.append(data[start_index:end_index])
                start_index = end_index

            return [mean(segment) for segment in segments]
        return data

    ################################################################################################################
    #                                           Data preparation methods                                           #
    ################################################################################################################

    def prepare_data_general(self) -> Dict[str, Dict[str, Tuple[np.ndarray, np.ndarray, int]]]:
        """
        Prepare data for plotting general features. More specifically, group the number of reads 
        and mean quality at each given position by their reference sequence. Calculate the median 
        for each group. The grouped data is then condensed into a set number of bins and scaled 
        between 0 and 1 for easier comparisons. Also calculates the number of positions for each
        sequence. 
        If more than one sequences are found in the data, calculate each statistic for all positions.
        Dictionary is sorted by referenece sequences.

        Returns:
        - Dict[str, Dict[str, Tuple[np.ndarray, np.ndarray, int]]]: Dictionary containing the condensed data.
        """

        data_grouped = defaultdict(lambda: {"n_reads": [], "q_mean": [], "count": 0})

        # group the data by sequence names
        for sequence_name, n_reads, q_mean in zip(self.data["chr"],
                                            self.data["n_reads"],
                                            self.data["q_mean"]):
            data_grouped[sequence_name]["n_reads"].append(n_reads) # type: ignore
            data_grouped[sequence_name]["q_mean"].append(q_mean) # type: ignore
            data_grouped[sequence_name]["count"] += 1 # type: ignore

        # add the total entry only if multiple sequences are present 
        # otherwise the same information is show for total and the single sequence
        if len(data_grouped.keys()) > 1:
            data_grouped["Total"]["n_reads"] = self.data["n_reads"]
            data_grouped["Total"]["q_mean"] = self.data["q_mean"]
            data_grouped["Total"]["count"] = len(self.data["q_mean"])

        data_grouped = dict(data_grouped)

        # condense the data into n_bins number of bins for more compact plot size later on
        n_bins = 100
        
        for sequence_name in data_grouped.keys():
            for c in ["n_reads", "q_mean"]:
                median = np.median(data_grouped[sequence_name][c])
                bin_value, bin_range = np.histogram(data_grouped[sequence_name][c], bins=n_bins, density=True)
                # scale bin values between 0 and 1
                # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html
                bin_value_scaled = (bin_value-bin_value.min()) / (bin_value.max()-bin_value.min()) 
                # replace the raw count by the bins, the scaled frequencies and the median value
                data_grouped[sequence_name][c] = (bin_range, bin_value_scaled, median) # type: ignore
        
        # data_grouped = dict(sorted(data_grouped.items()))
        return data_grouped # type: ignore

    def prepare_data_mism_general(self) -> Dict[str, Tuple[int|List[float], int|List[float], int|List[float]]]:
        """
        Prepare mismatch data for plotting general mismatch information.

        Returns:
        - Dict[str, Tuple[int|List[float], int|List[float]]]: Dictionary containing binned or original mismatch data.
        """
        data_mis = {"mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "refskip_rate": []}
        data_del = {"mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "refskip_rate": []}
        data_mat = {"mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "refskip_rate": []}

        for d in zip(self.data["ref_base"], 
                     self.data["majority_base"], 
                     self.data["mismatch_rate"], 
                     self.data["deletion_rate"], 
                     self.data["insertion_rate"],
                     self.data["refskip_rate"]):
            if d[0] == d[1]:
                data_mat["mismatch_rate"].append(d[2])
                data_mat["deletion_rate"].append(d[3])
                data_mat["insertion_rate"].append(d[4])
                data_mat["refskip_rate"].append(d[5])
            elif d[1] == "-":
                data_del["mismatch_rate"].append(d[2])
                data_del["deletion_rate"].append(d[3])
                data_del["insertion_rate"].append(d[4])
                data_del["refskip_rate"].append(d[5])
            else:
                data_mis["mismatch_rate"].append(d[2])
                data_mis["deletion_rate"].append(d[3])
                data_mis["insertion_rate"].append(d[4])
                data_mis["refskip_rate"].append(d[5])

        data_dict = {}
        data_dict["overall"] = (len(data_mat["mismatch_rate"]), len(data_mis["mismatch_rate"]), len(data_del["mismatch_rate"]))
        for mismatch_type in ["mismatch_rate", "deletion_rate", "insertion_rate", "refskip_rate"]:
            if self.n_bins is not None:
                if len(data_mat[mismatch_type]) > self.n_bins:
                    data_mat[mismatch_type] = self.bin_data(data_mat[mismatch_type])
                if len(data_mis[mismatch_type]) > self.n_bins:
                    data_mis[mismatch_type] = self.bin_data(data_mis[mismatch_type])
                if len(data_del[mismatch_type]) > self.n_bins:
                    data_del[mismatch_type] = self.bin_data(data_del[mismatch_type])
            data_dict[mismatch_type] = (data_mat[mismatch_type], data_mis[mismatch_type], data_del[mismatch_type])

        return data_dict

    def prepare_data_mism_types(self) -> Tuple[Dict[str, Dict[str, int]], Dict[str, Dict[str, List[str|float]]]]:
        """
        Prepare general data for mismatch type plots.

        Returns:
        - Tuple[Dict[str, Dict[str, int]], Dict[str, List[str|float]]]: 
        Tuple containing data the heatmap and box plots for mismatch types analysis.
        """
        mis_count = {"A": {"A": 0, "C": 0, "G": 0, "U": 0, "Del": 0}, 
                    "C": {"A": 0, "C": 0, "G": 0, "U": 0, "Del": 0}, 
                    "G": {"A": 0, "C": 0, "G": 0, "U": 0, "Del": 0}, 
                    "U": {"A": 0, "C": 0, "G": 0, "U": 0, "Del": 0}}
        mis_rates= {"A": {"mismatch_type": [], "mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "refskip_rate": []}, 
                    "C": {"mismatch_type": [], "mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "refskip_rate": []}, 
                    "G": {"mismatch_type": [], "mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "refskip_rate": []}, 
                    "U": {"mismatch_type": [], "mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "refskip_rate": []}}

        for ref, maj, *error_rates in zip(self.data["ref_base"], 
                                          self.data["majority_base"], 
                                          self.data["mismatch_rate"], 
                                          self.data["deletion_rate"], 
                                          self.data["insertion_rate"], 
                                          self.data["refskip_rate"]):
            if (ref != "N") & (maj != "N"):
                if maj=="-": maj="Del"
                mis_count[ref][maj] += 1
                if ref != maj:
                    mis_rates[ref]["mismatch_type"].append(f"{ref}-{maj}")
                    mis_rates[ref]["mismatch_rate"].append(error_rates[0])
                    mis_rates[ref]["deletion_rate"].append(error_rates[1])
                    mis_rates[ref]["insertion_rate"].append(error_rates[2])
                    mis_rates[ref]["refskip_rate"].append(error_rates[3])

        return mis_count, mis_rates

    def prepare_data_motifs(self) -> Tuple[Dict[str, Dict[str, List[str|float]]], Dict[str, int]]:
        """
        Prepare data for motif-wise error rate plotting.

        Returns:
        - Tuple[Dict[str, Dict[str, List[str|float]]], Dict[str, int]]: Dictionary containing error rates for each motif 
            and a dictionary containing the number of occurences for each motif
        """
        motif_error_rates = defaultdict(lambda: {"mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "refskip_rate": []})

        # extract the data for each 3 base-pair motif; store error rates in dict by motifs
        motif_center_idx = len(self.data["motif"][0]) // 2
        for motif, *error_rates in zip(self.data["motif"], self.data["mismatch_rate"], self.data["deletion_rate"], self.data["insertion_rate"], self.data["refskip_rate"]):
            motif_3bp = motif[motif_center_idx-1:motif_center_idx+2]
            for i, err_type in enumerate(["mismatch_rate", "deletion_rate", "insertion_rate", "refskip_rate"]):
                motif_error_rates[motif_3bp][err_type].append(error_rates[i])
        motif_error_rates = dict(motif_error_rates)

        # get the count for each motif before subsetting the data
        motif_counts = {}
        for motif in motif_error_rates.keys():
            motif_counts[motif] = len(motif_error_rates[motif]["mismatch_rate"])

        # subsample data for each error rate for each motif
        if self.n_bins is not None:
            for motif in motif_error_rates.keys():
                if len(motif_error_rates[motif]["mismatch_rate"]) > self.n_bins:
                    for err_type in ["mismatch_rate", "deletion_rate", "insertion_rate", "refskip_rate"]:
                        motif_error_rates[motif][err_type] = self.bin_data(motif_error_rates[motif][err_type])

        # sort dict by motif
        motif_error_rates = dict(sorted(motif_error_rates.items()))

        # set up data for each subplot (i.e. center A, C, G, U)
        center_base_error_rates = defaultdict(lambda: {"motif": [], "mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "refskip_rate": []})
        for motif, error_rates in motif_error_rates.items():
            center_base = motif[1]
            if center_base == "N": continue # only subplots for center A, C, G, U
            num_sites = len(error_rates["mismatch_rate"])
            center_base_error_rates[center_base]["motif"] += [motif] * num_sites
            for i, err_type in enumerate(["mismatch_rate", "deletion_rate", "insertion_rate", "refskip_rate"]):
                center_base_error_rates[center_base][err_type] += error_rates[err_type]

        return dict(center_base_error_rates), motif_counts
    
    ##############################################################################################################
    #                                             Plotting functions                                             #
    ##############################################################################################################

    def create_error_placeholder(self, e: Exception):
        """
        Create a placeholder plot with an error message.

        Parameters:
        - e (Exception): The exception that occurred.

        Returns:
        - fig: Plotly Figure: Placeholder figure with an error message.
        """
        hs.print_update(f"An error occured: {str(e)}. Replacing plot with empty placeholder. ", with_time=False, line_break=False)
        fig = self.update_plot(make_subplots(rows=1, cols=1))
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='text', text=[f"An error occured: {str(e)}"]))
        fig.update_layout(
            dragmode=False,  # Disable panning
            hovermode='closest',  # Maintain hover behavior
            uirevision='true'  # Disable double-click autoscale
        )
        return fig

    def create_general_plot(self) -> go.Figure:
        """
        Create a general plot displaying coverage and quality distributions for each chromosome in a ridge plot.
        Figure contains three subplots: 1. Horizontal bar graph showing the number of positions for each reference
        sequence. 2. Ridge plot showing the coverage distributions for each reference sequence. 3. Ridge plot 
        showing the quality distributions for each reference sequence.

        Returns:
        - go.Figure: Plotly Figure for general plot.
        """

        def generate_colors(n: int) -> List[str]:
            """
            Generate a list of n colors in hex format, progressively lighter from #0f3957 to #beddf4.

            Parameters:
                - n (int): Number of colors to generate.

            Returns:
                List[str]: A list of n colors represented in hex format.
            """
            if n<=1: return ["#1f77b4"]
            start_color = (15, 57, 87)  # RGB values for #0f3957
            end_color = (190, 221, 244) # RGB values for #beddf4
            # Calculate the step size for each color channel
            step_r = (end_color[0] - start_color[0]) / (n - 1)
            step_g = (end_color[1] - start_color[1]) / (n - 1)
            step_b = (end_color[2] - start_color[2]) / (n - 1)
            colors = []
            for i in range(n):
                # Calculate the RGB values for the current step
                r = int(start_color[0] + step_r * i)
                g = int(start_color[1] + step_g * i)
                b = int(start_color[2] + step_b * i)
                # Convert the RGB values to hex format and append to the list
                colors.append('#{:02x}{:02x}{:02x}'.format(r, g, b))
            return colors

        try:
            data_grouped = self.prepare_data_general()

            offset = 0.8

            # Approach to figure is inspired by
            # https://python-graph-gallery.com/ridgeline-graph-plotly/
            fig = make_subplots(cols=3, shared_yaxes=True, horizontal_spacing = 0.01)

            n_sequences = len(data_grouped.keys())
            y_ticks = []
            show_legend = True
            y_offsets = [i*offset for i in range(n_sequences)][::-1]
            colors = generate_colors(n_sequences)

            fig = self.update_plot(fig, height=min(n_sequences*400, 1000), width=1200)

            # iterate through all keys from the data grouped by sequence 
            for y_offset, sequence_name, color in zip(y_offsets, data_grouped.keys(), colors):
                y = y_offset+offset/2
                y_ticks.append(y)
                x = data_grouped[sequence_name]["count"]
                # add number of positions per plot
                bar = go.Bar(x=[x], y=[y], orientation="h", name=sequence_name, showlegend=False, width=0.5, marker=dict(color=color, line_color="black", line_width=2))
                fig.add_trace(bar, row=1, col=1)

                # add number of reads and q_mean distribution subplots
                for col, c in zip([2,3], ["n_reads", "q_mean"]):
                    x = data_grouped[sequence_name][c][0]
                    y = data_grouped[sequence_name][c][1] + y_offset
                    hover_labels = data_grouped[sequence_name][c][1]
                    median = data_grouped[sequence_name][c][2]
                    
                    # line to cut off the fill color at the base (y_offset) of each distribution
                    line = go.Scatter(x=(x.min(), x.max()), y=(y_offset, y_offset), mode="lines", line_color="white", showlegend=False)
                    # line indicating the median value
                    median_line = go.Scatter(x=[median, median], y=[y_offset, y_offset+1], name=f"Median", mode="lines", line = dict(color="black", width=2, dash='dot'),
                                            legendgroup=1, showlegend=show_legend,
                                            hovertemplate="Median: %{x}")
                    if show_legend: show_legend = False

                    # distribution itself
                    hist = go.Scatter(x=x, y=y, fill='tonexty', name=sequence_name, customdata=hover_labels, showlegend=False, line_shape='spline', line_color="black", 
                                    fillcolor=color, hovertemplate="<br>".join(["Coverage: %{x:.1f}", "Density: %{customdata:.5f}"]))

                    fig.add_traces([line, hist, median_line], rows=[1,1,1], cols=[col, col, col])

            # update axes of subplots 
            fig.update_yaxes(showexponent = 'all',
                            exponentformat = 'e',
                            tickmode = "array",
                            tickvals = y_ticks,
                            ticktext = list(data_grouped.keys()), row=1, col=1)
            fig.update_xaxes(title=dict(text="Number of covered positions",  font=dict(size=20)), row=1, col=1)

            fig.update_yaxes(tickmode = "array", tickvals = [], row=1, col=2)
            fig.update_xaxes(title=dict(text="Number of reads",  font=dict(size=20)), row=1, col=2)

            fig.update_yaxes(tickmode = "array", tickvals = [], row=1, col=3)
            fig.update_xaxes(title=dict(text="Mean quality",  font=dict(size=20)), row=1, col=3)

            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, bgcolor='#f5f5f5', bordercolor='#000000', borderwidth=2))

        except Exception as e:
            fig = self.create_error_placeholder(e)

        return fig

    def create_mism_general_plot(self) -> go.Figure:
        """
        Create a general plot displaying mismatch frequencies, deletion frequencies, 
        insertion frequencies and reference skip frequencies at matched and mismatched sites, 
        and an overall pie chart.

        Returns:
        - go.Figure: Plotly Figure for general mismatch plot.
        """
        try:
            def boxplot(data, group: str = "match", showlegend: bool = False):
                if group == "match":
                    name = "Match"
                    fillcolor = "#4c72b0"
                    legendgroup = "match"
                elif group == "mismatch":
                    name = "Mismatch"
                    fillcolor = "#dd8452"
                    legendgroup = "mism"
                else:
                    name = "Deletion"
                    fillcolor = "#2ca02c"
                    legendgroup = "del"
                return go.Box(y=data, name=name, marker=dict(color="black", outliercolor="black", size=2), 
                            fillcolor=fillcolor, showlegend=showlegend, legendgroup=legendgroup)

            data_processed = self.prepare_data_mism_general()

            fig = make_subplots(rows=1, cols=5, 
                                specs=[[{"type": "box"}, {"type": "box"}, {"type": "box"}, {"type": "box"}, {"type": "pie"}]], 
                                shared_yaxes=True,
                                horizontal_spacing=0.01,
                                column_titles=("Mismatch frequency", "Deletion frequency", "Insertion frequency", "Reference skip frequ.", None))
            fig = self.update_plot(fig, height=600, width=1200)

            for i, (dname, legend) in enumerate(zip(["mismatch_rate", "deletion_rate", "insertion_rate", "refskip_rate"], [True, False, False, False]), start=1):
                box_mat = boxplot(data_processed[dname][0], group="match", showlegend=legend)
                box_mis = boxplot(data_processed[dname][1], group="mismatch", showlegend=legend)
                box_del = boxplot(data_processed[dname][2], group="deletion", showlegend=legend)
                fig.add_traces([box_mat, box_mis, box_del], rows=1, cols=i)

            pie = go.Pie(labels=["Match", "Mismatch", "Deletion"], 
                        values=[data_processed["overall"][0], data_processed["overall"][1], data_processed["overall"][2]], 
                        hoverinfo="label+percent", 
                        textinfo="value", 
                        textfont_size=20, 
                        marker=dict(colors=["#4c72b0", "#dd8452", "#2ca02c"], line=dict(color="#000000", width=2)), 
                        showlegend=False,
                        sort=False)
            fig.add_trace(pie, row=1, col=5)

            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1, bgcolor='#f5f5f5', bordercolor='#000000', borderwidth=2))
            fig.update_annotations(font_size=21)
            fig.update_yaxes(showticklabels=False, ticks=None, row=1, col=2)
            fig.update_yaxes(showticklabels=False, ticks=None, row=1, col=3)
            fig.update_yaxes(showticklabels=False, ticks=None, row=1, col=4)

        except Exception as e:
            fig = self.create_error_placeholder(e)

        return fig

    def create_mism_types_plots(self) -> List[go.Figure]:
        """
        Create mismatch type plots including a confusion matrix, a pie chart, and a box plot.

        Returns:
        - List[go.Figure]: List of Plotly Figures for mismatch type plots.
        """
        try:
            mis_count, mis_rates = self.prepare_data_mism_types()
        except Exception as e:
            fig = self.create_error_placeholder(e)
            fig = fig
            return [fig, fig, fig]

        try:
            fig = go.Figure()
            fig = self.update_plot(fig, ylab="Reference base", xlab="Called base")

            counts = [[mis_count[row][col] for col in ["A", "C", "G", "U", "Del"]] for row in ["A", "C", "G", "U"]]
            # excluding the colorscaling for the match counts (usually many more than mismatches --> better color scaling)
            max_count = max([mis_count[row][col] for row in ["A", "C", "G", "U"] for col in ["A", "C", "G", "U", "Del"] if row!=col])
            heatmap = go.Heatmap(x=["A", "C", "G", "U", "Del"],
                                y=["A", "C", "G", "U"],
                                z=counts,
                                colorscale="portland",
                                hoverinfo="z",
                                hovertemplate="%{y}-%{x}<br>Count: %{z}",
                                zmin=0,
                                zmax=max_count,
                                name="",
                                colorbar=dict(title="Count"))
            heatmap.update(dict(showscale=True))
            fig.add_trace(heatmap)

            # Add text annotations
            total_count = sum([sum(mis_count[row].values()) for row in mis_count.keys()])
            annotations = []
            for i, row in enumerate(["A", "C", "G", "U"]):
                for j, col in enumerate(["A", "C", "G", "U", "Del"]):
                    # add black border around each cell
                    fig.add_shape(type="rect",
                            x0=j - 0.5, y0=i - 0.5,
                            x1=j + 0.5, y1=i + 0.5,
                            line=dict(color="#000000", width=1),
                            fillcolor="rgba(0,0,0,0)",
                            xref="x", yref="y")
                    # add percent values as annotations to each cell
                    annotations.append(
                        dict(
                            x=j, y=i,
                            text=f"{(mis_count[row][col] / total_count)*100:.2f}%",
                            showarrow=False,
                            font=dict(color="#000000"),
                            xref="x",
                            yref="y"
                        )
                    )

            fig.update_layout(annotations=annotations)
            matrix = fig

        except Exception as e:
            fig = self.create_error_placeholder(e)
            matrix = fig

        try:
            fig = make_subplots(rows=2, cols=2, shared_yaxes=True, vertical_spacing=0.1, horizontal_spacing=0.05)
            fig = self.update_plot(fig, width=1200, height=1000)

            show_legend = True
            for i, (row, col) in zip(["A", "C", "G", "U"], [(1,1), (1,2), (2,1), (2,2)]):
                x = mis_rates[i]["mismatch_type"]
                for group, (feature_name, feature_label, color) in enumerate([("mismatch_rate", "Mismatch rate", "#55a868"),
                                                                            ("deletion_rate", "Deletion rate", "#c44e52"), 
                                                                            ("insertion_rate", "Insertion rate", "#8172b3"), 
                                                                            ("refskip_rate", "Reference skip rate", "#937860")]):
                    # https://community.plotly.com/t/grouped-boxplots-in-subplots-have-gaps-in-the-x-axis/46736/6
                    box = go.Box(x=x, y=mis_rates[i][feature_name], name=feature_label, showlegend=show_legend, legendgroup=group, offsetgroup=group, 
                                line=dict(color="black"), marker=dict(outliercolor="black", size=2), fillcolor=color)
                    fig.add_trace(box, row=row, col=col)

                if show_legend: show_legend=False

            fig.update_layout(boxmode="group",
                            boxgap=0.1,
                            boxgroupgap=0,
                            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1.0, bgcolor='#f5f5f5', bordercolor='#000000', borderwidth=2))

            fig.update_xaxes(categoryorder='array', categoryarray=["A-C", "A-G", "A-U", "A-Del"], row=1, col=1)
            fig.update_xaxes(categoryorder='array', categoryarray=["C-A", "C-G", "C-U", "C-Del"], row=1, col=2)
            fig.update_xaxes(title="Mismatch type", categoryorder='array', categoryarray=["G-A", "G-C", "G-U", "G-Del"], row=2, col=1)
            fig.update_xaxes(title="Mismatch type", categoryorder='array', categoryarray=["U-A", "U-C", "U-G", "U-Del"], row=2, col=2)

            fig.update_yaxes(title="Error rate", row=1, col=1)
            fig.update_yaxes(title="Error rate", row=2, col=1)

            box = fig

        except Exception as e:
            fig = self.create_error_placeholder(e)
            box = fig

        return [matrix, box]
    
    def create_motif_plot(self) -> Tuple[go.Figure, go.Figure]:
        """
        Create a plot showing error rates for different motifs and a plot showing the corresponding 
        counts for each motif. The plots are grouped into four subplots for each center base.

        Returns:
        - Tuple[go.Figure, go.Figure]: Plotly Figure for the error rates by motif and the motif counts.
        """
        try: 
            motif_data, motif_counts = self.prepare_data_motifs()
        except Exception as e:
            return self.create_error_placeholder(e), self.create_error_placeholder(e)
        
        x_order = {"A": ["AAA", "AAC", "AAG", "AAU", "CAA", "CAC", "CAG", "CAU", "GAA", "GAC", "GAG", "GAU", "UAA", "UAC", "UAG", "UAU"], 
                   "C": ["ACA", "ACC", "ACG", "ACU", "CCA", "CCC", "CCG", "CCU", "GCA", "GCC", "GCG", "GCU", "UCA", "UCC", "UCG", "UCU"],
                   "G": ["AGA", "AGC", "AGG", "AGU", "CGA", "CGC", "CGG", "CGU", "GGA", "GGC", "GGG", "GGU", "UGA", "UGC", "UGG", "UGU"],
                   "U": ["AUA", "AUC", "AUG", "AUU", "CUA", "CUC", "CUG", "CUU", "GUA", "GUC", "GUG", "GUU", "UUA", "UUC", "UUG", "UUU"]}
        
        # create subplots showing the error rates for different 3bp motifs
        try:   
            rates_fig = make_subplots(rows=2, cols=2, 
                                    specs=[[{"type": "box"}, {"type": "box"}], [{"type": "box"}, {"type": "box"}]], 
                                    shared_yaxes=True, 
                                    vertical_spacing=0.1, horizontal_spacing=0.05)
            rates_fig = self.update_plot(rates_fig, height=900, width=1200)

            for center_base, row, col in zip(["A", "C", "G", "U"], [1,1,2,2], [1,2,1,2]):
                d = motif_data[center_base]
                traces = []
                for i, (err_type, name, color) in enumerate(zip(["mismatch_rate", "deletion_rate", "insertion_rate", "refskip_rate"], ["Mismatch", "Deletion", "Insertion", "Reference skip"], ["#55a868", "#c44e52", "#8172b3", "#937860"])):
                    trace = go.Box(x=d["motif"], y=d[err_type], name=name, 
                                line=dict(color="black", width=1), 
                                marker=dict(outliercolor="black", size=1), 
                                fillcolor=color,
                                legendgroup=i,
                                showlegend=True if center_base == "A" else False,
                                offsetgroup=i)
                    traces.append(trace)

                rates_fig.add_traces(traces, rows=row, cols=col)
                rates_fig.update_xaxes(categoryorder='array', categoryarray=x_order[center_base], row=row, col=col)

            rates_fig.update_layout(boxmode="group", boxgroupgap=0, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor='#f5f5f5', bordercolor='#000000', borderwidth=2))
            rates_fig.update_xaxes(title = "3bp Motif", row=2, col=1)
            rates_fig.update_xaxes(title = "3bp Motif", row=2, col=2)
            rates_fig.update_yaxes(title = "Error rate", row=1, col=1)
            rates_fig.update_yaxes(title = "Error rate", row=2, col=1)
        except Exception as e:
            rates_fig = self.create_error_placeholder(e)

        # create subplots showing counts of the different 3bp motifs
        try: 
            counts_fig = make_subplots(rows=2, cols=2, 
                                    specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]], 
                                    shared_yaxes=True, 
                                    vertical_spacing=0.15, horizontal_spacing=0.05)
            counts_fig = self.update_plot(counts_fig, height=600, width=1200)

            for center_base, row, col in zip(["A", "C", "G", "U"], [1,1,2,2], [1,2,1,2]):
                x = x_order[center_base]
                y = [motif_counts[motif] if motif in motif_counts.keys() else 0 for motif in x]
                bar = go.Bar(x=x, y=y, name=f"Center {center_base}", showlegend=False,
                            marker=dict(color="#A0A0A0", line_color="#000000", line_width=2))
                counts_fig.add_trace(bar, row=row, col=col)

            counts_fig.update_xaxes(title = "3bp Motif", row=2, col=1)
            counts_fig.update_xaxes(title = "3bp Motif", row=2, col=2)
            counts_fig.update_yaxes(title = "Count", row=1, col=1)
            counts_fig.update_yaxes(title = "Count", row=2, col=1)
        except Exception as e:
            counts_fig = self.create_error_placeholder(e)
        
        return rates_fig, counts_fig

    ################################################################################################################
    #                                               Create HTML file                                               #
    ################################################################################################################
    def write_svg(self, fig: go.Figure, name: str) -> None:
        """
        Write the Plotly Figure to an SVG file.

        Args:
        - fig (go.Figure): Plotly Figure.
        - name (str): Name to include in the output SVG file.

        Returns:
        - None
        """
        outpath = f"{os.path.splitext(self.output_path)[0]}_{name}.svg"
        fig.write_image(outpath)

    def figs_to_str(self, plot_figs: List[go.Figure]) -> List[str]:
        """
        Convert a list of Plotly Figures to their HTML string representation.

        Args:
        - plot_figs (List[go.Figure]): List of Plotly Figures.

        Returns:
        - List[str]: List of HTML strings representing the Plotly Figures.
        """
        plot_str = list(map(lambda x: to_html(x, include_plotlyjs=False, full_html=False), plot_figs))
        return plot_str

    def write_to_html(self, n_positions, n_chr, plot_figs: List[go.Figure]) -> None:
        """
        Generate an HTML summary page with collapsible sections for different types of analysis.
        
        Parameters:
        - n_positions (int): Total number of positions extracted.
        - n_chr (int): Total number of chromosomes.
        - plot_figs (List[go.Figure]): List of Plotly figures for different analyses.

        The function exports SVG versions of the Plotly figures if `export_svg` is True.

        The HTML template includes collapsible sections for general statistics, mismatch statistics,
        error rates by motifs, and more. Each section contains relevant Plotly charts and informative text.

        The final HTML template is written to the specified `output_path`.

        Returns:
        None
        """
        if self.export_svg:
            for fig, name in zip(plot_figs, ["summary_general_info", "summary_chr_info", "summary_mismatch_stats", 
                                             "summary_mismatch_matrix", "summary_mismatch_pie", 
                                             "summary_error_rates_by_mismatch", "summary_error_rates_by_motif"]):
                self.write_svg(fig, name)
        plots = self.figs_to_str(plot_figs)

        css_string, plotly_js_string = hs.load_html_template_str()

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_point_descr = f"Each data point corresponds to the average value along all positions in one of {self.n_bins} bins" if self.n_bins else "Each data point corresponds to one extracted position"
        template = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Neet - Position extractor summary</title>
                        <style>{css_string}</style>
                    </head>

                    <body>
                        <script>{plotly_js_string}</script>

                        <header>
                            <h1>Pileup extractor summary</h1>
                            <p>Produced by <a href="https://github.com/dietvin/neet">Neet</a> on <b>{time}</b></p>
                        </header>
                    
                        <section>
                            <p class="intro-text">
                                This summary file was created from the extracted features in file <b>{self.input_path}</b>. 
                                {f"Data was averaged into <b>{self.n_bins}</b> bins to allow for better performance." if self.n_bins else ""}
                                In total <b>{n_positions}</b> positions were extracted along <b>{n_chr}</b> {"sequences" if n_chr > 1 else "sequence"}. 
                                The plots are interactive and provide further information by hovering, zooming and panning.
                            </p>
                        </section>

                        <section>
                            <button class="collapsible">General statistics</button>
                            <div class="collapsible-content">
                                <h2 class="hiddentitle" id="general_statistics"></h2>

                                <h3>Number of covered sites, coverage- and quality distribtions of all sequences</h3>
                                <div class="plot-container">
                                    {plots[0]}
                                </div>
                                <p>
                                    For each reference sequence: Number of covered positions (<b>left</b>) and distributions of coverage (<b>middle</b>) 
                                    and mean quality (<b>right</b>) at these positions. The distributions show the probability density scaled to values
                                    between 0 and 1 for each sequence separately for easy comparison. The mean quality at a given position x is 
                                    calculated from the quality scores from all mapped reads at this position.
                                </p>
                        </section>

                        <section>
                            <button class="collapsible">Mismatch statistics</button>
                            <div class="collapsible-content">
                                <h2 class="hiddentitle" id="mismatch_statistics"></h2>

                                <h3>Mismatch, deletetion and insertion rates for matched and mismatched positions</h3>
                                <div class="plot-container">
                                    {plots[1]}
                                </div>
                                <p>
                                    Overview of the number of mismatches and what types of errors contribute to them. Match refers to the positions where the correct base was called. 
                                    Mismatch refers to the positions where the wrong base was called. The pie chart on the right shows the number of matched and mismatched positions
                                    along all chromosomes. The boxplots on the left show the distributions of the mismatch (<b>leftmost</b>), deletion (<b>second from left</b>), insertion (<b>second from right</b>)
                                    and reference skip (<b>right</b>) rates at matched and mismatched positions. {data_point_descr}.
                                </p>

                                <h3>Abundances of different type of mismatches</h3>

                                <h4>Mismatch/Deletion counts</h4>
                                <div class="plot-container">
                                    {plots[2]}
                                </div>
                                <p>
                                    Abundance of matches by base (diagonal) and all types of mismatches <i>from Reference base to Called base</i>. Warmer colors indicate higher counts.
                                </p>
                            
                                <h3>Mismatch, deletion and insertion rates by type of mismatch</h3>
                                <div class="plot-container">
                                    {plots[3]}
                                </div>
                                <p>
                                    Distribtions of Mismatch, Deletion, Insertion and Refernce skip rates for each observed mismatch type (<i>[FROM] - [TO]</i>).
                                    Plots are split by central A (<b>top left</b>), C (<b>top right</b>), G (<b>bottom left</b>) and U (<b>bottom right</b>)
                                    Each data point corresponds to one position.
                                </p>
                            </div>
                        </section>

                        <section>
                            <button class="collapsible">Error rate by motifs</button>
                            <div class="collapsible-content">
                                <h2 class="hiddentitle" id="error_motif"></h2>

                                <h3>Mismatch, insertion, deletion and reference skip rates for 3bp motifs</h3>
                                <div class="plot-container">
                                    {plots[4]}
                                </div>
                                <p>
                                    Distributions of Mismatch, deletion and insertion rates for different three base motifs with center A (<b>top left</b>), C (<b>top right</b>),
                                    G (<b>bottom left</b>) and U (<b>bottom right</b>). {data_point_descr}.
                                </p>

                                <h3>Number of positions for each 3bp motif</h3>
                                <div class="plot-container">
                                    {plots[5]}
                                </div>
                                <p>
                                    Number of positions for each three base motifs with center A (<b>top left</b>), C (<b>top right</b>),
                                    G (<b>bottom left</b>) and U (<b>bottom right</b>).
                                </p>

                            </div>
                        </section>

                        <script>
                            var coll = document.getElementsByClassName("collapsible");
                            var i;

                            for (i = 0; i < coll.length; i++) {{
                            coll[i].addEventListener("click", function() {{
                                this.classList.toggle("active");
                                var content = this.nextElementSibling;
                                if (content.style.display === "none") {{
                                content.style.display = "block";
                                }} else {{
                                content.style.display = "none";
                                }}
                            }});
                            }}
                        </script>
                    </body>
                    <footer></footer>
                    </html> 
                    """
        with open(self.output_path, "w") as o:
            o.write(template)


if __name__=="__main__":
    s = SummaryCreator(in_path="/home/vincent/projects/neet_project/data/45s_rrna/test/drna_cyt_extracted.tsv", export_svg=True)
    s.main()
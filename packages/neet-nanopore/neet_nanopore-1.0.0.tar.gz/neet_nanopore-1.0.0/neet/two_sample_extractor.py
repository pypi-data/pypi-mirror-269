from typing import List, Dict, Any, Tuple, Set
import os, sys, datetime, math
from collections import Counter, defaultdict
import plotly.graph_objects as go
from plotly.io import to_html

try: # when invoked from the package
    from neet import helper_functions as hs
except ImportError: # when invoked directly
    import helper_functions as hs

SITE = Tuple[str, int]

class PositionExtractor:
    out_dir: str
    export_svg: bool

    in_paths_a: List[str]
    in_paths_b: List[str]

    label_a: str
    label_b: str

    error_feature_idx: int
    error_threshold: float
    coverage_threshold: int

    ref_path: str
    n_bins_seqmap: int

    a_and_b: List[SITE]
    a_excl: List[SITE]
    b_excl: List[SITE]

    def __init__(self, 
                 in_paths_a: str, 
                 in_paths_b: str, 
                 ref_path: str, 
                 out_dir: str | None = None, 
                 error_feature: str = "mismatch_alt", 
                 error_threshold: float = 0.5, 
                 coverage_threshold: int = 40, 
                 label_a: str = "sample_a", 
                 label_b: str = "sample_b", 
                 export_svg: bool = False, 
                 n_bins_seqmap: int = 200) -> None:
        """
        Initialize the PositionExtractor object with input parameters.

        Parameters:
        - in_paths_a (str): Comma-separated string of file paths for dataset A.
        - in_paths_b (str): Comma-separated string of file paths for dataset B.
        - out_dir (str): Output directory for the extracted data.
        - ref_path (str): File path to the reference data in FASTA format.
        - error_feature (str): The type of error feature to be analyzed. One of: mismatch, mismatch_alt, deletion, insertion. (Default: "mismatch")
        - error_threshold (float): Threshold for the specified error feature. (Default: 0.5)
        - coverage_threshold (int): Threshold for the coverage of positions to be considered. (Default: 10)
        - label_a (str): Label for dataset A. (Default: "sample_a")
        - label_b (str): Label for dataset B. (Default: "sample_b")
        - export_svg (bool, optional): Flag indicating whether to export SVG plots (Default: False).

        Raises:
        - Exception: If an invalid error feature is provided.
        """
        self.in_paths_a = self.process_in(in_paths_a)
        self.in_paths_b = self.process_in(in_paths_b)

        if out_dir:
            out_dir = os.path.abspath(out_dir)
            ext = os.path.splitext(out_dir)[1]
            if ext:
                hs.print_update(f"Warning: Extension {ext} was found. Make sure to provide a single output directory.")
            hs.check_create_dir(out_dir)
            self.out_dir = out_dir
        else:
            self.out_dir = os.path.dirname(self.in_paths_a[0])

        self.export_svg = export_svg

        self.label_a = label_a
        self.label_b = label_b
        
        try:
            feature_idx = {"deletion": 16,
                           "insertion": 17,
                           "mismatch": 19,
                           "mismatch_alt": 20}
            self.error_feature_idx = feature_idx[error_feature]
        except KeyError:
            raise Exception(f"Invalid error feature '{error_feature}'. Use one of: mismatch, mismatch_alt, deletion, insertion")

        self.error_threshold = error_threshold
        self.coverage_threshold = coverage_threshold

        self.ref_path = ref_path
        self.n_bins_seqmap = n_bins_seqmap

    ##############################################################################################################
    #                                           Initialization methods                                           #
    ##############################################################################################################

    def process_in(self, in_paths: str) -> List[str]:
        """
        Process a comma-separated string of input file paths.

        Parameters:
        - in_paths (str): A comma-separated string of input file paths.

        Returns:
        - in_list (List[str]): A list of validated input file paths.

        Raises:
        - Exception: If any input file does not exist or has an unexpected file extension.
        - Exception: If input files are of different kinds (either .bam or .pileup). All files must be of the same kind.
        """
        in_list = [os.path.abspath(p) for p in in_paths.split(",")]
        extensions = []
        for path in in_list:
            ext = os.path.splitext(path)[1]
            extensions.append(ext)
            hs.check_input_path(path, extensions=[".tsv"])

        if len(set(extensions)) > 1:
            raise Exception("Input files of different kind. All files must be .bam or .pileup, not mixed.")
        return in_list

    ##############################################################################################################
    #                                             Processing methods                                             #
    ##############################################################################################################

    def extract_positions(self) -> None:
        """
        Extract positions based on coverage and error thresholds, identify systematic positions 
        (i.e. those that are found in all replicates), and categorize them into overlapping and 
        exclusive sets for datasets A and B. Identified positions are stored in the a_and_b, 
        a_excl and b_excl member variables.
        """
        a_high_cvg, b_high_cvg, a_high_err, b_high_err = [], [], [], []
        for paths, high_cvg, high_err in [(self.in_paths_a, a_high_cvg, a_high_err), (self.in_paths_b, b_high_cvg, b_high_err)]:
            for path in paths:
                hc, he = self.extract_suffient_cvg_pos(path)
                high_cvg.append(hc)
                high_err.append(he)

        a_high_cvg_syst = self.find_systematic_pos(a_high_cvg)
        del(a_high_cvg)
        a_high_err_syst = self.find_systematic_pos(a_high_err)
        del(a_high_err)

        b_high_cvg_syst = self.find_systematic_pos(b_high_cvg)
        del(b_high_cvg)
        b_high_err_syst = self.find_systematic_pos(b_high_err)
        del(b_high_err)

        a_and_b = set.intersection(a_high_err_syst, b_high_err_syst)
        # filter out positions that are exclusive because of high error rates (not insufficient coverage)
        a_excl = set.intersection(a_high_err_syst, b_high_cvg_syst-a_and_b)
        b_excl = set.intersection(b_high_err_syst, a_high_cvg_syst-a_and_b)

        self.a_and_b = sorted(a_and_b)
        self.a_excl = sorted(a_excl)
        self.b_excl = sorted(b_excl)

    def extract_suffient_cvg_pos(self, path: str) -> Tuple[List[SITE], List[SITE]]:
        """
        Extract positions with sufficient coverage and error rate from the specified input file.

        Parameters:
        - path (str): Path to the input file.

        Returns:
        - List[Tuple[str, int]]: Sites with high coverage (>=coverage threshold)
        - List[Tuple[str, int]]]: Sites with high coverage AND high error rate (>=error rate threshold)

        Note:
        - Uses the error feature index specified during object initialization.
        """
        hs.print_update(f"Processing {path} ... ", line_break=False)
        sys.stdout.flush()
        with open(path, "r") as file:
            high_cvg_sites = []
            high_cvg_high_err_sites = []

            next(file)
            for line in file:
                line = line.split("\t")
                chrom, site, n_reads, n_ref_skip, error_rate = line[0], int(line[1]), int(line[2]), int(line[11]), float(line[self.error_feature_idx])            
                if n_reads-n_ref_skip >= self.coverage_threshold:
                    high_cvg_sites.append((chrom, site)) 
                    if error_rate >= self.error_threshold:
                        high_cvg_high_err_sites.append((chrom, site))

            hs.print_update("done", with_time=False)

            return high_cvg_sites, high_cvg_high_err_sites

    def find_systematic_pos(self, replicate_pos: List[List[SITE]]) -> Set[SITE]:
        """
        Identify systematic positions that are common across multiple replicates.

        Parameters:
        - replicate_pos (List[List[Tuple[str, int]]]): List of lists, where each sublist contains coordinates from a given replicate.

        Returns:
        - List[Tuple[str, int]]: List of systematic positions.
        """
        # https://stackoverflow.com/questions/2541752/best-way-to-find-the-intersection-of-multiple-sets
        replicate_pos_set = [set(pos) for pos in replicate_pos]
        return set.intersection(*replicate_pos_set) # type: ignore

    def write_bed_files(self) -> None:
        """Write BED files for overlapping and exclusive positions."""
        self.positions_to_bed(self.a_and_b, self.out_dir, f"{self.label_a}_{self.label_b}")
        self.positions_to_bed(self.a_excl, self.out_dir, f"{self.label_a}_excl")
        self.positions_to_bed(self.b_excl, self.out_dir, f"{self.label_b}_excl")

    def positions_to_bed(self, positions: List[SITE], out_dir: str, name: str) -> None:
        """
        Write positions to a BED file.

        Parameters:
        - positions (Set[Tuple[str, int]]): Set of positions to be written.
        - out_dir (str): Output directory.
        - name (str): Name for the output BED file.
        """
        path = os.path.join(out_dir, f"{name}.bed")
        hs.print_update(f"Writing {len(positions)} sites to {path}")
        with open(path, "w") as out:
            for position in positions:
                chrom, site = position[0], position[1]
                out.write(f"{chrom}\t{site-1}\t{site}\t{name}\n")

    

    ##############################################################################################################
    #                                          Summary creation methods                                          #
    ##############################################################################################################

    def custom_sort_key(self, item) -> Tuple[int] | Tuple[float, Any]:
        """
        Define a custom sorting key for sorting mixed alphanumeric items.

        This method defines a custom sorting key that can be used with the `sorted()` function or other sorting functions.
        It allows for sorting a list of mixed alphanumeric items in a way that numeric values are sorted numerically,
        and non-numeric values are placed at the end of the sorted list.

        Parameters:
            item (str): The item to be sorted.

        Returns:
            tuple: A tuple used as a sorting key. The tuple consists of two elements:
            - If the item is numeric, its integer value is placed first to sort numerically.
            - If the item is not numeric, it is placed last with a float('inf') value to ensure it comes after numeric values.

        Example:
            To sort a list of mixed alphanumeric items, you can use this custom sorting key as follows:
            ```
            sorted_list = sorted(my_list, key=obj.custom_sort_key)
            ```
        """
        if item.isdigit():  # Check if the item is a digit
            return (int(item),)  # Convert to integer and sort numerically
        else:
            return (float('inf'), item)  # Place non-digits at the end

    def update_plot(self, fig, title: str|None = None, xlab: str|None = None, ylab: str|None = None, height: int = 500, width: int = 800) -> go.Figure:
        """
        Updates the layout of a Plotly figure.

        Parameters:
        - fig (go.Figure): The Plotly figure to be updated.
        - title (str | None): Title of the plot (optional).
        - xlab (str | None): Label for the x-axis (optional).
        - ylab (str | None): Label for the y-axis (optional).
        - height (int): Height of the plot (default: 500).
        - width (int): Width of the plot (default: 800).

        Returns:
        - go.Figure: The updated Plotly figure.
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

    def prepare_data_map(self) -> Tuple[List[float], Dict[str, Dict[str, List[int]]], Dict[str, Dict[str, List[int]]], Dict[str, List[int]]]:
        """
        Prepare data for generating a genomic sequence map.

        Returns:
        - List[float]: A list of y-values that function as the y-values between 0 and 1 for each bin.
        - Dict[str, Dict[str, List[int]]]: Nested dictionary containing the counts scaled between 0 and 255 for each 
                                            sequence (upper level) and group (lower level). Values for each group are 
                                            combined to create a RGB color based on the counts
        - Dict[str, Dict[str, List[int]]]: Nested dictionary containing the absolute counts for each sequence (upper 
                                            level) and group (lower level)
        - Dict[str, List[int]]: A dictionary mapping sequence names to lists of maximum values for bin boundaries.         
        """
        # transform the sets into dictionaries for easier data handling
        a_and_b_dict = defaultdict(lambda: [])
        a_excl_dict = defaultdict(lambda: [])
        b_excl_dict = defaultdict(lambda: [])
        for d, d_dict in [(self.a_and_b, a_and_b_dict), (self.a_excl, a_excl_dict), (self.b_excl, b_excl_dict)]:
            for seq, coord in d:
                d_dict[seq].append(coord)
        a_and_b_dict = dict(a_and_b_dict)
        a_excl_dict = dict(a_excl_dict)
        b_excl_dict = dict(b_excl_dict)

        # Calculate chromosome lengths
        def get_ref_len(ref_path: str) -> Dict[str, int]:
            """Reads reference file and extracts chromosome lengths."""
            with open(ref_path, "r") as ref:
                refs = {}
                line = next(ref)
                seq_name = line[1:].strip().split(" ")[0]
                seq_len = 0

                for line in ref:
                    if line.startswith(">"):
                        refs[seq_name] = seq_len
                        seq_name = line[1:].strip().split(" ")[0]
                        seq_len = 0
                    else:
                        seq_len += len(line.strip())
                refs[seq_name] = seq_len # add the last dict entry
            return refs
        ref_lens = get_ref_len(self.ref_path)

        # get sequences that are present (iterate over these only)
        present_seq = set(a_and_b_dict.keys()) | set(a_excl_dict.keys()) | set(b_excl_dict.keys())
        # initialize the counts for all three groups with zeroes
        counts = defaultdict(lambda: {f"{self.label_a}+{self.label_b}": [0]*self.n_bins_seqmap, self.label_a: [0]*self.n_bins_seqmap, self.label_b: [0]*self.n_bins_seqmap})
        bin_sizes = {} 
        max_vals = {} # stores the values for labelling the bins
        for seq in present_seq:
            seq_len = ref_lens[seq]

            bin_size = math.ceil(seq_len / self.n_bins_seqmap)
            bin_sizes[seq] = bin_size
            # initialize the maximum coordinates that a bin may contain (excluded)
            max_vals[seq] = [bin_size*i for i in range(1,self.n_bins_seqmap)] + [seq_len+1] 

            # fill the counts dictionary
            for d_dict, key in [(a_and_b_dict, f"{self.label_a}+{self.label_b}"), (a_excl_dict, self.label_a), (b_excl_dict, self.label_b)]:
                if seq in d_dict.keys():
                    for coord in d_dict[seq]:
                        bin_index = coord // bin_size
                        counts[seq][key][bin_index] += 1    
        counts = dict(counts)

        # scale the values between 0 and 255 to use as RGB values for each bin of the map
        counts_scaled = {}
        max_val_ab = max([max(counts[seq][f"{self.label_a}+{self.label_b}"]) for seq in present_seq])
        max_val_a = max([max(counts[seq][self.label_a]) for seq in present_seq])
        max_val_b = max([max(counts[seq][self.label_b]) for seq in present_seq])
        for seq in counts.keys():
            counts_scaled[seq] = {}
            for group, max_val in [(f"{self.label_a}+{self.label_b}", max_val_ab), (self.label_a, max_val_a), (self.label_b, max_val_b)]:
                scaled = [round(i/max_val * 255) if max_val>0 else 0 for i in counts[seq][group]]
                counts_scaled[seq][group] = scaled

        # Generate y-values for bin positions along the chromosome
        y_vals = [i/self.n_bins_seqmap for i in range(self.n_bins_seqmap)]

        return y_vals, counts_scaled, counts, max_vals

    def create_map_plot(self) -> go.Figure:
        """
        Create a genomic sequence map plot using Plotly.

        Returns:
        - go.Figure: A Plotly figure object representing the genomic sequence map.
        """
        y_vals, counts_scaled, counts, max_vals = self.prepare_data_map()
        fig = go.Figure()
        fig = self.update_plot(fig, width=1200, height=1000)
        tickvals = []
        ticktext = []
        bin_height = y_vals[1]
        # set up a map for each sequence that is present
        for x, seq in enumerate(counts.keys(), start = 1):
            tickvals.append(x)
            ticktext.append(seq)
            bin_start = [1]+max_vals[seq] # first position of a bin (included)
            bin_end = max_vals[seq] # last position of a bin (excluded)
            bins = []
            for y, r, g, b, count_ab, count_a, count_b, lab_start, lab_end in zip(y_vals, 
                                                                                counts_scaled[seq][f"{self.label_a}+{self.label_b}"], 
                                                                                counts_scaled[seq][self.label_a], 
                                                                                counts_scaled[seq][self.label_b], 
                                                                                counts[seq][f"{self.label_a}+{self.label_b}"], 
                                                                                counts[seq][self.label_a], 
                                                                                counts[seq][self.label_b], 
                                                                                bin_start, bin_end):
                # the fill color is determined by the number of shared and exclusive positions in a bin
                # red portion corresponds to the number of shared positions, green and blue to A excl. and 
                # b excl. respectively. I.e.: High red portion in the color of a bin -> more shared positions
                # and so on
                color = f"rgb({r},{g},{b})"
                # create a rectangle for each bin
                bin = go.Scatter(x=[x-0.3, x-0.3, x+0.3, x+0.3, x-0.3], 
                                y=[y,y+bin_height,y+bin_height,y,y], 
                                name=f"{lab_start}-{lab_end}<br>{self.label_a}+{self.label_b}: {count_ab}<br>{self.label_a}: {count_a}<br>{self.label_b}: {count_b}",
                                fill="toself", 
                                fillcolor=color,
                                marker=dict(color=color),
                                showlegend=False, mode='lines')
                bins.append(bin)
            # add rectangles of one sequence to figure
            fig.add_traces(bins)
            # surround rectangles by a shape as a border
            fig.add_shape(type="rect",
                        x0=x - 0.3, y0=0,
                        x1=x + 0.3, y1=1,
                        line=dict(color="#000000", width=3),
                        fillcolor="rgba(0,0,0,0)",
                        xref="x", yref="y")

        fig.update_xaxes(tickmode = 'array',
                        tickvals = tickvals,
                        ticktext = ticktext)
        fig.update_yaxes(tickmode = 'array',
                        tickvals = [0,1],
                        ticktext = ["5'", "3'"])
        fig.update_xaxes(range=[0.5,tickvals[-1]+0.5])

        # clean up hoverlabels
        fig.update_layout(hoverlabel=dict(namelength=0)) 
        return fig

    def get_file_paths(self) -> Tuple[str, str]:
        """
        Get formatted HTML lists of input file paths for datasets A and B.

        Returns:
        - Tuple[str, str]: Formatted HTML lists of file paths for datasets A and B.
        """
        def create_list(paths: List[str]):
            path_list = "<ul>"
            for path in paths:
                path_list += f"<li>{path}</li>"
            path_list += "</ul>"
            return path_list
        
        return create_list(self.in_paths_a), create_list(self.in_paths_b)

    def create_count_table(self) -> str:
        """
        Create an HTML table showing the counts of occurrences of chromosomes in each set.

        Returns:
        - str: The HTML representation of the count table.
        """
        # Count occurrences of chromosomes in each set
        a_and_b_counts = Counter(chromosome for chromosome, _ in self.a_and_b)
        a_excl_counts = Counter(chromosome for chromosome, _ in self.a_excl)
        b_excl_counts = Counter(chromosome for chromosome, _ in self.b_excl)

        # Get all unique chromosomes from the sets
        all_chromosomes = set(a_and_b_counts.keys()) | set(a_excl_counts.keys()) | set(b_excl_counts.keys())

        # Create HTML table
        html_table = """
        <table border="1">
        <thead><tr>
            <th></th>
        """

        # Add column headers
        for chromosome in all_chromosomes:
            html_table += f"<th>{chromosome}</th>"
        html_table += "<th>Total</th></tr></thead><tbody>"

        # Add rows and counts
        for set_name, counts in [(f'{self.label_a} + {self.label_b}', a_and_b_counts), (f'{self.label_a} excl.', a_excl_counts), (f'{self.label_b} excl.', b_excl_counts)]:
            html_table += f"<tr><td><b>{set_name}</b></td>"
            total_count = sum(counts.values())
            for chromosome in all_chromosomes:
                html_table += f"<td>{counts[chromosome]}</td>"
            html_table += f"<td>{total_count}</td></tr>"

        html_table += "</tbody></table>"
        return html_table
    
    def write_svg(self, fig: go.Figure, name: str) -> None:
        """
        Write a Plotly figure to an SVG file.

        Parameters:
        - fig (go.Figure): The Plotly figure to be written.
        - name (str): The name of the SVG file.
        """
        outpath = os.path.join(self.out_dir, f"{name}.svg")
        fig.write_image(outpath)

    def create_summary(self) -> None:
        """
        Create a summary HTML file containing an overview of shared and exclusive positions in samples A and B.

        This method generates a summary HTML file that includes information about the input files, a count table, and a genome map.

        If export_svg is True, the genome map is saved as an SVG file in the specified output directory.

        The HTML file is saved with the format: "<out_dir>/<label_a>_<label_b>_diff.html".
        """
        plot = self.create_map_plot()
        if self.export_svg:
            self.write_svg(plot, "twosample_map")
        
        plot = to_html(plot, include_plotlyjs=False)

        paths_1, paths_2 = self.get_file_paths()
        count_table = self.create_count_table()
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        css_string, plotly_js_string = hs.load_html_template_str()

        outpath = os.path.join(self.out_dir, f"{self.label_a}_{self.label_b}_diff.html")
        hs.print_update(f"Writing summary to {outpath}")
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
                            <h1>Position extractor summary</h1>
                            <p>Produced by <a href="https://github.com/dietvin/neet">Neet</a> on <b>{time}</b></p>
                        </header>
                    
                        <section>
                            <p class="intro-text">
                                This summary file contains an overview of the shared and exclusive positions in samples <i>{self.label_a}</i> and <i>{self.label_b}</i>.
                                Files provided for sample <i>{self.label_a}</i>:
                            </p>
                            {paths_1}
                            <p class="intro-text">Files provided for sample <i>{self.label_b}</i>:</p>
                            {paths_2}
                        </section>

                        <section>
                            <button class="collapsible">General information</button>
                            <div class="collapsible-content">
                                <h2 class="hiddentitle" id="general_information"></h2>
                                <h3>Count table</h3>
                                <p>
                                    Positions are only regarded if they are present in all replicates of a sample. The count table displays the number of individual genomic positions for different groups in each row. These groups are: 
                                    <ol>
                                        <li><i>{self.label_a}</i> + <i>{self.label_b}</i>:       Positions that are shared between samples {self.label_a} and {self.label_b}</li>
                                        <li><i>{self.label_a}</i> excl.:              Positions that are exclusive to sample {self.label_a}</li>
                                        <li><i>{self.label_b}</i> excl.:              Positions that are exclusive to sample {self.label_b}</li>
                                    </ol>
                                </p>
                                <div class="table-box">
                                    {count_table}
                                </div>
                            </div>
                        </section>

                        <section>
                            <button class="collapsible">Sequence map</button>
                            <div class="collapsible-content">
                                <h2 class="hiddentitle" id="genome_map"></h2>
                                <h3>Sequence map displaying shared and exclusive positions between samples <i>{self.label_a}</i> and <i>{self.label_b}</i></h3>
                                <div class="plot-container">
                                    {plot}
                                </div>
                                <p>
                                    Sequence map displaying the positions that are present in both samples, only in sample <i>{self.label_a}</i> and only in sample <i>{self.label_b}</i>.
                                    Sequences are split into {self.n_bins_seqmap} chunks of equal size. The color of a chunk is determined by the number of shared and exclusive positions,
                                    where the count of <span style="color:red;">shared positions</span> influences the <span style="color:red;">red</span> portion of a given RGB color, the count of 
                                    <span style="color:green;"><i>{self.label_a}</i>-exclusive positions</span> influence the <span style="color:green;">green</span> portion and 
                                    <span style="color:blue;"><i>{self.label_b}</i>-exclusive positions</span> influence the <span style="color:blue;">blue</span> portion. Higher counts in a given 
                                    category increases the intensity of the given color portion. Black indicates sequence segments where no high-coverage and high-error sites were indentified.
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
        with open(outpath, "w") as out:
            out.write(template)

    ##############################################################################################################
    #                                                Main method                                                 #
    ##############################################################################################################

    def main(self) -> None:
        """
        Execute the main workflow of the PositionExtractor class.

        This method performs the following tasks:
        1. Extract positions from input files.
        2. Write BED files for shared and exclusive positions.
        3. Create a summary HTML file containing an overview of shared and exclusive positions.
        """
        self.extract_positions()
        self.write_bed_files()
        self.create_summary()
        hs.print_update("Finished.")


if __name__=="__main__":
    e = PositionExtractor(in_paths_a="/home/vincent/projects/neet_project/testing/testing_pileup_extractor/data1/cyt1.tsv,/home/vincent/projects/neet_project/testing/testing_pileup_extractor/data1/cyt2.tsv,/home/vincent/projects/neet_project/testing/testing_pileup_extractor/data1/cyt3.tsv",
                          in_paths_b="/home/vincent/projects/neet_project/testing/testing_pileup_extractor/data1/nuc1.tsv,/home/vincent/projects/neet_project/testing/testing_pileup_extractor/data1/nuc2.tsv,/home/vincent/projects/neet_project/testing/testing_pileup_extractor/data1/nuc3.tsv",
                          ref_path="/home/vincent/projects/neet_project/testing/data1/ref/ref.fa")
    e.main()
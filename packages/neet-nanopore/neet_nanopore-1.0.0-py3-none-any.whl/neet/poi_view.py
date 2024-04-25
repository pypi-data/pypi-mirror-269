from typing import Tuple, List, Dict
import os, datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tqdm import tqdm

try: # when invoked from the package
    from neet import helper_functions as hs
except ImportError: # when invoked directly
    import helper_functions as hs

SITE = Tuple[str, int]

class POIView:
    positions: List[SITE]
    nb_size: int

    basename_a: str
    basename_b: str | None
    
    paths_a: List[str]
    paths_b: List[str] | None
    bed_path: str
    out_dir: str

    # see get_data method for details
    data: Dict[str, Dict[str, Dict[SITE, List[str]]]]

    export_svg: bool

    colors = {"A": "#2ca02c", "C": "#1f77b4", "G": "#ff7f0e", "U": "#d62728", 
              "match": "#9467bd", "mis": "#8c564b", "del": "#e377c2", 
              "ins": "#7f7f7f", "ref_skip": "#7f7f7f"}

    def __init__(self, 
                 paths_a: str, 
                 bed_path: str, 
                 out_dir: str | None = None, 
                 paths_b: str | None = None,
                 basename_a: str = "sample_a", 
                 basename_b: str = "sample_b", 
                 nb_size: int = 2, 
                 export_svg: bool = False) -> None:
        
        self.basename_a = basename_a
        self.basename_b = basename_b if paths_b else None

        hs.check_input_path(bed_path, extensions=[".bed"])
        self.get_positions(bed_path)
        self.bed_path = os.path.abspath(bed_path)
        self.basename_bed = os.path.splitext(os.path.basename(bed_path))[0]
        self.nb_size = nb_size

        self.export_svg = export_svg

        paths_a_list = self.process_in(paths_a)
        paths_b_list = self.process_in(paths_b) if paths_b else None
        self.paths_a = paths_a_list
        self.paths_b = paths_b_list

        if out_dir:
            out_dir = os.path.abspath(out_dir)
            ext = os.path.splitext(out_dir)[1]
            if ext:
                hs.print_update(f"Warning: Extension {ext} was found. Make sure to provide a single output directory.")
            hs.check_create_dir(out_dir)
            self.out_dir = out_dir
        else:
            self.out_dir = os.path.dirname(self.paths_a[0])

        self.get_data(paths_a_list, paths_b_list)

    ##########################################################################################################
    #                                  Methods called during initialization                                  #
    ##########################################################################################################
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

    def get_positions(self, bed_path: str) -> None:
        """
        Extract positions from the specified BED file.

        Parameters:
        - bed_path (str): The path to the BED file.

        Returns:
        - None
        """
        hs.print_update(f"Extracting positions from {bed_path}... ", line_break=False)
        with open(bed_path, "r") as bed_file:
            positions = []
            for line in bed_file:
                line = line.strip().split("\t")
                chrom, site = line[0], int(line[2])
                positions.append((chrom, site))
            hs.print_update(f"Found {len(positions)} sites.", with_time=False)
            self.positions = positions

    def get_data(self, paths_a: List[str], paths_b: List[str] | None) -> None:
        """
        Process input files to extract relevant data for both samples. Stores the data in a nested Dictionary of 
        the following format: Dict[str, Dict[str, Dict[Tuple[str, int], List[str]]]]
        - first level: sample
        - second level: replicate
        - third level: position (seq, site)
        
        For example, features of site (chrA, 100) in replicate 1 and sample A can be accessed via data[A][1][(chrA,100)].

        Parameters:
        - paths_a (List[str]): List of input file paths for sample A.
        - paths_b (List[str]): List of input file paths for sample B.

        Returns:
        - None
        """
        target_sites = set([(seq, site+i) for i in range(-self.nb_size, self.nb_size+1) for seq, site in self.positions])
        samples = [self.basename_a, self.basename_b]
        paths = [paths_a, paths_b]
        # collect data from given feature tables by sample (first level), replicates (second level) and position (seq, site) (third level)
        data = {}
        for sample, paths in zip(samples, paths):
            if sample: # skip sample b if it is not given
                data[sample] = {}
                for replicate, path in [(f"{sample} {i}", path) for i, path in enumerate(paths, start=1)]:
                    data[sample][replicate] = {}
                    hs.print_update(f"Processing file {path}")
                    with open(path, "r") as file:
                        next(file)
                        for line in file:
                            line = line.strip().split("\t")
                            current_pos = line[0], int(line[1])
                            if (current_pos[0], current_pos[1]) in target_sites:
                                data[sample][replicate][current_pos] = line
        self.data = data

    ##########################################################################################################
    #                                    Methods called for plot creation                                    #
    ##########################################################################################################
    def create_bar_trace_base_composition(self, pos_data: List[str]|None, x: int = 0, center: bool = True, show_legend: bool = False) -> List[go.Bar]:
        """
        Create a list of Plotly Bar traces for base composition visualization.

        Parameters:
        - pos_data (List[str]): List of position data.
        - x (int, optional): X-coordinate for the bars (default is 0).
        - center (bool, optional): Whether to center the bars at the specified x-coordinate (default is True).
        - show_legend (bool, optional): Whether to display legends for the bars (default is False).

        Returns:
        - List[go.Bar]: List of Plotly Bar traces.
        """
        if pos_data:
            a, c, g, u = int(pos_data[5]), int(pos_data[6]), int(pos_data[7]), int(pos_data[8])
            cvg = a+c+g+u
            a_rel, c_rel, g_rel, u_rel = a/cvg, c/cvg, g/cvg, u/cvg

        else:
            a, c, g, u = 0, 0, 0, 0
            a_rel, c_rel, g_rel, u_rel = 0.0, 0.0, 0.0, 0.0
            cvg = 0

        a_bar = go.Bar(x = [x], y = [a_rel], name = "A", 
                    marker = dict(color = self.colors["A"], line_color="black", line_width=1.5) if center else dict(color = self.colors["A"]), 
                    legendgroup = 1, 
                    opacity = 1 if center else 0.75, 
                    showlegend = show_legend, 
                    customdata = [[[a], [round(a_rel*100, 2)], [cvg]]], 
                    hovertemplate = "n=%{customdata[0]} (%{customdata[1]}%)<br>Total=%{customdata[2]}",
                    width=0.75)
        c_bar = go.Bar(x = [x], y = [c_rel], name = "C", 
                    marker = dict(color = self.colors["C"], line_color="black", line_width=1.5) if center else dict(color = self.colors["C"]), 
                    legendgroup = 2, 
                    opacity = 1 if center else 0.75, 
                    showlegend = show_legend, 
                    customdata = [[[c], [round(c_rel*100, 2)], [cvg]]], 
                    hovertemplate = "n=%{customdata[0]} (%{customdata[1]}%)<br>Total=%{customdata[2]}",
                    width=0.75)
        g_bar = go.Bar(x = [x], y = [g_rel], name = "G", 
                    marker = dict(color = self.colors["G"], line_color="black", line_width=1.5) if center else dict(color = self.colors["G"]),
                    legendgroup = 3, 
                    opacity = 1 if center else 0.75, 
                    showlegend = show_legend, 
                    customdata = [[[g], [round(g_rel*100, 2)], [cvg]]], 
                    hovertemplate = "n=%{customdata[0]} (%{customdata[1]}%)<br>Total=%{customdata[2]}",
                    width=0.75)
        u_bar = go.Bar(x = [x], y = [u_rel], name = "U", 
                    marker = dict(color = self.colors["U"], line_color="black", line_width=1.5) if center else dict(color = self.colors["U"]), 
                    legendgroup = 4, 
                    opacity = 1 if center else 0.75, 
                    showlegend = show_legend, 
                    customdata = [[[u], [round(u_rel*100, 2)], [cvg]]], 
                    hovertemplate = "n=%{customdata[0]} (%{customdata[1]}%)<br>Total=%{customdata[2]}",
                    width=0.75)
        return [a_bar, c_bar, g_bar, u_bar]

    def create_bar_trace_error_rates(self, pos_data: List[str] | None, x: int = 0, center: bool = True, show_legend: bool = False) -> List[go.Bar]:
        """
        Create a list of Plotly Bar traces for error rates visualization.

        Parameters:
        - pos_data (List[str]): List of position data.
        - x (int, optional): X-coordinate for the bars (default is 0).
        - center (bool, optional): Whether to center the bars at the specified x-coordinate (default is True).
        - show_legend (bool, optional): Whether to display legends for the bars (default is False).

        Returns:
        - List[go.Bar]: List of Plotly Bar traces.
        """        
        base_idx_rel = {"A": 12, "C": 13, "G": 14, "U": 15}
        base_idx_abs = {"A": 5, "C": 6, "G": 7, "U": 8}

        if pos_data:
            n_match = int(pos_data[base_idx_abs[pos_data[3]]])
            n_mismatch = int(pos_data[5]) + int(pos_data[6]) + int(pos_data[7]) + int(pos_data[8])
            n_deletion = int(pos_data[9])
            n_refskip = int(pos_data[11])

            match_rate = float(pos_data[base_idx_rel[pos_data[3]]])
            mismatch_rate = float(pos_data[19])
            deletion_rate = float(pos_data[16])
            refskip_rate = float(pos_data[18])

            cvg = n_match + n_mismatch + n_deletion + n_refskip
        else:
            n_match, n_mismatch, n_deletion, n_refskip = 0, 0, 0, 0
            match_rate, mismatch_rate, deletion_rate, refskip_rate = 0.0, 0.0, 0.0, 0.0
            cvg = 0
            
        match_bar = go.Bar(x = [x], y = [match_rate], name = "Match", 
                        marker = dict(color = self.colors["match"], line_color="black", line_width=1.5) if center else dict(color = self.colors["match"]), 
                        legendgroup = 5, 
                        opacity = 1 if center else 0.75, 
                        showlegend = show_legend, 
                        customdata = [[[n_match], [round(match_rate*100, 2)], [cvg]]], 
                        hovertemplate = "n=%{customdata[0]} (%{customdata[1]}%)<br>Total=%{customdata[2]}",
                        width=0.75)
        mismatch_bar = go.Bar(x = [x], y = [mismatch_rate], name = "Mismatch", 
                            marker = dict(color = self.colors["mis"], line_color="black", line_width=1.5) if center else dict(color = self.colors["mis"]), 
                            legendgroup = 6, 
                            opacity = 1 if center else 0.75, 
                            showlegend = show_legend, 
                            customdata = [[[n_mismatch], [round(mismatch_rate*100, 2)], [cvg]]], 
                            hovertemplate = "n=%{customdata[0]} (%{customdata[1]}%)<br>Total=%{customdata[2]}",
                            width=0.75)
        deletion_bar = go.Bar(x = [x], y = [deletion_rate], name = "Deletion", 
                            marker = dict(color = self.colors["del"], line_color="black", line_width=1.5) if center else dict(color = self.colors["del"]),
                            legendgroup = 7, 
                            opacity = 1 if center else 0.75, 
                            showlegend = show_legend, 
                            customdata = [[[n_deletion], [round(deletion_rate*100, 2)], [cvg]]], 
                            hovertemplate = "n=%{customdata[0]} (%{customdata[1]}%)<br>Total=%{customdata[2]}",
                            width=0.75)
        refskip_bar = go.Bar(x = [x], y = [refskip_rate], name = "Reference skip", 
                            marker = dict(color = self.colors["ref_skip"], line_color="black", line_width=1.5) if center else dict(color = self.colors["ref_skip"]), 
                            legendgroup = 8, 
                            opacity = 1 if center else 0.75, 
                            showlegend = show_legend, 
                            customdata = [[[n_refskip], [round(refskip_rate*100, 2)], [cvg]]], 
                            hovertemplate = "n=%{customdata[0]} (%{customdata[1]}%)<br>Total=%{customdata[2]}",
                            width=0.75)
        return [match_bar, mismatch_bar, deletion_bar, refskip_bar]

    def create_bar_trace_insertion_rate(self, pos_data: List[str] | None, x: int = 0, center: bool = True, show_legend: bool = False) -> List[go.Bar]:
        """
        Create a list of Plotly Bar traces for insertion rate visualization.

        Parameters:
        - pos_data (List[str]): List of position data.
        - x (int, optional): X-coordinate for the bars (default is 0).
        - center (bool, optional): Whether to center the bars at the specified x-coordinate (default is True).
        - show_legend (bool, optional): Whether to display legends for the bars (default is False).

        Returns:
        - List[go.Bar]: List of Plotly Bar traces.
        """     
        if pos_data:     
            n_ins = int(pos_data[10])
            ins_rate = float(pos_data[17])
        else:
            n_ins, ins_rate = 0, 0.0

        ins_bar = go.Bar(x = [x], y = [ins_rate], name = "Insertion", 
                        marker = dict(color = self.colors["ins"], line_color="black", line_width=1.5) if center else dict(color = self.colors["ins"]), 
                        legendgroup = 9, 
                        opacity = 1 if center else 0.75, 
                        showlegend = show_legend, 
                        customdata = [[[n_ins], [round(ins_rate*100, 2)]]], 
                        hovertemplate = "n=%{customdata[0]} (%{customdata[1]}%)",
                        width=0.75)
        return [ins_bar]

    def get_rep_bar_traces(self, data: List[List[str]|None], plot_type: str, showlegend: bool = False) -> List[go.Bar]:
        """
        Get a list of Plotly Bar traces for a replicate.

        Parameters:
        - data (List[List[str]]): List of data for a replicate.
        - plot_type (str): Type of plot (base_composition, error_rates, insertion_rate).
        - showlegend (bool, optional): Whether to display legends for the bars (default is False).

        Returns:
        - List[go.Bar]: List of Plotly Bar traces.
        """
        x_vals = range(-self.nb_size,self.nb_size+1)
        is_center_pos = [False]*self.nb_size + [True] + [False]*self.nb_size
        show_legend = is_center_pos if showlegend else [showlegend]*(2*self.nb_size+1)

        if plot_type == "base_composition":
            create_bar_func = self.create_bar_trace_base_composition
        elif plot_type == "error_rates":
            create_bar_func = self.create_bar_trace_error_rates
        elif plot_type == "insertion_rate":
            create_bar_func = self.create_bar_trace_insertion_rate
        else:
            raise Exception(f"Unknown plot type given: {plot_type}. Must be one of the following: base_composition, error_rates, insertion_rate")
        
        bar_traces = [create_bar_func(d, x, c, l) for d, x, c, l in zip(data, x_vals, is_center_pos, show_legend)]
        return [item for t in bar_traces for item in t]

    def create_position_plots(self, position: SITE) -> go.Figure:
        """
        Create Plotly plot containing showing base compositions, error rates, and insertion rates for each position.

        Parameters:
        - position (Tuple[str, int]): Position for which the plot should be created.

        Returns:
        - go.Figure: Plotly figure for position
        """        
        n_rep_a = len(self.data[self.basename_a].keys())
        n_rep_b = len(self.data[self.basename_b].keys()) if self.basename_b else 0
        n_samples = n_rep_a+n_rep_b

        fig = make_subplots(cols=3, rows=n_samples, shared_xaxes=True, column_widths=[2,1,1])
        height = 225*(n_samples) if n_samples>1 else 500
        fig = hs.update_plot(fig, height=height, width=1200)

        # Three columns correspond to the features that are displayed (base_composition, error_rates, insertion_rate)
        # Half of the rows correspond to replicates of sample A, the other half to sample B
        rep_labels = []
        for col, plot_type in enumerate(["base_composition", "error_rates", "insertion_rate"], start=1):
            current_row = 1
            for sample in [self.basename_a, self.basename_b]:
                if sample: # skip sample b if it is not given
                    for rep in self.data[sample].keys():
                        rep_labels.append(rep)
                        # get the data for the position itself and nb_size number of positions up- and downstream
                        position_data = [self.data[sample][rep][(position[0], position[1]+i)] if (position[0], position[1]+i) in self.data[sample][rep].keys() else None for i in range(-self.nb_size, self.nb_size+1)]
                        bars = self.get_rep_bar_traces(position_data, plot_type=plot_type, showlegend=True) if current_row==1 else self.get_rep_bar_traces(position_data, plot_type=plot_type)
                        fig.add_traces(bars, rows=[current_row]*len(bars), cols=[col]*len(bars))
                        current_row += 1
        fig.update_layout(barmode="stack", legend_tracegroupgap=0) # reduce spacing between legend items 
        
        # Update y ticklabels (show only for first column)
        for i in range(n_samples):
            fig.update_yaxes(title=rep_labels[i], row=i+1, col=1)
        
        # Update x ticklabels (show only for last row and show the bases instead of coordinates)
        x_ticks = [d[3] if d else "N" for d in position_data] # type: ignore dont see how it can be unbound...
        for col in range(1,4):
            for i in range(1, n_samples):
                fig.update_xaxes(tickvals=[], ticktext=[], row=i, col=col)
            fig.update_xaxes(tickvals=list(range(-self.nb_size,self.nb_size+1)), ticktext=x_ticks, row=n_samples, col=col)

        return fig

    def create_html_section(self, position: SITE, plot: go.Figure) -> str:
        """
        Create an HTML section for a genomic position with embedded plots.

        Parameters:
        - position (Tuple[str, int]): Genomic position (chromosome, site).
        - plot (go.Figure): Plotly figure showing base composition, error rates, and insertion rates at the given position.

        Returns:
        - str: HTML section for the genomic position with embedded plots.
        """
        chrom, site = position[0], position[1]
    
        plot_str = plot.to_html(include_plotlyjs=False)

        collapsible_section = f"""
            <section>
                <button class="collapsible">{chrom}:{site}</button>

                <div class="collapsible-content">
                <h2 class="hiddentitle" id="{chrom}_{site}"></h2>

                    <h3>Base compositions and error rates</h3>
                    <div class="plot-container">
                        {plot_str}
                    </div>
                    <p>
                        Base- (left) and error (middle, right) compositions {self.nb_size} bases up- and downstream around position {chrom}, {site}.
                        Hover for detailed information about coverage, absolute and relative counts. 
                    </p>
                </div>
            </section>
        """
        return collapsible_section

    def get_file_paths(self) -> Tuple[str, str]:
        """
        Get formatted HTML lists of input file paths for datasets A and B.
        Collapsible sections are adapted from: https://github.com/wdecoster/NanoPlot/blob/master/nanoplot/report.py

        Returns:
        - Tuple[str, str]: Formatted HTML lists of file paths for datasets A and B.
        """        
        def create_list(paths: List[str]):
            path_list = "<ul>"
            for path in paths:
                path_list += f"<li>{path}</li>"
            path_list += "</ul>"
            return path_list
        
        list_a = create_list(self.paths_a)
        list_b = create_list(self.paths_b) if self.paths_b else ""
        return list_a, list_b

    def write_svg(self, fig: go.Figure, position: SITE, output_dir: str) -> None:
        """
        Write the three plots (base composition, error rates and insertion rates) to three separate SVG files in
        output_dir. The name of the file is in the following format: <chr>_<coordinate>_<plot-type>.svg
        All plots are written to the directory created beforehand.

        Parameters:
        - figs (Tuple[go.Figure, go.Figure, go.Figure]): Plotly figures of base composition, error rates and insertion rates
        - positions (Tuple[str, int]): Genomic position (chromosome, site).
        - output_dir (str): Output directory as created beforehand in main method.

        Returns:
        - None
        """
        outpath = os.path.join(output_dir, f"{position[0]}_{position[1]}_overview.svg")
        fig.write_image(outpath)

    def main(self) -> None:
        """
        Main method to generate the HTML summary report.
        """
        collapsible_sections = ""

        if self.export_svg:
            filename = f"{self.basename_a}_{self.basename_b}_{self.basename_bed}" if self.basename_b else f"{self.basename_a}_{self.basename_bed}"
            export_dir = os.path.join(self.out_dir, filename) 
            os.makedirs(export_dir, exist_ok=True)
        for position in tqdm(self.positions, total=len(self.positions), desc="Creating plots"):
            plot = self.create_position_plots(position)
            if self.export_svg:
                self.write_svg(plot, position, export_dir) # type: ignore if export_svg, export_dir has been specified a few lines above
            collapsible_sections += self.create_html_section(position, plot) 
        
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        files_a, files_b = self.get_file_paths()
        
        css_string, plotly_js_string = hs.load_html_template_str()

        template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Neet - POI View</title>
                <link rel="stylesheet" type="text/css" href="/home/vincent/projects/neet_project/neet/summary/style.css">
                <style>{css_string}</style>
            </head>

            <body>
                <script>{plotly_js_string}</script>
                <header>
                    <h1>Position of Interest View</h1>
                    <p>Produced by <a href="https://github.com/dietvin/neet">Neet</a> on <b>{time}</b></p>
                </header>
            
                <section>
                    <p class="intro-text">
                        This summary file contains an overview of {len(self.positions)} positions found in <i>{self.bed_path}</i>. 
                    </p>
                    <p class="intro-text">Files provided for sample <i>{self.basename_a}</i>:</p>
                    {files_a}
                    {f'<p class="intro-text">Files provided for sample <i>{self.basename_b}</i>:</p>' if self.basename_b else ""}
                    {files_b}
                </section>

                {collapsible_sections}

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
        filename = f"{self.basename_a}_{self.basename_b}_{self.basename_bed}_view.html" if self.basename_b else f"{self.basename_a}_{self.basename_bed}_view.html"
        outfile = os.path.join(self.out_dir, filename)
        with open(outfile, "w") as out:
            hs.print_update(f"Writing summary file to: {outfile}")
            out.write(template)

        hs.print_update("Finished.")

if __name__=="__main__":
    p = POIView(paths_a="/home/vincent/projects/neet_project/data/45s_rrna/feature_tables/drna_cyt_extracted.tsv",
                paths_b="/home/vincent/projects/neet_project/data/45s_rrna/feature_tables/drna_nuc_extracted.tsv",
                bed_path="/home/vincent/projects/neet_project/data/45s_rrna/test/sample_b_excl.bed",
                out_dir="/home/vincent/projects/neet_project/data/45s_rrna/test")
    p.main()
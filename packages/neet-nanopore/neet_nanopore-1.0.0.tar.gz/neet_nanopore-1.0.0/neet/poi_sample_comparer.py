import os
import plotly.graph_objects as go
from collections import defaultdict
from typing import List, Dict, Tuple, Any
from scipy.stats import ttest_rel, wilcoxon, normaltest, bartlett
from statsmodels.stats.multitest import fdrcorrection
from math import log10
from tqdm import tqdm

try: # when invoked from the package
    from neet import helper_functions as hs
except ImportError: # when invoked directly
    import helper_functions as hs

SITE = Tuple[str, int]
SAMPLE = str
FEATURE = str

class PoiSampleComparer:
    in_path_a: str
    in_path_b: str
    bed_path: str
    basename_a: str
    basename_b: str
    out_dir: str
    num_neighbours: int
    n_reads_threshold: int
    alpha: float
    store_stat: bool

    poi_sites: Dict[SITE, List[SITE]]
    data: Dict[SAMPLE, Dict[SITE, Dict[FEATURE, Any]|None]] # Any one of int, str, float; None if a site is not found
    poi_sites_usable: Dict[SITE, List[SITE]] # containing only the sites that are available and sufficiently covered (as indentified in in self.get_usable_pois)

    def __init__(self, path_a: str, path_b: str, bed_path: str,
                 out_dir: str | None = None,
                 basename_a: str = "sample_a", 
                 basename_b: str = "sample_a", 
                 num_neighbours: int = 2, 
                 n_reads_threshold: int = 15, 
                 alpha: float = 0.01, 
                 store_stat: bool = False) -> None:
        
        hs.check_input_path(path_a, extensions=[".tsv"])
        self.in_path_a = os.path.abspath(path_a)
        hs.check_input_path(path_b, extensions=[".tsv"])
        self.in_path_b = os.path.abspath(path_b)

        hs.check_input_path(bed_path, extensions=[".bed"])
        self.bed_path = os.path.abspath(bed_path)

        if not basename_a:
            raise Exception(f"Given basename for sample a '{basename_a}' is not valid.")
        elif not basename_b:
            raise Exception(f"Given basename for sample b '{basename_b}' is not valid.")
        elif basename_a == basename_b:
            raise Exception(f"Basenames '{basename_a}' and '{basename_b}' must differ from each other.")
        self.basename_a = basename_a
        self.basename_b = basename_b

        if out_dir:
            out_dir = os.path.abspath(out_dir)
            ext = os.path.splitext(out_dir)[1]
            if ext:
                hs.print_update(f"Warning: Extension {ext} was found. Make sure to provide a single output directory.")
            hs.check_create_dir(out_dir)
            self.out_dir = out_dir
        else: 
            self.out_dir = os.path.dirname(self.in_path_a)

        if num_neighbours <= 0:
            raise Exception(f"Number of neighbours must be larger than 0. Given number: {num_neighbours}")
        self.num_neighbours = num_neighbours

        if n_reads_threshold <= 0:
            raise Exception(f"Threshold for the number of reads must be larger than 0. Given number: {n_reads_threshold}")
        self.n_reads_threshold = n_reads_threshold

        if (alpha < 0) | (alpha > 1):
            raise Exception(f"Alpha must be in range (0,1). Given number: {alpha}")
        self.alpha = alpha

        self.store_stat = store_stat

        # load data
        hs.print_update(f"Loading POIs from {bed_path}.")
        self.load_bed_sites(bed_path)
        hs.print_update(f"Loading data from {path_a}.")
        data_a = self.load_data(path_a)
        hs.print_update(f"Loading data from {path_b}.")
        data_b = self.load_data(path_b)
        # self.data: nested dict with 1. samples, 2. POI site, 3. feature 
        self.data = {basename_a: data_a, basename_b: data_b}

    ##############################################################################################################
    #                                           Initialization methods                                           #
    ##############################################################################################################

    def load_bed_sites(self, bed_path):
        """
        Loads positions of interest (POIs) and their neighboring sites from the provided BED file.

        Parameters:
        - bed_path (str): The file path to the BED file containing POIs.

        Notes:
            The BED file is expected to be tab-delimited with three columns: chromosome, start position, and end position.
            Only the chromosome and end position are used to define POIs, and the start position is ignored.
            Neighboring sites are defined as the specified number of bases up- and downstream from each POI.
            The neighboring sites are stored in the 'poi_sites' attribute as a dictionary with POI sites as keys
            and lists of neighboring sites as values.
        """
        with open(bed_path, "r") as f:
            center_sites = []
            for line in f:
                line = line.strip().split("\t")
                seq, site = line[0], int(line[2])
                center_sites.append((seq,site))
        center_sites = set(center_sites)
        all_sites = {}
        for site in center_sites:
            all_sites[site] = [(site[0], site[1]+i) for i in range(-self.num_neighbours,self.num_neighbours+1)]
        
        self.poi_sites = all_sites

    def load_data(self, input_path) -> Dict[SITE, Dict[str, Any]|None]:
        """
        Loads genomic data from the specified input file and organizes it into a dictionary.

        Parameters:
        - input_path (str): The file path to the input genomic data file.

        Returns:
        Dict[Tuple[str, int], Dict[str, Any]|None]: A nested dictionary containing genomic data for each POI.
            - The outer dictionary's keys are tuples representing POI sites (chromosome, position).
            - The inner dictionary contains genomic data for each POI, with keys representing different features.

        Notes:
        - The input file is expected to be a feature table created by the Pileup Extractor.
        - Missing data for a POI (if any) will be represented as None in the inner dictionary.
        """
        cols = ["n_reads", "ref_base", "majority_base", "deletion_rate", "insertion_rate", "refskip_rate", "mismatch_rate", "q_mean", "motif"]

        col_idx = {'chr': 0, 'site': 1, 'n_reads': 2, 'ref_base': 3, 'majority_base': 4, 'n_a': 5, 'n_c': 6, 'n_g': 7, 'n_t': 8, 'n_del': 9, 'n_ins': 10, 'n_ref_skip': 11, 'a_rate': 12, 'c_rate': 13, 'g_rate': 14, 'u_rate': 15, 'deletion_rate': 16, 'insertion_rate': 17, 'refskip_rate': 18, 'mismatch_rate': 19, 'mismatch_rate_alt': 20, 'motif': 21, 'q_mean': 22, 'q_std': 23, 'neighbour_error_pos': 24}
        dtypes = {'chr': str, 'site': int, 'n_reads': int, 'ref_base': str, 'majority_base': str, 'n_a': int, 'n_c': int, 'n_g': int, 'n_t': int, 'n_del': int, 'n_ins': int, 'n_ref_skip': int, 'a_rate': float, 'c_rate': float, 'g_rate': float, 'u_rate': float, 'deletion_rate': float, 'insertion_rate': float, 'refskip_rate': float, 'mismatch_rate': float, 'mismatch_rate_alt': float, 'motif': str, 'q_mean': float, 'q_std': float, 'neighbour_error_pos': str}
        
        poi_sites = []
        for sites in self.poi_sites.values():
            poi_sites += sites
        data = dict(zip(poi_sites, [None]*len(poi_sites)))
        
        n_lines = hs.get_num_lines(input_path)

        with open(input_path, "r") as f:
            next(f)
            for line in tqdm(f, total=n_lines):
                line = line.strip().split("\t")
                site = (line[0], int(line[1]))
                if site in poi_sites:
                    site_data = {}
                    for col in cols:
                        site_data[col] = dtypes[col](line[col_idx[col]])
                    data[site] = site_data # type: ignore None is overwritten if the site is found in the feature table
            return data # type: ignore see above

    ##############################################################################################################
    #                                           Main processing methods                                          #
    ##############################################################################################################
    def main(self) -> None:
        """
        Performs the main processing steps including data loading, statistical analysis, and report generation.

        Notes:
        - This method orchestrates the entire process of statistical analysis and report generation.
        - It sequentially calls other methods to load data, identify usable POIs, retrieve feature values,
          calculate p-values, adjust p-values for false discovery rates, create an interactive plot,
          optionally store statistical results in a table, and generate an HTML report.
        - The HTML report summarizes the analysis, providing an overview of statistical results and an interactive plot.
        """
        hs.print_update(f"Filtering usable POIs... ", line_break=False)
        poi_sites_overview, total, usable = self.get_usable_pois()
        hs.print_update(f"{usable} out of {total} usable.", with_time=False)

        hs.print_update("Collecting feature values and performing tests.")
        stat_features = self.get_feature_values()
        stat_results = self.calc_pvals(stat_features)
        # add fdr and -log10(fdr) in place
        hs.print_update("Adjusting p-values.")
        self.calc_fdr(stat_results)
        hs.print_update("Setting up plot.")
        fig = self.create_fdr_plot(stat_results)

        if self.store_stat:
            self.write_stat_table(stat_results)
        self.write_html(poi_sites_overview, fig)
        
        hs.print_update("Finished.")

    def get_usable_pois(self) -> Tuple[str, int, int]:
        """
        Identifies usable positions of interest (POIs) based on data availability and read counts.

        Returns:
        - str: A summary string describing the number of POIs extracted from the BED file
               and the number of POIs used in the statistical comparison.

        Notes:
        - This method iterates through each POI and its neighboring sites to check if the data is available
          and the number of reads is sufficient in both samples.
        - POIs and their neighboring sites that meet the criteria are considered usable and stored in the 'poi_sites_usable' attribute.
        - The summary string includes information about the total number of POIs extracted from the BED file,
          the number of usable POIs, and the criteria used for determining usability.
        """
        poi_sites_usable = {}
        # for both samples, for all POIs check if the data is available and the number of reads is sufficient
        # at the site itself AND all surrounding sites 
        for sample in [self.basename_a, self.basename_b]:
            for center_site, nb_sites in self.poi_sites.items():
                usable = True
                for nb_site in nb_sites:
                    if self.data[sample][nb_site]:
                        n_reads = self.data[sample][nb_site]["n_reads"] # type: ignore if statement above ensures that its not None
                        if n_reads < self.n_reads_threshold:
                            usable = False
                            break # if one site in the neighbourhood is unusable, the POI at hand gets skipped
                    else: 
                        usable = False
                        break # if one site in the neighbourhood is unusable, the POI at hand gets skipped
                if usable:
                    poi_sites_usable[center_site] = self.poi_sites[center_site]

        num_center_sites = len(self.poi_sites.keys())
        num_usable_center_sites = len(poi_sites_usable.keys())

        section_str = f"""
                    {num_center_sites} positons were extracted from {self.bed_path}. From these, {num_usable_center_sites} sites were used in the statistical
                     comparison, as the site itself and all neighbouring sites {self.num_neighbours} bases up- and downstream have sufficient number of reads 
                     (>= {self.n_reads_threshold}) in both sample <i>{self.basename_a}</i> and <i>{self.basename_b}</i>.
                    """
        
        # Update the POI sites to contain only usable sites
        self.poi_sites_usable = poi_sites_usable
        return section_str, num_center_sites, num_usable_center_sites

    def get_feature_values(self) -> Dict[SAMPLE, Dict[int, Dict[FEATURE, List[float]]]]:
        """
        Retrieves feature values for each sample at each position of interest (POI).

        Returns:
        - Dict[str, Dict[int, Dict[str, List[float]]]]: A nested dictionary containing feature values for each sample
          at each relative position around POIs.
            - The outer dictionary's keys are sample names.
            - The inner dictionary's keys are relative positions (-num_neighbours to +num_neighbours).
            - The innermost dictionary contains feature values as lists, with keys representing different features.

        Notes:
            - This method extracts feature values for each sample at each position of interest and its neighboring positions.
            - Feature values are stored in lists corresponding to different features such as mismatch rate, deletion rate, etc.
        """
        stat_features_dict = {}
        # extract the values for each feature at each position for each sample and store them in a list for later access and comparison
        for sample in [self.basename_a, self.basename_b]:
            stat_features_dict[sample] = defaultdict(lambda: {"mismatch_rate": [], "deletion_rate": [], "insertion_rate": [], "q_mean": []})
            for nb_sites in self.poi_sites_usable.values():
                for i, nb_site in enumerate(nb_sites, start=-self.num_neighbours):
                    site_data = self.data[sample][nb_site]
                    for feature in ["mismatch_rate", "deletion_rate", "insertion_rate", "q_mean"]:
                        stat_features_dict[sample][i][feature].append(site_data[feature]) # type: ignore in self.get_usable_pois is ensured that the data is available here  

            stat_features_dict[sample] = dict(stat_features_dict[sample])
        return stat_features_dict
    
    def calc_pvals(self, stat_features: Dict[SAMPLE, Dict[int, Dict[FEATURE, List[float]]]]) -> Dict[FEATURE, Dict[int, Dict[str, float|str]]]:
        """
        Calculates p-values for statistical tests comparing feature values between samples.

        Parameters:
        - stat_features (Dict[str, Dict[int, Dict[str, List[float]]]]): A nested dictionary containing feature values for each sample
                                                                        at each relative position around POIs.

        Returns:
        - Dict[str, Dict[int, Dict[str, float|str]]]: A nested dictionary containing calculated p-values for each feature
          at each relative position around POIs.
                - The outer dictionary's keys are feature names.
                - The inner dictionary's keys are relative positions (-num_neighbours to +num_neighbours).
                - The innermost dictionary contains p-values and the test used for comparison.

        Notes:
            - This method performs statistical tests (t-test or Wilcoxon test) to compare feature values between two samples.
            - The resulting p-values and the test used for comparison are stored in a nested dictionary structure.
        """
        stat_results = {}

        for feature in ["mismatch_rate", "deletion_rate", "insertion_rate", "q_mean"]:
            stat_results[feature] = {}
            for rel_pos in range(-self.num_neighbours, self.num_neighbours+1):
                pval, test_used = self.perform_test(stat_features[self.basename_a][rel_pos][feature], stat_features[self.basename_b][rel_pos][feature], alpha=self.alpha)
                stat_results[feature][rel_pos] = {"pval": pval, "test": test_used}
        
        return stat_results
 
    def perform_test(self, set1: List[float], set2: List[float], alpha: float = 0.01) -> Tuple[float, str]:
        """
        Performs a series of tests to compare two sets of data. It checks for normality in both 
        samples and equal variances using normaltest and bartlett tests. If the conditions are
        met, it performs an t-test for connected samples, otherwise, it performs a Wilcoxon-test for
        connected samples. If the test fails returns None for the p-value and 'ERROR' for the test that was used.

        Parameters:
        - set1 (List[float]): The first set of data.
        - set2 (List[float]): The second set of data.
        - alpha (float): The significance level for the tests (default is 0.01).

        Returns:
        - float|None: p-value of the test or None if an Exception was raised
        - str: string indicating the test that was used
        """
        try:
            if (normaltest(set1)[1] >= alpha) & (normaltest(set2)[1] >= alpha) & (bartlett(set1, set2)[1] >= alpha): # normal distributions in both samples + equal variances
                return ttest_rel(a=set1, b=set2)[1], "t-test"
            else: # normal distribution in both samples and equal variances
                # return f"{mannwhitneyu(x=set1, y=set2)[1]:.5e} (MWU)"
                return wilcoxon(x=set1, y=set2)[1], "Wilcoxon-test"
        except:
            return -1, "ERROR"

    def calc_fdr(self, stat_results: Dict[FEATURE, Dict[int, Dict[str, float|str]]]) -> None:
        """
        Calculates false discovery rates (FDR) for each test.

        Parameters:
            - stat_results (Dict[str, Dict[int, Dict[str, float|str]]]): A nested dictionary containing calculated p-values
                for each feature at each relative position around POIs.

        Notes:
            - This method calculates FDRs for each feature at each relative position based on the p-values obtained
            from statistical tests.
            - It adjusts the p-values using the Benjamini-Hochberg procedure to control the FDR.
            - The adjusted p-values (FDR) are stored in the 'fdr' key within the inner dictionaries of 'stat_results'.
            - Additionally, the negative logarithm of the adjusted p-values is calculated and stored as 'neg_log_fdr'.
        """
        pvals = []
        features = []
        rel_pos = []
        for feature in stat_results.keys():
            for pos in stat_results[feature].keys():
                pvals.append(stat_results[feature][pos]["pval"])
                features.append(feature)
                rel_pos.append(pos)
        fdrs = fdrcorrection(pvals)[1]
        # add values in place
        for feature, pos, fdr in zip(features, rel_pos, fdrs):
            stat_results[feature][pos]["fdr"] = fdr
            stat_results[feature][pos]["neg_log_fdr"] = -log10(fdr)

    def create_fdr_plot(self, stat_results: Dict[FEATURE, Dict[int, Dict[str, float|str]]]) -> go.Figure:
        """
        Creates an interactive plot visualizing adjusted p-values (-log10(FDR)) for different features at each relative position.

        Parameters:
            - stat_results (Dict[str, Dict[int, Dict[str, float|str]]]): A nested dictionary containing adjusted p-values
                (FDR) for each feature at each relative position around POIs.

        Returns:
            - go.Figure: An interactive plotly Figure object displaying adjusted p-values (-log10(FDR)) for different features.

        Notes:
            - This method generates a plot to visualize the adjusted p-values (FDR) for each feature at each relative position.
            - Adjusted p-values are transformed into negative logarithms for better visualization.
            - The plot is interactive and allows users to hover over data points to see detailed information.
            - Features are represented by different traces on the plot, with relative positions on the x-axis and
            -log10(FDR) on the y-axis.
        """
        fig = hs.update_plot(go.Figure(), width=1000, height=500)
        fig.add_hline(y=2, line_color="black", line_dash="dash", line_width=3, name=f"FDR={self.alpha}")
        for feature, name in zip(["mismatch_rate", "deletion_rate", "insertion_rate", "q_mean"], ["Mismatch rate", "Deletion rate", "Insertion rate", "Mean q-score"]):
            x = list(stat_results[feature].keys())
            y = [stat_results[feature][pos]["neg_log_fdr"] for pos in x]
            # https://stackoverflow.com/questions/59057881/how-to-customize-hover-template-on-with-what-information-to-show
            customdata = [[round(stat_results[feature][pos]["fdr"],6), stat_results[feature][pos]["test"]] for pos in x] # type: ignore "fdr" entry is always float
            scatter = go.Scatter(x=x, y=y, 
                                 name=name, 
                                 customdata=customdata, 
                                 hovertemplate="Rel. position: %{x}<br>-log(FDR): %{y}<br>FDR: %{customdata[0]}<br>Test: %{customdata[1]}",
                                 line_width=3, marker_size=10)
            fig.add_trace(scatter)

        fig.update_xaxes(title=f"Relative position in {2*self.num_neighbours+1}-mer", tickmode = 'array', tickvals = [i for i in range(-self.num_neighbours,self.num_neighbours+1)])
        fig.update_yaxes(title="-log10( FDR )")

        return fig
    
    def write_stat_table(self, stat_results: Dict[FEATURE, Dict[int, Dict[str, float | str]]]) -> None:
        """
        Writes statistical results including p-values, adjusted p-values (FDR), and the test used to a tab-separated file.

        Parameters:
            - stat_results (Dict[str, Dict[int, Dict[str, float|str]]]): A nested dictionary containing statistical results
                for each feature at each relative position around POIs.

        Notes:
            - This method writes statistical results to a tab-separated file for further analysis or documentation.
            - The file contains columns for feature name, relative position, p-value, adjusted p-value (FDR), negative logarithm of FDR,
            and the test used for comparison.
            - Each row represents statistical results for a specific feature at a specific relative position.
        """
        bed_name = os.path.basename(os.path.splitext(self.bed_path)[0])
        output_path = os.path.join(self.out_dir, f"{self.basename_a}_{self.basename_b}_{bed_name}_statcompare.tsv")
        hs.print_update(f"Writing (adjusted) p-values to {output_path}.")
        
        table = "feature\trelative_position\tp_value\tfdr\tneg_log10_fdr\ttest_used\n"
        for feature in stat_results.keys():
            for rel_pos in stat_results[feature].keys():
                pval = str(stat_results[feature][rel_pos]["pval"])
                test = str(stat_results[feature][rel_pos]["test"])
                fdr = str(stat_results[feature][rel_pos]["fdr"])
                neg_log_fdr = str(stat_results[feature][rel_pos]["neg_log_fdr"])
                row = "\t".join([feature, str(rel_pos), pval, fdr, neg_log_fdr, test]) + "\n"
                table += row

        with open(output_path, "w") as o:
            o.write(table)

    def write_html(self, poi_sites_overview: str, fig: go.Figure) -> None:
        """
        Writes the statistical comparison results and an interactive plot to an HTML report.

        Parameters:
            - poi_sites_overview (str): A summary string describing the number of POIs used in the statistical comparison.
            - fig (go.Figure): An interactive plotly Figure object displaying adjusted p-values (-log10(FDR)) for different features.

        Notes:
            - This method generates an HTML report summarizing the statistical comparison results and an interactive plot.
            - The HTML report includes general information about the analysis, a summary of usable POIs, and an interactive plot.
            - The interactive plot allows users to explore adjusted p-values (-log10(FDR)) for different features at each relative position.
            - The HTML report is generated with CSS styling for better presentation and readability.
        """
        css_string, plotly_js_string = hs.load_html_template_str()
        time = hs.get_time()
        fig_str = fig.to_html(include_plotlyjs=False)

        bed_name = os.path.basename(os.path.splitext(self.bed_path)[0])
        output_path = os.path.join(self.out_dir, f"{self.basename_a}_{self.basename_b}_{bed_name}_statcompare.html")
        hs.print_update(f"Writing HTML summary to {output_path}.")

        template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Neet - POI comparison</title>                        
                <style>{css_string}</style>
            </head>

            <body>
                <script>{plotly_js_string}</script>

                <header>
                    <h1>Statistical comparison of positions of interest ({self.basename_a}-{self.basename_b})</h1>
                    <p>Produced by <a href="https://github.com/dietvin/neet">Neet</a> on <b>{time}</b></p>
                </header>
                
                <section>
                    <p class="intro-text">
                        This summary file was created from the extracted features in file <b>{self.in_path_a}</b> for sample <b>{self.basename_a}</b> 
                        and <b>{self.in_path_b}</b> for sample <b>{self.basename_b}</b>. POIs were provided in <b>{self.bed_path}</b>. The plots are 
                        interactive and allow further information by hovering, zooming and panning.
                    </p>
                </section>

                
                <section>
                    <button class="collapsible">Resuls of the statistical comparison</button>
                    <div class="collapsible-content">
                        <h2 class="hiddentitle" id="map"></h2>

                        <h3>General information</h3>
                        <p>
                            {poi_sites_overview}
                        </p>

                        <h3>Overview of adjusted p-values</h3>
                        <div class="plot-container">
                            {fig_str}
                        </div>
                        <p>
                            False-discovery rates (FDR) of different error features at positions {self.num_neighbours} bases up- and downstream from
                            positions of interest. Features were statistically compared between '{self.basename_a}' and '{self.basename_b}' using 
                            a t-test or Wilcoxon test for connected samples. The dashed line indicates <b>alpha={self.alpha}</b>.  
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
        with open(output_path, "w") as out:
            out.write(template)


if __name__=="__main__":
    p = PoiSampleComparer(path_a="/home/vincent/projects/neet_project/data/45s_rrna/test/drna_cyt_extracted.tsv",
                          path_b="/home/vincent/projects/neet_project/data/45s_rrna/test/drna_nuc_extracted.tsv",
                          basename_a="Cytoplasm",
                          basename_b="Nucleus",
                          bed_path="/home/vincent/projects/neet_project/data/45s_rrna/test/psu_sites.bed",
                          out_dir="/home/vincent/projects/neet_project/data/45s_rrna/test", 
                          store_stat=True)

    p.main()
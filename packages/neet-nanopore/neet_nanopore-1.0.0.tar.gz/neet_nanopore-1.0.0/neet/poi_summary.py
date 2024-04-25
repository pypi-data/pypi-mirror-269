from typing import List, Dict, Tuple, Any
import os, math, datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.io import to_html
from intervaltree import IntervalTree
from collections import defaultdict
from statistics import median, mean
from scipy.stats import normaltest, bartlett, ttest_ind, mannwhitneyu
from statsmodels.stats.multitest import fdrcorrection
from tqdm import tqdm

try: # when invoked from the package
    from neet import helper_functions as hs
except ImportError: # when invoked directly
    import helper_functions as hs

class POISummary():

    in_path: str
    bed_path: str
    ref_path: str

    perc_mismatch_col: str
    output_tsv: bool
    export_svg: bool

    data: Dict[str, List[Any]] # dtypes can be str, int, float, str|None
    bed_categories: List[str]
    bed_categories_counterparts: List[str] | List[None]
    output_paths: List[str]

    category_data: Dict[str, List[Any]] # dtypes can be str, int, float, str|None
    counterpart_data: Dict[str, List[Any]] | None
    current_category: str
    current_counterpart: str | None 

    n_bins_seqmap: int
    n_bins: int
    
    def __init__(self, in_path: str, bed_path: str, ref_path: str,
                 categories: str,
                 out_dir: str | None = None, 
                 canonical_counterpart: str | None = None,
                 output_tsv: bool = True, 
                 use_perc_mismatch_alt: bool = False,
                 export_svg: bool = False,
                 n_bins_seqmap: int = 200,
                 n_bins: int = 5000) -> None:
        """
        Initialize an instance of the GenomicDataProcessor class.

        Parameters:
        - in_path (str): The path to the input TSV file containing genomic data.
        - out_dir (str|None): The path to the output directory where results will be saved.
        - bed_path (str): The path to the BED file containing genomic intervals.
        - ref_path (str): The path to the reference FASTA file.
        - categories (str): A comma-separated string containing bed categories.
        - canonical_counterpart (str): A comma-separated string containing bases corresponding to bed categories.
        - output_tsv (bool, optional): Whether to output results as a TSV file. Default is True.
        - use_perc_mismatch_alt (bool, optional): Whether to use 'mismatch_rate_alt' instead of 'mismatch_rate' column. Default is False.
        """
        self.process_path(in_path, bed_path, ref_path)
        self.load_data()
        self.add_bed_info()
        self.perc_mismatch_col = "mismatch_rate_alt" if use_perc_mismatch_alt else "mismatch_rate"

        self.process_categories(categories, canonical_counterpart, out_dir)

        # number of bins in which the coordinates of present sequences will be grouped for the sequence map plot
        self.n_bins_seqmap = n_bins_seqmap
        # number of data points to display in boxplots (to reduce file size for large datasets)
        self.n_bins = n_bins

        self.output_tsv = output_tsv
        self.export_svg = export_svg

    ##############################################################################################################
    #                                           Initialization methods                                           #
    ##############################################################################################################

    def process_path(self, in_path: str, bed_path: str, ref_path: str) -> None:
        """
        Validate input paths and assign paths to member variables.

        Parameters:
        - in_path (str): The path to the input TSV file containing genomic data.
        - bed_path (str): The path to the BED file containing genomic intervals.
        - ref_path (str): The path to the reference FASTA file.
        """
        hs.check_input_path(in_path, [".tsv"])
        self.in_path = os.path.abspath(in_path)
        hs.check_input_path(bed_path, [".bed"])
        self.bed_path = os.path.abspath(bed_path)
        hs.check_input_path(ref_path, [".fasta", ".fa", ".fn"])
        self.ref_path = os.path.abspath(ref_path)

    def load_data(self) -> None:
        """
        Load data from the specified input file into the POISummary instance.

        Reads the data from a tab-separated values (tsv) file as created by the PileupExtractor module
        and stores it in the 'data' attribute of the class.
        """
        cols = ["chr", "site", "n_reads", "ref_base", "majority_base", "a_rate", "c_rate", "g_rate", "u_rate", "deletion_rate", "insertion_rate", "refskip_rate", "mismatch_rate", "mismatch_rate_alt", "q_mean", "motif", "neighbour_error_pos"]

        col_idx = {'chr': 0, 'site': 1, 'n_reads': 2, 'ref_base': 3, 'majority_base': 4, 'n_a': 5, 'n_c': 6, 'n_g': 7, 'n_t': 8, 'n_del': 9, 'n_ins': 10, 'n_ref_skip': 11, 'a_rate': 12, 'c_rate': 13, 'g_rate': 14, 'u_rate': 15, 'deletion_rate': 16, 'insertion_rate': 17, 'refskip_rate': 18, 'mismatch_rate': 19, 'mismatch_rate_alt': 20, 'motif': 21, 'q_mean': 22, 'q_std': 23, 'neighbour_error_pos': 24}
        dtypes = {'chr': str, 'site': int, 'n_reads': int, 'ref_base': str, 'majority_base': str, 'n_a': int, 'n_c': int, 'n_g': int, 'n_t': int, 'n_del': int, 'n_ins': int, 'n_ref_skip': int, 'a_rate': float, 'c_rate': float, 'g_rate': float, 'u_rate': float, 'deletion_rate': float, 'insertion_rate': float, 'refskip_rate': float, 'mismatch_rate': float, 'mismatch_rate_alt': float, 'motif': str, 'q_mean': float, 'q_std': float, 'neighbour_error_pos': str}
        
        with open(self.in_path, "r") as file:
            next(file)
            data = dict(zip(cols, [[] for _ in cols]))
            for line in file:
                line = line.strip().split("\t")
                for col in cols[:-1]:
                    data[col].append(dtypes[col](line[col_idx[col]]))
                if len(line) < 25:
                    data["neighbour_error_pos"].append(None)
                else:
                    data["neighbour_error_pos"].append(line[24])

            self.data = data
    
    def add_bed_info(self) -> None:
        """
        Add BED information to the data object based on a BED file.
        """
        tree = self.build_interval_tree(self.bed_path)
        self.data["bed_name"] = [self.get_name_for_position(chrom, site, tree) for chrom, site in zip(self.data["chr"], self.data["site"])]

    def get_name_for_position(self, chrom: str, site: int, interval_tree: IntervalTree) -> str|None:
        """
        Retrieve the name associated with a given genomic position from an interval tree.

        Parameters:
        - chrom (str): Sequence name of the given position.
        - site (int): Coordinate on the sequence.
        - interval_tree (IntervalTree): An IntervalTree data structure containing genomic intervals.

        Returns:
        - str | None: The name associated with the provided position if found, or None if not found.
        """
        results = interval_tree[site:site+1]  # Query the interval tree
        for interval in results:
            chromosome, name = interval.data
            if chromosome == chrom:
                return name
        return None

    def build_interval_tree(self, bed_file: str) -> IntervalTree:
        """
        Build an IntervalTree data structure from positions in a BED file.

        Parameters:
        - bed_file (str): The path to the BED file containing genomic intervals.

        Returns:
        - IntervalTree: An IntervalTree data structure containing the genomic intervals from the BED file.
        """
        interval_tree = IntervalTree()
        with open(bed_file, 'r') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    chromosome = parts[0]
                    start = int(parts[1])+1 # +1 to account for 0-index in BED files 
                    end = int(parts[2])+1 # +1 to account for 0-index in BED files
                    name = parts[3] if len(parts) >= 4 else None
                    interval_tree[start:end] = (chromosome, name)
        return interval_tree

    def process_categories(self, categories: str, counterparts: str|None, out_dir: str|None) -> None:
        """
        Process categories, counterparts, and output paths.

        Parameters:
        - categories (str): Comma-separated string of categories to be processed.
        - counterparts (str|None): Comma-separated string of counterparts or None if not provided.
        - out_dir (str): Path to a single output directory.

        Raises:
        - Exception: If a specified category is not found in the bed file.
        - Exception: If the number of counterparts does not match the number of categories.
        - Exception: If the number of output paths does not match the number of categories.

        Note:
        - If only one output path is provided, it is considered a directory, and individual
        output paths for each category are generated based on this directory.
        """
        # process given categories
        cat_split = categories.split(",")
        unique_cat = list(sorted([i for i in set(self.data["bed_name"]) if i]))
        for category in cat_split:
            if category not in unique_cat:
                raise Exception(f"Given name '{category}' was not found in the bed file.")
            
        # if given, process counterparts
        if counterparts:
            cou_split = counterparts.upper().split(",")
            if len(cou_split) != len(cat_split):
                raise Exception(f"For the {len(cat_split)} categories {len(cou_split)} corresponding bases were given. Each category must have a base it corresponds to.")
        else:
            cou_split = [None for _ in cat_split]

        # process output paths
        if out_dir:
            out_dir = os.path.abspath(out_dir)
            ext = os.path.splitext(out_dir)[1]
            if ext:
                hs.print_update(f"Warning: Extension {ext} was found. Make sure to provide a single output directory.")
            hs.check_create_dir(out_dir)
            out_paths = []
            for category, counterpart in zip(cat_split, cou_split):
                in_filename = os.path.splitext(os.path.basename(self.in_path))[0]
                filename = f"{in_filename}_{category}_{counterpart}_poisummary.html" if counterpart else f"{in_filename}_{category}_poisummary.html"
                out_paths.append(os.path.join(out_dir, filename))
        else:
            path_base = os.path.splitext(self.in_path)[0]
            out_paths = []
            for category, counterpart in zip(cat_split, cou_split):
                filepath = f"{path_base}_{category}_{counterpart}_poisummary.html" if counterpart else f"{path_base}_{category}_poisummary.html"
                out_paths.append(filepath)

        self.bed_categories = cat_split
        self.bed_categories_counterparts = cou_split
        self.output_paths = out_paths

    ##############################################################################################################
    #                                           Main processing methods                                          #
    ##############################################################################################################

    def main(self) -> None:
        """
        Main entry point of the script.

        This method iterates through the bed categories and their corresponding bases, processing each category using
        the `process_category` method.
        """
        for category, corr_base, output_path in zip(self.bed_categories, self.bed_categories_counterparts, self.output_paths):
            self.process_category(category, corr_base, output_path)

    def process_category(self, category: str, corresponding_base: str|None, output_path: str) -> None:
        """
        Process and analyze the data for a specific category and (optionally) corresponding base.

        This method generates multiple plots and saves them along with a summary HTML template. Optionally, it also
        writes the processed data to a TSV file.

        Parameters:
        - category (str): The category of interest.
        - corresponding_base (str): The corresponding base for the category.
        """
        time = hs.get_time()

        hs.print_update(f"Processing {category} sites. Subsetting data...", line_break=False)
        self.subset_category_data(category, corresponding_base)
        if corresponding_base:
            hs.print_update(f"Done. Found {len(self.category_data['chr'])} {category} and {len(self.counterpart_data['chr'])} {corresponding_base} sites.", with_time=False) # type: ignore
        else:
            hs.print_update(f"Done. Found {len(self.category_data['chr'])} {category} sites.", with_time=False)

        total = 8 if self.output_tsv else 7
        with tqdm(desc=f"{time} | POI map", total=total) as progress: 
            plot_mod_map = self.create_map_plot()
            progress.update()

            progress.set_description(f"{time} | Mismatch types")
            plot_motif = self.create_motif_plot()
            progress.update()

            progress.set_description(f"{time} | Mismatch types")
            plot_mism_types = self.create_mism_types_plot()
            progress.update()

            progress.set_description(f"{time} | Base compositions")
            plot_comp, p_val_table_comp = self.create_composition_plot()
            progress.update()

            progress.set_description(f"{time} | Error rates")
            plot_errrate, p_val_table_errrate = self.create_error_rate_plot()
            progress.update()
        
            progress.set_description(f"{time} | Neighbour mismatches")
            plot_nb = self.create_nb_plot()
            progress.update()

            plots = [plot_mod_map, plot_motif, plot_mism_types, plot_comp, plot_errrate, plot_nb]
            tables = [p_val_table_comp, p_val_table_errrate]

            progress.set_description(f"{time} | Writing to HTML")
            self.write_template(plots, tables, output_path)
            progress.update()

            if self.output_tsv:
                progress.set_description(f"{time} | Updating feature table")
                ft_path = self.write_tsv()
                progress.update()
                hs.print_update(f"Finished processing {category}. Wrote HTML summary to {output_path}. Wrote updated table to {ft_path}")
        if not self.output_tsv:
            hs.print_update(f"Finished processing {category}. Wrote output to {output_path}")

        hs.print_update("Finished.")


    ##############################################################################################################
    #                                          Data preparation methods                                          #
    ##############################################################################################################
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
            if total_length <= num_segments:
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

    def subset_category_data(self, category: str, counterpart: str|None) -> None:
        """
        Filters the internal data based on the provided category and counterpart values,
        creating two subsets: one for the specified category and another for the counterpart (if provided).

        It updates the following attributes:
        - self.category_data (dict): A dictionary containing subsets of data for the specified category.
        - self.counterpart_data (dict): A dictionary containing subsets of data for the specified counterpart.
        - self.current_category (str): The currently selected category.
        - self.current_counterpart (str|None): The currently selected counterpart.
        
        Parameters:
        - category (str): The category to filter the data by.
        - counterpart (str|None): The counterpart to filter the data by. If None, counterpart filtering is skipped.

        """
        bed_name_idx = list(self.data.keys()).index("bed_name")
        ref_base_idx = list(self.data.keys()).index("ref_base")
        data_keys = self.data.keys()
        key_idx = dict(zip([i for i in range(len(data_keys))], data_keys))

        subset_category = dict(zip(data_keys, [[] for _ in range(len(data_keys))]))
        subset_counterpart = dict(zip(data_keys, [[] for _ in range(len(data_keys))]))
        
        for elements in zip(*(self.data[key] for key in data_keys)):
            if elements[bed_name_idx] == category:
                for i, element in enumerate(elements):
                    subset_category[key_idx[i]].append(element)
            if counterpart:
                if elements[ref_base_idx] == counterpart:
                    for i, element in enumerate(elements):
                        subset_counterpart[key_idx[i]].append(element)
        
        self.category_data = subset_category
        self.counterpart_data = subset_counterpart

        self.current_category = category
        self.current_counterpart = counterpart

    def prepare_data_map(self) -> Tuple[List[float], Dict[str, List[int]], Dict[str, List[int]]]: 
        """
        Prepare data for creating a chromosome map.

        Parameters:
        - ref_path (str): Path to the reference file containing chromosome lengths.
        - category_data (Dict[str, List[int]]): Dictionary containing chromosome names ('chr') and their corresponding genomic coordinates ('site').
        - n_bins_seqmap (int, optional): Number of bins to divide each chromosome into. Default is 100.

        Returns:
        - List[float]: A list of y-values representing the positions of bins along the chromosome.
        - Dict[str, List[int]]: A dictionary containing chromosome names as keys and lists of counts of genomic coordinates falling into each bin as values.
        - Dict[str, List[int]]: A dictionary containing chromosome names as keys and integers representing the maximum coordinate value (exclusive) that each bin may contain.

        Example:
        AAAACCGCGUUGUG -> len=14, n_bins_seqmap=4 -> binsize=ceil(14/4)=ceil(3.5)=4 
        01234567890123                     -> [4,8,12]+[15]=[4,8,12,15]
                                        -> [1,4), [4,8), [8,12), [12,15)
        
        With coordinates = [1,5,6,7,14] -> counts=[1,3,0,1]
        """
        def custom_sort_key(item):
            """Custom sorting key function to sort chromosome names."""
            if item.isdigit():  # Check if the item is a digit
                return (int(item),)  # Convert to integer and sort numerically
            else:
                return (float('inf'), item)  # Place non-digits at the end

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

        # Calculate chromosome lengths
        ref_lens = get_ref_len(self.ref_path)
        present_seq = list(sorted(set(self.category_data["chr"]).intersection(ref_lens.keys()), key=custom_sort_key))

        pos_count = {} # stores the values for coloring the bins
        bin_sizes = {} 
        max_vals = {} # stores the values for labelling the bins
        for seq in present_seq:
            seq_len = ref_lens[seq]

            bin_size = math.ceil(seq_len / self.n_bins_seqmap)
            bin_sizes[seq] = bin_size
            # initialize the maximum coordinates that a bin may contain (excluded)
            max_vals[seq] = [bin_size*i for i in range(1,self.n_bins_seqmap)] + [seq_len+1] 
            # initialize counts for each bin with 0
            pos_count[seq] = [0]* self.n_bins_seqmap 

        # Count genomic coordinates falling into each bin
        for seq, site in zip(self.category_data["chr"], self.category_data["site"]):
            bin_index = site // bin_sizes[seq]
            pos_count[seq][bin_index] += 1

        # Generate y-values for bin positions along the chromosome
        y_vals = [i/self.n_bins_seqmap for i in range(self.n_bins_seqmap)]

        return y_vals, pos_count, max_vals
    
    def prepare_data_motif(self) -> Tuple[Dict[str, Dict[str, int]], int]:
        """
        Prepare data for a bar plot showing the motifs of the POIs. 

        Returns:
        - Dict[str, Dict[str, int]]: Dictionary containing the counts (int) for each relative position (second level) 
                                     and reference base (first level)
                                     
        """
        motif_len = len(self.category_data["motif"][0])
        middle_idx = motif_len//2
        rel_positions = [pos - middle_idx for pos in range(motif_len)]
        counts = defaultdict(lambda: dict(zip(rel_positions, [0]*len(rel_positions))))

        for idx, pos in enumerate(rel_positions):
            for motif in self.category_data["motif"]:
                base = motif[idx]
                counts[base][pos] += 1

        return dict(counts), motif_len

    def prepare_data_mism_types(self) -> Dict[str, Dict[str, int]]:
        """
        Prepare data for a confusion matrix based on mismatch counts.

        Returns:
        - Dict[str, Dict[str, int]]: Dictionary containing the counts for all combination of reference and
                                     called bases.
        """
        mis_count = {"A": {"A": 0, "C": 0, "G": 0, "U": 0, "Del": 0}, 
                    "C": {"A": 0, "C": 0, "G": 0, "U": 0, "Del": 0}, 
                    "G": {"A": 0, "C": 0, "G": 0, "U": 0, "Del": 0}, 
                    "U": {"A": 0, "C": 0, "G": 0, "U": 0, "Del": 0}}
        for ref, maj in zip(self.category_data["ref_base"], self.category_data["majority_base"]):
            if (ref != "args") & (maj != "N"):
                if maj=="-": maj="Del"
                mis_count[ref][maj] += 1
        return mis_count

    def prepare_data_composition(self) -> Tuple[Dict[str, Dict[str, float]], 
                                                Dict[str, Dict[str, float]], 
                                                List[str], 
                                                Dict[Tuple[str, str], Dict[str, str]]]:
        """
        Prepare the data for visualizing the base composition and performs the statistical comparisons of the base
        rates between the different groups in the data. The groups can be the following:
        - matched POIs
        - mismatched POIs

        If a canonical counterpart base is given:
        - matched counterpart base
        - mismatched counterpart base

        A, C, G and U rates are extracted for all given groups, the rates are statistically compared, the median of
        the rates are calculated for each group, the median rates are scaled to add up to 1 for each group and the
        x-values for the plotting functions are set up accordingly to the given groups. 
        The data is stored in nested Dictionaries where the first key corresponds to the group (matched POI, ...)
        and the second key corresponds to the feature (A-rate, ...). 

        Returns:
        - Dict[str, Dict[str, float]],         : Scaled median base rates
        - Dict[str, Dict[str, float]],         : Median base rates
        - List[str],                           : x-values for the plotting function
        - Dict[Tuple[str, str], Dict[str, str]]: Results of the statistical tests (returned by the compare_groups method)
        """
        def get_counts_rates(for_category: bool) -> Tuple[Dict[str, int], Dict[str, Dict[str, List[float]]]]:
            """
            Get the A, C, G and U rates at mismatched and matched sites for either positions of interest or at canonical
            counterpart bases (depending on for_category value). Also count the number of positions in each group.

            Parameters:
            - for_category (bool): Boolean for specifying the group at hand.

            Returns:
            - Dict[str, int]: Counts of matched and mismatched sites within the given groups
            - Dict[str, Dict[str, List[float]]]: A, C, G and U rates for each of the given groups
            """
            key_match, key_mismatch = ("category_match", "category_mismatch") if for_category else ("counterpart_match", "counterpart_mismatch")
            data = self.category_data if for_category else self.counterpart_data

            counts = {key_match: 0, key_mismatch: 0}
            rates = {key_match: {"A": [], "C": [], "G": [], "U": []}, 
                    key_mismatch: {"A": [], "C": [], "G": [], "U": []}}

            for ref, maj, a_rate, c_rate, g_rate, u_rate in zip(*(data[col] for col in ["ref_base", "majority_base", "a_rate", "c_rate", "g_rate", "u_rate"])): # type: ignore
                key = key_match if ref==maj else key_mismatch
                data_select = {"A": a_rate, "C": c_rate, "G": g_rate, "U": u_rate}
                counts[key] += 1
                for feature in ["A", "C", "G", "U"]:
                    rates[key][feature].append(data_select[feature])
            return counts, rates

        def get_median_rates(rate_dict: Dict[str, Dict[str, List[float]]]) -> Dict[str, Dict[str, float]]:
            """
            Calculates the median A, C, G and U rates for each group.

            Parameters:
            - rate_dict (Dict[str, Dict[str, List[float]]]): Dictionary containing the base rates for different groups
                as returned by the get_counts_rates function.
            
            Returns:
            - Dict[str, Dict[str, float]]: Median values of the different base rates for each group
            """
            median_rate_dict = {}
            for group in rate_dict.keys():
                median_rate_dict[group] = {}
                for subgroup in rate_dict[group].keys():
                    median_rate_dict[group][subgroup] = median(rate_dict[group][subgroup]) if len(rate_dict[group][subgroup])>0 else 0
            return median_rate_dict

        def get_scaled_median_rates(median_rate_dict: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
            """
            Scales the median base rates to add up to 1 for each group. Intended for visualizing different groups
            in a bar chart of height 1. 

            Parameters:
            - Dict[str, Dict[str, float]]: Median values of the different base rates for each group (as returned
                by get_median_rates)
            
            Returns:
            - Dict[str, Dict[str, float]]: Median values of the different base rates for each group scaled to 1
            """
            scaled_rate_dict = {}
            # calculate the sum of the A-, C-, G- and U-rates for each group
            for group, medians in median_rate_dict.items():
                scaled_rate_dict[group] = {}
                total = sum(medians.values())
                for feature in medians.keys():
                    scaled_rate_dict[group][feature] = median_rate_dict[group][feature] / total if total>0 else 0
            return scaled_rate_dict

        counts, rates = get_counts_rates(for_category=True)
        if self.current_counterpart:
            counts_cou, rates_cou = get_counts_rates(for_category=False)
            # merge dictionaries from category and counterpart
            # https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python#26853961
            counts = counts | counts_cou
            rates = rates | rates_cou
            # reorder dictionary
            counts = {k: counts[k] for k in ["category_match", "counterpart_match", "category_mismatch", "counterpart_mismatch"]}
            rates = {k: rates[k] for k in ["category_match", "counterpart_match", "category_mismatch", "counterpart_mismatch"]}

            x_vals = [f"<i>{self.current_category}</i> match<br>(n = {counts['category_match']})",
                    f"{self.current_counterpart} match<br>(n = {counts['counterpart_match']})",
                    f"<i>{self.current_category}</i> mismatch<br>(n = {counts['category_mismatch']})",
                    f"{self.current_counterpart} mismatch<br>(n = {counts['counterpart_mismatch']})"]
        else:
            x_vals = [f"<i>{self.current_category}</i> match<br>(n = {counts['category_match']})",
                    f"<i>{self.current_category}</i> mismatch<br>(n = {counts['category_mismatch']})"]

        median_rates = get_median_rates(rates)
        scaled_median_rates = get_scaled_median_rates(median_rates)
        stat_comp_results = self.compare_groups(rates)

        return scaled_median_rates, median_rates, x_vals, stat_comp_results
    
    def prepare_data_errorrates(self) -> Tuple[Dict[str, List[float]], 
                                        List[str], 
                                        Dict[Tuple[str, str], Dict[str, str]]]:
        """
        Prepare the data for visualizing the error rates and quality scores as boxplots and performs the 
        statistical comparisons of the rates between the different groups in the data. The groups can be 
        the following:
        - matched POIs
        - mismatched POIs

        If a canonical counterpart base is given:
        - matched counterpart base
        - mismatched counterpart base

        Mismatch, deletion, insertion, reference skip rates and qualtiy scores are extracted for all given groups and
        the rates are statistically compared. To get the data into the right shape for the plotly Box function, the 
        x- and y-values are flattened into two long lists X and Y where position i contains a x,y pair in X[i],Y[i]. 

        Returns:
        - Dict[str, List[float]],              : Scaled median base rates
        - List[str],                           : x-values for the plotting function
        - Dict[Tuple[str, str], Dict[str, str]]: Results of the statistical tests (returned by the compare_groups method)
        """
        def get_counts_rates(for_category: bool) -> Tuple[Dict[str, int], Dict[str, Dict[str, List[float]]]]:
            """
            Get the mismatch, deletion, insertion and reference skip rates and mean q-scores at mismatched and matched sites for either 
            positions of interest or at canonical counterpart bases (depending on for_category value). Also count the number of positions 
            in each group.

            Parameters:
            - for_category (bool): Boolean for specifying the group at hand.

            Returns:
            - Dict[str, Dict[str, List[float]]]: mismatch, deletion, insertion and reference skip rates and mean q-scores for each of the 
                                                given groups
            """
            key_match, key_mismatch = ("category_match", "category_mismatch") if for_category else ("counterpart_match", "counterpart_mismatch")
            data = self.category_data if for_category else self.counterpart_data
            
            counts = {key_match: 0, key_mismatch: 0}
            rates = {key_match: {"Mismatch rate": [], "Deletion rate": [], "Insertion rate": [], "Reference skip rate": [], "Mean q-score": []}, 
                    key_mismatch: {"Mismatch rate": [], "Deletion rate": [], "Insertion rate": [], "Reference skip rate": [], "Mean q-score": []}}
            
            cols = ["ref_base", "majority_base", self.perc_mismatch_col, "deletion_rate", "insertion_rate", "refskip_rate", "q_mean"]
            for ref, maj, mis_rate, del_rate, ins_rate, refskip_rate, q_mean in zip(*(data[col] for col in cols)): # type: ignore
                key = key_match if ref==maj else key_mismatch
                data_select = {"Mismatch rate": mis_rate, "Deletion rate": del_rate, "Insertion rate": ins_rate, "Reference skip rate": refskip_rate, "Mean q-score": q_mean}
                counts[key] += 1
                for feature in ["Mismatch rate", "Deletion rate", "Insertion rate", "Reference skip rate", "Mean q-score"]:
                    rates[key][feature].append(data_select[feature])
            return counts, rates

        counts, rates = get_counts_rates(for_category=True)
        if self.current_counterpart:
            counts_cou, rates_cou = get_counts_rates(for_category=False)
            # merge dictionaries from category and counterpart
            # https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python#26853961
            counts = counts | counts_cou
            rates = rates | rates_cou
            # reorder dictionary
            rates = {k: rates[k] for k in ["category_match", "counterpart_match", "category_mismatch", "counterpart_mismatch"]}

        # for plotly boxplots the x and y values need to be one long list containing x,y pairs at a position i in each list
            x_vals = [f"<i>{self.current_category}</i> match"] * min(counts["category_match"], self.n_bins) + \
                    [f"{self.current_counterpart} match"] * min(counts["counterpart_match"], self.n_bins) + \
                    [f"<i>{self.current_category}</i> mismatch"] * min(counts["category_mismatch"], self.n_bins) + \
                    [f"{self.current_counterpart} mismatch"] * min(counts["counterpart_mismatch"], self.n_bins)
        else:
            x_vals = [f"<i>{self.current_category}</i> match"] * min(counts["category_match"], self.n_bins) + \
                    [f"<i>{self.current_category}</i> mismatch"] * min(counts["category_mismatch"], self.n_bins)

        stat_comp_results = self.compare_groups(rates)

        # flatten the counts to be compatible with the plotly boxplot function
        # this is done here at the end so the statistical comparison can be performed beforehand
        rates_flat = {}
        for feature in rates["category_match"].keys():
            rates_flat[feature] = []
            for group in rates.keys():
                rates_flat[feature] += self.bin_data(rates[group][feature])

        return rates_flat, x_vals, stat_comp_results

    def prepare_nb_counts(self) -> Tuple[List[int], List[int], List[int], List[int], List[str], List[int]]:
        """
        Prepare data for analyzing neighboring error positions in a specified bed category.

        Returns:
            Tuple[List[int], List[int], List[int], List[int], List[str], List[int]]:
            A tuple containing:
            - x_vals (List[int]): Positions of neighboring errors.
            - y_vals (List[int]): Counts of neighboring errors.
            - x_vals_mod (List[int]): Positions of neighboring errors due to modifications.
            - y_vals_mod (List[int]): Counts of neighboring errors due to modifications.
            - pie_labs (List[str]): Labels for a pie chart indicating the presence of surrounding errors.
            - pie_vals (List[int]): Counts for the pie chart categories.

        Note:
            This method prepares data for analyzing neighboring error positions in a specified bed category.
            It extracts relevant data from the DataFrame, including neighboring error positions, and counts
            of these positions. Additionally, it identifies neighboring errors that are due to modifications.
            The resulting data is organized into lists for plotting, including a pie chart indicating the presence
            of surrounding errors.

        """
        def to_numeric(pos_str: str) -> List[int]:
            if len(pos_str) > 0:
                if pos_str.endswith(","): 
                    pos_str = pos_str[:-1] 
                return list(map(int, pos_str.split(",")))
            return []

        sites = [(c, s) for c, s in zip(self.category_data["chr"], self.category_data["site"])]

        n_no_nb = 0
        n_has_nb = 0
        n_has_nb_mod = 0

        counts = defaultdict(lambda: 0)
        counts_mod = defaultdict(lambda: 0)

        for site, nb_info in zip(sites, self.category_data["neighbour_error_pos"]):
            if nb_info:
                nb_info = to_numeric(nb_info)
                for distance in nb_info:
                    # check if pos + distance corresponds to another mod site
                    if (site[0], site[1]+distance) in sites:
                        n_has_nb_mod += 1
                        counts_mod[distance] += 1
                    else:
                        n_has_nb += 1
                        counts[distance] += 1
            else:
                n_no_nb += 1

        pie_labs = ["No surrounding errors", "Has surrounding errors", "Has surrounding error due to mod."]
        pie_vals = [n_no_nb, n_has_nb, n_has_nb_mod]

        return list(counts.keys()), list(counts.values()), list(counts_mod.keys()), list(counts_mod.values()), pie_labs, pie_vals

    ##############################################################################################################
    #                                            p-val table methods                                             #
    ##############################################################################################################
    def perform_test(self, set1: List[float], set2: List[float], alpha: float = 0.01) -> Tuple[float|None, str]:
        """
        Performs a series of tests to compare two sets of data. It checks for normality in both 
        samples and equal variances using normaltest and bartlett tests. If the conditions are
        met, it performs an independent t-test (TT), otherwise, it performs a Mann-Whitney U test (MWU).
        If the test fails returns None for the p-value and 'ERROR' for the test that was used.

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
                # return f"{ttest_ind(a=set1, b=set2)[1]:.5e} (TT)"
                return (ttest_ind(a=set1, b=set2)[1], "TT")
            else: # normal distribution in both samples and equal variances
                # return f"{mannwhitneyu(x=set1, y=set2)[1]:.5e} (MWU)"
                return (mannwhitneyu(x=set1, y=set2)[1], "MWU")
        except:
            return (None, "ERROR")

    def compare_groups(self, data: Dict[str, Dict[str, List[float]]]) -> Dict[Tuple[str, str], Dict[str, str]]:
        """
        Perform statistical tests between different combinations of (mis-)matched category and counterpart positions.

        Parameters:
        - data (Dict[str, Dict[str, List[float]]]): Dictionary containing the groups in the first level and some features for
                                                    a given group in the second level.

        Returns:
        - Dict[Tuple[str, str], Dict[str, str]]: Adjusted p-values For each statistical comparison. The groups that have been compared are 
                                                stored in the first level (Tuple[str,str]). The second level stores the feature (str) with
                                                the FDR and the test that was used. 
        """
        # get the groups that will be compared 
        if self.current_counterpart:
            comparisons = [("category_match", "counterpart_match"), 
                           ("category_mismatch", "counterpart_mismatch"), 
                           ("category_match", "category_mismatch"), 
                           ("counterpart_match", "counterpart_mismatch")]
        else:
            comparisons = [("category_match", "category_mismatch")]
        # get the features that are present the groups in the data at hand
        present_features = list(data["category_match"].keys())

        # collect the results in a list first to perform multiple testing correction later
        comps = []
        features = []
        p_vals = [] 
        tests = []
        comps_failed = []
        for group1, group2 in comparisons:
            for feature in present_features:
                res, test = self.perform_test(data[group1][feature], data[group2][feature], alpha=0.1)
                if res:
                    comps.append((group1, group2))
                    features.append(feature)
                    p_vals.append(res)
                    tests.append(test)
                else:
                    comps_failed.append((group1, group2))
        # adjust the p-values
        p_vals = list(fdrcorrection(p_vals)[1])
        
        # groups the data in a dictionary (level 1: groups that are compared, level 2: features)
        values = [{}, {}, {}, {}] if self.current_counterpart else [{}, {}]
        stat_results = dict(zip(comparisons, values))
        for groups, feature, fdr, test in zip(comps, features, p_vals, tests):
            stat_results[groups][feature] = f"{fdr:.5e} ({test})"
        for groups in comps_failed:
            for feature in present_features:
                stat_results[groups][feature] = "ERROR"
        return stat_results # type: ignore

    def create_stat_table(self, pvals: Dict[Tuple[str, str], Dict[str, str]]) -> str:
        """
        Given a nested dictionary containing (adjusted) p-values, aggregates these into a HTML table represented in
        a single string.
        
        Parameters:
        - pvals (Dict[Tuple[str, str], Dict[str, str]]): Nested dictionary, where the first key (Tuple[str, str])
            represents the two groups (group1, group2) to which the tests correspond. The second key corresponds
            to the features that were tested for these groups. P-values are stored as strings with the test that
            were used indicated behind it.

        Returns:
        - str: String representation of the HTML table containing all p-values. Each column corresponds to a 
            comparison between two groups. Each row corresponds to one feature. 
        """
        groups = list(pvals.keys())
        features = pvals[groups[0]].keys()
        
        colnames = {('category_match', 'counterpart_match'):       f"<th>{self.current_category} match vs. {self.current_counterpart} match</th>",
                    ('category_mismatch', 'counterpart_mismatch'): f"<th>{self.current_category} mismatch vs. {self.current_counterpart} mismatch</th>",
                    ('category_match', 'category_mismatch'):       f"<th>{self.current_category} match vs. {self.current_category} mismatch</th>",
                    ('counterpart_match', 'counterpart_mismatch'): f"<th>{self.current_counterpart} match vs. {self.current_counterpart} mismatch</th>"}
        header = "".join([colnames[g] for g in groups]) # type: ignore

        table = "<table><thead><th></th>"+header+"</thead><tbody>"

        for feature in features:
            row = f"<tr><td>{feature}</td>"
            for group in groups:
                row += f"<td>{pvals[group][feature]}</td>"
            table += row+"</tr>"
        table += "</tbody></table>"
        return table

    ##############################################################################################################
    #                                              Plotting methods                                              #
    ##############################################################################################################

    def create_map_plot(self) -> go.Figure:
        """
        Creates a plot showing the approximate positions of interest on the given sequences. Sequences are represented
        by a set number of bins that group specific ranges of coordinates. The number of POIs in each of these ranges
        is indicated by the colors. Only sequences that contains POIs are shown in the plot to keep it simple.

        Returns:
            go.Figure: A Plotly figure object representing the map plot. 
        """
        try:
            y_vals, pos_count, max_vals = self.prepare_data_map()

            fig = go.Figure()
            fig = hs.update_plot(fig, height=600, width=1200)
            tickvals = []
            ticktext = []
            bin_height = y_vals[1]
            # set up a map for each sequence that is present
            for x, seq in enumerate(pos_count.keys(), start = 1):
                tickvals.append(x)
                ticktext.append(seq)
                bins = []
                # transform the counts integer into color values from 0 to the maximum count
                max_count = max(pos_count[seq])
                colors = px.colors.sample_colorscale("portland", [val/max_count for val in pos_count[seq]])
                bin_start = [1]+max_vals[seq]
                bin_end = max_vals[seq]
                for y, color, count, lab_start, lab_end in zip(y_vals, colors, pos_count[seq], bin_start, bin_end):
                    # create a rectangle for each bin
                    bin = go.Scatter(x=[x-0.3, x-0.3, x+0.3, x+0.3, x-0.3], 
                                    y=[y,y+bin_height,y+bin_height,y,y], 
                                    name=f"{lab_start}-{lab_end} | #POIs: {count}",
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
        except Exception as e:
            fig = hs.create_error_placeholder(e)
        return fig

    def create_motif_plot(self) -> go.Figure:
        """
        Create a bar plot visualizing the motifs at positions of interest.

        Returns:
        - go.Figure: A Plotly figure representing the motifs at positions of interest.
        """
        try:
            counts, motif_len = self.prepare_data_motif()
            fig = go.Figure()
            fig = hs.update_plot(fig, width=1200)

            colors = {"A": "#2ca02c", "C": "#1f77b4", "G": "#ff7f0e", "U": "#d62728"}
            bars = []
            for base in sorted(counts.keys()):
                x_vals = list(counts[base].keys())
                y_vals = list(counts[base].values())
                color = colors[base] if base in colors.keys() else "#A0A0A0"
                bar = go.Bar(x=x_vals, y=y_vals, name=base, marker=dict(color=color, line_color="#000000", line_width=2))
                bars.append(bar)

            fig.add_traces(bars)
            fig.update_layout(barmode="stack") 
            fig.update_xaxes(title=f"Relative {motif_len}-mer position")
            fig.update_yaxes(title="Count")
        except Exception as e:
            fig = hs.create_error_placeholder(e)
        return fig

    def create_mism_types_plot(self) -> go.Figure:
        """
        Create a heatmap plot visualizing mismatch types.

        Returns:
        go.Figure:
            A Plotly figure representing the mismatch types heatmap.

        The method generates a heatmap plot that visualizes mismatch types between called and reference bases.
        The x-axis represents the called bases, the y-axis represents the reference bases, and the color
        represents the count of occurrences for each mismatch type. The plot is customized for clear visualization.
        """
        mis_count = self.prepare_data_mism_types()

        try:
            fig = go.Figure()
            fig = hs.update_plot(fig, ylab="Reference base", xlab="Called base")
            counts = [[mis_count[row][col] for col in ["A", "C", "G", "U", "Del"]] for row in ["A", "C", "G", "U"]]
            heatmap = go.Heatmap(x=["A", "C", "G", "U", "Del"],
                                y=["A", "C", "G", "U"],
                                z=counts,
                                colorscale="portland",
                                hoverinfo="z",
                                hovertemplate="%{y}-%{x}<br>Count: %{z}",
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
        except Exception as e:
            fig = hs.create_error_placeholder(e)
        return fig

    def create_composition_plot(self) -> Tuple[go.Figure, str]:
        """
        Creates a figure displaying the base compositions at positions of interest and their corresponding
        canonical counterpart bases (if specified). Also sets up an HTML table to display the statistical
        comparisons between the base rates of the different groups.

        Returns:
        - go.Figure: Base composition figure
        - str: String representation of the HTML table containing adjusted p-values
        """
        median_base_rates_scaled, median_base_rates, x_vals, fdrs = self.prepare_data_composition()
        try:
            keys = median_base_rates_scaled.keys()

            fig = go.Figure()
            fig = hs.update_plot(go.Figure(), ylab="Relative abundance", height=600, width=1200)

            bars = []
            for feature, color in [("A", "#2ca02c"), ("C", "#1f77b4"), ("G", "#ff7f0e"), ("U", "#d62728")]:
                bar = go.Bar(x=x_vals, y=[median_base_rates_scaled[i][feature] for i in keys], name=feature, marker=dict(color=color), customdata=[median_base_rates[i][feature] for i in keys], hovertemplate="Scaled median rate: %{y}<br>Unscaled median rate: %{customdata}")
                bars.append(bar)

            fig.add_traces(bars)
            fig.update_layout(barmode="stack")
            fig.update_traces(marker=dict(line=dict(color="black", width=1.5)))
        except Exception as e:
            fig = hs.create_error_placeholder(e)

        stat_results_table = self.create_stat_table(fdrs)

        return fig, stat_results_table

    def create_error_rate_plot(self) -> Tuple[go.Figure, str]:
        """
        Create a grouped box plot visualizing error rates and quality scores.
        Generates a grouped box plot that visualizes error rates and quality scores for different groups. 
        The x-axis represents different conditions, and the y-axis represents the error rate or quality 
        score.
        
        Returns:
        - go.Figure: Plotly figure representing the box plots
        - str: HTML table summarizing statistical test results

        The method 
        """
        error_rates, x_vals, stat_comp_results = self.prepare_data_errorrates()
        try:
            fig = make_subplots(rows=1, cols=2, column_widths=[0.75, 0.25])
            fig = hs.update_plot(fig, height=800, width=1200)

            boxes = []
            for offset, (feature, color) in enumerate([("Mismatch rate", "#8c564b"), ("Deletion rate", "#e377c2"), ("Insertion rate", "#7f7f7f"), ("Reference skip rate", "#bcbd22")]):
                box = go.Box(x=x_vals, y=error_rates[feature], name=feature, offsetgroup=offset, line=dict(color="black"), marker=dict(outliercolor="black", size=2), fillcolor=color)
                boxes.append(box)
            fig.add_traces(boxes, rows=[1]*4, cols=[1]*4)

            box = go.Box(x=x_vals, y=error_rates["Mean q-score"], name="Mean q-score", offsetgroup=0, line=dict(color="black"), marker=dict(outliercolor="black", size=2), fillcolor="#17becf")
            fig.add_trace(box, row=1, col=2)

            fig.update_layout(boxmode="group")
            fig.update_yaxes(title_text="Error rate", row = 1, col = 1)
            fig.update_yaxes(title_text="Quality score", row = 1, col = 2)
        except Exception as e:
            fig = hs.create_error_placeholder(e)

        p_val_table = self.create_stat_table(stat_comp_results)

        return fig, p_val_table

    
    def create_nb_plot(self) -> go.Figure:
        """
        Create a neighbor position plot for a specified modification type.

        Returns:
            go.Figure: A Plotly figure representing the bar and pie plot.

        This method creates a neighbor position plot for a specified modification type. It prepares data for
        the plot, generates stacked bar charts for neighbor positions with and without modification errors,
        as well as a pie chart showing the distribution of surrounding errors, using Plotly, and returns the
        resulting plot as HTML code.

        """
        x_vals, y_vals, x_vals_mod, y_vals_mod, pie_labs, pie_vals = self.prepare_nb_counts()

        try:
            fig = hs.update_plot(make_subplots(rows=1, cols=2, column_widths=[0.75, 0.25], specs=[[{"type": "bar"}, {"type": "pie"}]]), width=1200)

            fig.add_trace(go.Bar(x=x_vals, y=y_vals, marker=dict(color="#d62728", line=dict(color='#000000', width=1.5)), name="nb. error"), row=1, col=1)
            fig.add_trace(go.Bar(x=x_vals_mod, y=y_vals_mod, marker=dict(color="#dd8452", line=dict(color='#000000', width=1.5)), name="nb. mod error"), row=1, col=1)
            fig.update_layout(barmode="stack")

            fig.update_xaxes(title = f"Relative position to {self.current_category} positions", row=1, col=1)
            fig.update_yaxes(title = "Count", row=1, col=1)

            fig.add_trace(go.Pie(labels=pie_labs, values=pie_vals, name="", 
                                marker=dict(colors=["#4c72b0", "#d62728", "#dd8452"], line=dict(color='#000000', width=1.5))), row=1, col=2)

            fig.update_layout(showlegend=False)
        except Exception as e:
            fig = hs.create_error_placeholder(e)
        return fig    
    
    ##############################################################################################################
    #                                               Output methods                                               #
    ##############################################################################################################
    def write_svg(self, fig: go.Figure, name: str, output_path) -> None:
        """
        Write a Plotly figure to an SVG file.

        Parameters:
        - fig (go.Figure): Plotly figure to be saved.
        - name (str): Name to be used for the output SVG file.

        Returns:
        None

        The method takes a Plotly figure and a name as input and writes the figure to an SVG file.
        The output file will be saved with a name based on the provided 'name' parameter and the
        instance's 'output_path'.
        """
        outpath = f"{os.path.splitext(output_path)[0]}_{name}.svg"
        fig.write_image(outpath)

    def figs_to_str(self, plot_figs: List[go.Figure]) -> List[str]:
        """
        Convert a list of Plotly figures to a list of HTML strings.

        Parameters:
        - plot_figs (List[go.Figure]): List of Plotly figures to be converted.

        Returns:
        List[str]: List of HTML strings representing the Plotly figures.

        The method takes a list of Plotly figures as input and converts each figure
        to its corresponding HTML representation. The resulting list contains HTML strings
        for each figure, suitable for embedding in a web page or displaying in an HTML environment.
        """
        return list(map(lambda x: to_html(x, include_plotlyjs=False), plot_figs))

    def write_template(self, plot_figs: List[go.Figure], tables: List[str], output_path: str) -> None:
        """
        Write a summary HTML report with interactive plots and tables.

        Parameters:
        - plot_figs (List[go.Figure]): List of Plotly figures to be included in the report.
        - tables (List[str]): List of HTML tables to be included in the report.

        Returns:
        None

        The method takes a list of Plotly figures and HTML tables, and generates an HTML report
        containing interactive plots and tables. The report includes sections for mapping positions,
        mismatch types, base compositions, error rates, and neighboring errors. If specified, SVG files
        of individual plots are also saved.
        """
        name = f"<i>{self.current_category}</i>"
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if self.export_svg:
            for fig, name in zip(plot_figs, ["poi_map", "poi_mismatch_types", "poi_base_comp", 
                                             "poi_error_rates", "poi_neighbours"]):
                self.write_svg(fig, name, output_path)

        plots = self.figs_to_str(plot_figs)

        css_string, plotly_js_string = hs.load_html_template_str()
        
        template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Neet - {self.current_category} summary</title>                        
                <style>{css_string}</style>
            </head>

            <body>
                <script>{plotly_js_string}</script>

                <header>
                    <h1>Positions of interest: {name}</h1>
                    <p>Produced by <a href="https://github.com/dietvin/neet">Neet</a> on <b>{time}</b></p>
                </header>
                
                <section>
                    <p class="intro-text">
                        This summary file was created from the extracted features in file <b>{self.in_path}</b> 
                        with <b>{self.current_category}</b> positions extracted from file <b>{self.bed_path}</b>. 
                        The plots are interactive and allow further information by hovering, zooming and panning.
                    </p>
                </section>

                
                <section>
                    <button class="collapsible">{name} positions - general information</button>
                    <div class="collapsible-content">
                        <h2 class="hiddentitle" id="map"></h2>

                        <h3>Mapping of {name} positions across the reference sequences</h3>
                        <div class="plot-container">
                            {plots[0]}
                        </div>
                        <p>
                            Map of sequences containing positions of interest. Sequences are binned into {self.n_bins_seqmap} chunks.
                            Number of {name} positions in each chunk are indicated by the coloring. Fasta file '{self.ref_path}' 
                            was used to extract reference sequence(s). Hover on positions for exact coordinates. 
                        </p>

                        <h3>Motifs at {name} positions</h3>
                        <div class="plot-container">
                            {plots[1]}
                        </div>
                        <p>
                            Motif compositions around {name} sites. Hover for the count of a base at each relative position in the kmer. 
                        </p>

                    </div>
                </section>

                <section>
                    <button class="collapsible">Mismatch types</button>
                    <div class="collapsible-content">
                        <h2 class="hiddentitle" id="mismatch_types"></h2>
                        
                        <h3>Confusion matrix of {name} positions containing mismatch types</h3>
                        <div class="plot-container">
                            {plots[2]}
                        </div>
                        <p>
                            Abundances of (mis-)match types at {name} sites. Hover for absolute counts.
                        </p>
                    </div>
                </section>

                <section>
                    <button class="collapsible">Base compositions</button>
                    <div class="collapsible-content">
                        <h2 class="hiddentitle" id="base_comp"></h2>

                        <h3>Base compositions for different {name} {f"and {self.current_counterpart} " if self.current_counterpart else ""}subsets</h3>
                        <div class="plot-container">
                            {plots[3]}
                        </div>
                        <p>
                            Each A/C/G/U element in the bars corresponds to the median count of a given base in a subset. The four medians were scaled to add up to one. 
                            {name} match: positions labelled {name} from the bed file, where the called base is equal to the reference base. 
                            {f"{self.current_counterpart} match: positions with reference base {self.current_counterpart}, where the called base is equal." if self.current_counterpart else ""}
                            {name} mismatch: positions labelled {name} from the bed file, where the called base differs from the reference base. 
                            {f"{self.current_counterpart} mismatch: positions with reference base {self.current_counterpart} , where the called base differs." if self.current_counterpart else ""}
                        </p>

                        <h3>Statistical comparisons of base rates from {name} {f"and {self.current_counterpart} " if self.current_counterpart else ""}subsets</h3>
                        <p>
                            False discovery rates (FDRs) from statistical tests between the A, C, G and U rates of different groups. "TT"=t-test for independent samples. "MWU"=Mann-Whitney-U test.
                            t-Tests are performed if both samples of a given comparison are normally distributed and the variances do not differ significantly.
                        </p>
                        <div class="table-box">
                            {tables[0]}
                        </div>

                    </div>
                </section>

                <section>
                    <button class="collapsible">Error rates</button>
                    <div class="collapsible-content">
                        <h2 class="hiddentitle" id="error_rates"></h2>

                        <h3>Error rates for different {name} {f"and {self.current_counterpart} " if self.current_counterpart else ""}subsets</h3>
                        <div class="plot-container">
                            {plots[4]}
                        </div>
                        
                        <p>
                            Left: Distributions of mismatch, deletion, insertion and reference skip rates for different subsets. Right: Distribution of mean quality scores for different subsets. 
                            {name} match: positions labelled {name} from the bed file, where the called base is equal to the reference base. 
                            {f"{self.current_counterpart} match: positions with reference base {self.current_counterpart}, where the called base is equal." if self.current_counterpart else ""}
                            {name} mismatch: positions labelled {name} from the bed file, where the called base differs from the reference base. 
                            {f"{self.current_counterpart} mismatch: positions with reference base {self.current_counterpart} , where the called base differs." if self.current_counterpart else ""}
                        </p>

                        <h3>Statistical comparisons of error rates from {name} {f"and {self.current_counterpart} " if self.current_counterpart else ""}subsets</h3>
                        <p>
                            False discovery rates (FDRs) from statistical tests between the mismatch, insertion deletion and reference skip rates of different groups. "TT"=t-test for independent 
                            samples. "MWU"=Mann-Whitney-U test. t-Tests are performed if both samples of a given comparison are normally distributed and the variances do not differ significantly.
                        </p>
                        <div class="table-box">
                            {tables[1]}
                        </div>

                    </div>
                </section>

                <section>
                    <button class="collapsible">Neighbouring errors</button>
                    <div class="collapsible-content">
                        <h2 class="hiddentitle" id="nb_errors"></h2>

                        <h3>Count of positions with high error rate in the surrounding of {name} positions</h3>
                        <div class="plot-container">
                            {plots[5]}
                        </div>
                        <p>
                            Left: Occurences of high mismatch rates two bases up- and downstream from {name} positions.
                            Right: Pie chart shows the (relative count) of different types of central {name} positions. 
                            Red indicates errors in the surrounding positions where the position in question
                            is also of type {name}. The count of surrounding error positions that do not fall under {name}
                            are colored orange. Blue corresponds to {name} positions where no surrounding errors are found.
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

    def write_tsv(self) -> str:
        """
        Write the processed data to a tab-separated values (TSV) file.

        The method writes the processed data, stored in the class attribute 'data', to a TSV file.
        The file will be named based on the input file path, and the suffix '_w_bed_info.tsv' will
        be added to indicate that bed information has been appended to the original data.

        Parameters:
        None

        Returns:
        - str: path to the newly written file

        Example:
        If self.in_path = "input_folder/example.txt", the output TSV file will be named
        "input_folder/example_w_bed_info.tsv".
        """
        outpath = f"{os.path.splitext(self.in_path)[0]}_w_bed_info.tsv"
        with open(outpath, "w") as out:
            out.write("\t".join(self.data.keys())+"\n")
            for vals in zip(*self.data.values()):
                vals = [str(val) for val in vals]
                out.write("\t".join(vals)+"\n")
        return outpath

if __name__=="__main__":
    p = POISummary(in_path="/home/vincent/projects/neet_project/data/45s_rrna/test/drna_cyt_extracted.tsv",
                    bed_path="/home/vincent/projects/neet_project/data/45s_rrna/rRNA_modifications_conv_cleaned.bed",
                    ref_path="/home/vincent/projects/neet_project/data/45s_rrna/RNA45SN1.fasta",
                    categories="psu", canonical_counterpart="U", output_tsv=False)
    p.main()
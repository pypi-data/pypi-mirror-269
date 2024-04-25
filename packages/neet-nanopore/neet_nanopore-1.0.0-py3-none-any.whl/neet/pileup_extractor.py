import re, os, io, tempfile, logging, datetime
from typing import Dict, List, Tuple
from tqdm import tqdm
import numpy as np
from multiprocessing import Queue, Process, cpu_count
from threading import Thread

try: # when invoked from the package
    from neet import helper_functions as hs
    from neet.summary import SummaryCreator
except ImportError: # when invoked directly
    import helper_functions as hs
    from summary import SummaryCreator


class FeatureExtractor:

    input_paths : List[str]
    output_paths : List[str]
    ref_path : str
    ref_sequences : Dict[str, str]
    
    filter_num_reads: int
    filter_perc_mismatch: float
    filter_perc_mismatch_alt: float
    filter_mean_quality: float
    filter_genomic_region: Tuple[str, int, int] | None

    num_processes_worker: int
    num_processes_writer: int
    queue_size: int
    temp_file_line_count: int

    window_size: int
    neighbour_error_threshold: float

    no_summary: bool

    use_logging: bool
    logger: logging.Logger
    loglevel: int
    logpath: str

    def __init__(self, 
                 in_paths: str,
                 ref_path: str,
                 out_dir: str | None = None, 
                 num_reads: int | None = None, 
                 mismatch_rate: float | None = None, 
                 mismatch_rate_alt: float | None = None,
                 perc_deletion: float | None = None,
                 mean_quality: float | None = None,
                 genomic_region: str | None = None,
                 num_processes: int = 16,
                 queue_size: int = 5000,
                 temp_file_line_count: int = 100000,
                 window_size: int = 2,
                 neighbour_error_threshold: float = 0.5,
                 no_summary: bool = False,
                 logging_level: str | None = None,
                 log_path: str | None = None) -> None:

        self.process_paths(ref_path, in_paths, out_dir)    

        # if one of the following arguments was not provided (i.e. arg=None), set variable to a value so nothing gets filtered out
        self.filter_num_reads = num_reads if num_reads is not None else 1
        self.filter_perc_mismatch = mismatch_rate if mismatch_rate else 0
        self.filter_perc_mismatch_alt = mismatch_rate_alt if mismatch_rate_alt else 0
        self.filter_perc_deletion = perc_deletion if perc_deletion else 0
        self.filter_mean_quality = mean_quality if mean_quality else 0
        self.filter_genomic_region = self.extract_positional_info(genomic_region) if genomic_region else None

        # set up number of processes and parameters for multiprocessing
        max_processes = cpu_count()-1 
        if num_processes > max_processes:
            hs.print_update(f"Specified {num_processes} processes, but only {max_processes} are available. Using {max_processes} processes instead.")
            self.log_message(f"Specified {num_processes} processes, but only {max_processes} are available. Using {max_processes} processes instead.", logging.INFO)
            num_processes = max_processes
        if num_processes >= 4:
            num_processes -= 1 # -1 for the combiner process
            self.num_processes_worker = int(round(0.7 * num_processes))
            self.num_processes_writer = num_processes - self.num_processes_worker
        else:
            hs.print_update(f"Specified {num_processes} processes, but at least 4 processes are needed. Assigning 2 worker, 1 writer and 1 progress process.")
            self.log_message(f"Specified {num_processes} processes, but at least 4 processes are needed. Assigning 2 worker, 1 writer and 1 progress process.", logging.INFO)
            self.num_processes_worker = 2
            self.num_processes_writer = 1
        self.queue_size = queue_size
        self.temp_file_line_count = temp_file_line_count
        # neighbour mismatch search parameters
        self.window_size = window_size
        self.neighbour_error_threshold = neighbour_error_threshold
        # create HTML summary
        self.no_summary = no_summary 

        # set up logging if specified
        if logging_level:
            self.use_logging = True
            self.set_up_logger(logging_level, log_path)
            self.log_init()
        else:
            self.use_logging = False


    #################################################################################################################
    #                                    Methods called during initialization                                       #
    #################################################################################################################

    def process_paths(self, ref_path: str, in_paths_str: str, out_dir: str | None) -> None:
        """
        Process input and output file paths for the data processing.

        This method processes the file paths provided for reference sequence, input data,
        and output data. It checks the validity of the paths and stores the processed
        information in the respective instance variables.

        Parameters:
        - ref_path (str): The file path to the reference fasta file.
        - in_paths (str): Comma-separated list of input file paths.
        - out_paths (str): Output file path or directory path.
        """
        # process input path(s)
        in_paths = in_paths_str.split(",")
        for path in in_paths: hs.check_input_path(path, [".msf", ".pup", ".pileup"])
        self.input_paths = [os.path.abspath(p) for p in in_paths]

        # process output path(s)
        self.output_paths = self.process_outpaths(out_dir)

        # process path to reference fasta
        hs.check_input_path(ref_path, [".fasta", ".fna", ".ffn", ".faa", ".frn", ".fa"])
        self.ref_sequences = hs.get_references(ref_path)
        self.ref_path = os.path.abspath(ref_path)

    def process_outpaths(self, out_dir: str|None) -> List[str]:
        """
        Checks if the given output directory is valid and joins it with a fitting filename for each input file.
        Output file paths are collected in a list and returned.

        Outfile format: "<out_dir>/<basename_infile>_extracted.tsv"

        Parameters:
        - out_dir (str): The output directory path. 
        
        Returns:
        - List[str]: List containing the filenames of one or more output files (depending on the number of input files)
        """
        if out_dir:
            out_dir = os.path.abspath(out_dir)
            ext = os.path.splitext(out_dir)[1]
            if ext:
                hs.print_update(f"Warning: Extension {ext} was found. Make sure to provide a single output directory.")
            hs.check_create_dir(out_dir)
            out_paths = []

            for in_path in self.input_paths:
                basename = os.path.splitext(os.path.basename(in_path))[0]
                outfile_path = os.path.join(out_dir, f"{basename}_extracted.tsv")
                out_paths.append(outfile_path)
        else:
            out_paths = []
            for in_path in self.input_paths:
                outfile_path = os.path.splitext(in_path)[0] + "_extracted.tsv"
                out_paths.append(outfile_path)

        return out_paths

    def extract_positional_info(self, data_string: str) -> Tuple[str, int, int] | None:
        """
        Extracts the chromosome name, start value, and end value from a string in the format "chromosome_name:start-end".
        Used if the user specified a specific genomic region.

        Parameters:
        - data_string (str): The input string in the format "chromosome_name:start-end".

        Returns:
        - Tuple[str, int, int]: A tuple containing the chromosome name (str), start value (int), and end value (int).
        """
        if (":" in data_string) & ("-" in data_string): 
            chromosome, positions = data_string.split(':')
            start_str, end_str = positions.split('-')
            start = int(start_str.replace(',', ''))
            end = int(end_str.replace(',', ''))
        else:
            chromosome = data_string
            start = 1
            end = len(self.ref_sequences[chromosome])

        if self.region_is_valid(chromosome, start, end):
            return chromosome, start, end
    
    def region_is_valid(self, chr: str, start: int, end: int) -> bool:
        """
        Checks if the chromosome is found in the reference sequences and if so, whether the given start and end
        coordinates are in range of the corresponding sequence.

        Parameters:
        - chr (str): sequence name
        - start (int): start coordinate
        - end (int): end coordinate

        Returns:
        - bool: True, if all information is valid

        Raises:
        - Exception, if not all information is valid. 
        """
        # check if chromosome name is found in self.ref_sequences
        if chr not in list(self.ref_sequences.keys()):
            raise Exception(f"Chromosome region error: Name '{chr}' not found in reference sequences from file '{self.ref_path}'")
        # check if start < end
        if start >= end:
            raise Exception(f"Chromosome region error: End position {end} must be larger than start position {start}.")
        # check if start is in range
        chr_len = len(self.ref_sequences[chr])
        if start <= 0 or start > chr_len:
            raise Exception(f"Chromosome region error: Start position {start} not in range of corrdinates 1-{chr_len} (both incl.).")
        # check if end is in range
        if end <= 0 or end > chr_len:
            raise Exception(f"Chromosome region error: End position {end} not in range of corrdinates 1-{chr_len} (both incl.).")
        return True


    #################################################################################################################
    #                                                Loggin methods                                                 #
    #################################################################################################################

    def set_up_logger(self, loglevel: str, logpath: str|None) -> None:
        """
        Sets the logging configuration (path to the log file; logging level) and initializes the logger.

        Parameters:
        - loglevel (str): Logging level that will be used for a given run
        - logpath (int | None): Path to the log file/directory. If None, a log file will be placed in the current directory.
        """
        # check if the loglevel is given correctly
        numeric_level = getattr(logging, loglevel.upper())
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {loglevel}")
        
        # check if a (valid) logpath is given or set a valid one
        filename = f"neet_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        if not logpath:
            logpath = os.path.join(os.getcwd(), filename)
        elif os.path.isfile(logpath):
            hs.check_output_path(logpath, extensions=[".log"])
        elif os.path.isdir(logpath):
            logpath = os.path.join(logpath, filename)

        # set up config
        logging.basicConfig(filename=logpath, level=numeric_level, filemode="w")
        self.logger = logging.getLogger("PileupExtractor")
        hs.print_update(f"Logging to file '{logpath}' with level {loglevel}")

    def log_message(self, msg: str, level: int) -> None:
        """
        Receives a message and the logging level and logs the message accordingly.

        Parameters:
        - msg (str): Logging message
        - level (int): Logging level (corresponding logging.DEBUG etc.)
        """
        if self.use_logging:
            if level == logging.DEBUG:
                self.logger.debug(msg)
            elif level == logging.INFO:
                self.logger.info(msg)
            elif level == logging.WARNING:
                self.logger.warn(msg)
            elif level == logging.ERROR:
                self.logger.error(msg)
            elif level == logging.CRITICAL:
                self.logger.critical(msg)

    def log_init(self) -> None:
        """
        Logs the parameters given for initialization. 
        """
        self.log_message(f"Starting Feature Extractor - {hs.get_time()}", logging.INFO)
        self.log_message("The following parameters have been specified:", logging.DEBUG)
        for var_name, val in zip(
            ["input_paths", "output_paths", "ref_path", "ref_sequences", 
              "filter_num_reads", "filter_perc_mismatch", "filter_perc_mismatch_alt", 
              "filter_mean_quality", "filter_genomic_region", "num_processes_worker",
              "num_processes_writer", "queue_size", "temp_file_line_count", 
              "window_size", "neighbour_error_threshold", "no_summary"],
            [self.input_paths, self.output_paths, 
             self.ref_path, list(self.ref_sequences.keys()), 
             self.filter_num_reads, self.filter_perc_mismatch, 
             self.filter_perc_mismatch_alt, self.filter_mean_quality, 
             self.filter_genomic_region, self.num_processes_worker, 
             self.num_processes_writer, self.queue_size, 
             self.temp_file_line_count, self.window_size, 
             self.neighbour_error_threshold, self.no_summary]
             
        ):
            self.log_message(f"{var_name} :  {val}", level=logging.DEBUG)

    def log_messages_mp(self, log_queue: Queue) -> None:
        """
        During processing of an input file, receives the logging messages from parallel processes
        from the Queue and directs them to the log_message method.

        Parameters:
        - log_queue (Queue[Tuple[str, int]]): Queue containing tuples of the message and logging level.
        """
        msg_elements = log_queue.get()
        while msg_elements:
            self.log_message(*msg_elements)
            msg_elements = log_queue.get()

    #################################################################################################################
    #                                   Methods called during the main processing                                   #
    #################################################################################################################

    def main(self) -> None:
        """
        Process multiple pairs of input and output files. Reads .pileup files and processes them in parallel using multiprocessing.
        """ 
        for in_file, out_file in zip(self.input_paths, self.output_paths):
            hs.print_update(f"Processing file '{in_file}'.")
            hs.print_update(f"Writing to '{out_file}'.")
            self.log_message(f"Start processing file '{in_file}'. Will write finished output to '{out_file}'.", logging.INFO)

            self.process_file(in_file, out_file)
            if not self.no_summary:
                self.create_summary_file(out_file)
        hs.print_update("Finished.")


    def process_file(self, in_file: str, out_file: str) -> None:
        """
        Process a single input file and write the extracted features to an output file.

        Parameters:
        - in_file (str): Path to the input file.
        - out_file (str): Path to the output file.
        """
        hs.print_update("Counting number of lines to process.")
        self.log_message(f"Counting lines in input file.", logging.INFO)

        n_lines = hs.get_num_lines(in_file)
        self.log_message(f"{n_lines} lines found in file", logging.INFO)

        hs.print_update(f"Initializing {self.num_processes_worker} worker processes.")
        self.log_message(f"Initializing {self.num_processes_worker} worker processes.", logging.INFO)
        
        input_queue = Queue(maxsize=self.queue_size)
        output_queue = Queue(maxsize=self.queue_size)
        tmpname_queue = Queue(maxsize=self.queue_size)
        progress_queue = Queue(maxsize=self.queue_size)
        log_queue = Queue(maxsize=self.queue_size)

        # initialize the logger thread to collect the logging messages from different processes
        logger_thread = Thread(target=self.log_messages_mp, args=(log_queue,))
        logger_thread.start()

        # initialize worker processes (processes that process the pileup input into an output string)
        worker_processes = []
        for _ in range(self.num_processes_worker):
            p = Process(target=self.worker, args=(input_queue, output_queue, log_queue))
            p.start()
            worker_processes.append(p)
        
        # initialize the writer processes (that write threshold number of lines to a SORTED temp file)
        writer_processes = []
        for i in range(self.num_processes_writer):
            p = Process(target=self.writer, args=(output_queue, tmpname_queue, progress_queue, i, log_queue))
            p.start()
            writer_processes.append(p)
        
        # combine the sorted tempfiles into one sorted output file
        combiner_process = Process(target=self.combine_tmp_files, args=(tmpname_queue, out_file, log_queue))
        combiner_process.start()

        progress_thread = Thread(target=self.update_progress, args=(progress_queue, n_lines))
        progress_thread.start()

        with open(in_file, "r") as f:
            for idx, line in enumerate(f):
                input_queue.put((idx, line))

        for _ in range(self.num_processes_worker): input_queue.put((None, None))
        for p in worker_processes: p.join()

        for _ in range(self.num_processes_writer): output_queue.put((None, None))
        for p in writer_processes: p.join()

        progress_queue.put(None)
        progress_thread.join()

        tmpname_queue.put(None)
        combiner_process.join()

        log_queue.put(None)
        logger_thread.join()

    def worker(self, input_queue: Queue, output_queue: Queue, log_queue: Queue):
        """
        Worker process to process lines from the input queue and put processed results into the output queue.

        Parameters:
        - input_queue (Queue[Tuple[int, str]]): Input queue containing Tuples of line indices and lines to be processed.
        - output_queue (Queue[Tuple[int, str]]): Output queue containing Tuples of line indices and processed results.
        - log_queue (Queue[Tuple[str, int]]): Queue containing Tuples of logging messages and the logging level 
        """
        idx, line = input_queue.get()
        while idx:
            processed_line = self.process_position(line, idx, log_queue)
            output_queue.put((idx, processed_line))
            idx, line = input_queue.get()
        
    def writer(self, output_queue: Queue, tmpname_queue: Queue, progress_queue: Queue, process_id: int, log_queue: Queue):
        """
        Writer process to collect processed lines and write them to temporary files.

        Parameters:
        - output_queue (Queue[Tuple[int, str]]): Output queue containing Tuples of indices and processed lines.
        - tmpname_queue (Queue[str]): Queue to store names of temporary files.
        - progress_queue (Queue[bool]): Queue to update progress. Add True to update progress bar.
        - threshold (int): Threshold number of lines before writing to a temporary file.
        - process_id (int): Process identifier.
        - log_queue (Queue[Tuple[str, int]]): Queue containing Tuples of logging messages and the logging level 
        """                   
        outline_collection = []

        output_element = output_queue.get()
        # collect output lines until the threshold is reached, at this point a tempfile is created and the collected 
        # lines are written to file and the outline_collection is reset
        while output_element[0]:
            # only add sucessfully processed lines to the collection (doing it here and not in the worker process
            # to keep the progress bar from updating properly) 
            if output_element[1] != "":
                outline_collection.append(output_element)

            if len(outline_collection) > self.temp_file_line_count:
                self.__write_tempfile(outline_collection, process_id, tmpname_queue, log_queue)
                outline_collection = []

            progress_queue.put(True)
            output_element = output_queue.get()

        # write the remaining elements in the collection to file
        self.__write_tempfile(outline_collection, process_id, tmpname_queue, log_queue)

    def __write_tempfile(self, outline_collection: List[Tuple[int, str]], process_id: int, tmpname_queue: Queue, log_queue: Queue) -> None:
        """
        Write the collected outlines to a temporary file.

        Parameters:
        - outline_collection (List[Tuple[int, str]]): Collection of outlines, each containing an index and a string.
        - process_id (int): Identifier of the process.
        - tmpname_queue (Queue[str]): Queue to store the name of the temporary file.
        - log_queue (Queue[Tuple[str, int]]): Queue containing Tuples of logging messages and the logging level 
        """
        with tempfile.NamedTemporaryFile(mode="w", prefix=f"neet_{str(process_id)}_", delete=False) as tmpfile:
            log_queue.put((f"Creating temporary file {tmpfile.name}", logging.DEBUG))
            outline_collection = sorted(outline_collection, key=lambda x: x[0])
            tmpfile.writelines([f"{outline[0]}|{outline[1]}" for outline in outline_collection])
            tmpname_queue.put(tmpfile.name)

    def update_progress(self, progress_queue: Queue, n_lines: int):
        """
        Update progress using tqdm based on progress queue.

        Parameters:
        - progress_queue (Queue[bool]): Progress queue.
        - n_lines (int): Total number of lines to process.
        """
        with tqdm(total=n_lines, desc=f"{hs.get_time()} | Processing pileup rows") as progress:
            increment = progress_queue.get()
            while increment:
                progress.update()
                increment = progress_queue.get()
        
    def combine_tmp_files(self, tmpname_queue: Queue, output_file: str, log_queue: Queue) -> None:
        """
        Combine temporary files into one sorted output file using the SortedFileMerge
        class to perform the merging in a multithreaded fashion for big runtime boost.        
        Example with 400 files with 100000 lines each:
        
        Single threaded:
        Merging temporary files: 100%|█████████▉| 399/399 [1:07:40<00:10, 10.18s/it]
        Multi threaded:
        Merging temporary files: 100%|██████████| 399/399 [09:39<00:00,  1.45s/it]

        Parameters:
        - tmpname_queue (Queue[str]): Queue containing names of temporary files.
        - output_file (str): Output file path.
        - log_queue (Queue[Tuple[str, int]]): Queue containing Tuples of logging messages and the logging level 
        """
        tmpfiles = []
        tmpfile = tmpname_queue.get()
        while tmpfile:
            tmpfiles.append(tmpfile)
            tmpfile = tmpname_queue.get()
        
        log_queue.put((f"Start combining {len(tmpfiles)} temporary files", logging.INFO))
        tmp_file_merger = hs.SortedFileMerge(tmpfiles, n_threads=50)
        final_tmpfile = tmp_file_merger.start()
        self.__write_final_output(final_tmpfile, output_file)

    def __write_final_output(self, last_tmpfile: str, output_file: str) -> None:
        """
        Write final output file from the last temporary file. This includes removing the first index
        columns as well as performing the neighbouring mismatch search.

        Parameters:
        - last_tmpfile (str): Path to the last temporary file.
        - output_file (str): Output file path.
        """
        final_output_progress = tqdm(desc=f"{hs.get_time()} | Writing final output")
        self.log_message("Starting final processing iteration. Performing neighbourhood error search.", logging.INFO)

        nb_size_full = 1 + 2 * self.window_size
        nb_lines = []
        nb_first = True
        with open(last_tmpfile, "r") as tmp, open(output_file, "w") as out:
            out.write("chr\tsite\tn_reads\tref_base\tmajority_base\tn_a\tn_c\tn_g\tn_u\tn_del\tn_ins\tn_ref_skip\ta_rate\tc_rate\tg_rate\tu_rate\tdeletion_rate\tinsertion_rate\trefskip_rate\tmismatch_rate\tmismatch_rate_alt\tmotif\tq_mean\tq_std\tneighbour_error_pos\n")
            
            for line in tmp:
                outline = line.split("|")[1]
                # fill up the sliding window to the specified size
                nb_lines.append(outline)
                # remove the first element if the sliding window moved
                if len(nb_lines) > nb_size_full:
                    nb_lines.pop(0)
                # process the sliding window (i.e. add the neighbourhood info and write to the output file)
                if len(nb_lines) == nb_size_full:
                    if nb_first:
                        nb_first = False
                        self.__write_edge_lines(nb_lines, out, start=True)
                    self.__write_center_line(nb_lines, out)
                final_output_progress.update()
            # process the remaining lines once the final tempfile has run through completely 
            if len(nb_lines) < nb_size_full:
                for current_pos in range(len(nb_lines)):
                    outline = self.process_small(current_pos, nb_lines)
                    out.write(outline)
            else:
                self.__write_edge_lines(nb_lines, out, start=False)

            os.unlink(last_tmpfile)

            final_output_progress.update()
        final_output_progress.close()

        hs.print_update(f"Finished. Wrote output to '{output_file}'.")
        self.log_message(f"Finished processing. Final output file at '{output_file}'.", logging.INFO)

    def __write_edge_lines(self, neighbourhood: List[str], outfile: io.TextIOWrapper, start: bool = True) -> None:
        """
        Writes the neighbourhood information for the first or last rows as returned by the process_edge method.

        Parameters:
        - neighbourhood: A list of lines representing the current neighbourhood.
        - outfile: The output file to write the edge lines to.
        - start: A boolean indicating if it's the start or end of the neighbourhood.
        """
        k = self.window_size
        r = range(k) if start else range(k+1, 2*k+1)
        for current_pos in r:
            outline = self.process_edge(current_pos, neighbourhood, start)
            outfile.write(outline)

    def __write_center_line(self, neighbourhood: List[str], outfile: io.TextIOWrapper) -> None:
        """
        Writes the neighbourhood information for the center position of a full-sized neighbourhood.

        Parameters:
        - neighbourhood: A list of lines representing the current neighbourhood.
        - outfile: The output file to write the edge lines to.
        """
        outline = self.process_neighbourhood(neighbourhood)
        outfile.write(outline)
                
    def create_summary_file(self, file_path: str) -> None:
        """
        Create a summary file from the newly created tsv file.

        Parameters:
        - file_path (str): Path to the newly created tsv output.
        """
        summary_creator = SummaryCreator(file_path)
        summary_creator.main()

    #################################################################################################################
    #                                   Methods called during feature extraction                                    #
    #################################################################################################################

    def process_position(self, line_str: str, idx: int, log_queue: Queue) -> str:
        """
        Processes a single position from the pileup data.

        Parameters:
        - line_str (str): A string containing tab-separated data for a single position from the pileup file.
        - idx (int): index corresponding to the position of the line in the pileup file.
        - log_queue (Queue[Tuple[str, int]]): Queue containing Tuples of logging messages and the logging level 

        Returns:
        - str: The processed line as a string.
        """
        line = line_str.split("\t")
        # extract elements from list
        try:
            chr, site, ref_base, read_bases, read_qualities = line[0], int(line[1]), line[2].replace("T", "U"), line[4], line[5]
        except:
            log_queue.put((f"{idx} - Failed to extract elements", logging.DEBUG))
            return ""
            
        # filter by genomic region
        region = self.filter_genomic_region
        if region is not None:
            if not(chr == region[0] and site >= region[1] and site <= region[2]): # both start and end inclusive
                log_queue.put((f"{idx} - Position filtered because outside of specified regions.", logging.DEBUG))
                return ""

        # extract coverage and filter by number of reads if the standard coverage option is used 
        n_reads = int(line[3])
        if n_reads < self.filter_num_reads: 
            log_queue.put((f"{idx} - Position filtered because of low coverage.", logging.DEBUG))
            return ""

        # get reference sequence 
        try:
            ref = self.ref_sequences[chr]
        except:
            log_queue.put((f"{idx} - Could not get reference sequence from sequence {chr}.", logging.DEBUG))
            return ""
        # get absolute number of A, C, G, U, ins, del
        count, ref_skip_positions = self.parse_pileup_string(read_bases, ref_base)

        # get qualitiy measures
        quality_mean, quality_std = self.get_read_quality(read_qualities, ref_skip_positions)
        # filter by mean read quality
        if quality_mean < self.filter_mean_quality: 
            log_queue.put((f"{idx} - Position filtered because of low quality.", logging.DEBUG))
            return ""

        # in case the alternative way of calculating the coverage is specified
        # could use if else statement and get the other case down here, but then 
        # the count will be calculated each time, potentially wasting time in case the 
        # filter_num_reads is used
        n_reads_alt = count["a"]+count["c"]+count["g"]+count["u"]

        # get relative number of A, C, G and U counts
        count_rel = self.get_relative_count(count, n_reads)
        count_rel_alt = self.get_relative_count(count, n_reads_alt)

        # filter by percentage of deletions
        if count_rel["del"] < self.filter_perc_deletion: 
            log_queue.put((f"{idx} - Position filtered because of low deletion rate.", logging.DEBUG))
            return ""

        # get allele fraction
        mismatch_rate = self.get_mismatch_perc(count_rel, ref_base)
        mismatch_rate_alt = self.get_mismatch_perc(count_rel_alt, ref_base)

        # filter by mismatch_rate
        if mismatch_rate < self.filter_perc_mismatch:
            log_queue.put((f"{idx} - Position filtered because of low mismatch rate.", logging.DEBUG))
            return ""
        if mismatch_rate_alt < self.filter_perc_mismatch_alt:
            log_queue.put((f"{idx} - Position filtered because of low alternative mismatch rate.", logging.DEBUG))
            return ""

        # get majority base
        majority_base = self.get_majority_base(count)

        # get 11b motif
        motif = self.get_motif(site, ref, k=2)
        if motif == "":
            log_queue.put((f"{idx} - Could not extract motif from reference sequence.", logging.DEBUG))


        out = f'{chr}\t{site}\t{n_reads}\t{ref_base}\t{majority_base}\t{count["a"]}\t{count["c"]}\t{count["g"]}\t{count["u"]}\t{count["del"]}\t{count["ins"]}\t{count["ref_skip"]}\t{count_rel["a"]}\t{count_rel["c"]}\t{count_rel["g"]}\t{count_rel["u"]}\t{count_rel["del"]}\t{count_rel["ins"]}\t{count_rel["ref_skip"]}\t{mismatch_rate}\t{mismatch_rate_alt}\t{motif}\t{quality_mean}\t{quality_std}\n'
        return out

    def remove_indels(self, pileup_string: str) -> str:
        """
        Takes a pileup string and removes all occurences of the following patterns:
        '\\+[0-9]+' for insertions
        '\\-[0-9]+' for deletions
        In addition to the pattern itself, remove the following n characters,
        where n is the number specified after + or -.

        Parameters:
        - pileup_string (str): Pileup string extracted from the fifth column of a pileup file

        Returns:
        - str: Pileup strings with all occurences of the patterns above removed
        """
        pattern = "(\\+|\\-)[0-9]+"
        
        # get the start and end indices of all found patterns 
        coords = []
        for m in re.finditer(pattern, pileup_string):
            str_len_as_str = pileup_string[m.start()+1:m.end()]
            num_digits = len(str_len_as_str)
            str_len = int(str_len_as_str)
            coords.append((m.start(), m.start()+1+num_digits+str_len))

        # remove the patterns by the indices
        for start, end in reversed(coords): # reverse list as to not shift the index downstream
            pileup_string = pileup_string[:start] + pileup_string[end:]

        return pileup_string

    def parse_pileup_string(self, pileup_string: str, ref_base: str) -> Tuple[Dict[str, int], List[int]]:
        """
        Extracts the number of each base called at a given position, as well as the number
        of insertions and deletions. Information is extracted from a pileup string (fifth
        column in a pileup file).

        Parameters:
        - pileup_string (str): Pileup string extracted from the fifth column of a pileup file
        - ref_base (str): reference base at the position corresponding to the pileup string

        Returns:
        - Dict[str, int]: Dictionary containing the number of A, U, C, G, insertions, deletions and reference skips.
        - List[int]: List of indices in the pileup string where a reference skip is found 
            -
            
        """
        pileup_string = pileup_string.lower()
        # remove all occurences of a caret and the following letter (could contain a,c,g,t)
        pileup_string = re.sub(r'\^.', '', pileup_string)

        ref_base = ref_base.lower()
        count_dict = {"a": 0, "u": 0, "c": 0, "g": 0, "del": 0, "ins": 0}
        
        # get number of deletions
        count_dict["del"] = pileup_string.count("*")
        # get number of insertions
        count_dict["ins"] = len(re.findall(r'\+[0-9]+[ACGTNacgtn]+', pileup_string))

        # remove indel patterns to count the number of mismatches correctly
        pileup_string = self.remove_indels(pileup_string)

        # get number of mismatches (i.e. [ACGT])
        count_dict["a"] = pileup_string.count("a")
        count_dict["u"] = pileup_string.count("t")
        count_dict["c"] = pileup_string.count("c")
        count_dict["g"] = pileup_string.count("g")

        # get number of matches (determine where to count matches bases on ref_base)
        n_matches = pileup_string.count('.') + pileup_string.count(',')
        count_dict[ref_base] = n_matches

        # get number of reference skips
        n_ref_skips = pileup_string.count("<") + pileup_string.count(">")
        count_dict["ref_skip"] = n_ref_skips

        # get the indices from the > & < positions, to filter out of the quality string later on
        # (the corresponding positions refer to the read quality, not the quality of the position on the reads)
        pileup_string = re.sub(r'\*', "", pileup_string)

        # get the indices of reference skips in the pileup string (needed for the extraction of quality scores)
        ref_skip_idc = [i for i, char in enumerate(pileup_string) if (char==">") | (char=="<")]

        return count_dict, ref_skip_idc

    def get_relative_count(self, count_dict: Dict[str, int], n_reads: int) -> Dict[str, float]:
        """
        Gets a dictionary containing the absolute counts for A, C, G and U
        and calculates the relative proportions

        Parameters:
        - count_dict (Dict[int]): Dictionary containing the absolute counts for A, C, G and U
        - n_reads (int): Number of reads at the given position

        Returns:
        - Dict[str, float]: Dictionary containing the relative counts (float) for A, C, G and U (str)
        """
        #n_reads = sum([count_dict["a"], count_dict["c"], count_dict["g"], count_dict["u"]])
        rel_dict = {}
        for category in ["a", "c", "g", "u", "del", "ins", "ref_skip"]:
            try:
                rel_dict[category] = count_dict[category] / n_reads
            except:
                rel_dict[category] = 0

        return rel_dict

    def get_majority_base(self, count_dict: Dict[str, int]) -> str:
        """
        Gets a dictionary containing the absolute counts for A, C, G and U and returns the
        key of the one with the highest count.

        Parameters:
        - count_dict (Dict[str, int]): Dictionary containing the absolute counts for A, C, G and U

        Returns:
        - str: Key from the dictionary corresponding to the largest value
        """
        dict_subset = dict((k, count_dict[k]) for k in ("a", "c", "g", "u"))
        dict_subset["-"] = count_dict["del"] # type: ignore

        return max(dict_subset, key = lambda k: dict_subset[k]).upper()

    def get_motif(self, site: int, ref: str, k: int) -> str:
        """
        Extracts the motif of k bases up- and downstream from a given chromosomal site.
        Around the start and end of a refernce sequence the missing bases are filled with
        Ns.

        Parameters:
        - site (int): Position on the chromosome (1-indexed)
        - ref (str): Reference sequence for the given chromosome 
        - k (int): Number of bases to be regarded in both up- and downstream direction 
            
        Returns:
        - str: Sequence of k bases around the center site
        """ 
        idx = site-1
        n_ref = len(ref)

        if idx >= 0 and idx < n_ref:
            idx_l = idx-k
            idx_r = idx+k+1
            # left overhang
            if idx_l < 0:
                len_overhang = abs(idx_l)
                overhang = "N" * len_overhang
                motif = overhang + ref[:idx_r]
            # right overhang
            elif idx_r > n_ref:
                len_overhang = idx_r - n_ref
                overhang = "N" * len_overhang
                motif = ref[idx_l:] + overhang
            # no overhang
            else:
                motif = ref[idx_l:idx_r]

            return motif.replace("T", "U")
        return ""
        
    def get_mismatch_perc(self, count_dict_rel: Dict[str, float], ref_base: str) -> float:
        """
        Calculates the number of reads containing a mismatch, insertion or deletion 
        at a given position.

        Parameters:
        - count_dict_rel (Dict[str, float]): Dictionary containing the relative number of occurences 
                                             of A,C,G,U,ins,del for a given position
        - ref_base (str): Reference base at the given position

        Returns:
        - float: Mismatch rate at the given position
        """
        mismatch_perc_sum = 0
        for b in ["a", "c", "g", "u"]:
            if b != ref_base.lower():
                mismatch_perc_sum += count_dict_rel[b]

        return mismatch_perc_sum

    def get_read_quality(self, read_qualities: str, ref_skip_positions: List[int]) -> Tuple[float, float]:
        """
        Calculates the mean and std from the read qualities given in the sixth row
        of a pileup file.

        Parameters:
        - read_qualities (str): Read quality string from pileup file

        Returns:
        - float: Mean quality score
        - float: Standard deviation of the quality scores 
        """
        # remove quality values corresponding to reference skips
        read_qualities_len = len(read_qualities)
        read_qualities_list = list(read_qualities)
        ref_skip_positions.reverse()
        
        for i in ref_skip_positions:
            if i < read_qualities_len: # when >/< comes at the end, the quality values don't seem to be added to the string
                read_qualities_list.pop(i)
        read_qualities = "".join(read_qualities_list)

        if len(read_qualities) > 0:
            # transform string to list of corresponding phred numeric values
            vals = [code - 33 for code in read_qualities.encode("ascii")]
            
            mean = np.mean(vals).astype(float)
            std = np.std(vals).astype(float)
        else:
            mean = -1
            std = -1

        return mean, std 
    
    #################################################################################################################
    #                                   Methods called during neighbour search                                      #
    #################################################################################################################
    def process_small(self, current_pos: int, neighbourhood: List[str]) -> str:
        """
        Process a small neighbourhood in case the full window size is smaller than the number of lines.

        Parameters:
        - current_pos (int): The current position within the neighbourhood.
        - neighbourhood (List[str]): A list of lines representing the neighbourhood.
        - n_lines (int): The total number of lines in the input.

        Returns:
        - str: The processed line as a string.
        """        
        ref_str = neighbourhood[current_pos].strip("\n")
        nb = neighbourhood.copy()
        ref = nb[current_pos].strip("\n").split("\t")
        del(nb[current_pos])

        nb_info = self.get_neighbour_info(ref, nb)
        ref_str += f"\t{nb_info}\n"
        return ref_str

    def process_edge(self, current_pos: int, neighbourhood: List[str], start: bool = True) -> str:
        """
        Process a neighbourhood at the beginning or the end of the input.

        Parameters:
        - current_pos (int): The current position within the neighbourhood.
        - neighbourhood (List[str]): A list of lines representing the neighbourhood.
        - start (bool, optional): A boolean indicating if it's the start or end of the neighbourhood. Defaults to True.

        Returns:
        - str: The processed line as a string.
        """
        k = self.window_size
        ref_str = neighbourhood[current_pos].strip("\n")
        nb = neighbourhood.copy()
        ref = nb[current_pos].strip("\n").split("\t")

        if start:
            nb = nb[:current_pos+k+1]
            del(nb[current_pos])
        else:       
            del(nb[current_pos])
            nb = nb[current_pos-k:]

        nb_info = self.get_neighbour_info(ref, nb)
        ref_str += f"\t{nb_info}\n"
        return ref_str

    def process_neighbourhood(self, neighbourhood: List[str]) -> str:
        """
        Get 2*window_size+1 rows ([row i-k, ..., row i, ..., row i+k]) that are next to each other in the tsv file and compare the row i to all 
        remaining ones. Check if the other rows are on the same chromosome and if the relative distance between them is smaller or equal to k.
        Create a summary string that indicates the error position relative to the center position.
        Add new information to the row and return.

        Parameters:
        - neighbourhood (List[str]): List of k number of rows extracted from a tsv file.

        Returns:
        - str: New line containing the neighbourhood information for a given center position.
        """        
        k = self.window_size

        ref_str = neighbourhood[k].strip("\n")
        nb = neighbourhood.copy()

        ref = nb[k].strip("\n").split("\t")
        del nb[k]

        nb_info = self.get_neighbour_info(ref, nb)
        ref_str += f"\t{nb_info}\n"
        return ref_str

    def get_neighbour_info(self, ref: List[str], neighbourhood: List[str]) -> str:
        """
        From a range of neighbouring lines in a file (neighbourhood), check if positions in these lines are neighbours on the reference genome 
        (based on chromosome and site) and if close genomic positions can be regarded as errors based on the given error threshold.

        Parameters:
        - ref (List[str]): Line of the central position for which neighbours are searched.
        - neighbourhood (List[str]): List containing the lines surrounding the central position.

        Returns:
        - str: A string giving the relative distance to all neighbouring errors to the central position, if any were found.
        """        
        k = self.window_size
        ref_chr = ref[0]
        ref_site = int(ref[1])

        nb_info = ""

        # for each neighbour check if they are 1.on the same chr and 2.neighbours
        for pos in neighbourhood:
            pos = pos.strip("\n").split("\t")
            chr = pos[0]
            perc_error = float(pos[19])

            if (chr == ref_chr) & (perc_error >= self.neighbour_error_threshold): # check if same chromosome & if pos is error
                site = int(pos[1])
                relative_pos = site - ref_site

                if (abs(relative_pos) <= k): # check if pos are close to each other
                    nb_info += str(relative_pos)+","
        return nb_info
    

if __name__=="__main__":
    f = FeatureExtractor(in_paths="/home/vincent/projects/neet_project/data/45s_rrna/pileups/drna_nuc.pileup",
                         out_dir="/home/vincent/projects/neet_project/data/45s_rrna/test/test.tsv",
                         ref_path="/home/vincent/projects/neet_project/data/45s_rrna/RNA45SN1.fasta",
                         num_processes=24)
    f.main()
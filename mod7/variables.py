N_IO_WORKERS = 69

N_SERP_RESULTS = 33

SEARCH_TERMS_CSV_PATH = 'top_1000_search_terms.csv'
SERP_RESULTS_CSV_PATH = 'serp_results.csv'
METRICS_CSV_PATH = 'pagespeed_results.csv'


def set_search_terms_csv_path(path):
    global SEARCH_TERMS_CSV_PATH, SERP_RESULTS_CSV_PATH, METRICS_CSV_PATH
    SEARCH_TERMS_CSV_PATH = path
    SERP_RESULTS_CSV_PATH = SEARCH_TERMS_CSV_PATH[:-4] + '_serp_results.csv'
    METRICS_CSV_PATH = SEARCH_TERMS_CSV_PATH[:-4] + '_metrics.csv'

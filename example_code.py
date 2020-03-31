
from concurrent.futures import as_completed, ThreadPoolExecutor
import csv
import json

from serpapi.google_search_results import GoogleSearchResults


N_THREADS = 100 # no. of concurrent serpapi requests

with open("/Users/sandylee/.secret/serpapi.json") as f: #TODO: load secrets with dotenv
	GoogleSearchResults.SERP_API_KEY = json.load(f)['api_key']
	
pool = ThreadPoolExecutor(max_workers=N_THREADS)

def _top_100(keyword):
	out = []
	query_parameters = {"q": keyword,
						"hl": "en",
						"gl": "us",
						"google_domain": "google.com",
						"num": 100,
						}
    response = GoogleSearchResults(query_parameters).get_dict()
	
	for result in response["organic_results"]:
		out.append((result["position"], result["link"]))
	# ~ out = [(1, 'http://blah.com'), (2, 'http://MEH.com'),(3, 'http://bleh.com'), ]
	# ~ import time; time.sleep(.2)
	return out


def main():
	
	with open("top_1000_search_terms.csv") as f:
		reader = csv.reader(f)
		next(reader) # skip header
		keywords = [kwd for (kwd,) in reader]
	
	future_to_kwd = {pool.submit(_top_100, kwd): kwd 
						for kwd in keywords}
						
	with open('herp_derp_results.csv', 'w') as f:
		csvwriter = csv.writer(f)
		csvwriter.writerow(["keyword", "position", "result"])
		
		i = 0
		for future in as_completed(future_to_kwd):
			kwd = future_to_kwd[future]
			try:
				data = future.result()
				csvwriter.writerows([(kwd, pos, lnk) 
										for (pos, lnk) in data])
				i += 1
				print(f"\rcompleted {i/len(future_to_kwd):.0%}", end='')
			except Exception as exc:
				print(f'exception: {exc}')
		print('\ndone')

if __name__ == '__main__':
	main()

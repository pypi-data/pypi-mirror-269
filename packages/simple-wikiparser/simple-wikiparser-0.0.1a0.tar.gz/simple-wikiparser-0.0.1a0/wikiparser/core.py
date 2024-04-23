import mwparserfromhell, json, os, bz2
import lxml.etree as etree
from tqdm.notebook import tqdm
import requests
from datasets import Dataset


class WikiMediaDumpParser(object):
    def __init__(self, language, out_dir="./", dump_format="jsonl", stream_rate=200) -> None:
        """WikiMediaDumpParser: Module to parse wikipedia dump
        
        Args:
            language (str): wikipedia Language e.g. say English, or Odia, Telugu
            out_dir (str, optional): dumps data or dataset to this directory. Defaults to "./".
            dump_format (str, optional): intial parsed dump format . Defaults to "jsonl".
            stream_rate (int, optional): streaming rate in Kilobyte per chunk . Defaults to 200.
        """
        self.language_code, self.language_locale = self.get_language_code(language)
        self.out_dir = out_dir
        self.latest_dump_url = f'https://dumps.wikimedia.org/{self.language_code}wiki/latest/{self.language_code}wiki-latest-pages-articles.xml.bz2'
        self.dump_file_path = os.path.join(out_dir, f'{self.language_code}wiki-latest-pages-articles.xml.bz2')
        self.stream_rate = stream_rate
        
    def clean_text(self, wikicode):
        """
        Clean and extract plain text from MediaWiki markup using mwparserfromhell.
        """
        parsed_wikicode = mwparserfromhell.parse(wikicode)
        return parsed_wikicode.strip_code().strip()

    def download_wikipedia_dump_with_progress(self, url, output_path):
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        chunk_size = 1024*self.stream_rate  # 5 Kilobyte block
        total_chunks = total_size_in_bytes / chunk_size

        print(f"Starting download... Total size: {total_size_in_bytes / 1024 / 1024:.2f} MB")
        print(f"dumping data to {output_path}")

        chunks_downloaded = 0
        with open(output_path, 'wb') as file:
            for data in response.iter_content(chunk_size):
                file.write(data)
                chunks_downloaded += 1
                percent_completed = (chunks_downloaded / total_chunks) * 100
                print(f"Downloaded {percent_completed:.2f}%", end='\r', flush=True)

        print("\nDownload completed successfully.")

    def parse(self, file_path=None):
        """
        Process the Wikipedia dump, extracting title, URL, and cleaned text.
        """

        if not file_path or os.path.exists(file_path):
            if not os.path.exists(self.dump_file_path):
                self.download_wikipedia_dump_with_progress(self.latest_dump_url, self.dump_file_path)
        
        file_path = self.dump_file_path
        outfile = os.path.basename(file_path).replace(".xml.bz2", "")+".jsonl"

        with bz2.open(file_path, "r") as f, open(outfile, "a") as fo:
            context = etree.iterparse(f, events=('end',), tag='{http://www.mediawiki.org/xml/export-0.10/}page')
            for event, elem in tqdm(context):
                ns = elem.find('{http://www.mediawiki.org/xml/export-0.10/}title').text
                text_elem = elem.find('.//{http://www.mediawiki.org/xml/export-0.10/}text')
                if text_elem is not None:
                    text = self.clean_text(text_elem.text)
                    url = f"https://{self.language_code}.wikipedia.org/wiki/{ns.replace(' ', '_')}"
                    fo.write(json.dumps({"title":ns, "url":url, "text":text}, ensure_ascii=False)+"\n")

                # It's important to clear the elements to save memory
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
    
    def export_hf_dataset(self, input_file, dataset_name, ignore_subpage_tag=True):
        with open(input_file) as fp:
            data = [json.loads(d) for d in fp.readlines()]
        
        if ignore_subpage_tag:
            data = [d for d in data if not ":" in d["title"] ]
        
        dataset_hf = Dataset.from_list(data)
        dataset_hf.save_to_disk(os.path.join(self.out_dir, dataset_name))
        
    def get_language_code(self, language):
        self.wiki_language_map = {
            "English" :{"code":"en", "locale":"English"},
            "Hindi" :{"code":"hi", "locale":"हिन्दी"},
            "Telugu" :{"code":"te", "locale":"తెలుగు"},
            "Tamil" : {"code":"ta", "locale":"தமிழ்"},
            "Kannada" : {"code":"kn", "locale":"ಕನ್ನಡ"},
            "Gujarati" : {"code":"gu", "locale":"ગુજરાતી"},
            "Marathi" : {"code":"mr", "locale":"मराठी"},
            "Malayalam" : {"code":"ml", "locale":"മലയാളം"},
            "Bangla":{"code":"bn", "locale":"বাংলা"},
            "Bengali":{"code":"bn", "locale":"বাংলা"},
            "Odia" :{"code":"or", "locale":"ଓଡ଼ିଆ"}
        }
        return self.wiki_language_map.get(language)["code"], self.wiki_language_map.get(language)["locale"]

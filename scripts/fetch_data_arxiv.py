import arxiv
import json
import requests
import fitz
import PyPDF2
import os
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from tqdm import tqdm
from datetime import datetime

from text_utils import (
    get_top_ngrams,
    get_top_words,
    readability_score,
    title_features,
    clean_text,
    lemmatize
)

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')


def get_data(categories, max_res, filename="data/arxiv_data.json", verbose=True, save_body = True):
    save_json = True
    if not os.path.exists('temp'):
        os.makedirs('temp')

    results = []

    for cat in categories:
        if verbose:
            print(f"Gathering {cat} articles...")

        search = arxiv.Search(
            query=f"cat:{cat}",
            max_results=max_res,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        for result in tqdm(search.results(), total=max_res, disable=not verbose, ncols=80):
            temp_pdf = f"temp/{result.get_short_id()}.pdf"
            try:
                download_pdf(result.pdf_url, temp_pdf)
                num_figs = count_figures(temp_pdf)
                num_refs = count_references(temp_pdf)
                full_text = extract_body_text(temp_pdf)
                num_words = word_count_text(full_text)
            except Exception as e:
                print(f'PDF parsing failed for {result.get_short_id()}: {e}')
                num_figs, num_refs, num_words, full_text = None, None, None, ""

            # Text util features
            title_text = result.title.strip()
            abstract_text = result.summary.strip().replace("\n", " ")

            text_features = {
                'title_top_ngrams': get_top_ngrams(title_text),
                'abstract_readability': readability_score(abstract_text),
                'abstract_top_words': get_top_words(abstract_text),
                'body_top_words': get_top_words(full_text),
                'body_top_ngrams': get_top_ngrams(full_text),
                'body_lemmatized': lemmatize(clean_text(full_text)),
                'full_body': full_text if save_body else ""
            }

            results.append({
                "id": result.get_short_id(),
                "title": title_text,
                "abstract": abstract_text,
                "authors": ", ".join([a.name for a in result.authors]),
                'num_authors': len(result.authors),
                "published_date": result.published.date().isoformat(),
                'days_since_pub': (datetime.today().date() - result.published.date()).days,
                "updated_date": result.updated.date().isoformat(),
                'days_since_update': (datetime.today().date() - result.updated.date()).days,
                "comment": result.comment if result.comment else "",
                "primary_category": result.primary_category,
                "categories": ", ".join(result.categories),
                "pdf_url": result.pdf_url,
                'figures': num_figs,
                'references': num_refs,
                'word_count': num_words,
                'pdf_accessible': True if num_figs is not None else False,
                **text_features
            })

            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)

    if save_json:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

    return pd.DataFrame(results)


def download_pdf(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        f.write(r.content)


def count_figures(pdf_path):
    doc = fitz.open(pdf_path)
    return sum(len(page.get_images(full=True)) for page in doc)


def extract_body_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    found_references = False

    for page in doc:
        t = page.get_text()
        if found_references:
            break
        if "references" in t.lower() or "bibliography" in t.lower():
            split_idx = t.lower().find("references")
            if split_idx == -1:
                split_idx = t.lower().find("bibliography")
            t = t[:split_idx]
            found_references = True
        text += t + "\n"

    return text


def count_references(pdf_path, pages_to_scan=2):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        last_pages = reader.pages[-pages_to_scan:] if len(reader.pages) > pages_to_scan else reader.pages
        ref_text = "".join(page.extract_text() for page in last_pages)
    lines = ref_text.split("\n")
    ref_lines = [line for line in lines if any(k in line.lower() for k in ['doi', 'arxiv', 'vol', '[', 'et al', 'http'])]
    return len(ref_lines)


def word_count_text(text):
    tokens = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    stop_words = set(stopwords.words('english'))
    return len([t for t in tokens if t not in stop_words])


test = get_data(['math.NA'], 20, save_body = False)
# ML-Driven Bibliometric Forecasting of Academic Papers on arXiv

## Overview

This project aimed to predict the long-term citation impact of academic papers using lightweight NLP and metadata-based features extracted from titles, abstracts, and structured metadata sources. The dataset was constructed by integrating papers from arXiv and enriching them with citation, reference, and topical metadata from the Semantic Scholar (S2) API.

The project emphasized efficient, interpretable, and reproducible feature engineering without relying on full-body PDF parsing.

## Data Sources
- **arXiv API**: To retrieve basic paper metadata (title, abstract, categories, authorship, publication dates).
- **Semantic Scholar API**: To supplement citation counts, reference counts, figure counts (if available), and fields of study.

## Features Extracted

The following features were engineered:

- **Metadata features**:
  - Days since publication and last update
  - Number of authors
  - Primary and full arXiv categories
  - Citation and reference counts
- **Title-level features**:
  - Word count
  - Word diversity
  - Average word length
  - Average sentence length
  - Sentiment class (e.g., optimistic, cautious)
- **Abstract-level features**:
  - Word count
  - Word diversity
  - Average word length
  - Average sentence length
  - Readability score (Flesch-Kincaid)
  - Sentiment class (e.g., positive, neutral, assertive)

All feature engineering functions were modularized through a `text_utils.py` script.

## Current Status

- A modular pipeline for downloading and preprocessing arXiv metadata was completed.
- A multithreaded fetch script for downloading and enriching papers was written and tested.
- PDF parsing was removed to improve speed and robustness; citation and reference metadata are sourced entirely from S2.
- Lightweight NLP features (word diversity, sentence length, readability, sentiment) were implemented and tested on sample datasets.

## Remaining Tasks

- Finalize the batch enrichment process using the Semantic Scholar API with the obtained API key.
- Test a small pilot batch (~100–200 papers) to validate metadata joins and feature extraction.
- Collect and preprocess the full dataset (~25,000 papers).
- Engineer supervised labels for citation impact (e.g., highly cited vs not) based on empirical citation distributions.
- Apply clustering methods on engineered features to explore writing style groupings.
- Build and evaluate supervised models (classification and regression) in R.
- Finalize a full report describing methodology, results, and key findings.

## Technologies Used
- **Python**: Data scraping, preprocessing, NLP feature engineering.
- **R**: Planned for model building, cross-validation, and evaluation.
- **Google Colab**: Used for faster parallel data collection.

## License
This project is licensed under the MIT License.

---

> Author: Prajwal Bhandari
> Project Start Date: April 2025
> Status: Active (Paused during final exam period)


# topic_modelling.py

import os
import re
import matplotlib.pyplot as plt
from collections import Counter
from bertopic import BERTopic
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer
from src.helpers.path_helpers import *

# ---------- Helpers ----------

def _clean_caption(t: str) -> str:
    """Light cleaning for social captions."""
    if not isinstance(t, str):
        return ""
    t = t.lower()
    t = re.sub(r"#\w+", " ", t)      # remove hashtags
    t = re.sub(r"@\w+", " ", t)      # remove mentions
    t = re.sub(r"http\S+", " ", t)   # remove URLs
    t = re.sub(r"[^\w\s]", " ", t)   # punctuation/emoji remnants
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _build_stopwords():
    """EN/DE/FR/RU stopwords + IG fluff."""
    sw = set(get_stop_words("en") + get_stop_words("de") +
             get_stop_words("fr") + get_stop_words("ru"))
    sw |= {
        "and","to","in","you","with","for","your","the","a","of","on","amp",
        "follow","dm","linkinbio","like","share","subscribe","im","ive","we","us"
    }
    return sw


def _make_vectorizer(stopwords, n_docs: int) -> CountVectorizer:
    """Adaptive thresholds so min_df/max_df never clash."""
    if n_docs <= 20:
        min_df, max_df = 1, 1.0
    elif n_docs <= 100:
        min_df, max_df = 2, 0.95
    else:
        min_df, max_df = 3, 0.90

    return CountVectorizer(
        stop_words=list(stopwords),
        ngram_range=(1, 2),
        min_df=min_df,
        max_df=max_df,
        lowercase=True,
        token_pattern=r"(?u)\b\w\w+\b"
    )

# ---------- Main API ----------

def get_topics(
    caption_list,
    topic_count: int,
    output_filename,
    output_path="data\\visualizations\\topics",
    min_topic_size: int = 5
):
    """
    Train BERTopic on captions, print Top-N topics, and save a PNG bar chart.

    Args:
        caption_list (list[str]): Raw captions.
        topic_count (int): Number of most-frequent topics to show.
        output_path (str): Where to save the PNG.
        min_topic_size (int): Minimum cluster size for BERTopic.

    Returns:
        list[int]: Top-N topic IDs (excluding outlier -1). Empty if none.
    """

    output_path = join_paths(output_path, output_filename)

    # 0) Clean + sanity
    captions_clean = [_clean_caption(c) for c in caption_list]
    captions_clean = [c for c in captions_clean if c]
    n_docs = len(captions_clean)
    if n_docs == 0:
        print("⚠ No captions after cleaning. Nothing to model.")
        return []

    # 1) Stopwords + vectorizer
    stopwords = _build_stopwords()
    vectorizer_model = _make_vectorizer(stopwords, n_docs)

    # 2) Fit BERTopic with our vectorizer (and a small min_topic_size for short texts)
    topic_model = BERTopic(
        language="multilingual",
        vectorizer_model=vectorizer_model,
        min_topic_size=min_topic_size
    )

    # Try fitting; if df thresholds still clash for some reason, relax and retry once
    try:
        topics, probs = topic_model.fit_transform(captions_clean)
    except ValueError as e:
        if "max_df corresponds to < documents than min_df" in str(e):
            vectorizer_model = CountVectorizer(
                stop_words=list(stopwords),
                ngram_range=(1, 2),
                min_df=1,
                max_df=1.0,
                lowercase=True,
                token_pattern=r"(?u)\b\w\w+\b"
            )
            topic_model = BERTopic(
                language="multilingual",
                vectorizer_model=vectorizer_model,
                min_topic_size=min_topic_size
            )
            topics, probs = topic_model.fit_transform(captions_clean)
        else:
            raise

    # 3) Count topics and remove outliers
    topic_counts = Counter(topics)
    outliers = topic_counts.get(-1, 0)
    topic_counts.pop(-1, None)

    if not topic_counts:
        print(f"⚠ All {n_docs} documents assigned to outlier (-1). "
              f"Try min_df=1, looser cleaning, or a larger dataset.")
        return []

    # 4) Select Top-N topic IDs
    top_ids = [t for t, _ in topic_counts.most_common(topic_count)]

    # 5) Prepare labels + frequencies; print detailed topic words
    labels, freqs = [], []
    for tid in top_ids:
        words = [w for w, _ in topic_model.get_topic(tid)]
        label = ", ".join(words[:3]) if words else f"Topic {tid}"
        labels.append(label)
        freqs.append(topic_counts[tid])
        print(f"Topic {tid}: {topic_model.get_topic(tid)}")

    # 6) Plot and save PNG
    plt.figure(figsize=(12, 7))
    plt.barh(range(len(freqs)), freqs)
    plt.yticks(range(len(freqs)), labels)
    plt.xlabel("Number of Captions")
    plt.title(f"Top Topics in Captions  (docs={n_docs}, outliers={outliers})")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✔ Plot saved to {output_path}")

    return top_ids
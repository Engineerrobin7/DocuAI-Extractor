import re
import spacy
from transformers import pipeline

# Load models (they will be downloaded on first use)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If not found, download it or handle appropriately
    # Note: In a production script, you'd run python -m spacy download en_core_web_sm
    # Here, we'll assume it's available or handle errors in main.py
    nlp = None

# Pipelines for Summarization and Sentiment
# Using specific models mentioned in spec
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    print(f"Warning: Could not load summarization pipeline. Error: {e}")
    # Fallback to text2text-generation if summarization is not found
    try:
        summarizer = pipeline("text2text-generation", model="facebook/bart-large-cnn")
    except Exception as e2:
        print(f"Error: Could not load fallback pipeline either. Error: {e2}")
        summarizer = None

sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def extract_entities(text: str):
    """Extract entities (names/orgs/locs/dates) using spaCy."""
    if not nlp:
        return []
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        })
    return entities

def extract_money(text: str):
    """Extract money amounts using regex (₹/$ and amounts)."""
    # Regex for currency symbols followed by numbers with optional decimals/commas
    money_pattern = r'([\$₹]\s?\d+(?:,\d{3})*(?:\.\d{2})?)'
    return re.findall(money_pattern, text)

def get_summary(text: str):
    """Generate summary using BART."""
    if not text or len(text.strip()) < 50:
        return text
    
    if summarizer is None:
        return text[:200] + "..."  # Basic fallback summary
    
    # BART has a max input length, truncate text if needed
    input_text = text[:1024] 
    try:
        summary = summarizer(input_text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return text[:200] + "..."

def get_sentiment(text: str):
    """Get sentiment using DistilBERT."""
    if not text:
        return "NEUTRAL"
    
    # Truncate text for sentiment analysis if needed
    input_text = text[:512]
    result = sentiment_analyzer(input_text)[0]
    return result['label']

def analyze_document(text: str):
    """Run all AI analysis on the extracted text."""
    if not text.strip():
        return {
            "summary": "No text extracted for summarization.",
            "entities": [],
            "money": [],
            "sentiment": "NEUTRAL"
        }
    
    return {
        "summary": get_summary(text),
        "entities": extract_entities(text),
        "money": extract_money(text),
        "sentiment": get_sentiment(text)
    }

from transformers import pipeline
sentiment_fn = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def score_comment(txt):
    # truncate long blobs
    res = sentiment_fn(txt[:512])[0]

    return 1 if res["label"] == "POSITIVE" else -1, res["score"]

def thread_summary(comments):
    scores = [score_comment(c.body)[0] for c in comments]
    mean = sum(scores)/len(scores) if scores else 0
    return {
        "n_comments": len(scores),
        "net_score": sum(scores),
        "avg_polarity": mean,
    }
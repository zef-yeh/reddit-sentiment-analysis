import sys
from reddit_client import fetch_threads
from sentiment import thread_summary
from db import RedditThread, save_thread
from pathlib import Path

output_dir = Path("results")
output_dir.mkdir(exist_ok=True)

def review_product(product: str, limit: int = 30):
    print(f"\n🔍  Searching Reddit for: “{product}”")
    threads = list(fetch_threads(product, limit=limit))
    print(f"   → {len(threads)} threads returned\n")

    for t in threads:
        # show first 80 chars of title
        print(f"• {t.title[:80]}") 
        t.comments.replace_more(limit=0)
        comments = t.comments.list()
        print(f"  ↳ pulled {len(comments)} comments")

        summ = thread_summary(comments)
        rec = RedditThread(
            id=t.id,
            product=product,
            title=t.title,
            url=t.url,
            n_comments=summ["n_comments"],
            net_score=summ["net_score"],
            avg_polarity=summ["avg_polarity"],
        )
        save_thread(rec)

    print("\nAll done! Results saved to reviews.db")

    import sqlite3
    import pandas as pd
    from pathlib import Path

    db_path = output_dir / "reviews.db"
    csv_path = output_dir / f"{product.replace(' ', '_')}_summary.csv"

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(
            "SELECT title, url, n_comments, net_score, avg_polarity FROM redditthread WHERE product = ?",
            conn,
            params=(product,)
        )
        df.to_csv(csv_path, index=False)
        print(f"Summary exported to: {csv_path.absolute()}")

def plot_comparison_chart(csv_file="combined_product_reviews.csv"):
    import pandas as pd
    import matplotlib.pyplot as plt


    df = pd.read_csv(output_dir / csv_file)

    grouped = df.groupby("product")["avg_polarity"].mean().sort_values(ascending=False)

    plt.figure(figsize=(10, 5))
    grouped.plot(kind="bar", color="skyblue")
    plt.title("Average Sentiment per Product")
    plt.ylabel("Avg Sentiment (Polarity)")
    plt.ylim(-1, 1)
    plt.axhline(0, color="gray", linestyle="--")
    plt.tight_layout()
    plt.xticks(rotation=15)
    plt.savefig(output_dir / "product_sentiment_comparison.png")
    plt.show()

if __name__ == "__main__":
    import pandas as pd

    if len(sys.argv) < 2:
        print("Usage: python app.py \"Product A\" \"Product B\" ...")
        sys.exit(1)

    all_products = sys.argv[1:]
    all_data = []

    for product in all_products:
        review_product(product)
        
        # load individual product CSV
        csv_file = f"{product.replace(' ', '_')}_summary.csv"
        df = pd.read_csv(output_dir / csv_file)
        df["product"] = product
        all_data.append(df)

    # combine into one dataframe
    merged_df = pd.concat(all_data, ignore_index=True)

    # save combined CSV
    merged_df.to_csv(output_dir / "combined_product_reviews.csv", index=False)
    print("\n📄 Combined summary saved to: combined_product_reviews.csv")
    
    # print results
    print("\n Average Sentiment Per Product:")
    avg_sentiments = merged_df.groupby("product")["avg_polarity"].mean().sort_values(ascending=False)

    for product, avg in avg_sentiments.items():
        print(f"• {product}: {avg:.3f}")

    #show graph
    plot_comparison_chart()

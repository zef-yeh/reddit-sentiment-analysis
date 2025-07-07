from sqlmodel import SQLModel, Field, create_engine, Session
from pathlib import Path

output_dir = Path("results")
output_dir.mkdir(exist_ok=True)
db_path = output_dir / "reviews.db"

engine = create_engine(f"sqlite:///{db_path}")

class RedditThread(SQLModel, table=True):
    id: str = Field(primary_key=True)
    product: str
    title: str
    url: str
    n_comments: int
    net_score: int
    avg_polarity: float

SQLModel.metadata.create_all(engine)

def save_thread(s: RedditThread):
    with Session(engine) as sess:
        sess.merge(s) 
        sess.commit()

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def ensure_schema():
    """Ensure required columns exist (status, category)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='ads' AND column_name='status'
                    ) THEN
                        ALTER TABLE ads ADD COLUMN status VARCHAR(20);
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='ads' AND column_name='category'
                    ) THEN
                        ALTER TABLE ads ADD COLUMN category VARCHAR(50);
                    END IF;
                END$$;
            """)
            conn.commit()
    print("[DB] Ensured table 'ads' has columns: status, category")


def get_ad(ad_id):
    """Fetch ad record by ID."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ads WHERE id = %s", (ad_id,))
            row = cur.fetchone()
            return row


def update_ad_status(ad_id, approved, category):
    """Update ad approval status and category."""
    ensure_schema()
    status = "approved" if approved else "rejected"
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE ads SET status = %s, category = %s WHERE id = %s",
                (status, category, ad_id),
            )
            conn.commit()
    print(f"[DB] Updated ad {ad_id} → status={status}, category={category}")

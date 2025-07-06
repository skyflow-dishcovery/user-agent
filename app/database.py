from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql://postgres.otrdzattaqgegoicjckj:skyflow_dishcovery@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"  # From Supabase

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
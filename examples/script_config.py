import json
import os

from dotenv import load_dotenv
from os import path

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

base_url = os.getenv("BASE_URL", None)
api_token = os.getenv("API_TOKEN", None)
user_id = os.getenv("USER_ID", None)

def get_factor_id_by_type(factors, factor_type, provider="OKTA"):
    for factor in factors:
        if factor.factorType == factor_type and factor.provider == provider:
            return (factor.id, factor.profile)
    
    return None

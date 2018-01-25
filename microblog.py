from app import app, db
from app.models import Client, Product, Request

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Client': Client, 'Product': Product, 'Request': Request}
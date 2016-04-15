import os
from app import create_app

app = create_app()


with open('%s/static/generate/111.csv' % app.root_path,mode='w') as f:
    print 'yes'

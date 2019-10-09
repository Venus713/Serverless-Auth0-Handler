# Serverless-Auth0-Handler

## Install dependences
### Node dependencies for Serverless
"""
$ npm install
"""
### Python dependences
"""
$ pip install -r requirements.txt
"""

## How to deploy the solution
### Test on local
"""
$ sls invoke local --function auth0_handler
"""
### Deploy to aws
"""
$ sls deploy
"""
*** NOTE ***
"""
Make sure to make env.yml in the root directory before deploying to aws and set your environment variables according as env.example 
"""

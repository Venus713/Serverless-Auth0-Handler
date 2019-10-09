# Trial of serverless to handle s3

## Install dependences
### Node dependencies for sls
```
$ npm install
```
### Python dependences
```
$ pip install -r requirements.txt
```

## How to deploy the solution
### Test on local
```
$ sls invoke local --function demo
```
### Deploy to aws
```
$ serverless deploy
```
*** NOTE ***
```
Don't forget to make env.yml in the root directory according as env.example before deploying to aws
```# Serverless-Auth0-Handler

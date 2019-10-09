# Serverless-Auth0-Handler

## Install required dependences
```
$ npm install
$ pip install -r requirements.txt
```

## How to deploy the solution
### Prerequests!
Please make sure that you created `env.yml` in the root directory by using `env.example` template.
Here is the `env.yml` example as well.
```
dev:
    AUTH0_CLIENT_ID: RPpx1yeS....QCZVMY9VaRKvxNXQ
    AUTH0_DOMAIN: dev-your-id.eu.auth0.com
    AUTH0_CLIENT_SECRET: eawhdA4u0X...Xws1VtwBALJ
    AUTH0_CALLBACK_URL: https://<your-api-gateway-domain-or-custom-domain>/dev/callback/
    TABLE_NAME: auth0-users

```

If you integrated a specific custom domain with the api gateway, then you can use it in the place of **AUTH0_CALLBACK_URL**. In order to get the first api gateway's endpoint, you will need to try deploy even though it doesn't work at the first time.

### Deploy
```
$ sls deploy
```

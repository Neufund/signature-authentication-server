# signature-authentication-server

[![Build Status](https://travis-ci.org/Neufund/signature-authentication-server.svg)](https://travis-ci.org/Neufund/signature-authentication-server)  [![codecov](https://codecov.io/gh/Neufund/signature-authentication-server/branch/master/graph/badge.svg)](https://codecov.io/gh/Neufund/signature-authentication-server) [![](https://images.microbadger.com/badges/image/neufund/signature-authentication-server.svg)](https://microbadger.com/images/neufund/signature-authentication-server)  [![](https://images.microbadger.com/badges/version/neufund/signature-authentication-server.svg)](https://microbadger.com/images/neufund/signature-authentication-server)

Authentication server using Ethereum signatures, captcha and issuing JWT

## Getting started

Get the source code:
```
git clone https://github.com/Neufund/signature-authentication-server.git
cd signature-authentication-server

Build the container:
```
docker build . -t signature-authentication-server
```

Generate a keypair:
```
openssl ecparam -genkey -name secp521r1 -noout -out ec512.prv.pem
openssl ec -in ec512.prv.pem -pubout > ec512.pub.pem
```

Start the container:
```
docker run -ti -v (pwd)/ec512.prv.pem:/srv/ec512.prv.pem:ro -p 5000:5000 signature-authentication-server
```

## Using

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/api/signup -d '{"signature":"asd"}'
```

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/api/login -d '{"signature":"asd", "address":"foo"}'
```

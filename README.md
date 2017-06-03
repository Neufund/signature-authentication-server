# signature-authentication-server

[![Build Status](https://travis-ci.org/Neufund/signature-authentication-server.svg)](https://travis-ci.org/Neufund/signature-authentication-server)  [![codecov](https://codecov.io/gh/Neufund/signature-authentication-server/branch/master/graph/badge.svg)](https://codecov.io/gh/Neufund/signature-authentication-server) [![](https://images.microbadger.com/badges/image/neufund/signature-authentication-server.svg)](https://microbadger.com/images/neufund/signature-authentication-server)  [![](https://images.microbadger.com/badges/version/neufund/signature-authentication-server.svg)](https://microbadger.com/images/neufund/signature-authentication-server)

Authentication server using Ethereum signatures, captcha and issuing JWT

## Getting started

Get the source code:
```
git clone https://github.com/Neufund/signature-authentication-server.git
cd signature-authentication-server
```

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
docker run -ti -v (pwd)/ec512.prv.pem:/srv/ec512.prv.pem:ro -v (pwd)/ec512.pub.pem:/srv/ec512.pub.pem:ro -p 5000:5000 signature-authentication-server
```

## Using

In the following example session I assume you have an [Ethereum JSON-RPC](https://github.com/ethereum/wiki/wiki/JSON-RPC) running on port 8545. This can be [`testrpc`](https://github.com/ethereumjs/testrpc).


Get the address:
```
curl -X POST -H 'Content-Type: application/json' http://localhost:8545/ -d '{"jsonrpc":"2.0","method":"eth_accounts","params":[],"id":1}'
```
```
{"id":1,"jsonrpc":"2.0","result":["0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1","0xffcf8fdee72ac11b5c542428b35eef5769c409f0","0x22d491bde2303f2f43325b2108d26f1eaba1e32b","0xe11ba2b4d45eaed5996cd0823791e0c93114882d","0xd03ea8624c8c5987235048901fb614fdca89b117","0x95ced938f7991cd0dfcb48f0a06a40fa1af46ebc","0x3e5e9111ae8eb78fe1cc3bb8915d5d461f3ef9a9","0x28a8746e75304c0780e011bed21c72cd78cd535e","0xaca94ef8bd5ffee41947b4585a84bda5a3d3da6e","0x1df62f291b2e969fb0849d99d9ce41e2f137006e"]}
```


Generate a challenge:
```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/api/challenge -d '{"address":"0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1"}'
```
```
{
  "challenge": "90f8bf6a479f320ead074411a4b0e7944ea8c9c15932c5d68a1b539da0b0f8431d8e50e1a5b2b3bd4cfdcfc387a5ff85d7ef5fac429c4e0e4c1bfc36d4a99770b58f42924e126ece"
}
```

When using testrpc, be mindful of the following: https://github.com/ethereumjs/testrpc/issues/243


Sign the challenge:
```
curl -X POST -H 'Content-Type: application/json' http://localhost:8545/ -d '{"jsonrpc":"2.0","method":"eth_sign","params":["0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1", "0x90f8bf6a479f320ead074411a4b0e7944ea8c9c15932c5d68a1b539da0b0f8431d8e50e1a5b2b3bd4cfdcfc387a5ff85d7ef5fac429c4e0e4c1bfc36d4a99770b58f42924e126ece"],"id":1}'
```
```
{"id":1,"jsonrpc":"2.0","result":"0xfc0fddb82084f9ea7d2acdf62eebbc64c07c3c6102a279cc51e23a6df738086f615edf2b1880f0fcc9cf5e1ed95287e9b0493043dfdb504fac8d6735ecf3551100"}
```


Authenticate:
```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/api/login -d '{"address":"0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1", "challenge": "90f8bf6a479f320ead074411a4b0e7944ea8c9c15932c5d68a1b539da0b0f8431d8e50e1a5b2b3bd4cfdcfc387a5ff85d7ef5fac429c4e0e4c1bfc36d4a99770b58f42924e126ece", "response":"fc0fddb82084f9ea7d2acdf62eebbc64c07c3c6102a279cc51e23a6df738086f615edf2b1880f0fcc9cf5e1ed95287e9b0493043dfdb504fac8d6735ecf3551100"}'
```
```
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJzdWIiOiIweDkwZjhiZjZhNDc5ZjMyMGVhZDA3NDQxMWE0YjBlNzk0NGVhOGM5YzEiLCJleHAiOjE0OTY1MDUwNzQsIm5iZiI6MTQ5NjUwMzI3NCwiaXNzIjoiTmV1ZnVuZCIsImF1ZCI6IndlYjMiLCJpYXQiOjE0OTY1MDMyNzR9.AaOPxTqBV4iy6GVlAu8XfbmOsIoezKfYjkqZ0SZ_RW6E7qwW-tUwSq8fq-avJrLtmCzLOD2xO9T5esEiIykP3Z9SAKWrTkdo9RwGcqGfvAySurbVAiFgW4MZ9pf9cHcB6zRks53pPcq6X2yqaVzjw28N6kBRQRc23GrUFnEDK6P_t3Tv"
}
```


Renew authentication token:
```
curl -X POST -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJzdWIiOiIweDkwZjhiZjZhNDc5ZjMyMGVhZDA3NDQxMWE0YjBlNzk0NGVhOGM5YzEiLCJleHAiOjE0OTY1MDUwNzQsIm5iZiI6MTQ5NjUwMzI3NCwiaXNzIjoiTmV1ZnVuZCIsImF1ZCI6IndlYjMiLCJpYXQiOjE0OTY1MDMyNzR9.AaOPxTqBV4iy6GVlAu8XfbmOsIoezKfYjkqZ0SZ_RW6E7qwW-tUwSq8fq-avJrLtmCzLOD2xO9T5esEiIykP3Z9SAKWrTkdo9RwGcqGfvAySurbVAiFgW4MZ9pf9cHcB6zRks53pPcq6X2yqaVzjw28N6kBRQRc23GrUFnEDK6P_t3Tv' http://localhost:5000/api/renew
```
```
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJzdWIiOiIweDkwZjhiZjZhNDc5ZjMyMGVhZDA3NDQxMWE0YjBlNzk0NGVhOGM5YzEiLCJleHAiOjE0OTY1MDUwOTgsIm5iZiI6MTQ5NjUwMzI5OCwiaXNzIjoiTmV1ZnVuZCIsImF1ZCI6IndlYjMiLCJpYXQiOjE0OTY1MDMyOTh9.AAULrZlACQW1OkhTzU0DIFWTUwQ2L6hp6RwUzvawpGmPlwW9I52JZHqyaXBFc4hxjToMwzpwImfdlwr3Ur7VrFiqAWperFaIAdim5JhCmlRoja-bqG8aKbRFK2mF9YtVTp8xyiHTIf9pMwZtL0JRYhs_GBi9sQcF88JMcxxRdot5Hlus"
}
```

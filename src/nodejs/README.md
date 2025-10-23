# Node.js JWT demo

- [Node.js JWT demo](#nodejs-jwt-demo)
  - [Setup](#setup)
  - [Run (Development)](#run-development)
  - [Build and Run (Production)](#build-and-run-production)
  - [API Usage](#api-usage)

## Setup

```sh
cp .env.example .env
npm i
```

then add the JWT secret key in `.env`.

## Run (Development)

```sh
npm run dev
```

## Build and Run (Production)

```sh
npm run build
npm start
```

## API Usage

- POST `/sign`: Signs the payload in request body. Returns the signed JWT.
- POST `/verify`: Verifies the JWT contained in request body payload, in form of JSON `{ "token": "XXX" }`. Returns the claims and status (verified/invalid). If invalid, also returns the details.
- POST `/change-key`: Changes the secret key in-memory. No input, no output. Restarting the server also reuses the original key (in `.env`).

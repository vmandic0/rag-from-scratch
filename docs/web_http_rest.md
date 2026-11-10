# HTTP and REST APIs

## HTTP methods

GET reads a resource and must not change data. POST creates a new resource. PUT replaces a resource completely. PATCH changes part of a resource. DELETE removes a resource.

## Status codes

200 means OK. 201 means that a resource was created. 204 means success with no content. 400 means a bad request from the client. 401 means the user is not authenticated. 403 means the user is authenticated but not allowed. 404 means the resource was not found. 500 means an error on the server.

## REST principles

REST is an architectural style where every resource has its own URL, for example /api/transactions/5. The server is stateless: every request carries all information needed to process it, so the server does not remember previous requests. Data are usually exchanged as JSON.

## Ports and HTTPS

HTTP uses port 80 by default and HTTPS uses port 443. HTTPS encrypts traffic with TLS. During development, web servers often run on ports such as 3000, 5173 or 8000.

## Authentication

A token, for example a JWT, is sent in the Authorization header with the prefix Bearer. The server checks the token on every request. Passwords must never be stored in plain text; they are hashed, for example with bcrypt.

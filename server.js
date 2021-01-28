const express = require('express');
const app = express();

app.enable('trust proxy');

app.use((request, response, next) => {
    if (request.protocol !== 'https') {
        const secureUrl = `https://${request.headers.host + request.url}`;
        response.writeHead(301, { Location: secureUrl });
        response.end();
    }
    next();
})

app.use(express.static(`${__dirname}/dist/`))
app.get(/.*/, (request, response) => {
    response.sendFile(`${__dirname}/dist/index.html`)
})
app.listen(process.env.PORT || 443);
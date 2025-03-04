import express from 'express'
import fs from 'fs'

const app = express();
app.use(express.static('static'));
const port = 8020;

const index = fs.readFileSync("./html/index.html").toString();
const CLIENT_NONCE = process.env.CLIENT_NONCE || "aRandomString";

app.get('/', function(req, res){
	const partnerName = req.query.partnerName || "Kim Minji";
	const score = Math.floor(Math.random() * 100);
	res.setHeader("Content-Type", "text/html; charset=utf-8");
	res.send(index.replace(/{{nonce}}/g, CLIENT_NONCE).replace(/{{partnerName}}/g, partnerName).replace(/{{score}}/g, score));
});

app.listen(port, async () => {
    console.log(`[*] Webapp Listening on port ${port}`)
});
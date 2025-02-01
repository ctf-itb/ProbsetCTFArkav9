const express = require('express');
const ejs = require('ejs');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const SECRETKEY = process.env.SECRETKEY

app.set('view engine', 'ejs');
app.set('views','views');

app.use(express.static('public'));
app.use('/img', express.static(__dirname + '/Images'));

app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res) => {
    const token = req.cookies['token'];
    if (token) {
        res.render("home", { loggedIn: true });
    }
    else {
        res.render("home", { loggedIn: false });
    }
});

app.get("/login", (req, res) => {
    const token = req.cookies['token'];
    if (token) {
        res.render("login", { loggedIn: true });
    }
    else {
        res.render("login", { loggedIn: false });
    }
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const token = jwt.sign({ username: username, role: "USER" }, SECRETKEY, { expiresIn: '1h', algorithm: 'HS256' });
    res.cookie('token', token);
    res.redirect('/');
});

app.get("/flag", (req, res) => {
    const token = req.cookies['token'];

    if (token) {
        jwt.verify(token, SECRETKEY, (err, decoded) => {
            if (err) {
                res.render("noFlag", { loggedIn: true });
            }
            
            if (decoded.role === "ADMIN") {
                res.render("flag", {
                    flag: process.env.FLAG || "ARKAV{this_is_a_fake_flag}"
                });
            }
            else {
                res.render("noFlag", { loggedIn: true });
            }
        });
    }
    else {
        res.render("noFlag", { loggedIn: false });
    }
});

app.get('/logout', (req, res) => {
    res.clearCookie('token');
    res.redirect('/');
});

app.listen(process.env.PORT || 3000, () => {
    console.log("Server is running on port 3000");
});

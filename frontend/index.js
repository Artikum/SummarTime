const express = require('express');
const path = require('path');

const app = express();

app.use(express.static(__dirname));

app.get('/', (req, res) => {
	res.sendFile(path.resolve('index.html'));
})

app.listen(3000, () => console.log('sever listens 3000 port'));
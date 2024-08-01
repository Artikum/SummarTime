const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const app = express();

const pool = new Pool({ user: 'artikum', host: 'postgres', port: 5432, database: 'summarization_db', password: '12345qwerty' });

app.use(cors());

const getPgData = async(query, params = []) => {
	try {
		const pgData = await pool.query(query, params);
		return {
			status: 200,
			body: pgData.rows
		};
	} catch (e) {
		return {
			status: 400,
			body: e
		};
	}
}

const validateRequestParams = (expected, actual) => {
	let result = true;

	expected.forEach(parameter => {
		if(!actual.includes(parameter)) {
			result = false;
		}
	});

	actual.forEach(parameter => {
		if(!expected.includes(parameter)) {
			result = false;
		}
	});

	return result;
}



app.get('/users', async (req, res) => {
	const query = 'select u.id, u.username, u.password, u.create_date, r.role_type from users u join roles r on u.role_id = r.id';
	const pgData = await getPgData(query);
	
	return res.status(pgData.status).json(pgData.body);
});

app.get('/users/:id', async(req, res) => {
	const pgData = await getPgData('select * from users where id = $1', [req.params.id]);
	return res.status(pgData.status).json(pgData.body);
})

app.get('/logs/:id', async(req, res) => {
	const pgData = await getPgData('select * from logs where id = $1', [req.params.id]);
	return res.status(pgData.status).json(pgData.body);
})

app.get('/roles/:id', async(req, res) => {
	const pgData = await getPgData('select * from roles where id = $1', [req.params.id]);
	return res.status(pgData.status).json(pgData.body);
})

app.get('/logs', async (req, res) => {
	const query = 'select * from logs'
	const pgData = await getPgData(query);

	return res.status(pgData.status).json(pgData.body);
});

app.get('/roles', async (req, res) => {
	const query = 'select * from roles';
	const pgData = await getPgData(query);

	return res.status(pgData.status).json(pgData.body);
});

app.delete('/users/:id', async (req, res) => {
	const pgData = await getPgData('delete from users where id = $1', [req.params.id]);
	return res.status(pgData.status).send(pgData.body);
});

app.delete('/roles/:id', async (req, res) => {
	const pgData = await getPgData('delete from roles where id = $1', [req.params.id]);
	return res.status(pgData.status).send(pgData.body);
});

app.delete('/logs/:id', async(req, res) => {
	const pgData = await getPgData('delete from logs where id = $1', [req.params.id]);
	return res.status(pgData.status).send(pgData.body);
});

app.put('/users/:id', async(req, res) => {
	const requestParams = Object.keys(req.query);
	if(!validateRequestParams(['username', 'password', 'role_id'], requestParams)) {
		return res.status(400).send('Invalid parameters');
	}

	const query = 'update users set username=$2, password=$3, role_id=$4 where id=$1';
	const pgData = await getPgData(query, [
		req.params.id,
		req.query.username,
		req.query.password,
		req.query.role_id
	]);

	return res.status(pgData.status).send(pgData.body);
});

app.put('/roles/:id', async(req, res) => {
	const requestParams = Object.keys(req.query);
	if(!validateRequestParams(['role_type'], requestParams)) {
		return res.status(400).send('Invalid parameters');
	}

	const query = 'update roles set role_type = $2 where id = $1';
	const pgData = await getPgData(query, [
		req.params.id,
		req.query.role_type
	]);

	return res.status(pgData.status).send(pgData.body);
});

// app.put('/logs/:id', async(req, res) => {
// 	const requestParams = Object.keys(req.query);
// 	if(!validateRequestParams(['number'], requestParams)) {
// 		return res.status(400).send('Invalid parameters');
// 	}

// 	const query = 'update groups set number=$2 where id=$1';
// 	const pgData = await getPgData(query, [
// 		req.params.group_id,
// 		req.query.number,
// 	]);

// 	return res.status(pgData.status).send(pgData.body);
// });

app.post('/users', async(req, res) => {
	const requestParams = Object.keys(req.query);
	if(!validateRequestParams(['username', 'password', 'role_id'], requestParams)) {
		return res.status(400).send('Invalid parameters');
	}

	const query = 'insert into users(username, password, role_id) values($1, $2, $3)';
	const pgData = await getPgData(query, [
		req.query.username,
		req.query.password,
		req.query.role_id
	]);

    
	return res.status(pgData.status).send(pgData.body);
});

app.post('/roles', async(req, res) => {
	const requestParams = Object.keys(req.query);
	if(!validateRequestParams(['role_type'], requestParams)) {
		return res.status(400).send('Invalid parameters');
	}

	const pgData = await getPgData('insert into roles(role_type) values($1)', [req.query.role_type]);
	return res.status(pgData.status).send(pgData.body);
});

app.post('/logs', async(req, res) => {
	const requestParams = Object.keys(req.query);
	if(!validateRequestParams(['user_id','request_date', 'request', 'prohibition_flag', 'request_data'], requestParams)) {
		return res.status(400).send('Invalid parameters');
	}

	const query = 'insert into logs(user_id, request_date, request, prohibition_flag, request_data) values($1, $2, $3, $4, $5)';
	const pgData = await getPgData(query, [
		req.query.user_id,
		req.query.request_date,
		req.query.request,
		req.query.prohibition_flag,
		req.query.request_data
	]);
    
	return res.status(pgData.status).send(pgData.body);
});


app.listen(3000, () => console.log('server listens 3000 port'));
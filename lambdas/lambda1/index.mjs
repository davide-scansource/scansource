import https from 'https';

const getData = async () => {
  return new Promise((resolve, reject) => {
    https.get('https://restcountries.com/v3.1/capital/ottawa', (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        resolve(data);
      });
    }).on('error', (err) => {
      reject(err);
    });
  });
};

export const handler = async (event) => {
  try {
    console.log('Lambda1 called. Version 1.0.0');
    const response = await getData();
    return {
      headers: { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      statusCode: 200,
      body: response,
    };
  } catch (error) {
    // Log error for later debugging
    console.log(error)
    return {
      headers: { 'Content-Type': 'application/json' },
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal Server Error' }),
    };
  }
};


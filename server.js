const https = require('https');
const { exec } = require('child_process');
const fs = require('fs');


const port = 443;

const PASSWORD = "opensesame" 
#const PASSWORD = fs.readFileSync('pw.txt')


const cert = {
  key: fs.readFileSync('./cert/privkey1.pem'),
  cert: fs.readFileSync('./cert/cert1.pem'),
  ca: fs.readFileSync('./cert/chain1.pem')
};

const server = https.createServer(cert, (req, res) => {
  var param = new URL(req.url, `https://${req.headers.host}`).searchParams;
  
  if(check(param.get('key'))){
    
    command(param.get('q'));
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('success');
  }else{

      res.statusCode = 404;
      res.setHeader('Content-Type', 'text/plain');
      res.end("failed");
  }
  
});

server.listen(port, () => {
  console.log(`Server running`);
});


function check(key){
  if(key == PASSWORD){
    return true;
  }
  console.log("Password is incorrect!");
  return false;
}

function command(param){
  console.log(`Run!! (${param})`);
  exec('python run.py '+param, (error, stdout, stderr) => {
    if (error) {
      console.error(`run.py execution error: ${error}`);
      return;
    }
    console.log(`run.py output: ${stdout}`);
    console.error(`run.py error: ${stderr}`);
  });
}
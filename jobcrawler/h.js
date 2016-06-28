var casper = require('casper').create({
viewportSize: { width: 1024,height: 768},
verbose: true,
//logLevel: "debug",
pageSettings: {
    loadImages: false,
    loadPlugins: false 
  }
});
casper.onError = function(msg){
	this.echo("onError:"+msg);
}
phantom.outputEncoding="gb2312";
var fs = require("fs");

var sep="#$$#"; //separator
var nl="#NL#"//newline
//var url="http://search.51job.com/list/030200%252C00,%2B,2707,%2B,4,%2B,%2B,0,%2B.html?lang=c&stype=2&postchannel=0000&funtype_big=2707&postfrom=030200&btnSltPosition=...&image_x=36&image_y=15&specialarea=00";
var url="http://search.51job.com/list/030200,000000,0107,00,4,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=";
var curPage=1;
var jobUrls = [];
var nextListUrl;
var infos=[];

casper.start();

casper.thenOpen(url, function() {
	this.echo(this.getTitle());
	//this.captureSelector('index.png', 'html');
	//this.click('a'); 
});

function getJobUrl(){
	var as=document.querySelectorAll('#resultList div p a');
	var l=[];
	for(var i=0;i<as.length;i++){
		l.push(as[i].href);
		//if (i>=1)
		//	return l;
	}
	return l;
}


var main=function(){

casper.start();
casper.userAgent("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36");
this.echo('gogo');
//nextListUrl
try{
	casper.waitForSelector('li.bk', function() {
		//this.captureSelector('p'+cnt.toString()+ '.png', 'html');
		nextListUrl=this.evaluate(function(){	
			return document.querySelector('li.bk:last-child a').href;
		});
		this.echo('nextListUrl----'+nextListUrl); 
	});
}
catch (err){
	this.echo("err no li.bk");
}
	
//jobUrls	
try{
	casper.waitForSelector('#resultList div', function() {
		jobUrls=this.evaluate(getJobUrl);
		this.echo(jobUrls.length + ' ' +jobUrls[jobUrls.length-1]); 
	});
}
catch (err){
	this.echo("....err no home");
}

//itor job

casper.then(function(){
	casper.each(jobUrls, function(self, url) {
		self.thenOpen(url, function() {
			this.echo(this.getTitle());
			casper.wait(300);
			var msg={};
			msg=this.evaluate(function(){
				 var des=document.querySelector('div.bmsg.job_msg.inbox').innerText;
				 var name=document.querySelector('.cn h1').title;
				 var sal=document.querySelector('.cn strong').innerText;
				 var co=document.querySelector('.msg.ltype').innerText;
				 return {des:des,name:name,sal:sal,co:co};
			});
			infos.push({des:msg.des,name:msg.name,sal:msg.sal,co:msg.co});
		});
	});
	jobUrls.length=0;
});


casper.then(function(){
	this.echo(nextListUrl);
	casper.open(nextListUrl, function() {
		this.echo('thenopen');
		this.echo(this.getTitle());
	});	
});
};

function saveInfos(){
	casper.echo('save');
	var txt='';
	try{
	for(var i=0;i<infos.length;i++){
		//casper.echo(i);
		txt+=infos[i].name+ sep+infos[i].sal+ sep+infos[i].des+ sep+infos[i].co+nl;
	}
	fs.write("devJobs0.txt", txt, 'a');
	infos.length=0;
	}
	catch(err){
		casper.echo(err);
	}
}



var cnt=0;
var pro = function() {
	cnt++;
	this.echo(cnt);
	saveInfos();
	if (cnt<=100){	
		main.call(this);
		casper.run(pro);
	}
	else{
		this.echo("end");
		this.exit();
	}
	
}

casper.run(pro);
	


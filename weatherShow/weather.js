var casper = require('casper').create({
viewportSize: { width: 1800,height: 900},
verbose: true,
//logLevel: "debug",
pageSettings: {
    loadPlugins: false
  }
});

var url="http://www.weather.com.cn/weather1d/101280401.shtml";
var imgPath="/home/pi/weatherShow/img/";

casper.start();
casper.options.onResourceRequested=function(self,dt,nw){
	isWhite=dt.url.match(/weather.com/g) || dt.url.match(/tq121.com/g);
	if(!isWhite)
		nw.abort();
	//else
	//	casper.echo(dt.url);
};
casper.zoom(3).thenOpen(url, function() {
	this.echo(this.getTitle());
});
try{
	casper.waitForSelector('div.today .time', function() {
		this.captureSelector(imgPath+'p1.png', '#today .t');
	});
}
catch (err){
	this.echo("err no today");
}

casper.then(function(){
	var alarm=this.evaluate(function() {
		var al=document.querySelector('.today .sk_alarm a');
		if (al){ 
			var t=al.title;
			t=t.split('fabu');		
			if (t.length==2):
				t=t[1];
			return t;
		}
	});
	if (alarm)
		this.echo('alarm:'+alarm);
});

try{
casper.waitForSelector('.greatEvent ul li', function() {
	this.evaluate(function() {
		var l=document.querySelectorAll('.greatEvent ul li');
		for (var i=2;i<l.length;i++)
			l[i].parentNode.removeChild(l[i]);
		for (var i=0;i<2;i++){
			h=l[i].querySelector('h2');
			h.style.fontSize='23px';
			p=l[i].querySelector('a div p');
			p.style.fontSize='16px';
		}
	});
	});
}
catch (err){
	this.echo("err no greatEvent");
}
casper.then(function() {
	this.captureSelector(imgPath+'p2.png', '.greatEvent');
});

var url2="http://www.weather.com.cn/weather/101280401.shtml";
casper.zoom(3).thenOpen(url2, function() {
	this.echo(this.getTitle());
});
try{
	casper.waitForSelector('div[id="7d"] > ul li', function() {
		this.evaluate(function() {
			var l=document.querySelectorAll('div[id="7d"] > ul li');
			for (var i=3;i<l.length;i++)
				l[i].parentNode.removeChild(l[i]);
			var u=document.querySelector('div[id="7d"] > ul');
			u.style.width='291px';
		});
		this.captureSelector(imgPath+'p3.png', 'div[id="7d"] > ul');
	});
}
catch (err){
	this.echo("err no 7d");
}

casper.then(function(){
	this.exit();
});


casper.run();
	


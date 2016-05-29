var casper = require('casper').create({
viewportSize: { width: 1224,height: 768},
verbose: true,
//logLevel: "debug",
pageSettings: {
    loadImages: false,
    loadPlugins: false,
  }
});
phantom.outputEncoding="gb2312";

var imgPath='/home/pi/weatherShow/img/';


casper.start();
casper.options.onResourceRequested=function(self,dt,nw){
	isWhite=dt.url.match(/baidu.com/g) ;
	if(!isWhite)
		nw.abort();
	else
		casper.echo(dt.url);
};
casper.userAgent("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36");

/*
var url="http://news.baidu.com/n?cmd=6&loc=0&name=%B1%B1%BE%A9";

casper.zoom(2.2).thenOpen(url, function() {
	this.echo(this.getTitle());
});
casper.waitForSelector('#change_city', function() {
	this.click("#change_city");
	this.wait(1000);
	this.click("a[prop='广东||0']");
	this.wait(1000);
	//this.captureSelector('p.png', '.city_list');
	//this.echo(this.getHTML('.city_list'));
	this.click("a[prop='梅州|5570|0']");
	this.wait(1000);
});

casper.then(function() {
	this.waitForText("梅州新闻",function(){
		this.echo('梅州新闻Found');
	});
});


casper.then(function(){
	this.evaluate(function() {
			var p=document.querySelector('#identifier-pannel');
			p.style.display='none';
			document.querySelector('#ft').style.display='none';
			var l=document.querySelector('#con');
			l.style.width="600px";
			var ln=l.querySelector('#local_news');
			ln.style.paddingTop="8px";
			ln.style.paddingLeft="36px";
			document.body.style.backgroundColor='#eeeeee';
			var t=l.querySelectorAll('table');
						
			for (var i=3;i<t.length;i++){
				t[i].parentNode.removeChild(t[i]);
			}
			for (var i=0;i<3;i++){
				t[i].width="96%";
			}
			var b=l.querySelectorAll('br');
			for (var i=11;i<b.length;i++){
				b[i].parentNode.removeChild(b[i]);
			}
	});
});

try{
	casper.waitForSelector('#con', function() {
		this.captureSelector(imgPath+'news0.png', '#con');
	});
}
catch (err){
	this.echo("err no local_news");
}

*/
var us=new Array()
us['国内新闻']="http://news.baidu.com/n?cmd=1&class=civilnews&pn=1&tn=newsbrofcu";
us['财经新闻']="http://news.baidu.com/n?cmd=1&class=finannews&pn=1&tn=newsbrofcu";
us['互联网新闻']="http://news.baidu.com/n?cmd=1&class=internet&pn=1&tn=newsbrofcu";
us['房产新闻']="http://news.baidu.com/n?cmd=1&class=housenews&pn=1&tn=newsbrofcu";
us['科技新闻']="http://news.baidu.com/n?cmd=1&class=technnews&pn=1&tn=newsbrofcu";

var j=1;
for (var u in us){
 	//casper.echo(j+u+','+us[u]);
	getNews(us[u],j);
	j++;
}



function getNews(url,id){
	casper.zoom(2).thenOpen(url, function() {
		//this.echo(this.getTitle());
		this.wait(1000);
	});
	casper.waitForSelector('div.baidu', function() {
		var l=this.evaluate(function() {
			document.body.style.backgroundColor='#eeeeee';
			document.querySelector('.blk').style.fontSize="36px";
			var cn=document.body.childNodes;
			cn[0].remove();
			cn[cn.length-1].remove();
			var d=document.querySelector('div.baidu');
			d.style.lineHeight='46px';
			d.style.fontSize="23px";
			var m=d.querySelector('div a.more');
			m.parentNode.removeChild(m);
			var a=d.querySelectorAll('a');
			for(var i=0;i<a.length-4;i++){
				a[i].style.textDecoration='none';
			}
			for(var i=6;i<a.length;i++){
				a[i].remove();
			}
			var s=d.querySelectorAll('span');
			for(var i=0;i<s.length;i++){
				s[i].remove();
			}
			var b=d.querySelectorAll('br');
			for(var i=6;i<b.length;i++){
				b[i].remove();
			}
			var b=document.querySelector('body');
			b.style.paddingTop="20px";
			b.style.paddingLeft="32px";
		});
		this.captureSelector(imgPath+'news'+ id.toString() +'.png', 'body');
	});
}


casper.then(function(){
	this.exit();
});

casper.run();
	


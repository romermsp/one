var casper = require('casper').create({
viewportSize: { width: 1224,height: 768},
verbose: true,
//logLevel: "debug",
pageSettings: {
    //loadImages: false,   
    loadPlugins: false,
  }
});
phantom.outputEncoding="gb2312";

var imgPath='/home/pi/weatherShow/img/';

casper.start();

casper.userAgent("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36");

var url="http://stockpage.10jqka.com.cn/HQ.html#16_1A0001";

casper.zoom(2).thenOpen(url, function() {
	this.echo(this.getTitle());
});

casper.waitForSelector('li[period="daily"] a', function() {
	this.wait(3000);
	this.click('li[period="daily"] a');
});

casper.waitForSelector('#kTech', function() {
	this.wait(500);
	this.evaluate(function() {
		document.querySelector('.canvas-btn-box').remove();
	});
	this.wait(500);
	this.mouseEvent("mousemove","#canvasPanel","90%","20%");
});
casper.then(function(){
	this.wait(500);
	this.captureSelector(imgPath+'st.png', '#canvasPanel');
});

casper.then(function(){
	this.exit();
});
casper.run();

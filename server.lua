html = [[
<html><head>
<title>pulse</title>
<meta http-equiv="Content-Type" content="text/html charset=utf-8"/>
<style type="text/css">p{font-size:10px;line-height:2px;}#r{font-size:40px}</style>
</head>
<body>
<div id="d"></div>
<div id="r"></div>
<div id="m"></div>
<script>
var a       = new Array();
var d       = document.getElementById('d');
var r       = document.getElementById('r');
var xmlhttp = new XMLHttpRequest();
function req(){ 
    
    xmlhttp.open("GET","/p",false);
    xmlhttp.send(null);
    var ret     = xmlhttp.responseText.split('\r\n');
    var rate    = ret[0];
    for(var i=0;i<ret[1].length/2;i+=2)
        a.push(ret[1].substr(i,2));
    r.innerHTML = rate;
    document.getElementById('m').innerHTML=a.length;
    disp();
}
function gent(n)
{
var t="";    
for(var i=0;i<n;i++){t+="-";}
return t;
}

function disp(){
    i++;
    
    var v       = a.shift();
    if(v!=undefined){
        var p       = document.createElement("p");
        p.innerText = gent(v)+v;
        d.appendChild(p);
        var e = d.getElementsByTagName('p')[0];
        e.parentElement.removeChild(e);
        setTimeout("disp()",80);
    }
    else{
        req();
    }
}

for(var i=0;i<40;i++){
    var p       = document.createElement("p");
    p.innerText = "|";
    d.appendChild(p);
} 

var i = 0;
try{
setTimeout("disp()",3000);
}
catch(err){
document.getElementById('m').innerHTML = err.message;
}
</script>
</body></html>
]]


function pro(pl)
  local p    = string.match(pl,"GET /(.*) HTTP")
  local data = ""
  if (p=="") then
      data = html
  elseif (p=="p") then
      data =  getData()
    end
  return data
end

dofile("pulse.lua")

if (srv~=nil) then 
    srv:close()
end
srv = net.createServer(net.TCP)
srv:listen(80, function(c)
  c:on("receive", function(c, pl)
    local d = pro(pl)
    c:send(d)
  end)
  c:on("sent",function(conn) conn:close() end)
end)

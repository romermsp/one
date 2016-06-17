html = [[
<html><head>
<title>pulse</title>
<meta http-equiv="Content-Type" content="text/html charset=utf-8"/>
<script>
function req(c){ 
var xmlhttp = new XMLHttpRequest();
var url     = '/p';
xmlhttp.open("GET",url,false);
xmlhttp.send(null);
var msg='wait';
var ret=xmlhttp.responseText.replace(/\n/gi,'');
//if (ret!='ok')
    //msg='ok';
    document.getElementById('msg').innerHTML=ret;
}
</script></head>
<body>
<div id='msg'></div>
<div><input id='l' type=button value='L' onclick='req("r")'></div>
</body></html>
]]

sv:close()
sv   = net.createServer(net.TCP,5)
sv:listen(80, function(c)
  c:on("receive", function(c, pl)
    local d = pro(pl)
    c:send(d)
  end)
  c:on("sent",function(conn) conn:close() end)
end)

function pro(pl)
  local p    = string.match(pl,"GET /(.*) HTTP")
  local data = ""
  if (p=="") then
      data = html
  elseif (p=="p") then
      data = "okkkkkk"  
    end
  return data
end



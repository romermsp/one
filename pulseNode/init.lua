wifi.setmode(wifi.STATION)
wifi.sta.config("ssid","password")

function p()
    print('ip'..wifi.sta.getip())
end
tmr.alarm(0,3000,tmr.ALARM_AUTO ,function () 
    if (pcall(p)==false) then 
        print("fail")
    else
        tmr.stop(0)
        pcall(function() dofile("pulseServer.lua") end)
    end
end)


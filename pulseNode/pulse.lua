function init()
    zeroCount       = 0
    checkCount      = 0
    state           = 0
    step            = 0
    peak            = 0
    peakTime        = 0
    lastPeak        = 0
    lastPeakTime    = 0
    rate            = 60
    userRate        = 0
    userPulse       = ""
    notTouchCount = 0 
    n               = 0
end
function getStart() 
    if (sv <10) then
        zeroCount = zeroCount+1;
    else 
        if (zeroCount > 20) then
            state = 1;
        else 
            zeroCount = 0;
        end
    end
end
function getPeak(checkTimes)
    if (sv > peak) then
        peak       = sv;
        peakTime   = tmr.now();
        checkCount = 0;
    else 
        checkCount = checkCount +1;
        if (checkCount > checkTimes) then
            checkCount = 0;
            return true;
        end
    end
    return false;
end
function preGetPeak()
    if(getPeak(20)) then
        lastPeak     = peak
        lastPeakTime = peakTime
        state        = 2
    end
end
function getFirstBeat()
    if(getPeak(5)) then
        if (peak>lastPeak*0.8) then
            lastPeakTime = peakTime
            lastPeak     = peak
            state        = 3
        end
    end      
end
function getNextBeat()
    n = n+1
    if(getPeak(5)) then
        if (peak>lastPeak*0.8 and peakTime - lastPeakTime>300000) then
            local r = math.floor(60000000 / (peakTime - lastPeakTime))
            if (rate<r) then
                rate = rate+1
            elseif(rate>r) then
                rate = rate-1
            end
            lastPeakTime = peakTime
            lastPeak     = peak
            peak         = 0
            print("rate......"..rate)
            if (n>60) then
                userRate = rate
                n        = 0
            end
        end
        
    end
end

function isNotTouch()
    if (sv>900) then
        notTouchCount = notTouchCount+1
        if (notTouchCount > 8) then
            return true
        end
    else 
        notTouchCount = 0
        return false
    end
end

function savePulse(sv)
    local vv = math.floor((sv-350)/13)
    if(vv<0) then vv=0 end
    local p   = string.sub("00"..vv,-2)
    userPulse = userPulse..p
    --print(string.rep("-",vv)..sv)    
end

function getData()
    local d   = userRate.."\r\n"..userPulse
    userPulse = ""
    return d
end

init()  --初始化
tmr.alarm(0,50,tmr.ALARM_AUTO ,function () --定时器50毫秒循环
    sv = adc.read(0)  --读取传感器信号
    if(state~=0) then
        savePulse(sv)  --存下信号值
    end
    if(state==0) then 
        getStart()      --检查手指是否放上
    elseif (state==1) then
        preGetPeak()    --预先取得信号峰值，为下一峰值的有效性作参照
    elseif (state==2) then
        getFirstBeat()  --取得第一个心跳
    elseif(state==3) then
        getNextBeat()   --下一个心跳
    end
    if (state~=0 and isNotTouch()) then --检查手指是否离开
        print('init')
        init()
    end
end)
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
    checkTouchCount = 0 
    n               = 0
end

function getStartTime() 
    if (sv <10) then
        zeroCount = zeroCount+1;
    else 
        if (zeroCount > 20) then
            startTime = tmr.now();
            state     = 1;
            print(startTime);
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
function getLastBeat()
    if (step==0) then
        if(getPeak(20)) then
            lastPeak     = peak
            lastPeakTime = peakTime
            step         = 1
            print("peak"..lastPeak.."Time"..(lastPeakTime-startTime))
        end
    elseif(step==1) then
        if(getPeak(5)) then
            if (peak>lastPeak*0.8) then
                lastPeakTime = peakTime
                lastPeak     = peak
                state        = 2
                step         = 0
            end
        end     
    end  
end
function getNextBeat()
    n = n+1
    if(getPeak(5)) then
        if (peak>lastPeak*0.8 and peakTime - lastPeakTime>300000) then
            r            = math.floor(60000000 / (peakTime - lastPeakTime))
            if (rate<r) then
                rate = rate+1
            elseif(rate>r) then
                rate = rate-1
            end
            lastPeakTime = peakTime
            lastPeak     = peak
            peak         = 0
            print("rate......"..rate)
            if (n>30) then
                userRate = rate
                --print("userRate: "..userRate)
                n        = 0
            end
        end
        
    end
end

function isNotTouch(sv)
    if (sv>900) then
        checkTouchCount = checkTouchCount+1
        if (checkTouchCount > 8) then
            return true
        end
    else 
        checkTouchCount = 0
        return false
    end
end

init()
while true do
    sv = adc.read(0)
    if (sv == nil) then  
        sv = 0
    end
    if(state<4) then
        print(string.rep("-",sv/20)..sv)
    end
    if(state==0) then 
        getStartTime()
    elseif (state==1) then
        getLastBeat()
    elseif(state==2) then
        getNextBeat()
    end
    
    if (state~=0 and isNotTouch(sv)) then
        print('init')
        init()
    end
    tmr.delay(50000)
end

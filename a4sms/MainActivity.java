package com.example.romer.a4;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.NotificationCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;

import static android.app.Notification.FLAG_ONGOING_EVENT;

public class MainActivity extends AppCompatActivity {

    //NotificationCompat.Builder notifyBuilder ;
    //NotificationManager mNotificationManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //notifyBuilder = new NotificationCompat.Builder(this);
        //mNotificationManager = (NotificationManager) this.getSystemService(NOTIFICATION_SERVICE);
        //doNotify();
    }
    /*
    @Override
    protected void onStop() {
        super.onStop();
        Log.e("dsd", "onStop called.");
    }
    @Override
    protected void onDestroy() {
        Log.e("lk", "onDestory called.");
        mNotificationManager.cancel(3878);
        super.onDestroy();
    }

    protected void doNotify(){
        notifyBuilder.setContentTitle("MT");
        notifyBuilder.setContentText("......");
        notifyBuilder.setSmallIcon(R.drawable.common_full_open_on_phone);
        //notifyBuilder.setOngoing(true);
        mNotificationManager.notify(3878, notifyBuilder.build());
        //mNotificationManager.cancel(3878);
    }
    */

}

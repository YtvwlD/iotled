package de.ytvwld.iotled;

import android.app.Activity;
import android.os.Bundle;
import android.widget.ListView;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;

import retrofit2.Retrofit;
import retrofit2.Callback;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.converter.gson.GsonConverterFactory;
import java.util.List;

public class main extends Activity
{
    API api;
    ListView deviceList;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        deviceList = (ListView)findViewById(R.id.deviceList);

        Retrofit retrofit = new Retrofit.Builder()
          .baseUrl("https://iotled.ytvwld.de/api/app/")
          .addConverterFactory(GsonConverterFactory.create())
          .build();
        api = retrofit.create(API.class);
        getDevices();
      }

    private void getDevices()
    {
        Call<List<String>> call = api.listDevices();
        call.enqueue(new Callback<List<String>>()
        {
          @Override
          public void onResponse(Call<List<String>> call, Response<List<String>> resp)
          {
            List<String> devices = resp.body();
            for(String device: devices)
            {
              System.out.println(device);
            }
            ListAdapter adapter = new ArrayAdapter<String>(getApplicationContext(), android.R.layout.simple_list_item_1, devices);
            deviceList.setAdapter(adapter);
          }

          @Override
          public void onFailure(Call<List<String>> call, Throwable t) {} //TODO
        });
    }
}

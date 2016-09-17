package de.ytvwld.iotled;

import android.app.Activity;
import android.os.Bundle;

import retrofit2.Retrofit;
import retrofit2.Callback;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.converter.gson.GsonConverterFactory;
import java.util.List;

public class main extends Activity
{
    API api;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

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
            for(String device: resp.body())
            {
              System.out.println(device);
            }
          }

          @Override
          public void onFailure(Call<List<String>> call, Throwable t) {} //TODO
        });
    }
}

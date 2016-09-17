package de.ytvwld.iotled;

import retrofit2.http.GET;
import retrofit2.Call;
import java.util.List;

public interface API
{
	@GET("list")
	Call<List<String>> listDevices();
}

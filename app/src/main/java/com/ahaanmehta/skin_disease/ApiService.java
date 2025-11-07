package com.ahaanmehta.skin_disease;

import okhttp3.MultipartBody;
import retrofit2.Call;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface ApiService {
    @Multipart
    @POST("api/v1/predictions/")
    Call<PredictionResponse> uploadImage(@Part MultipartBody.Part image);
}

package com.ahaanmehta.skin_disease;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitClient {
    private static final String TAG = "RetrofitClient";
    private static final String PREFS_NAME = "app_prefs";
    private static final String PREF_BACKEND_URL = "backend_url";

    private static RetrofitClient instance;
    private ApiService apiService;
    private Retrofit retrofit;
    private String currentBaseUrl;

    private RetrofitClient(String baseUrl) {
        this.currentBaseUrl = baseUrl;
        Log.d(TAG, "Initializing Retrofit with base URL: " + baseUrl);
        buildRetrofit(baseUrl);
    }

    private void buildRetrofit(String baseUrl) {
        HttpLoggingInterceptor loggingInterceptor = new HttpLoggingInterceptor();
        loggingInterceptor.setLevel(HttpLoggingInterceptor.Level.BODY);

        OkHttpClient client = new OkHttpClient.Builder()
                .addInterceptor(loggingInterceptor)
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .retryOnConnectionFailure(true)
                .followRedirects(true)
                .followSslRedirects(true)
                .build();

        retrofit = new Retrofit.Builder()
                .baseUrl(baseUrl)
                .client(client)
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        apiService = retrofit.create(ApiService.class);
    }

    // Get backend URL from SharedPreferences first, then use default
    private static String getBackendUrl(Context ctx) {
        SharedPreferences prefs = ctx.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        String savedUrl = prefs.getString(PREF_BACKEND_URL, null);

        if (savedUrl != null && !savedUrl.isEmpty()) {
            Log.d(TAG, "Using saved backend URL: " + savedUrl);
            return savedUrl;
        }

        // Default URL - Replace with your actual backend server address
        // Example: http://YOUR_SERVER_IP:5000/ or http://192.168.1.X:5000/
        Log.d(TAG, "No saved URL, using default: http://YOUR_SERVER_IP:5000/");
        return "http://YOUR_SERVER_IP:5000/";
    }

    // Initialize or get instance
    public static synchronized RetrofitClient getInstance(Context ctx) {
        if (instance == null) {
            String baseUrl = getBackendUrl(ctx.getApplicationContext());
            instance = new RetrofitClient(baseUrl);

            // Log the URL being used
            Log.d(TAG, "RetrofitClient initialized with URL: " + baseUrl);
        }
        return instance;
    }

    // Reset instance (call this after user changes backend URL in settings)
    public static synchronized void resetInstance() {
        instance = null;
    }

    // Clear saved URL to force use of default
    public static void clearSavedUrl(Context ctx) {
        SharedPreferences prefs = ctx.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        prefs.edit().remove(PREF_BACKEND_URL).apply();
        Log.d(TAG, "Cleared saved backend URL");
        resetInstance();
    }

    public ApiService getApiService() {
        return apiService;
    }

    public String getCurrentBaseUrl() {
        return currentBaseUrl;
    }
}

package com.ahaanmehta.skin_disease;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import com.bumptech.glide.Glide;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;

import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private ImageView imageView;
    private MaterialButton btnCamera, btnGallery, btnAnalyze, btnSettings;
    private ProgressBar progressBar;
    private MaterialCardView resultCard;
    private TextView resultText, fileNameText;

    private Uri selectedImageUri;
    private File currentPhotoFile;

    private final ActivityResultLauncher<String[]> permissionLauncher =
            registerForActivityResult(new ActivityResultContracts.RequestMultiplePermissions(), result -> {
                Boolean cameraGranted = result.get(Manifest.permission.CAMERA);

                if (cameraGranted != null && cameraGranted) {
                    Toast.makeText(this, "Camera permission granted", Toast.LENGTH_SHORT).show();
                }
            });

    private final ActivityResultLauncher<Intent> cameraLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK) {
                    if (currentPhotoFile != null && currentPhotoFile.exists()) {
                        selectedImageUri = Uri.fromFile(currentPhotoFile);
                        displayImage(selectedImageUri);
                    }
                }
            });

    private final ActivityResultLauncher<Intent> galleryLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    selectedImageUri = result.getData().getData();
                    displayImage(selectedImageUri);
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initViews();
        checkPermissions();
        setupClickListeners();

        // Initialize Retrofit on background thread to avoid blocking UI
        new Thread(() -> {
            RetrofitClient.getInstance(this);
            Log.d("MainActivity", "Retrofit initialized");
        }).start();
    }

    private void initViews() {
        imageView = findViewById(R.id.imageView);
        btnCamera = findViewById(R.id.btnCamera);
        btnGallery = findViewById(R.id.btnGallery);
        btnAnalyze = findViewById(R.id.btnAnalyze);
        btnSettings = findViewById(R.id.btnSettings);
        progressBar = findViewById(R.id.progressBar);
        resultCard = findViewById(R.id.resultCard);
        resultText = findViewById(R.id.resultText);
        fileNameText = findViewById(R.id.fileNameText);

        // Set placeholder image initially
        imageView.setImageResource(R.drawable.ic_placeholder_image);
    }

    private void checkPermissions() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED ||
            ContextCompat.checkSelfPermission(this, Manifest.permission.READ_MEDIA_IMAGES) != PackageManager.PERMISSION_GRANTED) {
            permissionLauncher.launch(new String[]{
                    Manifest.permission.CAMERA,
                    Manifest.permission.READ_MEDIA_IMAGES,
                    Manifest.permission.READ_EXTERNAL_STORAGE
            });
        }
    }

    private void setupClickListeners() {
        btnCamera.setOnClickListener(v -> openCamera());
        btnGallery.setOnClickListener(v -> openGallery());
        btnAnalyze.setOnClickListener(v -> analyzeImage());
        btnSettings.setOnClickListener(v -> openSettings());
    }

    private void openCamera() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(this, "Camera permission required", Toast.LENGTH_SHORT).show();
            checkPermissions();
            return;
        }

        try {
            currentPhotoFile = createImageFile();
            Uri photoURI = FileProvider.getUriForFile(this,
                    getPackageName() + ".fileprovider",
                    currentPhotoFile);

            Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
            cameraLauncher.launch(cameraIntent);
        } catch (IOException e) {
            Toast.makeText(this, "Error creating image file", Toast.LENGTH_SHORT).show();
            android.util.Log.e("MainActivity", "Camera error", e);
        }
    }

    private void openGallery() {
        Intent galleryIntent = new Intent(Intent.ACTION_PICK);
        galleryIntent.setType("image/*");
        galleryLauncher.launch(galleryIntent);
    }

    private File createImageFile() throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(new Date());
        String imageFileName = "SKIN_" + timeStamp + "_";
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        return File.createTempFile(imageFileName, ".jpg", storageDir);
    }

    private void displayImage(Uri imageUri) {
        Glide.with(this)
                .load(imageUri)
                .into(imageView);

        resultCard.setVisibility(View.GONE);
    }

    private void analyzeImage() {
        if (selectedImageUri == null) {
            Toast.makeText(this, "Please select an image first", Toast.LENGTH_SHORT).show();
            return;
        }

        showLoading(true);

        // Run on background thread to avoid blocking UI
        new Thread(() -> {
            try {
                Log.d("MainActivity", "🔍 Starting image analysis...");
                File imageFile = getFileFromUri(selectedImageUri);

                // Verify file exists and has content
                if (!imageFile.exists()) {
                    runOnUiThread(() -> {
                        showLoading(false);
                        Toast.makeText(MainActivity.this, "Error: Image file not found", Toast.LENGTH_LONG).show();
                    });
                    Log.e("MainActivity", "❌ Image file does not exist: " + imageFile.getAbsolutePath());
                    return;
                }

                long fileSize = imageFile.length();
                Log.d("MainActivity", "✅ Image file size: " + fileSize + " bytes");

                if (fileSize == 0) {
                    runOnUiThread(() -> {
                        showLoading(false);
                        Toast.makeText(MainActivity.this, "Error: Image file is empty", Toast.LENGTH_LONG).show();
                    });
                    Log.e("MainActivity", "❌ Image file is empty!");
                    return;
                }

                // Determine MIME type
                String mimeType = "image/jpeg";
                if (imageFile.getName().toLowerCase().endsWith(".png")) {
                    mimeType = "image/png";
                }

                Log.d("MainActivity", "📝 File: " + imageFile.getName() + ", Size: " + fileSize + " bytes, MIME: " + mimeType);

                // Create multipart body with explicit file inclusion
                okhttp3.MultipartBody.Builder multipartBuilder = new okhttp3.MultipartBody.Builder()
                        .setType(okhttp3.MultipartBody.FORM);

                // Add the image file to multipart
                RequestBody fileBody = RequestBody.create(
                        MediaType.parse(mimeType),
                        imageFile
                );

                multipartBuilder.addFormDataPart(
                        "image",
                        imageFile.getName(),
                        fileBody
                );

                okhttp3.MultipartBody multipartBody = multipartBuilder.build();
                Log.d("MainActivity", "✅ Multipart body created with " + multipartBody.size() + " parts");

                // Create a custom request that ensures the multipart is sent properly
                Log.d("MainActivity", "📤 Preparing to send request...");

                ApiService apiService = RetrofitClient.getInstance(MainActivity.this).getApiService();
                String baseUrl = RetrofitClient.getInstance(MainActivity.this).getCurrentBaseUrl();
                Log.d("MainActivity", "🔗 Backend URL: " + baseUrl + "api/v1/predictions/");

                // Make the request using Retrofit's multipart
                MultipartBody.Part imagePart = MultipartBody.Part.createFormData(
                        "image",
                        imageFile.getName(),
                        fileBody
                );

                Call<PredictionResponse> call = apiService.uploadImage(imagePart);
                Log.d("MainActivity", "📤 Sending image to backend...");

                call.enqueue(new Callback<PredictionResponse>() {
                    @Override
                    public void onResponse(@NonNull Call<PredictionResponse> call, @NonNull Response<PredictionResponse> response) {
                        Log.d("MainActivity", "📥 Response received - Code: " + response.code());

                        runOnUiThread(() -> {
                            showLoading(false);

                            if (response.isSuccessful() && response.body() != null) {
                                PredictionResponse predictionResponse = response.body();
                                String result = predictionResponse.getResult();
                                String fileName = predictionResponse.getFile();

                                Log.d("MainActivity", "✅ SUCCESS! Result: " + result);
                                displayResult(result, fileName);
                            } else {
                                String errorMsg = "Error " + response.code();
                                try {
                                    if (response.errorBody() != null) {
                                        String errorBody = response.errorBody().string();
                                        errorMsg += ": " + errorBody;
                                        Log.e("MainActivity", "Error body: " + errorBody);
                                    }
                                } catch (IOException e) {
                                    Log.e("MainActivity", "Error reading response", e);
                                }
                                Log.e("MainActivity", "❌ " + errorMsg);
                                Toast.makeText(MainActivity.this, errorMsg, Toast.LENGTH_LONG).show();
                            }
                        });
                    }

                    @Override
                    public void onFailure(@NonNull Call<PredictionResponse> call, @NonNull Throwable t) {
                        Log.e("MainActivity", "❌ NETWORK ERROR: " + t.getClass().getSimpleName() + " - " + t.getMessage(), t);

                        runOnUiThread(() -> {
                            showLoading(false);
                            String errorMsg = "Connection Failed: " + t.getMessage();
                            Toast.makeText(MainActivity.this, errorMsg, Toast.LENGTH_LONG).show();
                        });
                    }
                });

            } catch (Exception e) {
                Log.e("MainActivity", "❌ Exception: " + e.getMessage(), e);
                runOnUiThread(() -> {
                    showLoading(false);
                    Toast.makeText(MainActivity.this, "Error: " + e.getMessage(), Toast.LENGTH_LONG).show();
                });
            }
        }).start();
    }

    private File getFileFromUri(Uri uri) throws IOException {
        Log.d("MainActivity", "getFileFromUri called with URI: " + uri);

        File tempFile = new File(getCacheDir(), "temp_image.jpg");
        Log.d("MainActivity", "Temp file path: " + tempFile.getAbsolutePath());

        // Delete old file if exists
        if (tempFile.exists()) {
            tempFile.delete();
            Log.d("MainActivity", "Deleted existing temp file");
        }

        InputStream inputStream = null;
        OutputStream outputStream = null;

        try {
            inputStream = getContentResolver().openInputStream(uri);

            if (inputStream == null) {
                Log.e("MainActivity", "ERROR: Could not open input stream from URI: " + uri);
                throw new IOException("Cannot open input stream from URI");
            }

            Log.d("MainActivity", "Input stream opened successfully");

            outputStream = new FileOutputStream(tempFile);

            byte[] buffer = new byte[4096];
            int bytesRead;
            int totalBytes = 0;

            while ((bytesRead = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
                totalBytes += bytesRead;
                Log.d("MainActivity", "Read and wrote " + bytesRead + " bytes (total: " + totalBytes + ")");
            }

            outputStream.flush();
            Log.d("MainActivity", "File writing complete. Total bytes: " + totalBytes);

            // Verify the file
            if (!tempFile.exists()) {
                Log.e("MainActivity", "ERROR: Temp file does not exist after writing!");
                throw new IOException("Temp file was not created");
            }

            long finalSize = tempFile.length();
            Log.d("MainActivity", "Final temp file size: " + finalSize + " bytes");

            if (finalSize == 0) {
                Log.e("MainActivity", "ERROR: Temp file is empty!");
                throw new IOException("Temp file is empty - no data was read from URI");
            }

            return tempFile;

        } catch (Exception e) {
            Log.e("MainActivity", "Exception in getFileFromUri: " + e.getMessage(), e);
            throw new IOException("Error converting URI to file: " + e.getMessage(), e);
        } finally {
            // Close streams properly
            if (inputStream != null) {
                try {
                    inputStream.close();
                    Log.d("MainActivity", "Input stream closed");
                } catch (IOException e) {
                    Log.e("MainActivity", "Error closing input stream", e);
                }
            }
            if (outputStream != null) {
                try {
                    outputStream.close();
                    Log.d("MainActivity", "Output stream closed");
                } catch (IOException e) {
                    Log.e("MainActivity", "Error closing output stream", e);
                }
            }
        }
    }

    private void showLoading(boolean show) {
        progressBar.setVisibility(show ? View.VISIBLE : View.GONE);
        btnAnalyze.setEnabled(!show);
        btnCamera.setEnabled(!show);
        btnGallery.setEnabled(!show);
    }

    private void displayResult(String result, String fileName) {
        resultCard.setVisibility(View.VISIBLE);
        resultText.setText(result != null ? result : "N/A");
        fileNameText.setText("File: " + (fileName != null ? fileName : "N/A"));

        Toast.makeText(this, "Analysis Complete!", Toast.LENGTH_SHORT).show();
    }

    private void openSettings() {
        Intent intent = new Intent(this, SettingsActivity.class);
        startActivity(intent);
    }
}

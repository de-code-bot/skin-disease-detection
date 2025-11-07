package com.ahaanmehta.skin_disease;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.InputType;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;

public class SettingsActivity extends AppCompatActivity {

    private static final String PREFS_NAME = "app_prefs";
    private static final String PREF_BACKEND_URL = "backend_url";

    private AppCompatButton btnChangeBackend, btnTestConnection;
    private SharedPreferences prefs;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);

        btnChangeBackend = findViewById(R.id.btnChangeBackend);
        btnTestConnection = findViewById(R.id.btnTestConnection);

        btnChangeBackend.setOnClickListener(v -> showChangeBackendDialog());
        btnTestConnection.setOnClickListener(v -> testConnection());
    }

    private void showChangeBackendDialog() {
        EditText input = new EditText(this);
        input.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_URI);
        input.setHint("http://YOUR_SERVER_IP:5000");

        String currentUrl = prefs.getString(PREF_BACKEND_URL, "Not set");
        input.setText(currentUrl);

        new AlertDialog.Builder(this)
                .setTitle("Backend Server Address")
                .setMessage("Enter your backend server IP and port.\nExample: http://192.168.X.X:5000")
                .setView(input)
                .setPositiveButton("Save", (dialog, which) -> {
                    String entered = input.getText().toString().trim();
                    if (!entered.isEmpty()) {
                        if (!entered.startsWith("http://") && !entered.startsWith("https://")) {
                            entered = "http://" + entered;
                        }
                        if (!entered.endsWith("/")) entered = entered + "/";

                        prefs.edit().putString(PREF_BACKEND_URL, entered).apply();
                        RetrofitClient.resetInstance();
                        Toast.makeText(this, "Saved: " + entered, Toast.LENGTH_SHORT).show();
                    }
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void testConnection() {
        String url = prefs.getString(PREF_BACKEND_URL, null);
        if (url == null || url.isEmpty()) {
            Toast.makeText(this, "No backend configured. Please set it first.", Toast.LENGTH_SHORT).show();
            return;
        }

        Toast.makeText(this, "Testing connection to " + url + "...", Toast.LENGTH_SHORT).show();

        new Thread(() -> {
            try {
                java.net.URL testUrl = new java.net.URL(url);
                java.net.HttpURLConnection conn = (java.net.HttpURLConnection) testUrl.openConnection();
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                int responseCode = conn.getResponseCode();
                conn.disconnect();

                runOnUiThread(() -> {
                    if (responseCode == 200 || responseCode == 307 || responseCode == 308) {
                        Toast.makeText(SettingsActivity.this, "✓ Connection successful! (Code: " + responseCode + ")", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(SettingsActivity.this, "✗ Got response " + responseCode + " (server may be having issues)", Toast.LENGTH_SHORT).show();
                    }
                });
            } catch (Exception e) {
                runOnUiThread(() -> Toast.makeText(SettingsActivity.this, "✗ Connection failed: " + e.getMessage(), Toast.LENGTH_SHORT).show());
            }
        }).start();
    }
}

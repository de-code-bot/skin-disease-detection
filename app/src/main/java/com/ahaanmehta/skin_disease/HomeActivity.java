package com.ahaanmehta.skin_disease;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;

public class HomeActivity extends AppCompatActivity {

    private MaterialButton btnAnalyzeNow, btnAboutUs;
    private MaterialCardView analyzeCard, aboutCard;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        initViews();
        setupClickListeners();
    }

    private void initViews() {
        btnAnalyzeNow = findViewById(R.id.btnAnalyzeNow);
        btnAboutUs = findViewById(R.id.btnAboutUs);
        analyzeCard = findViewById(R.id.analyzeCard);
        aboutCard = findViewById(R.id.aboutCard);
    }

    private void setupClickListeners() {
        // Analyze Now button - goes to MainActivity
        btnAnalyzeNow.setOnClickListener(v -> {
            Intent intent = new Intent(HomeActivity.this, MainActivity.class);
            startActivity(intent);
        });

        // About Us button - goes to AboutActivity
        btnAboutUs.setOnClickListener(v -> {
            Intent intent = new Intent(HomeActivity.this, AboutActivity.class);
            startActivity(intent);
        });

        // Card click listeners
        analyzeCard.setOnClickListener(v -> btnAnalyzeNow.performClick());
        aboutCard.setOnClickListener(v -> btnAboutUs.performClick());
    }
}

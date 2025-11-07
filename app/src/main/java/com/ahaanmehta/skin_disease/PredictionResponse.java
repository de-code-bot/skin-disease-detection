package com.ahaanmehta.skin_disease;

import com.google.gson.annotations.SerializedName;

public class PredictionResponse {
    @SerializedName("result")
    private String result;

    @SerializedName("file")
    private String file;

    @SerializedName("additional")
    private Additional additional;

    public String getResult() {
        return result;
    }

    public String getFile() {
        return file;
    }

    public Additional getAdditional() {
        return additional;
    }

    public static class Additional {
        @SerializedName("file_quantity")
        private String fileQuantity;

        public String getFileQuantity() {
            return fileQuantity;
        }
    }
}


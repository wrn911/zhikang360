package com.example.entity.DTO;

import lombok.Data;

@Data
public class SyncRequest {
    private Boolean forceUpdate = false;
    
    public SyncRequest() {}
    
    public SyncRequest(Boolean forceUpdate) {
        this.forceUpdate = forceUpdate;
    }
}
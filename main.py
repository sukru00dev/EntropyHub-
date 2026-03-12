from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# API Tanımlaması (Teknik döküman sayfa 13'e göre güncellendi)
app = FastAPI(
    title="EntropyHub API",
    description="Kaotik PRNG ve Kuantum Sonrası Kriptografi (Kyber-768) Servisi",
    version="1.1.0"
)

# Frontend Erişimi için CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Veri Modelleri (Request/Response Schemas)
class SeedRequest(BaseModel):
    seed_value: int

# 1. Görev: Sistem Durumu
@app.get("/api/system_status")
async def system_status():
    return {
        "status": "Online",
        "engine": "Aether-Rust Core v2.1.0",
        "quantum_seeding": "Ready",
        "kyber_status": "Active"
    }

# 2. Görev: Rastgele Veri Üretimi (GET /random/bytes/{n})
@app.get("/api/random/bytes/{n}")
async def get_random_bytes(n: int):
    # Mahmut Bey'in Rust çekirdeğine bağlanacak alan
    return {
        "bytes_hex": "a3f9...", 
        "entropy": 7.9998,
        "n": n
    }

# 3. YENİ GÖREV: Tohumlama (POST /random/seed)
@app.post("/api/random/seed")
async def set_seed(request: SeedRequest):
    # Mahmut Bey'in çekirdek tohumlama fonksiyonuna bağlanacak
    return {"message": f"Seed {request.seed_value} başarıyla uygulandı."}

# 4. YENİ GÖREV: Kyber Anahtar Çifti (GET /kyber/keypair)
@app.get("/api/kyber/keypair")
async def get_kyber_keys():
    # Kyber-768 modülünden gelecek veriler
    return {
        "public_key": "PQ-PK-768-EXAMPLE...",
        "secret_key": "PQ-SK-768-EXAMPLE..."
    }

# 5. Görev: NIST Test Sonuçları
@app.get("/api/nist_results")
async def nist_results():
    return {
        "test_suite": "NIST SP 800-22",
        "overall": "PASS",
        "shannon_entropy": 7.9998,
        "metrics": {
            "chi_square_p": 0.8234,
            "autocorrelation_lag1": -0.0017
        }
    }
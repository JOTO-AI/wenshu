#!/usr/bin/env python3
"""Test configuration loading"""

try:
    from app.core.config import settings
    print(f"✅ Config loaded successfully")
    print(f"📊 Database URL: {settings.DATABASE_URL}")
    
    from app.models.models import Base
    print(f"✅ Models imported successfully")
    print(f"📋 Tables: {list(Base.metadata.tables.keys())}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "live_records: verifies the real records tree under the committed "
        "armed producer-signing pins (no dormancy simulation)",
    )

"""Pin the official GenVM runner consumed by genlayer-test 0.29.2.

The published test loader otherwise requests a renamed v0.3.0 asset and 404s.
This is a test-runner version pin, not a mock of a contract response.
"""
import gltest.direct.sdk_loader as sdk_loader
sdk_loader.get_latest_version = lambda: "v0.2.16"

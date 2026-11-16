"""Temporary QA diagnostics for GenLayer Direct Mode stdin contract loader (NOT a production source)."""
import os
import gltest.direct.loader as loader

_original_inject = loader._inject_message_to_fd0

def _diagnose_inject(vm):
    try:
        c = loader.import_calldata()
        a = loader.import_address()
        print("QA_DIAG calldata:", getattr(c, "__file__", repr(c)), "Address:", a, flush=True)
    except Exception as exc:
        print("QA_DIAG pre-inject SDK import failed:", type(exc).__name__, str(exc), flush=True)
    _original_inject(vm)
    try:
        pos = os.lseek(0, 0, os.SEEK_CUR)
        contents = os.pread(0, 1024, 0)
        print("QA_DIAG fd0 pos:", pos, "size:", len(contents), "leading:", contents[:30].hex(), flush=True)
    except Exception as exc:
        print("QA_DIAG fd0 unavailable:", type(exc).__name__, str(exc), flush=True)

loader._inject_message_to_fd0 = _diagnose_inject

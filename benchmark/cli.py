from engine.provider_loader import providers

def main():
    print("BSI Benchmark")
    print("=============")

    for p in providers():
        print("✓", p.name)

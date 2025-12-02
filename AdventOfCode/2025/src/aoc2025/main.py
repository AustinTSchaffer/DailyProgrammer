def main():
    for i in range(1, 13):
        module_name = f"day_{i:02d}"
        try:
            module = __import__(module_name, fromlist='aoc2025')
            module.main()
        except:
            ...

if __name__ == "__main__":
    main()

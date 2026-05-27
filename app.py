from web.server import create_app

app = create_app()

if __name__ == "__main__":
    print("\n  HR Agent → http://localhost:5001\n")
    app.run(debug=False, port=5001)
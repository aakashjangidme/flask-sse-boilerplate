from app import create_app

app = create_app(config='app.config.DevelopmentConfig')

if __name__ == '__main__':
    app.run(debug=True)

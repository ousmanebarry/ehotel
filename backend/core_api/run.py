from main import create_app
from config import ProdConfig

config = ProdConfig()

app = create_app(config)

# Create a database connection based on the config
# db = Database(config.DB_NAME, config.DB_USER, config.DB_PASSWORD, config.DB_HOST, config.DB_PORT)

if __name__ == "__main__":
    app.run()

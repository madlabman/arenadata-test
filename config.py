class Config(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value


app_config = Config({
    'port': 5000,
    'host': 'http://localhost',
    'api_base': '/api/v1',
    'container_port': '5000/tcp'
})

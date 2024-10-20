from shared.config import Config


class ParserConfig:
    def __init__(self):
        self.config = Config()
        self.base_dir = self.config.base_dir / 'parser'

    @property
    def schedule_url(self):
        return self.config.get('parser', 'source', 'schedule_url')

    @property
    def groups_url(self):
        return self.config.get('parser', 'source', 'groups_url')

    @property
    def database_url(self):
        db_username = self.config.get('parser', 'database', 'username')
        db_password = self.config.get('parser', 'database', 'password')
        db_host = self.config.get('parser', 'database', 'host')
        db_port = self.config.get('parser', 'database', 'port')
        db_name = self.config.get('parser', 'database', 'name')
        return f'postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

    @property
    def parsing_interval(self):
        return self.config.get_int('parser', 'parsing', 'interval')

    @property
    def retry_attempts(self):
        return self.config.get_int('parser', 'parsing', 'retry_attempts')

    @property
    def retry_delay(self):
        return self.config.get_int('parser', 'parsing', 'retry_delay')

    @property
    def chunk_size(self):
        return self.config.get_int('parser', 'parsing', 'chunk_size')

    @property
    def chunk_delay(self):
        return self.config.get_float('parser', 'parsing', 'chunk_delay')

    @property
    def concurrent_requests(self):
        return self.config.get_int('parser', 'parsing', 'concurrent_requests')


parser_config = ParserConfig()

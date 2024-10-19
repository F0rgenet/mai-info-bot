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
        file_path = self.config.get('parser', 'database', 'url')
        base_dir = str(self.base_dir).replace('\\', '/')
        return f'sqlite+aiosqlite:///{base_dir}/{file_path}'

    @property
    def database_pool_size(self):
        return self.config.get_int('parser', 'database', 'pool_size')

    @property
    def database_max_overflow(self):
        return self.config.get_int('parser', 'database', 'max_overflow')

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
